import unittest
from vkinder import VKinder
from json_writer import Json_writer
from mongo_writer import Mongo_writer

class VKinder_test(unittest.TestCase):
    v = None

    def setUp(self):
        self.v = VKinder(('INSERT YOUR TOKEN'
                          'HERE (in 2 lines)'))
    def test_get_info(self):
        self.assertRaises(BaseException, self.v.get_info())

    def test_do(self):
        self.assertRaises(BaseException, self.v.do())

if __name__ == '__main__':
    unittest.main()
