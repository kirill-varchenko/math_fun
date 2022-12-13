from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Iterable, Protocol


class Label(Protocol):
    def __hash__(self) -> int:
        ...


class DAGException(Exception):
    pass


class NodeStatusError(DAGException):
    pass


class CycleError(DAGException):
    pass


class NodeStatus(Enum):
    PENDING = auto()
    READY = auto()
    ACTIVE = auto()
    DONE = auto()


@dataclass
class Node:
    label: Label
    status: NodeStatus = NodeStatus.PENDING
    ancestors: set[Label] = field(default_factory=set)
    descendants: set[Label] = field(default_factory=set)


class ComputationalDAG:
    def __init__(self, precomputed_nodes: Iterable[Label] | None = None) -> None:
        self.nodes: dict[Label, Node] = (
            {
                label: Node(label=label, status=NodeStatus.DONE)
                for label in precomputed_nodes
            }
            if precomputed_nodes
            else {}
        )

    def add_node(
        self, node: Label, depends_on: Iterable[Label] | None = None
    ) -> None:
        if node in self.nodes and self.nodes[node].status in {
            NodeStatus.DONE,
            NodeStatus.ACTIVE,
        }:
            raise NodeStatusError(
                f"Node {node!r} already has status {self.nodes[node].status}"
            )
        elif node not in self.nodes:
            self.nodes[node] = Node(label=node)

        if depends_on:
            self.nodes[node].ancestors |= set(depends_on)
            for dependence in depends_on:
                if dependence not in self.nodes:
                    self.nodes[dependence] = Node(label=dependence)
                self.nodes[dependence].descendants.add(node)
        else:
            self.nodes[node].status = NodeStatus.READY

    def _get_uncomputable_nodes(self) -> set:
        uncomputable = set()
        stack = [
            node
            for node in self.nodes.values()
            if node.status == NodeStatus.PENDING and not node.ancestors
        ]
        while stack:
            node = stack.pop()
            uncomputable.add(node.label)
            for v in node.descendants:
                stack.append(self.nodes[v])
        return uncomputable

    def iter_computable_nodes(self):
        ordered: list[Label] = []
        waiting: list[Node] = []
        permanents: set[Label] = set()
        temporaries: set[Label] = set()

        def visit(v: Node) -> None:
            if v.label in permanents:
                return
            if v.label in temporaries:
                raise CycleError(v.label)
            temporaries.add(v.label)
            for label in v.descendants:
                if self.nodes[label].status != NodeStatus.PENDING:
                    visit(self.nodes[label])
            temporaries.remove(v.label)
            permanents.add(v.label)
            if v.status in {NodeStatus.ACTIVE, NodeStatus.READY}:
                ordered.append(v.label)

        uncomputable = self._get_uncomputable_nodes()
        for node in self.nodes.values():
            if node.status in {NodeStatus.DONE, NodeStatus.READY}:
                waiting.append(node)
            elif node.label not in uncomputable:
                node.status = NodeStatus.ACTIVE

        while waiting:
            node = waiting.pop()
            if node.label in permanents:
                continue
            visit(node)

        yield from reversed(ordered)

        for node in self.nodes.values():
            if node.status == NodeStatus.ACTIVE:
                node.status = NodeStatus.PENDING

    def done(self, node: Label) -> None:
        self.nodes[node].status = NodeStatus.DONE

    @property
    def undone_count(self) -> int:
        return sum(node.status != NodeStatus.DONE for node in self.nodes.values())
