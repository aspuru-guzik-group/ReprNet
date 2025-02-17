# add parent directory to path
import sys
sys.path.append(".")

import chem_net
from repr_net.indexing import generate_network_from_module
from repr_net.visualization import display_network
output_path = sys.argv[1]
G = generate_network_from_module(chem_net)
display_network(G, show_browser=False, output_path=output_path, title="Chemistry Representation Network")
