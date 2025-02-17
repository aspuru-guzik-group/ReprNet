from __future__ import annotations

from typing import List


class Citation:
    def __init__(self, entry_dict):
        self.entry_dict = entry_dict

    def simple_dict(self):
        d = {
            "title": self.entry_dict["title"],
        }
        if "author" in self.entry_dict:
            d["author"] = self.entry_dict["author"]
        if "year" in self.entry_dict:
            d["year"] = self.entry_dict["year"]
        return d

class Entity:
    _id: int = None
    _file_path: str = None
    citations: List[Citation] = []
    description: str = ""
    contributors: List[str] = []


class Repr(Entity):
    edges: List[Transform] = []

    @classmethod
    def add_edge(cls, edge: Transform):
        cls.edges.append(edge)


class Transform(Entity):
    in_nodes: List[Repr] = []
    out_nodes: List[Repr] = []
    composer: Repr = None