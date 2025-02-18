from repr_net import Repr, Transform


class QuantumComputer(Repr):
    pass

class QuantumState(Repr):
    pass

class QuantumCircuit(Repr):
    pass

class MeasurementOutcome(Repr):
    pass


class QuantumStatePreparation(Transform):
    in_nodes = [QuantumCircuit]
    out_nodes = [QuantumState]
    composer = QuantumComputer

class QuantumMeasurement(Transform):
    in_nodes = [QuantumState]
    out_nodes = [MeasurementOutcome]
    composer = QuantumComputer
