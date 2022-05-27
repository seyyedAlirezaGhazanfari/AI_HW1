import os
import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        for filename in os.listdir(os.getcwd() + "\\in\\"):
            with open(os.getcwd() + "\\in\\" + filename, 'r') as f:
                with open(os.getcwd() + "\\out\\" + filename, 'r') as res:
                    pass


if __name__ == '__main__':
    unittest.main()
