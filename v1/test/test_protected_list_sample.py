from components.model import Model
import unittest

class GenericSample(metaclass=Model):
    gbase: str

class ProtectedListSample(metaclass=Model):
    base: [str]
    other: [GenericSample]

class TestProtectedListSample(unittest.TestCase):
    def test_protected_list_sample(self):
        try:
            sample = ProtectedListSample(base=["Hi"], other=[GenericSample(gbase="GS1")])
        except:
            self.fail("Failed to instanciate base sample")

        self.assertTrue(sample.base[0] == "Hi")

        sample.base.append("Hello")
        self.assertTrue(sample.base[1] == "Hello")

        # Lets try and overwrite the existing list
        with self.assertRaises(ValueError):
            sample.base = 1

        # Lets try and append an invalid value
        with self.assertRaises(TypeError):
            sample.base.append(1)

        sample.other.extend([
            GenericSample(gbase="GS2"),
            GenericSample(gbase="GS3")
        ])

        # Lets try and append an invalid value
        with self.assertRaises(TypeError):
            sample.other.append(1)

        # Lets serialise it
        serialised = sample.serialise()

        expected = {'base': [
                        'Hi',
                        'Hello'
                    ],
                    'other': [
                        {'gbase': 'GS1'},
                        {'gbase': 'GS2'},
                        {'gbase': 'GS3'}
                    ]}

        self.assertEqual(serialised, expected)

