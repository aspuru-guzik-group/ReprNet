from repr_net import Repr


class Text(Repr):
    pass


class Image(Repr):
    pass


class Number(Repr):
    pass


class Document(Text, Image):
    pass