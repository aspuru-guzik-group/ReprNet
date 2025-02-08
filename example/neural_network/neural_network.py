from repr_net.base import Repr, Edge
from repr_net.bibtex import load_bibtex


lib = load_bibtex("neural_network.bib")


class TrainingData(Repr):
    description = "Training data for a neural network"


class NeuralNetwork(Repr):
    description = "Neural networks"
    citations = [lib("lecun2015deep")]


class Optimizer(Repr):
    description = "Optimizers for training neural networks"

class Training(Edge):
    in_nodes = [TrainingData]
    out_nodes = [NeuralNetwork]
    authors = ["Zijian Zhang"]
    description = "Training a neural network using training data"
    composer = Optimizer