from __future__ import annotations

from typing import List


class Citation:
    def __init__(self, entry_dict):
        self.entry_dict = entry_dict


class Entity:
    citations: List[Citation] = []
    description: str = ""
    authors: List[str] = []


class Repr(Entity):
    edges: List[Edge] = []

    @classmethod
    def add_edge(cls, edge: Edge):
        cls.edges.append(edge)


class Edge(Entity):
    in_nodes: List[Repr] = []
    out_nodes: List[Repr] = []
    composer: Repr = None