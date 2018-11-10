from enumm import Enum

import unittest

class TestEnum(unittest.TestCase):
    def test_enum_of(self):
        try:
            enum = Enum.of(int, str)
        except:
            self.fail("Failed to use 'of' enum")

        self.assertTrue(Enum in enum.__bases__)

    def test_enum_validate(self):
        try:
            enum = Enum.of(int, str)
            enum.validate(1)
            enum.validate("Hello")
        except:
            self.fail("Failed to validate valid value with enum definition")

        with self.assertRaises(TypeError):
            enum.validate(True) # Boolean isnt in definition, this should fail