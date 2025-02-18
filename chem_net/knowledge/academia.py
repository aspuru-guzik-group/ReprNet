from chem_net.general import Document
from chem_net.meta import Human, HumanKnowledge
from repr_net import Transform


class Paper(Document):
    pass



class WritePaper(Transform):
    in_nodes = [HumanKnowledge]
    out_nodes = [Paper]
    composer = Human