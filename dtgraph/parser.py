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
# Or, flatened Constexpression:
ConstExpression = Combine((accesskey | constant) + ZeroOrMore("+" + (accesskey | constant)), adjacent=False, joinString=" ")
PropertyElement = Group(attribute('key') + EQUAL + ConstExpression('value'))

IDTuple = LPAR + ZeroOrMore(IDElement + Optional(COMMA))('ids') + RPAR
Labels = OneOrMore(label + Optional(COMMA))('labels')
PropertyList = LBRACE + OneOrMore(PropertyElement + Optional(COMMA))('properties') + RBRACE

ContentConstructor = Optional(freevar('alias') + EQUAL) + IDTuple + COLON + Optional(Labels) + Optional(PropertyList) 
NodeConstructor = LPAR + (ContentConstructor | freevar('alias')) + RPAR
RightEdgeConstructor = Group(NodeConstructor)('src') + Suppress('-[') + Group(ContentConstructor)('edge') + Suppress(']->') + Group(NodeConstructor)('tgt')
LeftEdgeConstructor = Group(NodeConstructor)('tgt') + Suppress('<-[') + Group(ContentConstructor)('edge') + Suppress(']-') + Group(NodeConstructor)('src')
EdgeConstructor = RightEdgeConstructor | LeftEdgeConstructor

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
            # Not enclosed in " 
            test
            # " is not escaped
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
            # Capitalized (should not be a label)
            Label
            # Cannot start with an integer
            1ax
        ''', failure_tests=True)
        status &= res
        res, _ = accesskey.runTests('''
            ##### Test accesskey: #####
            x1.de1
            x2.de2
            x3.de3
        ''')
        status &= res
        res, _ = accesskey.runTests('''
            # No attribute
            x1
            # Not a variable
            Label
            # should not use const on either side
            "test".de3
            x1."test"
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
            ("test", x, x1.de1, x2.de2, x3.de3, )
            ()
        ''')
        status &= res
        res, _ = IDTuple.runTests('''
            # Cannot have only one comma
            (,)
        ''', failure_tests=True)
        status &= res
        print(status)
        ConstExpression.runTests('''
            # Test ConstExpression:
            "test" + "cc"
        ''')
        print("Test ContentConstructor:")
        res = ContentConstructor.parseString('("test", x, x1.de1, x2.de2, x3.de3, ) : Person, State, { name = "test" + "cc", city = x.city, }  ')
        print(res.asDict())
        res = ContentConstructor.parseString('w = (x) : { name = x.name }  ')
        print(res.asDict())
        res = ContentConstructor.parseString('x = () : ')
        print(res.asDict())
        res = ContentConstructor.parseString('() : ')
        print(res.asDict())
        print("Test NodeConstructor:")
        res = NodeConstructor.parseString('( w = ("test", x, x1.de1, x2.de2, x3.de3, ) : Person, State, { name = "test" + x.name  , city = x.city + y.va, } ) ')
        print(res.asDict())
        res = NodeConstructor.parseString('(x)')
        print(res.asDict())
        print("Test RightEdgeConstructor:")
        res = RightEdgeConstructor.parseString('( (x) : Person { name = x.name }  ) -[ (x.a, "test") : HAS { name = x.name } ]-> (w)')
        print(res.asDict())
        print("Test EdgeConstructor:")
        res = EdgeConstructor.parseString('((x):P{n=x.n})<-[(x.a,"t"):H,T{m=x.m+y.c+"3"}]-(w=("r",x,x1.de1,L):P,S,{n="u"+x.n,c=x.c+y.va,})')
        print(res.asDict())
    except ParseException as pe:
        print("Did not Match: ", pe)
