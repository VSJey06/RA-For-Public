"""DequeEngine — runtime container for named deques.

Each deque is a collections.deque supporting double-ended operations.
Supports both queue (FIFO) and stack (LIFO) behavior through
push_front/pop_front and push_back/pop_back respectively.
"""

from __future__ import annotations

from collections import deque as _deque
from typing import Any


class DequeError(RuntimeError):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class DequeEngine:
    def __init__(self) -> None:
        self._deques: dict[str, _deque] = {}

    def create(self, name: str) -> None:
        if name not in self._deques:
            self._deques[name] = _deque()

    def has(self, name: str) -> bool:
        return name in self._deques

    def _get(self, name: str) -> _deque:
        if name not in self._deques:
            raise DequeError(f"Deque '{name}' is not defined")
        return self._deques[name]

    def push_front(self, name: str, value: Any) -> None:
        if name not in self._deques:
            self._deques[name] = _deque()
        self._deques[name].appendleft(value)

    def push_back(self, name: str, value: Any) -> None:
        if name not in self._deques:
            self._deques[name] = _deque()
        self._deques[name].append(value)

    def pop_front(self, name: str) -> Any:
        dq = self._get(name)
        if not dq:
            raise DequeError(f"Cannot pop_front from empty deque '{name}'")
        return dq.popleft()

    def pop_back(self, name: str) -> Any:
        dq = self._get(name)
        if not dq:
            raise DequeError(f"Cannot pop_back from empty deque '{name}'")
        return dq.pop()

    def peek_front(self, name: str) -> Any:
        dq = self._get(name)
        if not dq:
            raise DequeError(f"Cannot peek_front at empty deque '{name}'")
        return dq[0]

    def peek_back(self, name: str) -> Any:
        dq = self._get(name)
        if not dq:
            raise DequeError(f"Cannot peek_back at empty deque '{name}'")
        return dq[-1]

    def size(self, name: str) -> int:
        return len(self._get(name))

    def is_empty(self, name: str) -> bool:
        return len(self._get(name)) == 0

    def clear(self, name: str) -> None:
        if name not in self._deques:
            return
        self._deques[name].clear()
