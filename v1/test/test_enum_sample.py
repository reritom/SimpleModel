from components.model import Model
from components.enumm import Enum
import unittest

class GenericSample(metaclass=Model):
    gbase: str

class EnumSample(metaclass=Model):
    base: (str, int,)
    other: (GenericSample,)

class TesEnumSample(unittest.TestCase):
    def test_enum_sample(self):
        try:
            sample = EnumSample(base="Hi", other=GenericSample(gbase="GS1"))
        except:
            self.fail("Failed to instanciate base sample")

        self.assertTrue(sample.base == "Hi")

        sample.base = 1
        self.assertTrue(sample.base == 1)

        # Lets try and set an invalid type
        with self.assertRaises(TypeError):
            sample.base = False

        sample.other = GenericSample(gbase="GS2")

        # Lets serialise it
        serialised = sample.serialise()

        expected = {
           'base': {
                'int': 1
            },
           'other':{
              'GenericSample':{
                 'gbase':'GS"'
              }
           }
        }

        self.assertEqual(serialised, expected)
