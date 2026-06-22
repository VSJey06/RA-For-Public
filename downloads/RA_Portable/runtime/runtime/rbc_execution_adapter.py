"""RBC Execution Adapter — Bridge RestoredProgram → ExecutionContext → Executor.

Pipeline::

    RBC -> Loader -> Reconstruction -> Restoration
         -> RC Restorer -> ExecutionContext -> Runtime -> Executor

No execution logic — the adapter only bridges data structures.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from parser.ra_ast import ProgramNode
from runtime.execution_context import ExecutionContext
from rvm.bytecode.rc_restorer import RcProgram, RcRestorer
from rvm.bytecode.restoration import RestoredProgram


class RbcExecutionAdapterError(Exception):
    """Raised on RBC execution pipeline failures."""


class RbcExecutionAdapter:
    """Bridge between RestoredProgram and the RA Runtime.

    Usage::

        adapter = RbcExecutionAdapter()
        result = adapter.execute(restored_program)
    """

    def __init__(self) -> None:
        self._restorer = RcRestorer()

    def execute(
        self,
        restored: RestoredProgram,
    ) -> ExecutionContext:
        """Execute a RestoredProgram and return the execution context.

        Args:
            restored: The restored program with Registry + Metabase.

        Returns:
            An ``ExecutionContext`` with Runtime state populated.

        Raises:
            RbcExecutionAdapterError: On structural failures.
        """
        # Step 1: RC Restore — convert RestoredProgram to RC structures
        rc_program = self._restorer.restore(restored)

        if not rc_program.is_valid():
            raise RbcExecutionAdapterError(
                "RC restoration failed:\n  "
                + "\n  ".join(rc_program.errors)
            )

        # Step 2: Populate ExecutionContext from RC program
        exec_ctx = ExecutionContext()
        exec_ctx.populate_from_rc_program(rc_program)

        # Step 3: Attach GPC model
        exec_ctx.registry = restored.registry
        exec_ctx.metabase = restored.metabase

        # Step 4: Build program node and execute
        program_node = self._build_program_node(rc_program, exec_ctx)
        if program_node is not None:
            exec_ctx.execute(program_node)

        return exec_ctx

    def _build_program_node(
        self,
        rc_program: RcProgram,
        exec_ctx: ExecutionContext,
    ) -> Optional[ProgramNode]:
        """Build a ProgramNode from RC program session nodes.

        If the RC program has session nodes (top-level operations),
        return a ProgramNode containing them.  Otherwise return None
        (no-op execution).
        """
        from rvm.bytecode.rc_restorer import RcProgram

        if rc_program.session_nodes:
            return ProgramNode(body=rc_program.session_nodes, line=0)
        return None

    @staticmethod
    def execute_restored(
        restored: RestoredProgram,
    ) -> ExecutionContext:
        """Convenience static method for one-shot execution."""
        adapter = RbcExecutionAdapter()
        return adapter.execute(restored)
