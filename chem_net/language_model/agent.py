from chem_net.language_model.base import Token, LanguageModel
from chem_net.language_model.rag import RetrivalAugmentedGenerator
from chem_net.meta import Human, HumanKnowledge
from chem_net.program.base import Program
from repr_net import Transform


class Prompt(Token):
    pass


class MakePrompts(Transform):
    in_nodes = [HumanKnowledge]
    out_nodes = [Prompt]
    composer = Human


class LLM_Pipeline(Prompt, LanguageModel):
    pass


class AgentToolSet(Prompt, Program):
    pass


class AgentMemory(RetrivalAugmentedGenerator):
    pass