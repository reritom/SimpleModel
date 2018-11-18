from model import model
import unittest

@model
class BaseSample:
    base: str

@model
class Sample(BaseSample):
    meta: dict
    enum: (int, str,) = 1
    numbers: [BaseSample]

class TestModelDecorator(unittest.TestCase):
    def test_base_sample_empty_init(self):
        try:
            base_sample = BaseSample()
        except:
            self.fail("Failed to instanciate base sample")

        # Test the serialisation
        serialised = base_sample.serialise()
        expected = {}
        self.assertEqual(serialised, expected)

    def test_base_sample_with_kwargs(self):
        try:
            base_sample = BaseSample(base="Hello")
        except:
            self.fail("Failed to instanciate base sample")

        # Test the serialisation
        serialised = base_sample.serialise()
        expected = {'base': "Hello"}
        self.assertEqual(serialised, expected)

    def test_base_sample_set_invalid(self):
        try:
            base_sample = BaseSample()
        except:
            self.fail("Failed to instanciate base sample")

        with self.assertRaises(ValueError):
            base_sample.base = 1

    def test_sample_empty_init(self):
        try:
            sample = Sample()
        except:
            self.fail("Failed to instanciate sample")

        try:
            base_sample = BaseSample(base="String")
        except:
            self.fail("Failed to instanciate base sample")

        # Test the serialisation - nothing has been set, but there should be a default value from the definition
        serialised = sample.serialise()
        expected = {'Sample': {'enum': {'int': 1}}}
        self.assertEqual(serialised, expected)

        # Test deep serialisation of nested model
        sample.numbers.append(base_sample)
        serialised = sample.serialise()
        expected = {'Sample': {'numbers': [{'base': 'String'}], 'enum': {'int': 1}}}
        self.assertEqual(serialised, expected)

    def test_sample_invalid_enum(self):
        try:
            sample = Sample()
        except:
            self.fail("Failed to instanciate sample")

        with self.assertRaises(ValueError):
            sample.enum = True

    def test_nested_deserialise(self):
        serialised_sample = {'numbers': [{'base': 'String'}], 'enum': {'int': 1}}
        deserialised = Sample.deserialise(serialised_sample)

        self.assertEqual(deserialised.numbers[0].base, 'String')
        self.assertEqual(deserialised.enum, 1)

if __name__=='__main__':
    serialised_sample = {'numbers': [{'base': 'String'}], 'enum': {'int': 1}}
    deserialised = Sample.deserialise(serialised_sample)