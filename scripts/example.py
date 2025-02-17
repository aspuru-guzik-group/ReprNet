
import chem_net
from repr_net.indexing import generate_network_from_module
from repr_net.visualization import display_network
G = generate_network_from_module(chem_net)
display_network(G)
