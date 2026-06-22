"""GraphEngine — runtime container for named graphs.

Each graph stores nodes (as a set) and directed edges (adjacency list).
Supports BFS and DFS traversal.
"""

from __future__ import annotations

from collections import deque
from typing import Any, Dict, List, Set


class GraphError(RuntimeError):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class GraphEngine:
    def __init__(self) -> None:
        self._graphs: dict[str, dict] = {}

    def create(self, name: str) -> None:
        if name not in self._graphs:
            self._graphs[name] = {"nodes": set(), "edges": {}}

    def has(self, name: str) -> bool:
        return name in self._graphs

    def _get(self, name: str) -> dict:
        if name not in self._graphs:
            raise GraphError(f"Graph '{name}' is not defined")
        return self._graphs[name]

    def add_node(self, name: str, value: Any) -> None:
        g = self._get(name)
        g["nodes"].add(value)

    def remove_node(self, name: str, value: Any) -> None:
        g = self._get(name)
        if value not in g["nodes"]:
            raise GraphError(f"Node '{value}' not found in graph '{name}'")
        g["nodes"].discard(value)
        g["edges"].pop(value, None)
        for src in list(g["edges"]):
            g["edges"][src].discard(value)

    def has_node(self, name: str, value: Any) -> bool:
        g = self._get(name)
        return value in g["nodes"]

    def add_edge(self, name: str, source: Any, target: Any) -> None:
        g = self._get(name)
        if source not in g["nodes"]:
            raise GraphError(f"Source node '{source}' not found in graph '{name}'")
        if target not in g["nodes"]:
            raise GraphError(f"Target node '{target}' not found in graph '{name}'")
        if source not in g["edges"]:
            g["edges"][source] = set()
        g["edges"][source].add(target)

    def remove_edge(self, name: str, source: Any, target: Any) -> None:
        g = self._get(name)
        if source not in g["edges"] or target not in g["edges"].get(source, set()):
            raise GraphError(
                f"Edge '{source}->{target}' not found in graph '{name}'"
            )
        g["edges"][source].discard(target)

    def has_edge(self, name: str, source: Any, target: Any) -> bool:
        g = self._get(name)
        return source in g["edges"] and target in g["edges"][source]

    def neighbors(self, name: str, node: Any) -> List[Any]:
        g = self._get(name)
        if node not in g["nodes"]:
            raise GraphError(f"Node '{node}' not found in graph '{name}'")
        return sorted(g["edges"].get(node, set()), key=str)

    def node_count(self, name: str) -> int:
        return len(self._get(name)["nodes"])

    def edge_count(self, name: str) -> int:
        g = self._get(name)
        return sum(len(edges) for edges in g["edges"].values())

    def clear(self, name: str) -> None:
        if name not in self._graphs:
            return
        self._graphs[name] = {"nodes": set(), "edges": {}}

    def bfs(self, name: str, start: Any) -> List[Any]:
        g = self._get(name)
        if start not in g["nodes"]:
            raise GraphError(f"Start node '{start}' not found in graph '{name}'")
        visited: Set[Any] = set()
        result: List[Any] = []
        q: deque = deque([start])
        while q:
            node = q.popleft()
            if node in visited:
                continue
            visited.add(node)
            result.append(node)
            for neighbor in sorted(g["edges"].get(node, set()), key=str):
                if neighbor not in visited:
                    q.append(neighbor)
        return result

    def dfs(self, name: str, start: Any) -> List[Any]:
        g = self._get(name)
        if start not in g["nodes"]:
            raise GraphError(f"Start node '{start}' not found in graph '{name}'")
        visited: Set[Any] = set()
        result: List[Any] = []
        stack: List[Any] = [start]
        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            result.append(node)
            for neighbor in sorted(g["edges"].get(node, set()), key=str, reverse=True):
                if neighbor not in visited:
                    stack.append(neighbor)
        return result
