from pyparsing import *
import unittest

# Some voluntary differences with Cypher's syntax: https://neo4j.com/docs/cypher-manual/current/syntax/naming/
#   - We require variables to begin with a lowercase character.
#   - We require node labels and relationship types to start with an uppercase character.
#   - We disallow underscores in node labels, relationship types, property names, variables. (Hint: use camelCase)
#   - There is no support for undirected edges.

COMMA, COLON, LPAR, RPAR, LBRACE, RBRACE, EQUAL = map(Suppress, ",:(){}=")

#constant = Combine(Literal('"') + Word(alphanums) + Literal('"'))
constant = QuotedString('"', unquoteResults=False)
freevar = Word(alphas.lower(), alphanums)
attribute = Word(alphas, alphanums)
accesskey = Combine(freevar + Literal('.') + attribute)
label = Word(alphas.upper(), alphanums)

IDElement = (constant | accesskey | freevar | label)
# As list of constant or accesskey expressions:
#ConstExpression = DelimitedList(accesskey | constant, delim="+")
# Or, flatened ConstExpression:
ConstExpression = Combine((accesskey | constant) + ZeroOrMore("+" + (accesskey | constant)), adjacent=False, joinString=" ")
PropertyElement = Group(attribute('key') + EQUAL + ConstExpression('value'))

IDTuple = LPAR + Optional(DelimitedList(IDElement, allow_trailing_delim=True), default=[])('ids') + RPAR
Labels = DelimitedList(label, allow_trailing_delim=True)('labels')
PropertyList = LBRACE + DelimitedList(PropertyElement, allow_trailing_delim=True)('properties') + RBRACE

ContentConstructor = Optional(freevar('alias') + EQUAL) + IDTuple + COLON + Optional(Labels) + Optional(PropertyList) 
NodeConstructor = LPAR + (ContentConstructor | freevar('alias')) + RPAR
RightEdgeConstructor = Group(NodeConstructor)('src') + Suppress('-[') + Group(ContentConstructor)('edge') + Suppress(']->') + Group(NodeConstructor)('tgt')
LeftEdgeConstructor = Group(NodeConstructor)('tgt') + Suppress('<-[') + Group(ContentConstructor)('edge') + Suppress(']-') + Group(NodeConstructor)('src')
EdgeConstructor = RightEdgeConstructor | LeftEdgeConstructor

Constructor = EdgeConstructor | NodeConstructor
RightHandSide = DelimitedList(Group(Constructor), allow_trailing_delim=True)('constructors')

if __name__ == "__main__":
    try:
        status = True
        res, _ = constant.runTests('''
            ##### Test constant: #####
            "test"
            ""
        ''')
        status &= res
        res, _ = constant.runTests('''
            # Not enclosed in " ✘
            test
            # " not escaped ✘
            "fjek"fe"
        ''', failure_tests=True)
        status &= res
        res, _ = freevar.runTests('''
            ##### Test freevar: #####
            x
            x1
        ''')
        status &= res
        res, _ = freevar.runTests('''
            # Capitalized (should not be a label) ✘
            Label
            # Cannot start with an integer ✘
            1ax
        ''', failure_tests=True)
        status &= res
        res, _ = accesskey.runTests('''
            ##### Test accesskey: #####
            x.de
            x.de1
            x2.de
            x3.de3
        ''')
        status &= res
        res, _ = accesskey.runTests('''
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
        status &= res
        res, _ = IDElement.runTests('''
            ##### Test IDElement: #####
            "test" 
            x
            x1.de1 
            Label
        ''')
        status &= res
        res, out = IDTuple.runTests('''
            ##### Test IDTuple: #####
            (x1.de1, x2.de2, x3.de3)
            # list ending with a comma ✔
            ("test", x, x1.de1, x2.de2, x3.de3, )
            ()
        ''')
        status &= res
        res, _ = IDTuple.runTests('''
            # Should be a comma between the list elements ✘
            ("c" x.a)
            # Cannot have only one comma ✘
            (,)
        ''', failure_tests=True)
        status &= res
        res, _ = ConstExpression.runTests('''
            ##### Test ConstExpression: #####
            "test" + "cc"
            x.a
            x1.d2a + "test"
        ''')
        status &= res
        res, _ = ConstExpression.runTests('''
            # Variables cannot be used inside a constexpression ✘
            var1
            # Labels cannot be used inside a constexpression ✘
            Label
        ''', failure_tests=True)
        status &= res

        if status:
            print("\nAll tests passed!")
        else:
            print("\nSome tests failed...")
    except ParseException as pe:
        print("Did not Match: ", pe)
