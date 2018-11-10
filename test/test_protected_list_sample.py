from components.model import Model
import unittest

class GenericSample(metaclass=Model):
    base: str

class ProtectedListSample(metaclass=Model):
    base: [str]
    other: [GenericSample]