import unittest
from pyparsing import *
from dtgraph.parser import *

class DSLTestCase(pyparsing_test.TestParseResultsAsserts, unittest.TestCase):
    maxDiff = None

    def testConstant(self):
        self.assertRunTestResults(
            constant.runTests('''
                "test"
                ""
            ''')
        )
        self.assertRunTestResults(
            constant.runTests('''
                # Not enclosed inside " quotes ✘
                test
                # " not escaped ✘
                "fjek"fe"
            ''', failure_tests=True)
        )

    def testFreevar(self):
        self.assertRunTestResults(
            freevar.runTests('''
                x
                x1
            ''')
        )
        self.assertRunTestResults(
            freevar.runTests('''
                # Capitalized (should not be a label) ✘
                Label
                # Cannot start with an integer ✘
                1ax
            ''', failure_tests=True)
        )

    def testAccesskey(self):
        self.assertRunTestResults(
            accesskey.runTests('''
                x.de
                x.de1
                x2.de
                x3.de3
            ''')
        )
        self.assertRunTestResults(
            accesskey.runTests('''
                # No attribute ✘
                x1
                # Not a variable ✘
                Label
                # Should not use const on either side ✘
                "test".de3
                x1."test"
                # Does not work as a const ✘
                "test.de"
            ''', failure_tests=True)
        )

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
        self.assertRunTestResults(
            IDTuple.runTests('''
                # Should be a comma between the list elements ✘
                ("c" x.a)
                # Cannot have only one comma ✘
                (,)
            ''', failure_tests=True)
        )

    def testConstExpression(self):
        self.assertRunTestResults(
            ConstExpression.runTests('''
                "test" + "cc"
                x.a
                x1.d2a + "test"
            ''')
        )
        self.assertRunTestResults(
            ConstExpression.runTests('''
                # Variables cannot be used inside a constexpression ✘
                var1
                # Labels cannot be used inside a constexpression ✘
                Label
            ''', failure_tests=True)
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
            '( (x,) : Person { name = x.name }  ) -[ (x.a,"test") : HAS { name = x.name } ]-> (w)', {
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

    def testRightHandSide(self):
        self.assertParseAndCheckDict(
            RightHandSide, 
            '((x):P) -[ (x.a): ]-> ((L):), ((x):P{n=x.n})<-[(x.a,"t"):H,T{m=x.m+y.c+"3"}]-(w=("r",x, x1.d1,L):P, S,{n="u"+x.n,c=x.c+y.va,}), (w = ("t"):U{n=a.u}), (z = (L):V,J{n=a.u}), ', {
                'constructors': [{
                        'src': {
                            'ids': ['x'], 
                            'labels': ['P']}, 
                        'edge': {
                            'ids': ['x.a']}, 
                        'tgt': {
                            'ids': ['L']}
                    }, {
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
                            'ids': ['"r"', 'x', 'x1.d1', 'L'], 
                            'labels': ['P', 'S'], 
                            'properties': [{'key': 'n', 'value': '"u" + x.n'}, {'key': 'c', 'value': 'x.c + y.va'}]
                        }
                    }, {
                        'alias': 'w', 
                        'ids': ['"t"'], 
                        'labels': ['U'], 
                        'properties': [{'key': 'n', 'value': 'a.u'}]
                    }, {
                        'alias': 'z', 
                        'ids': ['L'], 
                        'labels': ['V', 'J'], 
                        'properties': [{'key': 'n', 'value': 'a.u'}]
                    }
                ]
            }
        )

    def testRuleParser(self):
        self.assertParseAndCheckDict(
            RuleParser,
            """
            MATCH (n) 
            RETURN n
            GENERATE
            (x = (n) : Person {
                name = "SK1(" + n.name + ")" 
            })-[(): Knows]->(y = (n) : Person {
                name = "SK2(" + n.name + ")" 
            })
            """, {
                'lhs': 'MATCH (n) \n            RETURN n',
                'constructors': [{
                    'src': {
                        'alias': 'x', 
                        'ids': ['n'], 
                        'labels': ['Person'], 
                        'properties': [{
                            'key': 'name', 
                            'value': '"SK1(" + n.name + ")"'
                        }]
                    }, 
                    'edge': {
                        'ids': [], 
                        'labels': ['Knows']
                    }, 
                    'tgt': {
                        'alias': 'y', 
                        'ids': ['n'], 
                        'labels': ['Person'], 
                        'properties': [{
                            'key': 'name', 
                            'value': '"SK2(" + n.name + ")"'
                        }]
                    }
                }]
            }
        )

        self.assertParseAndCheckDict(
            RuleParser,
            """
            MATCH (n) 
            RETURN n
            =>
            (x = (n) : Person {
                name = "SK1(" + n.name + ")" 
            })
            """, {
                'lhs': 'MATCH (n) \n            RETURN n',
                'constructors': [{
                        'alias': 'x', 
                        'ids': ['n'], 
                        'labels': ['Person'], 
                        'properties': [{
                            'key': 'name', 
                            'value': '"SK1(" + n.name + ")"'
                        }]
                }]
            }
        )

if __name__ == "__main__":
    unittest.main()