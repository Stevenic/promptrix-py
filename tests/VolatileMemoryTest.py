import unittest
from promptrix.VolatileMemory import VolatileMemory

class TestVolatileMemory(unittest.TestCase):
    def setUp(self):
        self.memory = VolatileMemory()
        self.obj = {'foo': 'bar'}

    def test_constructor(self):
        self.assertIsNotNone(self.memory)

    def test_constructor_with_initial_values(self):
        memory = VolatileMemory({"test": 123})
        self.assertIsNotNone(memory)
        self.assertTrue(memory.has("test"))

    def test_set_primitive_value(self):
        self.memory.set("test", 123)
        self.assertTrue(self.memory.has("test"))

    def test_set_object(self):
        self.memory.set("test2", self.obj)
        self.assertTrue(self.memory.has("test2"))

    def test_get_primitive_value(self):
        self.memory.set("test", 123)
        value = self.memory.get("test")
        self.assertEqual(value, 123)

    def test_get_object_clone(self):
        self.memory.set("test2", self.obj)
        value = self.memory.get("test2")
        self.assertEqual(value, {'foo': 'bar'})
        self.assertIsNot(value, self.obj)

    def test_get_undefined(self):
        value = self.memory.get("test3")
        self.assertIsNone(value)

    def test_has_value(self):
        self.memory.set("test", 123)
        self.assertTrue(self.memory.has("test"))

    def test_has_no_value(self):
        self.assertFalse(self.memory.has("test3"))

    def test_delete_value(self):
        self.memory.set("test", 123)
        self.memory.delete("test")
        self.assertFalse(self.memory.has("test"))
        self.assertTrue(self.memory.has("test2"))

    def test_clear_values(self):
        self.memory.set("test", 123)
        self.memory.clear()
        self.assertFalse(self.memory.has("test"))
        self.assertFalse(self.memory.has("test2"))

if __name__ == '__main__':
    unittest.main()
