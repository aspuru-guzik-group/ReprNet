import inspect
import os
from typing import Callable

import bibtexparser

from repr_net.base import Citation


class BibtexManager:
    loaded_bibtex = {}

    @classmethod
    def get_bibtex_lib(cls, bibtex_file_path):
        if bibtex_file_path in cls.loaded_bibtex:
            return cls.loaded_bibtex[bibtex_file_path]
        with open(bibtex_file_path, "r") as f:
            bibtex_string = f.read()
        bib_database = bibtexparser.loads(bibtex_string)
        bibtex_lib = BibtexLib(bib_database, bibtex_file_path)
        cls.loaded_bibtex[bibtex_file_path] = bibtex_lib
        return bibtex_lib


class BibtexLib:
    def __init__(self, bib_database, bib_file_path):
        self.bib_database = bib_database
        self.bib_file_path = bib_file_path

    def get_entry(self, entry_key)-> Citation:
        entry_dict = self.bib_database.entries_dict.get(entry_key, None)
        if entry_dict is None:
            raise KeyError(f"Entry {entry_key} not found in the bibtex file at {self.bib_file_path}")
        return Citation(entry_dict)


def load_bibtex(bibtex_file_path) -> Callable[[str], Citation]:
    # get the path of the file where the function is called
    caller_path = inspect.stack()[1].filename
    # get the directory of the caller file
    caller_dir = os.path.dirname(caller_path)
    # get the full path of the bibtex file
    bibtex_file_path = os.path.join(caller_dir, bibtex_file_path)
    # load the bibtex file
    bibtex_lib = BibtexManager.get_bibtex_lib(bibtex_file_path)
    return bibtex_lib.get_entry


def bib(bibtex_string: str) -> Citation:
    bib_database = bibtexparser.loads(bibtex_string)
    return Citation(bib_database.entries[0])