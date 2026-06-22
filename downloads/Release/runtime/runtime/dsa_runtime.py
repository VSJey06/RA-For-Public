"""
dsa_runtime.py — Centralised DSA execution support for the RA runtime.

Provides wrappers around the existing engines, exposing the standard RA
DSA API for queues, stacks, graphs, trees, deques, sorting, and searching.
"""

from __future__ import annotations

from typing import Any, List, Optional

from runtime.deque_engine import DequeEngine, DequeError
from runtime.graph_engine import GraphEngine, GraphError
from runtime.queue_engine import QueueEngine, QueueError
from runtime.searching_engine import SearchingEngine, SearchingError
from runtime.sorting_engine import SortingEngine, SortingError
from runtime.stack_engine import StackEngine, StackError
from runtime.tree_engine import TreeEngine, TreeError


class DSAError(RuntimeError):
    """Base exception for DSA runtime errors."""


class QueueRuntime:
    """RA Queue runtime — wraps ``QueueEngine`` with the standard API.

    Operations
    ----------
    enqueue(value)  — add to rear
    dequeue()       — remove and return from front
    peek()          — return front value without removal
    size()          — number of elements
    is_empty()      — True when no elements
    clear()         — remove all elements
    """

    def __init__(self, engine: QueueEngine, name: str) -> None:
        self._engine = engine
        self._name = name

    def enqueue(self, value: Any) -> None:
        self._engine.push(self._name, value)

    def dequeue(self) -> Any:
        return self._engine.pop(self._name)

    def peek(self) -> Any:
        return self._engine.peek(self._name)

    def size(self) -> int:
        return self._engine.size(self._name)

    def is_empty(self) -> bool:
        return self._engine.empty(self._name)

    def clear(self) -> None:
        self._engine.clear(self._name)


class StackRuntime:
    """RA Stack runtime — wraps ``StackEngine`` with the standard API.

    Operations
    ----------
    push(value)  — add to top
    pop()        — remove and return from top
    peek()       — return top value without removal
    size()       — number of elements
    is_empty()   — True when no elements
    clear()      — remove all elements
    """

    def __init__(self, engine: StackEngine, name: str) -> None:
        self._engine = engine
        self._name = name

    def push(self, value: Any) -> None:
        self._engine.push(self._name, value)

    def pop(self) -> Any:
        return self._engine.pop(self._name)

    def peek(self) -> Any:
        return self._engine.peek(self._name)

    def size(self) -> int:
        return self._engine.count(self._name)

    def is_empty(self) -> bool:
        return self._engine.empty(self._name)

    def clear(self) -> None:
        self._engine.clear(self._name)


class GraphRuntime:
    """RA Graph runtime — wraps ``GraphEngine`` with the standard API."""

    def __init__(self, engine: GraphEngine, name: str) -> None:
        self._engine = engine
        self._name = name

    def add_node(self, value: Any) -> None:
        self._engine.add_node(self._name, value)

    def remove_node(self, value: Any) -> None:
        self._engine.remove_node(self._name, value)

    def has_node(self, value: Any) -> bool:
        return self._engine.has_node(self._name, value)

    def add_edge(self, source: Any, target: Any) -> None:
        self._engine.add_edge(self._name, source, target)

    def remove_edge(self, source: Any, target: Any) -> None:
        self._engine.remove_edge(self._name, source, target)

    def has_edge(self, source: Any, target: Any) -> bool:
        return self._engine.has_edge(self._name, source, target)

    def neighbors(self, value: Any) -> List[Any]:
        return self._engine.neighbors(self._name, value)

    def node_count(self) -> int:
        return self._engine.node_count(self._name)

    def edge_count(self) -> int:
        return self._engine.edge_count(self._name)

    def clear(self) -> None:
        self._engine.clear(self._name)

    def bfs(self, start: Any) -> List[Any]:
        return self._engine.bfs(self._name, start)

    def dfs(self, start: Any) -> List[Any]:
        return self._engine.dfs(self._name, start)


class TreeRuntime:
    """RA Tree runtime — wraps ``TreeEngine`` with the standard API."""

    def __init__(self, engine: TreeEngine, name: str) -> None:
        self._engine = engine
        self._name = name

    def create_root(self, value: Any) -> None:
        self._engine.create_root(self._name, value)

    def add_child(self, parent: Any, value: Any) -> None:
        self._engine.add_child(self._name, parent, value)

    def remove_node(self, value: Any) -> None:
        self._engine.remove_node(self._name, value)

    def has_node(self, value: Any) -> bool:
        return self._engine.has_node(self._name, value)

    def children(self, value: Any) -> List[Any]:
        return self._engine.children(self._name, value)

    def parent(self, value: Any) -> Optional[Any]:
        return self._engine.parent(self._name, value)

    def depth(self, value: Any) -> int:
        return self._engine.depth(self._name, value)

    def height(self) -> int:
        return self._engine.height(self._name)

    def clear(self) -> None:
        self._engine.clear(self._name)

    def preorder(self) -> List[Any]:
        return self._engine.preorder(self._name)

    def postorder(self) -> List[Any]:
        return self._engine.postorder(self._name)

    def levelorder(self) -> List[Any]:
        return self._engine.levelorder(self._name)


class DequeRuntime:
    """RA Deque runtime — wraps ``DequeEngine`` with the standard API.

    Supports both queue (FIFO) and stack (LIFO) behavior:
      push_back / pop_front  — queue mode
      push_back / pop_back   — stack mode
    """

    def __init__(self, engine: DequeEngine, name: str) -> None:
        self._engine = engine
        self._name = name

    def push_front(self, value: Any) -> None:
        self._engine.push_front(self._name, value)

    def push_back(self, value: Any) -> None:
        self._engine.push_back(self._name, value)

    def pop_front(self) -> Any:
        return self._engine.pop_front(self._name)

    def pop_back(self) -> Any:
        return self._engine.pop_back(self._name)

    def peek_front(self) -> Any:
        return self._engine.peek_front(self._name)

    def peek_back(self) -> Any:
        return self._engine.peek_back(self._name)

    def size(self) -> int:
        return self._engine.size(self._name)

    def is_empty(self) -> bool:
        return self._engine.is_empty(self._name)

    def clear(self) -> None:
        self._engine.clear(self._name)


class SortingRuntime:
    """RA Sorting runtime — wraps ``SortingEngine``.

    Operations return a new sorted list (original is not mutated).
    """

    def __init__(self, engine: SortingEngine, name: str) -> None:
        self._engine = engine
        self._name = name

    def bubble_sort(self, data: List[Any]) -> List[Any]:
        return self._engine.bubble_sort(data)

    def selection_sort(self, data: List[Any]) -> List[Any]:
        return self._engine.selection_sort(data)

    def insertion_sort(self, data: List[Any]) -> List[Any]:
        return self._engine.insertion_sort(data)

    def quick_sort(self, data: List[Any]) -> List[Any]:
        return self._engine.quick_sort(data)

    def merge_sort(self, data: List[Any]) -> List[Any]:
        return self._engine.merge_sort(data)


class SearchingRuntime:
    """RA Searching runtime — wraps ``SearchingEngine``.

    Operations return index of target or -1 if not found.
    """

    def __init__(self, engine: SearchingEngine, name: str) -> None:
        self._engine = engine
        self._name = name

    def linear_search(self, data: List[Any], target: Any) -> int:
        return self._engine.linear_search(data, target)

    def binary_search(self, data: List[Any], target: Any) -> int:
        return self._engine.binary_search(data, target)
