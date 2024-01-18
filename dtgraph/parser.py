import pyparsing as pp

# Some known differences with Cypher's syntax: https://neo4j.com/docs/cypher-manual/current/syntax/naming/
#   - We require variables to begin with a lowercase character
#   - We require node labels and relationship types to start with an uppercase character
#   - We disallow underscores in node labels, relationship types, property names, variables

COMMA, COLON, LPAR, RPAR, LANGLE, RANGLE, EQUAL = map(pp.Suppress, ",:()⟨⟩=")

constant = pp.Combine(pp.Literal('"') + pp.Word(pp.alphanums) + pp.Literal('"'))
freevar = pp.Word(pp.alphas.lower(), pp.alphanums)
attribute = pp.Word(pp.alphas, pp.alphanums)
accesskey = pp.Combine(freevar('freevar') + pp.Literal('.') + attribute('key'))
label = pp.Word(pp.alphas.upper(), pp.alphanums)

# To see, this might explain why we need to use the name 'value' there: 
# https://stackoverflow.com/questions/74876130/how-do-i-correctly-name-parseresults
IDElement = constant('value') | accesskey('value') | freevar('value') | label('value')
PropertyElement = pp.Group(attribute('key') + EQUAL + ( constant('value') | accesskey('value')))

IDTuple = LPAR + pp.ZeroOrMore(IDElement + pp.Optional(COMMA))('ids') + RPAR
Labels = pp.ZeroOrMore(label + pp.Optional(COMMA))('labels')
PropertyList = pp.Optional(LANGLE + pp.OneOrMore(PropertyElement + pp.Optional(COMMA))('properties') + RANGLE)

ContentConstructor = LPAR + pp.Optional(freevar('alias') + EQUAL) + IDTuple + pp.Optional(COLON + Labels) + RPAR + PropertyList('properties')

try:
    print("Test base elements:")
    print(constant.parse_string(' "test" '))
    print(freevar.parse_string(' x '))
    print(accesskey.parse_string(' x1.de1 '))
    print(accesskey.parse_string(' x2.de2 ')['freevar'])
    print(accesskey.parse_string(' x3.de3 ')['key'])
    print("Test IDElement:")
    print(IDElement.parse_string(' "test" ')['value'])
    print(IDElement.parse_string(' x ')['value'])
    print(IDElement.parse_string(' x1.de1 ')['value'])
    print(IDElement.parse_string(' x2.de2 ')['value']['freevar'])
    print(IDElement.parse_string(' x3.de3 ')['value']['key'])
    print("Test accesskeys:")
    res = IDTuple.parse_string('( x1.de1, x2.de2, x3.de3 )')
    print(res['ids'][1])
    print(res['ids'][1]['freevar'])
    print(res['ids'][1]['key'])
    print("Test IDTuple:")
    res = IDTuple.parse_string('("test", x, x1.de1, x2.de2, x3.de3, )')
    print(res['ids'][0])
    print(res['ids'][1])
    print(res['ids'][2])
    print(res['ids'][2]['freevar'])
    print(res['ids'][2]['key'])
    print(res.as_dict())
    print("Test ContentConstructor:")
    res = ContentConstructor.parse_string('(("test", x, x1.de1, x2.de2, x3.de3, ) : Person, State,) ⟨ name = "test", city = x.city, ⟩')
    print(res.as_dict())
    res = ContentConstructor.parse_string('(w = (x) : ) ⟨name = x.name⟩')
    print(res.as_dict())
    res = ContentConstructor.parse_string('(x = () : ) ⟨ ⟩')
    print(res.as_dict())
    res = ContentConstructor.parse_string('(() : )')
    print(res.as_dict())
except pp.ParseException as pe:
    print("Did not Match: ", pe)
