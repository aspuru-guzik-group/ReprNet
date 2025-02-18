from chem_net.knowledge.base import MoleculePropertyKnowledge
from chem_net.molecule.base import AtomCoordinates
from chem_net.program.base import Program
from chem_net.quantum_computing.base import QuantumCircuit, QuantumComputer, \
    MeasurementOutcome, QuantumState
from repr_net import Transform


class VQE_Circuit_Optimization(Transform):
    in_nodes = [AtomCoordinates]
    out_nodes = [QuantumCircuit]
    composer = QuantumComputer

class MolecularStateEnergy(MeasurementOutcome, MoleculePropertyKnowledge):
    pass