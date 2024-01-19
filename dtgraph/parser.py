from pyparsing import *

# Some voluntary differences with Cypher's syntax: https://neo4j.com/docs/cypher-manual/current/syntax/naming/
#   - We require variables to begin with a lowercase character.
#   - We require node labels and relationship types to start with an uppercase character.
#   - We disallow underscores in node labels, relationship types, property names, variables. (Hint: use camelCase)

COMMA, COLON, LPAR, RPAR, LBRACE, RBRACE, EQUAL = map(Suppress, ",:(){}=")

#constant = Combine(Literal('"') + Word(alphanums) + Literal('"'))
# TODO support complex Cypher string operations such as concatenations
constant = QuotedString('"', unquoteResults=False)
freevar = Word(alphas.lower(), alphanums)
attribute = Word(alphas, alphanums)
accesskey = Combine(freevar + Literal('.') + attribute)
label = Word(alphas.upper(), alphanums)

IDElement = (constant | accesskey | freevar | label)
PropertyElement = Group(attribute('key') + EQUAL + ( constant('value') | accesskey('value')))

IDTuple = LPAR + ZeroOrMore(IDElement + Optional(COMMA))('ids') + RPAR
Labels = OneOrMore(label + Optional(COMMA))('labels')
PropertyList = LBRACE + OneOrMore(PropertyElement + Optional(COMMA))('properties') + RBRACE

ContentConstructor = LPAR + Optional(freevar('alias') + EQUAL) + IDTuple + COLON + Optional(Labels) + Optional(PropertyList) + RPAR 
NodeConstructor = ContentConstructor | LPAR + freevar('alias') + RPAR

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
    print("Test ContentConstructor:")
    res = ContentConstructor.parseString('(("test", x, x1.de1, x2.de2, x3.de3, ) : Person, State, { name = "test", city = x.city, } ) ')
    print(res.asDict())
    res = ContentConstructor.parseString('(w = (x) : { name = x.name } ) ')
    print(res.asDict())
    res = ContentConstructor.parseString('(x = () : ) ')
    print(res.asDict())
    res = ContentConstructor.parseString('(() : )')
    print(res.asDict())
    print("Test NodeConstructor:")
    res = NodeConstructor.parseString('(("test", x, x1.de1, x2.de2, x3.de3, ) : Person, State, { name = "test", city = x.city, } ) ')
    print(res.asDict())
    res = NodeConstructor.parseString('(x)')
    print(res.asDict())
except ParseException as pe:
    print("Did not Match: ", pe)
