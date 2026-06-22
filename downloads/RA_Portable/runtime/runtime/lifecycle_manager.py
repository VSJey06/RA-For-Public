"""LifecycleManager — Coordinates Runtime → RGC → Registry → SML → RMM lifecycle.

Orchestrates the full lifecycle flow for entities after successful execution:

    \u00C7 Created   (via GPCIntegration)
      \u2193  activate()
    \u00C5 Active    (RC \u2014 being worked on)
      \u2193  finalize() + RC\u2192PC
    \u27E9 Frozen    (PC \u2014 placeholder)
      \u2193  mark_dead()
    \u203D Dead      (PC \u2014 inactive, not reusable)
      \u2193  archive() + PC\u2192SC
    \u00C2 Archived  (SC \u2014 static, persisted)
      \u2193  reload() + SC\u2192RC
    \u00C5 Active    (RC \u2014 reloaded from archive)

Sprint-4C: \u00C5\u2192\u27E9 + RC\u2192PC via TransferManager.transfer.
Sprint-4D: \u27E9\u2192\u203D dead-state via Executor reusability analysis.
Sprint-4E: \u203D\u2192\u00C2 archival + PC\u2192SC via CleanupManager.cleanup.
Sprint-4F: \u00C2\u2192\u00C5 reload + SC\u2192RC via ReloadManager.reload.
"""

from __future__ import annotations

from typing import Any

from rvm.gpc.registry import ContainerLocation
from rvm.rgc.cleanup_manager import CleanupManager
from rvm.rgc.reload_manager import ReloadManager
from rvm.rgc.state_tracker import (
    A_ACTIVE,
    A_ARCHIVED,
    C_CREATED,
    Q_DEAD,
    R_FROZEN,
    StateTracker,
)
from rvm.rgc.transfer_manager import TransferManager
from rvm.rmm.method_memory import MethodMemory
from rvm.rmm.object_memory import ObjectMemory
from rvm.rmm.variable_memory import VariableMemory


class LifecycleError(Exception):
    """Raised when a lifecycle operation fails."""


