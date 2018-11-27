import unittest

from term_parser import *

class TestTextParser(unittest.TestCase):
    '''
    A small class to describe tests which should be executed
    before deploying the server.
    '''
    def testParser(self):
        count = count_terms("calca, aba, mala, aba")
        self.assertTrue(count["aba"] == 2)
        self.assertTrue("ala" not in count)
        self.assertTrue(count["mala"] == 1)

if __name__ == '__main__':
    unittest.main()