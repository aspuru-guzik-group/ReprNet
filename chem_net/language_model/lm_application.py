from chem_net.general import Text
from chem_net.language_model.agent import Prompt
from chem_net.language_model.base import LanguageModel
from chem_net.program.base import Program
from repr_net import Transform


class LM_CodeGeneration(Transform):
    in_nodes = [Prompt]
    out_nodes = [Program]
    composer = LanguageModel


class LM_TextGeneration(Transform):
    in_nodes = [Prompt]
    out_nodes = [Text]
    composer = LanguageModel