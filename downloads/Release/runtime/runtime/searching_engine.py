"""SearchingEngine — stateless searching algorithms.

All methods return the index of the target, or -1 if not found.
"""

from __future__ import annotations

from typing import Any, List


class SearchingError(RuntimeError):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class SearchingEngine:
    """Stateless searching utility."""

    @staticmethod
    def _require_list(data: Any) -> None:
        if not isinstance(data, list):
            raise SearchingError(f"Searching requires a list, got {type(data).__name__}")

    def linear_search(self, data: List[Any], target: Any) -> int:
        self._require_list(data)
        for i, val in enumerate(data):
            if val == target:
                return i
        return -1

    def binary_search(self, data: List[Any], target: Any) -> int:
        self._require_list(data)
        lo, hi = 0, len(data) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if data[mid] == target:
                return mid
            elif data[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1
