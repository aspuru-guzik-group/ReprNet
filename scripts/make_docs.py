# add parent directory to path
import sys
sys.path.append(".")

import chem_net
from repr_net.indexing import generate_network_from_module
from repr_net.visualization import display_network
output_path = sys.argv[1]
G = generate_network_from_module(chem_net)
description = """
Modify the network on <a href="https://github.com/aspuru-guzik-group/ReprNet">Github</a>
<br/>
<b>How to read the graph?</b> 
<br/>
Nodes: Green diamond: A transform; Red box: A representation; 
<br/>
Edges: Red line: Input edge; Green line: Output edge; Blue dashed line: Composer edge; Yellow line: Abstraction edge.
<br/>
"""
display_network(G, show_browser=False, output_path=output_path, title="Chemistry Representation Network", description=description)
