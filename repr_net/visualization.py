import json
import os

this_path = os.path.dirname(os.path.realpath(__file__))
template_path = os.path.join(this_path, "html_template", "index.html")
template_str = None
from string import Template
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
    for node in G.nodes(data=True):
        nodes.append({"id": node[0], "label": node[1]["name"]})
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
    for edge in G.edges():
        edges.append({"from": edge[0], "to": edge[1]})

    data = {"nodes": nodes, "edges": edges}
    data_json = json.dumps(data)
    data_declaration = f"var data = {data_json};"
    html = Template(template_str).substitute(data=data_declaration, title=title)
    with open(output_path, "w") as f:
        f.write(html)
    full_output_path = os.path.abspath(output_path)
    if show_browser:
        import webbrowser
        webbrowser.open(full_output_path)
