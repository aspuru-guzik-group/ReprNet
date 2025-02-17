# ReprNet: Build Representation Network with Python 


## Introduction: What's this?

Representation network is a directed graph that represents how different 
representations are related to each other. 

There are one type of node and two types of (hyper) edges in the representation network.

- Node: a representation, such as a vector, a paragraph, a computer program
- Transformation edge: a directed hyper edge from a set of representations to another set of representation representing a transformation from the source representations to the target representations. It also carries information of who is the composer of the transformation.
- Abstraction edge: a directed edge from a representation to a set of other representations, representing that the source representation can be abstracted from the target representation.

## Examples

### Transformation edge

- A calculator transform a set of numbers to another number. In the network, it can be represented as a transformation edge from
{calculator} to {number} with the composer being the calculator.

- The training of a neural network can be represented as a transformation edge from {neural network, training data} to {neural network} with the composer being the training algorithm.


### Abstraction edge

The abstract edge denote the direction where information is lost. 

- A graph neural network can be abstracted to a neural network, which can be abstracted to a computer program. Along the edge, information about which type is the computer program and which type is the neural network is lost.

Additionally, the abstraction edge can be used to represent how a complex representation is formed by combining simpler representations. 

- A pair of numbers can be abstracted to a number because it contains numbers. Along the edge, information about how the number is combined into more complex representation is lost.
- A function that takes a number and returns a number can be abstracted to {number, mapping} because it is related to a number and a mapping. Along the edge, information about how what is the mapping is lost.


## Represent the network in Python

In `repr_net`, we use Python classes the represent the network. To define a representation, one just need to define a subclass in the following way:

```python
from repr_net import Repr
class Number(Repr):
    pass
class Calculator(Repr):
    pass
```

A transformation edge can be defined as follows:

```python
from repr_net import Transform
class Calculate(Transform):
    in_nodes = [Number]
    out_nodes = [Number]
    composer = Calculator
```

A abstraction edge can be defined using inheritance:

```python
class NumberTuple(Number):
    pass
class Addition(Transform):
    in_nodes = [NumberTuple]
    out_nodes = [Number]
    composer = Calculator
```

## Meta information

`repr_net` also provides a way to store meta information about the representation network. For example, one can store the information about the node and transforms:


```python
from repr_net.bibtex import bib
from repr_net import Repr

class NeuralNetwork(Repr):
    description = "Artificial neural network"
    citations = [bib("""
@article{lecun2015deep,
  title={Deep learning},
  author={LeCun, Yann and Bengio, Yoshua and Hinton, Geoffrey},
  journal={nature},
  volume={521},
  number={7553},
  pages={436--444},
  year={2015},
  publisher={Nature Publishing Group UK London}
}""")]
    contributors = ["Bob", "Alice"]
    
class Inference(Transform):
    in_nodes = [Number]
    out_nodes = [Number]
    composer = Transform
    description = "Inference by a neural network"
```


## Visualization

`repr_net` also provides a way to visualize the representation network. After defining the transforms and nodes, one build a networkx graph and visualize it. We also provide a visualization tool to display the network.

```python
import module_contains_the_your_network # your network!
from repr_net.indexing import generate_network_from_module
from repr_net.visualization import display_network
G = generate_network_from_module(module_contains_the_your_network)
display_network(G)
```

See example network visualization [here](http://repr.evoevo.org/)!