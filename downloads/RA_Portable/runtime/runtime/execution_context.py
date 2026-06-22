"""ExecutionContext — Unified execution context shared by source and RBC paths.

Both execution paths converge here:

    Source: Source -> AST -> Executor
    RBC:    RBC -> Loader -> Reconstruction -> Restoration -> RC Restore -> Executor

Provides a common ``execute()`` interface that the ``RbcExecutionAdapter``
and the source ``main.py`` entry point can both use.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from parser.ra_ast import MethodNode, Node, ProgramNode
from runtime.interpreter import Runtime
from runtime.structural.class_system import ClassRegistry
from runtime.structural.method_system import MethodRegistry
from runtime.structural.object_system import ObjectRegistry
from rvm.gpc.ghost_metabase import GhostMetabase
from rvm.gpc.registry import Registry


class ExecutionContext:
    """Unified execution context for RA programs.

    Holds the ``Runtime`` instance, plus pointers to the GPC model
    (Registry + GhostMetabase) used by the execution pipeline.

    Usage (source path)::

        runtime = Runtime()
        exec_ctx = ExecutionContext(runtime)
        exec_ctx.execute(program_node)

    Usage (RBC path)::

        exec_ctx = ExecutionContext()
        exec_ctx.populate_from_rc_program(rc_program)
        exec_ctx.execute(rc_program.as_program_node())
    """

    def __init__(self, runtime: Optional[Runtime] = None) -> None:
        self.runtime = runtime or Runtime()

        # GPC model (populated by RBC path)
        self.registry: Optional[Registry] = None
        self.metabase: Optional[GhostMetabase] = None

    # ── Populate from RC Restorer output ─────────────────────────────

    def populate_from_rc_program(
        self,
        rc_program: Any,
    ) -> None:
        """Populate Runtime state from an ``RcProgram``.

        Sets:
            * Runtime.global_scope — variable values
            * Runtime._var_types — variable type annotations
            * Runtime._object_classes — object → class mapping
            * ClassRegistry — registered classes
            * MethodRegistry — registered methods with bodies
            * ObjectRegistry — registered objects
        """
        rt = self.runtime

        # Global scope
        for name, value in rc_program.global_scope.items():
            rt.global_scope[name] = value
        for name, type_name in rc_program.var_types.items():
            rt._var_types[name] = type_name
        for name, class_name in rc_program.object_classes.items():
            rt._object_classes[name] = class_name

        # Class registry — create ClassNode-like registration stubs
        for entity in rc_program.class_nodes:
            class_name = entity.value or entity.rid
            if not class_name:
                continue
            # Build a minimal ClassNode to register
            from parser.ra_ast import ClassNode
            class_node = ClassNode(name=class_name, members=[], line=0)
            try:
                rt.class_registry.register(class_node)
            except Exception:
                pass

        # Method registry — register with reconstructed body
        for method_name, rc_method in rc_program.methods.items():
            method_node = MethodNode(
                name=rc_method.name,
                body=rc_method.body_nodes,
                line=0,
            )
            try:
                rt.method_registry.register(method_node)
            except Exception:
                pass

    # ── Entry point ──────────────────────────────────────────────────

    def execute(self, program_node: ProgramNode) -> None:
        """Execute a program via the existing Runtime.

        Runs RARG analysis before execution (advisory only — never
        blocks execution).  This is the same path used by source and
        RBC execution.
        """
        self._run_rarg_analysis(program_node)
        self.runtime.execute(program_node)

    def _run_rarg_analysis(self, program_node: ProgramNode) -> None:
        """Run RARG analysis and print reports.

        Runs:
        1. AST-level pattern analysis
        2. Relationship analysis (when GPC model is available)
        3. Structural analysis (when GPC model is available)
        4. Cross-system analysis (when GPC model is available)

        All analyses are advisory only — never block execution.
        """
        try:
            from rarg import (
                analyze, analyze_relationships, analyze_structural,
                analyze_cross_system,
                print_report,
            )
            # AST-level analysis
            result = analyze(program_node.body)

            # Relationship + Structural + Cross-system analysis (when GPC model is attached)
            if self.registry is not None and self.metabase is not None:
                try:
                    rel_result = analyze_relationships(
                        self.registry, self.metabase,
                    )
                    # Merge relationship findings
                    result.warnings.extend(rel_result.warnings)
                    result.suggestions.extend(rel_result.suggestions)
                    result.recommendations.extend(rel_result.recommendations)
                    result.raw_findings.extend(rel_result.raw_findings)
                except Exception:
                    pass  # Relationship analysis is advisory-only

                try:
                    struct_result = analyze_structural(
                        program_node.body,
                        self.registry,
                        self.metabase,
                    )
                    # Merge structural findings
                    result.warnings.extend(struct_result.warnings)
                    result.suggestions.extend(struct_result.suggestions)
                    result.recommendations.extend(struct_result.recommendations)
                    result.raw_findings.extend(struct_result.raw_findings)
                except Exception:
                    pass  # Structural analysis is advisory-only

                try:
                    cross_result = analyze_cross_system(
                        program_node.body,
                        self.registry,
                        self.metabase,
                    )
                    # Merge cross-system findings
                    result.warnings.extend(cross_result.warnings)
                    result.suggestions.extend(cross_result.suggestions)
                    result.recommendations.extend(cross_result.recommendations)
                    result.raw_findings.extend(cross_result.raw_findings)
                except Exception:
                    pass  # Cross-system analysis is advisory-only

            if result.warnings or result.suggestions or result.recommendations:
                print_report(result)
        except Exception:
            pass  # RARG is advisory-only; never block execution

    # ── Results ──────────────────────────────────────────────────────

    @property
    def output_values(self) -> Dict[str, Any]:
        """Return the Runtime's global scope at completion."""
        return dict(self.runtime.global_scope)

    @property
    def last_output(self) -> Any:
        """Return the last printed value (stored in global_scope['_'])."""
        return self.runtime.global_scope.get("_")
