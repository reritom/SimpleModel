from model import model, Model

@model
class GenericBase:
    l: int = 1
    m: int
    n: int

@model
class GenericSample(GenericBase):
    x: int
    y: str
    z: bool
'''
@model
class Sample:
    a: str
    b: int = 1
    c: GenericSample
    d: [int]
    e: (str, int, "OK", "KO")
'''