"""GPCIntegration — Runtime → GPC → RMM bridge with lifecycle management.

Hooks into the RA interpreter to automatically:
    1. Generate RIDs via GPCManager
    2. Register entities in the GPC Registry
    3. Record lifecycle state in SML
    4. Place entity data into the appropriate RMM RC container
    5. Orchestrate lifecycle transitions (\u00C7\u2192\u00C5\u2192\u27E9 + RC\u2192PC)
       via the embedded LifecycleManager.

Sprint-4C adds automatic \u00C5\u2192\u27E9\u2192RC\u2192PC after successful execution.
"""

from __future__ import annotations

from typing import Any, Optional

from rvm.gpc.gpc_manager import GPCManager
from rvm.rmm.method_memory import MethodMemory
from rvm.rmm.object_memory import ObjectMemory
from rvm.rmm.variable_memory import VariableMemory

from runtime.lifecycle_manager import LifecycleManager


class GPCIntegration:
    """Bridges the RA runtime with GPC (RID/Registry/SML), RMM (RC containers),
    and RGC lifecycle.

    Each ``track_*`` method:
        * Generates a RID via ``GPCManager`` (which also registers in GPC
          Registry and records the initial SML transition)
        * Stores the entity data in the appropriate RMM RC container
        * Returns the generated RID string

    The embedded ``lifecycle`` manager handles \u00C5\u2192\u27E9\u2192RC\u2192PC transitions
    after successful execution.
    """

    def __init__(self) -> None:
        self.gpc = GPCManager()
        self.var_mem = VariableMemory()
        self.method_mem = MethodMemory()
        self.object_mem = ObjectMemory()
        self.lifecycle = LifecycleManager(
            registry=self.gpc.registry,
            sml=self.gpc.sml,
            var_mem=self.var_mem,
            method_mem=self.method_mem,
            object_mem=self.object_mem,
        )

        # Entity name → RID string mappings
        self._class_rids: dict[str, str] = {}
        self._method_rids: dict[str, str] = {}
        self._var_rids: dict[str, str] = {}
        self._object_rids: dict[str, str] = {}

    # ── Class ─────────────────────────────────────────────────────────

    def track_class(self, name: str) -> str:
        """Generate a RID and place class metadata in the RC container.

        Args:
            name: Class name (used as the naming hint).

        Returns:
            The generated RID string.
        """
        rid = self.gpc.create_class(name)
        self._class_rids[name] = rid.value
        self.var_mem.set(f"class:{name}", {"name": name, "rid": rid.value})
        return rid.value

    # ── Method ────────────────────────────────────────────────────────

    def track_method(
        self, name: str, body: Any = None,
        parent_class_rid: Optional[str] = None,
    ) -> str:
        """Generate a RID and place the method body in the RC container.

        When *parent_class_rid* is provided an OWNERSHIP relation is also
        registered in the Ghost Metabase.

        Args:
            name:             Method name (used as the naming hint).
            body:             The method body to store in RC.
            parent_class_rid: Optional RID of the owning class.

        Returns:
            The generated RID string.
        """
        from rvm.gpc.rid_discovery import RIDType
        from rvm.gpc.registry import ContainerLocation
        from rvm.gpc.ghost_metabase import RelationType
        from rvm.rgc.state_tracker import C_CREATED

        rid = self.gpc.rid_generator.generate(RIDType.METHOD, name)
        self.gpc.registry.register(rid, state=C_CREATED, location=ContainerLocation.NONE)
        self.gpc.sml.record_transition(rid.value, C_CREATED, C_CREATED)
        if parent_class_rid is not None:
            self.gpc.metabase.register_relation(
                parent_class_rid, rid.value, RelationType.OWNERSHIP,
            )
        self._method_rids[name] = rid.value
        if body is not None:
            self.method_mem.register(name, body)
        return rid.value

    # ── Variable ──────────────────────────────────────────────────────

    def track_variable(
        self,
        var_name: str,
        value: Any = None,
        is_declaration: bool = False,
    ) -> Optional[str]:
        """Generate a RID (on declaration) and place the value in RC.

        Args:
            var_name:      Variable name.
            value:         Current value to store in RC.
            is_declaration: If ``True``, generate a new RID for this
                           variable.  Otherwise only update the RC value
                           if the variable was already registered.

        Returns:
            The RID string if a new RID was generated, otherwise ``None``.
        """
        if is_declaration:
            rid = self.gpc.create_variable(var_name, scope="local")
            self._var_rids[var_name] = rid.value

        existing = self._var_rids.get(var_name)
        if existing is not None:
            self.var_mem.set(var_name, value)
        return self._var_rids.get(var_name)

    # ── Object ────────────────────────────────────────────────────────

    def track_object(self, var_name: str, class_name: str) -> str:
        """Generate a RID and place the object in the RC container.

        Args:
            var_name:   Variable name bound to this object instance.
            class_name: The class being instantiated.

        Returns:
            The generated RID string.
        """
        rid = self.gpc.create_object(class_name)
        self._object_rids[var_name] = rid.value
        self.object_mem.create(var_name, properties={"__class__": class_name})
        return rid.value

    # ── RID lookups ───────────────────────────────────────────────────

    def get_class_rid(self, name: str) -> Optional[str]:
        return self._class_rids.get(name)

    def get_method_rid(self, name: str) -> Optional[str]:
        return self._method_rids.get(name)

    def get_var_rid(self, name: str) -> Optional[str]:
        return self._var_rids.get(name)

    def get_object_rid(self, name: str) -> Optional[str]:
        return self._object_rids.get(name)

    # ── Sub-system access ─────────────────────────────────────────────

    @property
    def registry(self):
        return self.gpc.registry

    @property
    def sml(self):
        return self.gpc.sml

    @property
    def metabase(self):
        return self.gpc.metabase
