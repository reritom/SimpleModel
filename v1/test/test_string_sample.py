from components.model import Model
import unittest

class StringSample(metaclass=Model):
    base: str

class TestModel(unittest.TestCase):
    def test_string_sample(self):
        try:
            string_sample = StringSample(base="Hi")
        except:
            self.fail("Failed to instanciate base sample")

        self.assertTrue(string_sample.base == "Hi")

        string_sample.base = "Hello"

        with self.assertRaises(ValueError):
            string_sample.base = 1

    def test_string_sample_serialiser(self):
        try:
            string_sample = StringSample(base="Hi")
            serialised = string_sample.serialise()
        except:
            self.fail("Failed to serialise")

        self.assertEqual(serialised, {'base': "Hi"})