from components.model import Model
import unittest

class BaseSample(metaclass=Model):
    base: str

class Sample(BaseSample, metaclass=Model):
    meta: dict
    enum: (int, str,)
    numbers: [BaseSample]

class TestModel(unittest.TestCase):
    def test_base_sample(self):
        try:
            base_sample = BaseSample()
        except:
            self.fail("Failed to instanciate base sample")

        base_sample.base = "Hello"

        with self.assertRaises(ValueError):
            base_sample.base = 1