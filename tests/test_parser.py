from pyparsing import *
import unittest
from dtgraph.parser import *

class DSLTestCase(pyparsing_test.TestParseResultsAsserts, unittest.TestCase):
    def testIDTuple(self):
        self.assertParseAndCheckDict(
            IDTuple, 
            '(x1.de1, x2.de2, x3.de3)', {
                'ids': ['x1.de1', 'x2.de2', 'x3.de3']
            }
        )
        self.assertParseAndCheckDict(
            IDTuple, 
            '("test", x, x1.de1, x2.de2, x3.de3, )', {
                'ids': ['"test"', 'x', 'x1.de1', 'x2.de2', 'x3.de3']
            }
        )
        self.assertParseAndCheckDict(
            IDTuple, 
            '()', {
                'ids': []
            }
        )
    
    def testContentConstructor(self):
        self.assertParseAndCheckDict(
            ContentConstructor, 
            '("test", x, x1.de1, x2.de2, x3.de3, ) : Person, State, { name = "test" + "cc", city = x.city, }  ', {
                'ids': ['"test"', 'x', 'x1.de1', 'x2.de2', 'x3.de3'], 
                'labels': ['Person', 'State'], 
                'properties': [
                    {'key': 'name', 'value': '"test" + "cc"'}, 
                    {'key': 'city', 'value': 'x.city'}
                ]
            }
        )
        self.assertParseAndCheckDict(
            ContentConstructor, 
            'w = (x) : { name = x.name }  ', {
                'alias': 'w', 
                'ids': ['x'], 
                'properties': [{'key': 'name', 'value': 'x.name'}]
            }
        )
        self.assertParseAndCheckDict(
            ContentConstructor, 
            'x = () : ', {
                'alias': 'x', 
                'ids': []
            }
        )
        self.assertParseAndCheckDict(
            ContentConstructor, 
            '() : ', {
                'ids': []
            }
        )
    
    def testNodeConstructor(self):
        self.assertParseAndCheckDict(
            NodeConstructor, 
            '( w = ("test", x, x1.de1, x2.de2, x3.de3, ) : Person, State, { name = "test" + x.name  , city = x.city + y.va, } ) ', {
                'alias': 'w', 
                'ids': ['"test"', 'x', 'x1.de1', 'x2.de2', 'x3.de3'], 
                'labels': ['Person', 'State'], 
                'properties': [
                    {'key': 'name', 'value': '"test" + x.name'}, 
                    {'key': 'city', 'value': 'x.city + y.va'}
                ]
            }
        )
        self.assertParseAndCheckDict(
            NodeConstructor, 
            '(x)', {
                'alias': 'x'
            }
        )

    def testRightEdgeConstructor(self):
        self.assertParseAndCheckDict(
            RightEdgeConstructor, 
            '( (x) : Person { name = x.name }  ) -[ (x.a, "test") : HAS { name = x.name } ]-> (w)', {
                'src': {
                    'ids': ['x'], 
                    'labels': ['Person'], 
                    'properties': [
                        {'key': 'name', 'value': 'x.name'}
                    ]
                }, 
                'edge': {
                    'ids': ['x.a', '"test"'], 
                    'labels': ['HAS'], 
                    'properties': [
                        {'key': 'name', 'value': 'x.name'}
                    ]
                }, 
                'tgt': {
                    'alias': 'w'
                }
            }
        )
    
    def testEdgeConstructor(self):
        self.assertParseAndCheckDict(
            EdgeConstructor, 
            '((x):P{n=x.n})<-[(x.a,"t"):H,T{m=x.m+y.c+"3"}]-(w=("r",x,x1.de1,L):P,S,{n="u"+x.n,c=x.c+y.va,})', {
                'tgt': {
                    'ids': ['x'], 
                    'labels': ['P'], 
                    'properties': [{'key': 'n', 'value': 'x.n'}]
                }, 
                'edge': {
                    'ids': ['x.a', '"t"'], 
                    'labels': ['H', 'T'], 
                    'properties': [{'key': 'm', 'value': 'x.m + y.c + "3"'}]
                }, 
                'src': {
                    'alias': 'w', 
                    'ids': ['"r"', 'x', 'x1.de1', 'L'], 
                    'labels': ['P', 'S'], 
                    'properties': [
                        {'key': 'n', 'value': '"u" + x.n'}, 
                        {'key': 'c', 'value': 'x.c + y.va'}
                    ]
                }
            }
        )

if __name__ == "__main__":
    unittest.main()