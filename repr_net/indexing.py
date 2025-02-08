import os
import importlib.util
import inspect
from typing import List, Type

from bokeh.palettes import Blues8
from bokeh.transform import linear_cmap

from repr_net.base import Entity, Repr, Edge

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

EdgeClassID = 1 / 2
ReprClassID = 2 / 2

def extract_entities_from_directory() -> List[Type]:
    # get the path of the file where the function is called
    caller_path = inspect.stack()[1].filename
    # get the directory of the caller file
    caller_dir = os.path.dirname(caller_path)
    # load the classes
    classes = recursively_load_classes(caller_dir, class_filter=lambda x: issubclass(x, Entity))
    edges = [cls for cls in classes if issubclass(cls, Edge)]
    reprs = [cls for cls in classes if issubclass(cls, Repr)]
    cls_to_node = {}
    def check_and_add(cls):
        if cls not in cls_to_node:
            G.add_node(cls.__name__, name=cls.__name__, description=cls.description, class_id=ReprClassID)
            cls_to_node[cls] = cls.__name__

    G = nx.Graph()
    # add the classes to the graph
    #for repr_class in reprs:
    #    G.add_node(repr_class.__name__, name=repr_class.__name__, description=repr_class.description)
    #    cls_to_node[repr_class] = repr_class.__name__
    for edge_class in edges:
        for out_node in edge_class.out_nodes:
            check_and_add(out_node)
        check_and_add(edge_class.composer)
        G.add_node(edge_class.__name__, name=edge_class.__name__, description=edge_class.description, class_id=EdgeClassID)
        for in_node in edge_class.in_nodes:
            check_and_add(in_node)
            G.add_edge(in_node.__name__, edge_class.__name__)
        G.add_edge(edge_class.composer.__name__, edge_class.__name__)

        for out_node in edge_class.out_nodes:
            G.add_edge(edge_class.__name__, out_node.__name__)


    display_network(G)

def display_network(G):
    #https://melaniewalsh.github.io/Intro-Cultural-Analytics/06-Network-Analysis/02-Making-Network-Viz-with-Bokeh.html
    from bokeh.io import output_notebook, show, save
    from bokeh.models import Range1d, Circle, ColumnDataSource, MultiLine
    from bokeh.plotting import figure
    from bokeh.plotting import from_networkx
    HOVER_TOOLTIPS = [("Name", "@name"), ("Description", "@description")]
    title = "Network of representation"
    # Create a plot — set dimensions, toolbar, and title
    plot = figure(tooltips = HOVER_TOOLTIPS,
                  tools="pan,wheel_zoom,save,reset", active_scroll='wheel_zoom',
                  x_range=Range1d(-10.1, 10.1), y_range=Range1d(-10.1, 10.1), title=title)

    # Create a network graph object with spring layout
    # https://networkx.github.io/documentation/networkx-1.9/reference/generated/networkx.drawing.layout.spring_layout.html
    network_graph = from_networkx(G, nx.spring_layout, scale=10, center=(0, 0))
    color_by_this_attribute = "class_id"
    color_palette = Blues8
    # Set node size and color
    network_graph.node_renderer.glyph = Circle(radius="class_id", fill_color=linear_cmap(color_by_this_attribute,color_palette, 0, 5))

    # Set edge opacity and width
    network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.5, line_width=1)

    # Add network graph to the plot
    plot.renderers.append(network_graph)

    show(plot)
