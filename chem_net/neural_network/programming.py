from chem_net.neural_network.neural_network import Optimizer
from repr_net.base import Repr, Edge


class Code(Repr):
    pass

class Human(Repr):
    pass

class Compiler(Repr):
    pass

class CompilingOptimizer(Edge):
    in_nodes = [Code]
    out_nodes = [Optimizer]
    composer = Compiler