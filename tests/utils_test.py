import unittest

from utils.utils import mention

class TestUtils(unittest.TestCase):
    def test_mention(self):
        self.assertTrue(mention(20) == "<@20>")
