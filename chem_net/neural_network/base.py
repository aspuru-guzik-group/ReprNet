from repr_net.base import Repr, Transform
from repr_net.bibtex import load_bibtex, bib

lib = load_bibtex("neural_network.bib")


class TrainingData(Repr):
    description = "Training data for a neural network"


class NeuralNetwork(Repr):
    description = "Neural networks"
    citations = [lib("lecun2015deep")]


class Optimizer(Repr):
    description = "Optimizers for training neural networks"
    citations = [lib("kingma2014adam")]

class TrainingAlgorithm(Repr):
    description = "Training algorithms for neural networks"


class Training(Transform):
    in_nodes = [TrainingData]
    out_nodes = [NeuralNetwork]
    contributors = ["Zijian Zhang"]
    description = "Training a neural network using training data"
    composer = TrainingAlgorithm


class GraphNeuralNetwork(NeuralNetwork):
    description = "Graph Neural Network"
    citations = [bib("""
@article{wu2020comprehensive,
  title={A comprehensive survey on graph neural networks},
  author={Wu, Zonghan and Pan, Shirui and Chen, Fengwen and Long, Guodong and Zhang, Chengqi and Philip, S Yu},
  journal={IEEE transactions on neural networks and learning systems},
  volume={32},
  number={1},
  pages={4--24},
  year={2020},
  publisher={IEEE}
}
""")]


