from chem_net.general import Text
from chem_net.knowledge.base import MoleculePropertyKnowledge
from chem_net.meta import Human
from repr_net import Repr, Transform


class AtomCoordinates(Repr):
    description = "A set of coordinates for a molecule. Usually in .xyz format."

class ReadAtomCoordinates(Transform):
    in_nodes = [AtomCoordinates]
    out_nodes = [MoleculePropertyKnowledge]
    composer = Human

class MoleculeString(Text):
    pass

class MolecularFormula(MoleculeString):
    pass

class SMILES(MoleculeString):
    pass

class SELFIES(MoleculeString):
    pass

class GeometryOptimizer(Repr):
    pass

class ConformationalGeneration(Transform):
    in_nodes = [MoleculeString]
    out_nodes = [AtomCoordinates]
    composer = GeometryOptimizer

