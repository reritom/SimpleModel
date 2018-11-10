from protected_list import ProtectedList
import unittest

class TestAdd(unittest.TestCase):
    def test_creation_using_of(self):
        self.assertTrue(isinstance(ProtectedList.of(str), type))

        try:
            this_list = ProtectedList.of(str)()
        except:
            self.fail()

    def test_init(self):
        this_list = ProtectedList.of(str)(['Hello'])
        self.assertEqual(this_list[0], 'Hello')

        with self.assertRaises(TypeError):
            ProtectedList.of(str)([1])

    def test_append(self):
        this_list = ProtectedList.of(str)()

        this_list.append("Hello")
        self.assertEqual(this_list[0], "Hello")

        with self.assertRaises(TypeError):
            this_list.append(1)

    def test_insert(self):
        this_list = ProtectedList.of(str)()

        this_list.insert(0, "Hello")
        self.assertEqual(this_list[0], "Hello")

        with self.assertRaises(TypeError):
            this_list.insert(0, 1)

    def test_extend(self):
        this_list = ProtectedList.of(str)()

        this_list.extend(["Hello"])
        self.assertEqual(this_list[0], "Hello")

        with self.assertRaises(TypeError):
            this_list.extend([1])

if __name__ == '__main__':
    unittest.main()

