from components.model import Model
from components.enumm import Enum
import unittest

class GenericSample(metaclass=Model):
    base: str

class EnumSample(metaclass=Model):
    base: (str,)
    other: (GenericSample,)