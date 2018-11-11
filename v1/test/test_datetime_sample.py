from components.model import Model
from datetime import datetime
import unittest

class DatetimeSample(metaclass=Model):
    base: datetime

class TestModel(unittest.TestCase):
    def test_datetime_sample(self):
        try:
            now = datetime.now()
            datetime_sample = DatetimeSample(base=now)
        except:
            self.fail("Failed to instanciate datetime sample")

        self.assertEqual(datetime_sample.base, now)

        try:
            datetime_sample.base = datetime.now()
        except:
            self.fail("Valid datetime assignment failed")

        try:
            datetime_sample.base = 'Jun 1 2005  1:33PM'
        except:
            self.fail("Implicit conversion failed")

        with self.assertRaises(ValueError):
            datetime_sample.base = "Hello"

        with self.assertRaises(ValueError):
            datetime_sample.base = str

    def test_datetime_sample_serialiser(self):
        now = datetime.now()
        datetime_sample = DatetimeSample(base=now)
        serialised = datetime_sample.serialise()
        self.assertEqual(serialised, {'base': now})