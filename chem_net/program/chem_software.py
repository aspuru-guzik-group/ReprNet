from chem_net.knowledge.base import QuantumChemistryKnowledge
from chem_net.meta import HumanKnowledge, Human
from chem_net.molecule.base import AtomCoordinates
from chem_net.program.base import Program
from repr_net.base import Transform, Repr


class MakeChemistrySoftware(Transform):
    in_nodes = [HumanKnowledge]
    out_nodes = [Program]
    composer = Human


class QuantumChemistrySoftware(Program):
    pass

class MakeQuantumChemistrySoftware(Transform):
    in_nodes = [QuantumChemistryKnowledge]
    out_nodes = [QuantumChemistrySoftware]
    composer = Human


class ForceFieldInformation(Repr):
    pass

class CalculateForceField(Transform):
    in_nodes = [AtomCoordinates]
    out_nodes = [ForceFieldInformation]
    composer = QuantumChemistrySoftware


class CalculateForceFieldByDFT(CalculateForceField):
    pass


class OptimizeCoordinateByForceField(Transform):
    in_nodes = [AtomCoordinates, ForceFieldInformation]
    out_nodes = [AtomCoordinates]
    composer = QuantumChemistrySoftware