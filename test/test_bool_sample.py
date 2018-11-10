from components.model import Model
import unittest

class BoolSample(metaclass=Model):
    base: bool

class TestModel(unittest.TestCase):
    def test_bool_sample(self):
        try:
            base_sample = BoolSample(base=False)
        except:
            self.fail("Failed to instanciate base sample")

        self.assertEqual(base_sample.base, False)

        try:
            base_sample.base = True
        except:
            self.fail("Valid bool assignment failed")

        with self.assertRaises(ValueError):
            base_sample.base = "Hello"

        with self.assertRaises(ValueError):
            base_sample.base = str

    def test_bool_sample_serialiser(self):
        base_sample = BoolSample(base=False)
        serialised = base_sample.serialise()
        self.assertEqual(serialised, {'base': False})
