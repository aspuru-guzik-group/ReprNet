import json
import os
import importlib.util
import inspect
from typing import List, Type

from repr_net.base import Entity, Repr, Transform

import networkx as nx
def load_classes_from_file(file_path: str, class_filter=None) -> List[Type]:
    """Dynamically loads all classes from a given Python file."""
    classes = []
    if class_filter is None:
        class_filter = lambda x: True
    module_name = os.path.splitext(os.path.basename(file_path))[0]

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for name, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ == module_name:  # Ensure class is defined in this file
                if class_filter(obj):
                    obj._file_path = file_path
                    classes.append(obj)

    return classes


def recursively_load_classes(directory: str, class_filter=None) -> List[Type]:
    """Recursively loads all classes from Python files in a given directory."""
    all_classes = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                file_path = os.path.join(root, file)
                all_classes.extend(load_classes_from_file(file_path, class_filter=class_filter))
    return all_classes


def make_name_from_class_name(class_name: str) -> str:
    """
    :param class_name: names like LM_Embedding or EmbeddingVector
    :return: LM Embedding or Embedding Vector
    """
    name = []
    for i, c in enumerate(class_name):
        if c == "_":
            name.append(" ")
            continue
        if c.islower() and i<len(class_name)-1 and class_name[i+1].isupper():
            name.append(c + " ")
            continue
        name.append(c)
    return "".join(name)

TransformNodeClassID = 1
ReprNodeClassID = 2

InputEdgeClassID = 1
OutputEdgeClassID = 2
ComposerEdgeClassID = 3

RealizationEdgeClassID = 4

def generate_network_from_directory(dir) -> nx.Graph:
    # load the classes
    classes = recursively_load_classes(dir, class_filter=lambda x: issubclass(x, Entity))
    transforms = [cls for cls in classes if issubclass(cls, Transform)]
    reprs = [cls for cls in classes if issubclass(cls, Repr)]
    realizations = []

    for repr_class in reprs:
        parent_classes = repr_class.__bases__
        for parent_class in parent_classes:
            if parent_class is Repr:
                continue
            assert issubclass(parent_class, Repr)
            realizations.append((parent_class, repr_class))

    for transform_class in transforms:
        parent_classes = transform_class.__bases__
        assert len(parent_classes) == 1
        parent_class = parent_classes[0]
        if parent_class is Transform:
            continue
        realizations.append((parent_class, transform_class))

    cls_to_node_id = {}
    def check_and_add(cls):
        if cls in cls_to_node_id:
            return
        information = {
            "description": cls.description,
            "contributors": cls.contributors,
            "references": [c.simple_dict() for c in cls.citations]
        }
        class_id = ReprNodeClassID if issubclass(cls, Repr) else TransformNodeClassID
        if cls._file_path is None:
            cls._file_path = inspect.getfile(cls)
        cls._id = str(hash(cls._file_path + cls.__name__))
        G.add_node(cls._id, name=make_name_from_class_name(cls.__name__), information=information, class_id=class_id)
        cls_to_node_id[cls] = cls._id

    G = nx.MultiDiGraph()
    for transform_class in transforms:
        for out_node in transform_class.out_nodes:
            check_and_add(out_node)
        check_and_add(transform_class.composer)
        check_and_add(transform_class)
        #G.add_node(transform_class.__name__, name=transform_class.__name__, description=transform_class.description, class_id=TransformNodeClassID)
        for in_node in transform_class.in_nodes:
            check_and_add(in_node)
            G.add_edge(in_node._id, transform_class._id, class_id=InputEdgeClassID)
        G.add_edge(transform_class.composer._id, transform_class._id, class_id=ComposerEdgeClassID)

        for out_node in transform_class.out_nodes:
            G.add_edge(transform_class._id, out_node._id, class_id=OutputEdgeClassID)


    for parent_class, repr_class in realizations:
        check_and_add(parent_class)
        check_and_add(repr_class)
        G.add_edge(parent_class._id, repr_class._id, class_id=RealizationEdgeClassID)

    return G

def generate_network_here() -> nx.Graph:
    # get the path of the file where the function is called
    caller_path = inspect.stack()[1].filename
    # get the directory of the caller file
    caller_dir = os.path.dirname(caller_path)
    return generate_network_from_directory(caller_dir)


def generate_network_from_module(module) -> nx.Graph:
    module_path = inspect.getfile(module)
    module_dir = os.path.dirname(module_path)
    return generate_network_from_directory(module_dir)