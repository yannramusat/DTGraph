from pyparsing import *

# Some voluntary differences with Cypher's syntax: https://neo4j.com/docs/cypher-manual/current/syntax/naming/
#   - We require variables to begin with a lowercase character.
#   - We require node labels and relationship types to start with an uppercase character.
#   - We disallow underscores in node labels, relationship types, property names, variables. (Hint: use camelCase)
#   - There is no support for undirected edges

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

try:
    print("Test base elements:")
    print(constant.parseString(' "test" '))
    print(freevar.parseString(' x '))
    print(accesskey.parseString(' x1.de1 ').asDict)
    print(accesskey.parseString(' x2.de2 '))
    print(accesskey.parseString(' x3.de3 '))
    print("Test IDElement:")
    print(IDElement.parseString(' "test" ').asDict())
    print(IDElement.parseString(' x ').asDict())
    print(IDElement.parseString(' x1.de1 ').asDict())
    print(IDElement.parseString(' x2.de2 ').asDict())
    print(IDElement.parseString(' x3.de3 ').asDict())
    print("Test accesskeys:")
    res = IDTuple.parseString('( x1.de1, x2.de2, x3.de3 )')
    print(res.asDict())
    print(res['ids'][1])
    print("Test IDTuple:")
    res = IDTuple.parseString('("test", x, x1.de1, x2.de2, x3.de3, )')
    print(res['ids'][0])
    print(res['ids'][1])
    print(res['ids'][2])
    print(res.asDict())
    print("Test ConstExpression:")
    res = ConstExpression.parseString(' "test" + "cc" ')
    print(res.dump())
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
