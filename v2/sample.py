from model import model, Model

@model
class GenericBase:
    l: int = 1
    m: int
    n: int = 3

@model
class GenericSample(GenericBase):
    x: int
    y: str
    z: bool = False

@model
class Sample:
    a: str
    b: int = 1
    c: GenericSample
    d: [int] = [1]
    e: (int, str, "OK", "KO") = "OK"


#---------------
class GenericBase1(Model):
    l: int = 1
    m: int
    n: int = 3

class GenericSample1(GenericBase1):
    x: int
    y: str
    z: bool = False


