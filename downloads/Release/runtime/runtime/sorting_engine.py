"""SortingEngine — stateless sorting algorithms.

All methods return a new sorted list (do NOT mutate the original).
"""

from __future__ import annotations

from typing import Any, List


class SortingError(RuntimeError):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class SortingEngine:
    """Stateless sorting utility — methods return a new sorted list."""

    @staticmethod
    def _require_list(data: Any) -> None:
        if not isinstance(data, list):
            raise SortingError(f"Sorting requires a list, got {type(data).__name__}")

    def bubble_sort(self, data: List[Any]) -> List[Any]:
        self._require_list(data)
        result = list(data)
        n = len(result)
        for i in range(n):
            for j in range(0, n - i - 1):
                if result[j] > result[j + 1]:
                    result[j], result[j + 1] = result[j + 1], result[j]
        return result

    def selection_sort(self, data: List[Any]) -> List[Any]:
        self._require_list(data)
        result = list(data)
        n = len(result)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if result[j] < result[min_idx]:
                    min_idx = j
            result[i], result[min_idx] = result[min_idx], result[i]
        return result

    def insertion_sort(self, data: List[Any]) -> List[Any]:
        self._require_list(data)
        result = list(data)
        for i in range(1, len(result)):
            key = result[i]
            j = i - 1
            while j >= 0 and result[j] > key:
                result[j + 1] = result[j]
                j -= 1
            result[j + 1] = key
        return result

    def quick_sort(self, data: List[Any]) -> List[Any]:
        self._require_list(data)
        if len(data) <= 1:
            return list(data)
        return self._quick_rec(list(data))

    def _quick_rec(self, arr: List[Any]) -> List[Any]:
        if len(arr) <= 1:
            return arr
        pivot = arr[-1]
        left = [x for x in arr[:-1] if x <= pivot]
        right = [x for x in arr[:-1] if x > pivot]
        return self._quick_rec(left) + [pivot] + self._quick_rec(right)

    def merge_sort(self, data: List[Any]) -> List[Any]:
        self._require_list(data)
        return self._merge_rec(list(data))

    def _merge_rec(self, arr: List[Any]) -> List[Any]:
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = self._merge_rec(arr[:mid])
        right = self._merge_rec(arr[mid:])
        return self._merge(left, right)

    @staticmethod
    def _merge(left: List[Any], right: List[Any]) -> List[Any]:
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result
