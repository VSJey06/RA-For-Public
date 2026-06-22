"""TreeEngine — runtime container for named trees.

Each tree stores nodes with parent references and child lists.
Supports preorder, postorder, and levelorder traversals.
"""

from __future__ import annotations

from collections import deque
from typing import Any, Dict, List, Optional


class TreeError(RuntimeError):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class TreeEngine:
    def __init__(self) -> None:
        self._trees: dict[str, dict] = {}

    def create(self, name: str) -> None:
        if name not in self._trees:
            self._trees[name] = {"root": None, "nodes": {}}

    def has(self, name: str) -> bool:
        return name in self._trees

    def _get(self, name: str) -> dict:
        if name not in self._trees:
            raise TreeError(f"Tree '{name}' is not defined")
        return self._trees[name]

    def create_root(self, name: str, value: Any) -> None:
        t = self._get(name)
        if t["root"] is not None:
            raise TreeError(f"Tree '{name}' already has a root")
        if value in t["nodes"]:
            raise TreeError(f"Node '{value}' already exists in tree '{name}'")
        t["root"] = value
        t["nodes"][value] = {"parent": None, "children": []}

    def add_child(self, name: str, parent: Any, value: Any) -> None:
        t = self._get(name)
        if parent not in t["nodes"]:
            raise TreeError(f"Parent node '{parent}' not found in tree '{name}'")
        if value in t["nodes"]:
            raise TreeError(f"Node '{value}' already exists in tree '{name}'")
        t["nodes"][value] = {"parent": parent, "children": []}
        t["nodes"][parent]["children"].append(value)

    def remove_node(self, name: str, value: Any) -> None:
        t = self._get(name)
        if value not in t["nodes"]:
            raise TreeError(f"Node '{value}' not found in tree '{name}'")
        if t["root"] == value:
            raise TreeError(f"Cannot remove root node '{value}' from tree '{name}'")
        self._remove_subtree(t, value)

    def _remove_subtree(self, t: dict, value: Any) -> None:
        for child in list(t["nodes"][value]["children"]):
            self._remove_subtree(t, child)
        parent = t["nodes"][value]["parent"]
        if parent is not None:
            t["nodes"][parent]["children"].remove(value)
        del t["nodes"][value]

    def has_node(self, name: str, value: Any) -> bool:
        t = self._get(name)
        return value in t["nodes"]

    def children(self, name: str, value: Any) -> List[Any]:
        t = self._get(name)
        if value not in t["nodes"]:
            raise TreeError(f"Node '{value}' not found in tree '{name}'")
        return list(t["nodes"][value]["children"])

    def parent(self, name: str, value: Any) -> Optional[Any]:
        t = self._get(name)
        if value not in t["nodes"]:
            raise TreeError(f"Node '{value}' not found in tree '{name}'")
        return t["nodes"][value]["parent"]

    def depth(self, name: str, value: Any) -> int:
        t = self._get(name)
        if value not in t["nodes"]:
            raise TreeError(f"Node '{value}' not found in tree '{name}'")
        d = 0
        cur = t["nodes"][value]["parent"]
        while cur is not None:
            d += 1
            cur = t["nodes"][cur]["parent"]
        return d

    def height(self, name: str) -> int:
        t = self._get(name)
        if t["root"] is None:
            return -1
        return self._height_of(t, t["root"])

    def _height_of(self, t: dict, node: Any) -> int:
        children = t["nodes"][node]["children"]
        if not children:
            return 0
        return 1 + max(self._height_of(t, c) for c in children)

    def clear(self, name: str) -> None:
        if name not in self._trees:
            return
        self._trees[name] = {"root": None, "nodes": {}}

    def preorder(self, name: str) -> List[Any]:
        t = self._get(name)
        if t["root"] is None:
            return []
        result: List[Any] = []
        self._preorder_rec(t, t["root"], result)
        return result

    def _preorder_rec(self, t: dict, node: Any, result: List[Any]) -> None:
        result.append(node)
        for child in t["nodes"][node]["children"]:
            self._preorder_rec(t, child, result)

    def postorder(self, name: str) -> List[Any]:
        t = self._get(name)
        if t["root"] is None:
            return []
        result: List[Any] = []
        self._postorder_rec(t, t["root"], result)
        return result

    def _postorder_rec(self, t: dict, node: Any, result: List[Any]) -> None:
        for child in t["nodes"][node]["children"]:
            self._postorder_rec(t, child, result)
        result.append(node)

    def levelorder(self, name: str) -> List[Any]:
        t = self._get(name)
        if t["root"] is None:
            return []
        result: List[Any] = []
        q: deque = deque([t["root"]])
        while q:
            node = q.popleft()
            result.append(node)
            for child in t["nodes"][node]["children"]:
                q.append(child)
        return result
