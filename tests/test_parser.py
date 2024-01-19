from pyparsing import *
import unittest
from dtgraph.parser import *

class DSLTestCase(pyparsing_test.TestParseResultsAsserts, unittest.TestCase):
    def testIDTuple(self):
        self.assertParseAndCheckDict(
            IDTuple, 
            '(x1.de1, x2.de2, x3.de3)', 
            {'ids': ['x1.de1', 'x2.de2', 'x3.de3']}, 
            msg=None, 
            verbose=True
        )
        self.assertParseAndCheckDict(
            IDTuple, 
            '("test", x, x1.de1, x2.de2, x3.de3, )', 
            {'ids': ['"test"', 'x', 'x1.de1', 'x2.de2', 'x3.de3']}, 
            msg=None, 
            verbose=True
        )
        self.assertParseAndCheckDict(
            IDTuple, 
            '()', 
            {'ids': []}, 
            msg=None, 
            verbose=True
        )

if __name__ == "__main__":
    unittest.main()