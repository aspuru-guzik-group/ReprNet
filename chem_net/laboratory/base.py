from chem_net.general import Text, Image, Number, Document
from chem_net.meta import HumanKnowledge, Human
from repr_net import Repr, Transform

class PhysicalMolecule(Repr):
    pass


class Equipment(Repr):
    pass


class EquipmentReadout(Document):
    pass


class EquipmentMeasurement(Transform):
    in_nodes = [PhysicalMolecule]
    out_nodes = [EquipmentReadout]
    composer = Equipment


class ReadingEquipmentReadout(Transform):
    in_nodes = [EquipmentReadout]
    out_nodes = [HumanKnowledge]
    composer = Human