class LifecycleManager:
    """Coordinates lifecycle transitions across RGC, Registry, SML, and RMM.

    After finalization the Executor decides the entity's fate:

        * **REUSABLE** — stays in ⟩ (Frozen, PC placeholder)
        * **DEAD**     — mark_dead() → ‽ (terminal in PC)
        * **ARCHIVE**  — archive() → Â (persistent in SC)

    Archive is an explicit persistence decision, not an automatic
    step after Dead.  Dead entities are terminal (only deletable).

    All transitions are recorded in the GPC Registry (state + location)
    and the SML (transition log).

    Sprint-4D: Executor reusability analysis + ⟩→‽ dead-state.
    Sprint-4E: ⟩→Â archival + PC→SC static container integration.
    Sprint-4F: Â→Å reload + SC→RC static container reload.
    """

    def __init__(
        self,
        registry: Any,
        sml: Any,
        var_mem: VariableMemory,
        method_mem: MethodMemory,
        object_mem: ObjectMemory,
    ) -> None:
        self.tracker = StateTracker()
        self.transfer_mgr = TransferManager(self.tracker)
        self.cleanup_mgr = CleanupManager(self.tracker)
        self.reload_mgr = ReloadManager(self.tracker)
        self.registry = registry
        self.sml = sml
        self.var_mem = var_mem
        self.method_mem = method_mem
        self.object_mem = object_mem

    # ── Public API ─────────────────────────────────────────────────────

    def activate(self, rid_value: str, kind: str, name: str) -> None:
        """Transition entity to \u00C5 (Active) state.

        Handles:
            * \u00C7\u2192\u00C5 \u2014 first activation after creation
            * \u27E9\u2192\u00C5 \u2014 reactivation (state-only, no data rollback)
            * \u00C2\u2192\u00C5 \u2014 archived reload

        Dead entities (\u203D) cannot be activated; Dead is terminal.

        For \u27E9\u2192\u00C5 only the state marker changes; the caller
        is responsible for writing fresh RC data before ``finalize()``.
        """
        if not self.tracker.is_registered(rid_value):
            self.tracker.register(rid_value)

        current = self.tracker.get_state(rid_value)
        if current == C_CREATED:
            self.tracker.transition(rid_value, A_ACTIVE)
            self.registry.set_state(rid_value, A_ACTIVE)
            self.sml.record_transition(rid_value, C_CREATED, A_ACTIVE)
        elif current == R_FROZEN:
            self.tracker.set_state(rid_value, A_ACTIVE)
            self.registry.set_state(rid_value, A_ACTIVE)
            self.sml.record_transition(rid_value, R_FROZEN, A_ACTIVE)
        elif current == A_ACTIVE:
            pass
        elif current == A_ARCHIVED:
            triple = self._get_triple(kind, name)
            self.reload_mgr.reload(rid_value, triple)
            self.registry.set_state(rid_value, A_ACTIVE)
            self.registry.set_location(rid_value, ContainerLocation.RC)
            self.sml.record_transition(rid_value, A_ARCHIVED, A_ACTIVE)
        else:
            raise LifecycleError(
                f"Cannot activate '{rid_value}' from state '{current}'"
            )

    def finalize(self, rid_value: str, kind: str, name: str) -> None:
        """\u00C5\u2192\u27E9 + RC\u2192PC after successful execution.

        Uses TransferManager.transfer which validates:
            * Entity is in \u00C5 (Active) state
            * RC data exists
        Then promotes RC\u2192PC and sets state to \u27E9 (Frozen).
        """
        triple = self._get_triple(kind, name)
        self.transfer_mgr.transfer(rid_value, triple)
        self.registry.set_location(rid_value, ContainerLocation.PC)
        self.registry.set_state(rid_value, R_FROZEN)
        self.sml.record_transition(rid_value, A_ACTIVE, R_FROZEN)

    # ── Convenience wrappers ───────────────────────────────────────────

    def activate_variable(self, rid_value: str, var_name: str) -> None:
        self.activate(rid_value, "variable", var_name)

    def finalize_variable(self, rid_value: str, var_name: str) -> None:
        self.finalize(rid_value, "variable", var_name)

    def activate_method(self, rid_value: str, method_name: str) -> None:
        self.activate(rid_value, "method", method_name)

    def finalize_method(self, rid_value: str, method_name: str) -> None:
        self.finalize(rid_value, "method", method_name)

    def activate_class(self, rid_value: str, class_name: str) -> None:
        self.activate(rid_value, "class", class_name)

    def finalize_class(self, rid_value: str, class_name: str) -> None:
        self.finalize(rid_value, "class", class_name)

    def activate_object(self, rid_value: str, var_name: str) -> None:
        self.activate(rid_value, "object", var_name)

    def finalize_object(self, rid_value: str, var_name: str) -> None:
        self.finalize(rid_value, "object", var_name)

    # ── Dead state ──────────────────────────────────────────────────────

    def mark_dead(self, rid_value: str, kind: str, name: str) -> None:
        """⟩→‽: Mark entity as dead (not reusable).

        Updates StateTracker, Registry state, and SML.
        Location stays at PC (no archive, no PC→SC).
        """
        # Validate kind/name exist
        self._get_triple(kind, name)
        self.tracker.transition(rid_value, Q_DEAD)
        self.registry.set_state(rid_value, Q_DEAD)
        self.sml.record_transition(rid_value, R_FROZEN, Q_DEAD)

    def mark_variable_dead(self, rid_value: str, var_name: str) -> None:
        self.mark_dead(rid_value, "variable", var_name)

    def mark_method_dead(self, rid_value: str, method_name: str) -> None:
        self.mark_dead(rid_value, "method", method_name)

    def mark_class_dead(self, rid_value: str, class_name: str) -> None:
        self.mark_dead(rid_value, "class", class_name)

    def mark_object_dead(self, rid_value: str, var_name: str) -> None:
        self.mark_dead(rid_value, "object", var_name)

    # ── Archive ─────────────────────────────────────────────────────────

    def archive(self, rid_value: str, kind: str, name: str) -> None:
        """\u27E9\u2192\u00C2: Archive a frozen entity, moving PC\u2192SC.

        Validates the entity is in \u27E9 (Frozen) state, then:
            1. Calls CleanupManager.cleanup for PC\u2192SC + StateTracker\u2192\u00C2
            2. Updates Registry state\u2192\u00C2 + location\u2192SC
            3. Records \u27E9\u2192\u00C2 in SML

        Dead entities (\u203D) cannot be archived; archive is an explicit
        persistence decision made from Frozen state.

        Args:
            rid_value: The RID string of the entity to archive.
            kind:      Entity kind (variable, method, object, class).
            name:      Entity name as stored in RMM.

        Raises:
            LifecycleError: If the entity is not in \u27E9 (Frozen) state.
        """
        triple = self._get_triple(kind, name)

        current = self.tracker.get_state(rid_value)
        if current != R_FROZEN:
            raise LifecycleError(
                f"Cannot archive '{rid_value}' from state "
                f"'{current}'; expected '{R_FROZEN}' (Frozen)"
            )

        # CleanupManager.cleanup: validates Frozen/Dead, does PC\u2192SC,
        # updates StateTracker to \u00C2 (Archived).
        self.cleanup_mgr.cleanup(rid_value, triple)

        # Registry synchronisation
        self.registry.set_location(rid_value, ContainerLocation.SC)
        self.registry.set_state(rid_value, A_ARCHIVED)

        # SML recording
        self.sml.record_transition(rid_value, R_FROZEN, A_ARCHIVED)

    def archive_variable(self, rid_value: str, var_name: str) -> None:
        self.archive(rid_value, "variable", var_name)

    def archive_method(self, rid_value: str, method_name: str) -> None:
        self.archive(rid_value, "method", method_name)

    def archive_class(self, rid_value: str, class_name: str) -> None:
        self.archive(rid_value, "class", class_name)

    def archive_object(self, rid_value: str, var_name: str) -> None:
        self.archive(rid_value, "object", var_name)

    # ── Reload ──────────────────────────────────────────────────────────

    def reload(self, rid_value: str, kind: str, name: str) -> None:
        """Â→Å: Reload an archived entity, moving SC→RC.

        Validates the entity is in Â (Archived) state, then:
            1. Calls ReloadManager.reload for SC→RC + StateTracker→Å
            2. Updates Registry state→Å + location→RC
            3. Records Â→Å in SML

        Args:
            rid_value: The RID string of the entity to reload.
            kind:      Entity kind (variable, method, object, class).
            name:      Entity name as stored in RMM.

        Raises:
            LifecycleError: If the entity is not in Â (Archived) state.
        """
        triple = self._get_triple(kind, name)

        current = self.tracker.get_state(rid_value)
        if current != A_ARCHIVED:
            raise LifecycleError(
                f"Cannot reload '{rid_value}' from state "
                f"'{current}'; expected '{A_ARCHIVED}' (Archived)"
            )

        # ReloadManager.reload: validates Archived, does SC→RC,
        # updates StateTracker to Å (Active).
        self.reload_mgr.reload(rid_value, triple)

        # Registry synchronisation
        self.registry.set_location(rid_value, ContainerLocation.RC)
        self.registry.set_state(rid_value, A_ACTIVE)

        # SML recording
        self.sml.record_transition(rid_value, A_ARCHIVED, A_ACTIVE)

    def reload_variable(self, rid_value: str, var_name: str) -> None:
        self.reload(rid_value, "variable", var_name)

    def reload_method(self, rid_value: str, method_name: str) -> None:
        self.reload(rid_value, "method", method_name)

    def reload_class(self, rid_value: str, class_name: str) -> None:
        self.reload(rid_value, "class", class_name)

    def reload_object(self, rid_value: str, var_name: str) -> None:
        self.reload(rid_value, "object", var_name)

    # ── Queries ────────────────────────────────────────────────────────

    def get_state(self, rid_value: str) -> str | None:
        """Return the current lifecycle state via StateTracker."""
        return self.tracker.get_state(rid_value)

    # ── Internal ───────────────────────────────────────────────────────

    def _get_triple(self, kind: str, name: str) -> Any:
        """Retrieve the MemoryTriple for a given entity.

        Args:
            kind: ``"variable"``, ``"method"``, ``"object"``, or ``"class"``.
            name: Entity name as stored in the RMM container.

        Returns:
            The ``MemoryTriple`` instance holding RC/PC/SC data.
        """
        if kind == "variable":
            return self.var_mem._ensure(name)
        elif kind == "method":
            return self.method_mem._ensure(name)
        elif kind == "object":
            return self.object_mem._ensure(name)
        elif kind == "class":
            return self.var_mem._ensure(f"class:{name}")
        raise ValueError(f"Unknown entity kind: '{kind}'")
