from chem_net.general import Text, Image
from chem_net.meta import HumanKnowledge, Human
from chem_net.neural_network.base import NeuralNetwork, Training
from repr_net.base import Transform, Repr
from repr_net.bibtex import bib


class Token(Repr):
    pass


class ReadingToken(Transform):
    in_nodes = [Token]
    out_nodes = [HumanKnowledge]
    composer = Human



class Tokenizer(Repr):
    pass

class Tokenize(Transform):
    in_nodes = [Text]
    out_nodes = [Token]
    composer = Tokenizer



class LanguageModel(NeuralNetwork):
    description = "Language Model"
    citations = [
        bib("""
@misc{devlin2018bert,
    title={BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding},
    author={Jacob Devlin and Ming-Wei Chang and Kenton Lee and Kristina Toutanova},
    year={2018},
    eprint={1810.04805},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
"""),
    ]


class LM_Pretraining(Training):
    in_nodes = [Token]
    out_nodes = [LanguageModel]


class LM_inference(Transform):
    in_nodes = [Token]
    out_nodes = [Token]
    composer = LanguageModel


class MultimodalToken(Token):
    pass


class MultimodalTokenize(Transform):
    in_nodes = [Image]
    out_nodes = [MultimodalToken]
    composer = Tokenizer


class Multimodal_LanguageModel(LanguageModel):
    description = "Multimodal Language Model"