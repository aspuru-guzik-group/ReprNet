from chem_net.language_model.base import LanguageModel, Token
from chem_net.neural_network.embedding import EmbeddingVector
from repr_net.base import Transform, Repr


class TokensEmbeddingsPair(EmbeddingVector, Token):
    pass


class MakeLM_Embedding(Transform):
    in_nodes = [Token]
    out_nodes = [TokensEmbeddingsPair]
    composer = LanguageModel


class RetrivalAugmentedGenerator(TokensEmbeddingsPair, LanguageModel):
    pass

class RetrivalAugmentedGeneration(Transform):
    in_nodes = [Token]
    out_nodes = [Token]
    composer = RetrivalAugmentedGenerator