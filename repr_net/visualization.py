import json
import os

from repr_net.indexing import ComposerEdgeClassID, InputEdgeClassID, OutputEdgeClassID, \
    TransformNodeClassID, ReprNodeClassID, RealizationEdgeClassID

this_path = os.path.dirname(os.path.realpath(__file__))
template_path = os.path.join(this_path, "html_template", "index.html")
template_str = None
from string import Template


# See https://visjs.github.io/vis-network/examples/

default_color = "#000000"

node_class_id_to_color = {
    ReprNodeClassID: "#FF6B6B",  # Bright Coral Red
    TransformNodeClassID: "#4ECDC4",  # Vibrant Aqua
}

edge_class_id_to_color = {
    OutputEdgeClassID: "#4ECDC4",  # Vibrant Aqua
    InputEdgeClassID: "#FF6B6B",  # Bright Coral Red
    ComposerEdgeClassID: "#5E60CE",  # Soft Lavender Blue
    RealizationEdgeClassID: "#FFD166",  # Bright Yellow
}

def get_node_color(node):
    return node_class_id_to_color.get(node["class_id"], default_color)

def get_edge_color(edge):
    return edge_class_id_to_color.get(edge["class_id"], default_color)

def display_network(G, output_path="index.html", show_browser=True, title="Representation network"):
    global template_str
    if template_str is None:
        with open(template_path, "r") as f:
            template_str = f.read()
    """
    Format
    [
        { id: 1, label: "Node 1" },
        { id: 2, label: "Node 2" },
        { id: 3, label: "Node 3" },
        { id: 4, label: "Node 4" },
        { id: 5, label: "Node 5" },
      ]
    """
    nodes = []
    for node_id, node in G.nodes(data=True):
        nodes.append({"id": node_id, "label": node["name"],
                      "color": get_node_color(node),
                      "shape": "diamond" if node["class_id"] == TransformNodeClassID else "box", "information": node["information"]
                      })
    """
    Format
    [
        { from: 1, to: 3 },
        { from: 1, to: 2 },
        { from: 2, to: 4 },
        { from: 2, to: 5 },
        { from: 3, to: 3 },
      ]
    """
    edges = []
    for in_edge, out_edge, edge_data in G.edges(data=True):
        edges.append({"from": in_edge, "to": out_edge,
            "color": {
                "color": get_edge_color(edge_data)
            },
            "arrows": "to",
            "dashes": True if edge_data["class_id"] == ComposerEdgeClassID else False
        })

    data = {"nodes": nodes, "edges": edges}
    data_json = json.dumps(data)
    data_declaration = f"var data = {data_json};"
    html = Template(template_str).substitute(data=data_declaration, title=title)
    with open(output_path, "w") as f:
        f.write(html)
    full_output_path = 'file:///' + os.path.abspath(output_path)
    if show_browser:
        import webbrowser
        webbrowser.open(full_output_path)
