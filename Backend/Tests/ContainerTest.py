import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from Classes.Container import Container

class TestContainer(unittest.TestCase):
    def setUp(self):
        self.container = Container(
            position=(1, 2), weight=100, name="Container A")

    def test_initialization(self):
        self.assertEqual(self.container.position, (1, 2))
        self.assertEqual(self.container.weight, 100)
        self.assertEqual(self.container.name, "Container A")

    def test_repr(self):
        self.assertEqual(repr(self.container), "Container A, 100")

    def test_update_position(self):
        self.container.update_position((5, 6))
        self.assertEqual(self.container.position, (5, 6))

    def test_get_weight(self):
        self.assertEqual(self.container.get_weight(), 100)


if __name__ == "__main__":
    unittest.main()
