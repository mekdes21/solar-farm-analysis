import unittest

class TestExample(unittest.TestCase):
    def test_sample(self):
        self.assertEqual(2 * 2, 4)

    def test_failure(self):
        self.assertTrue(3 > 1)

if __name__ == "__main__":
    unittest.main()
