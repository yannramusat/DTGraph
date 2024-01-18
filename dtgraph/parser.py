import pyparsing as pp

# Some known differences with Cypher's syntax: https://neo4j.com/docs/cypher-manual/current/syntax/naming/
#   - We require variables to begin with a lowercase character
#   - We require node labels and relationship types to start with an uppercase character
#   - We disallow underscores in node labels, relationship types, property names, variables

constant = pp.Combine(pp.Literal('"') + pp.Word(pp.alphanums) + pp.Literal('"'))
freevar = pp.Word(pp.alphas.lower(), pp.alphanums)
attribute = pp.Word(pp.alphas, pp.alphanums)
accesskey = pp.Combine(
    freevar('freevar') + 
    pp.Literal('.') + 
    attribute('key'))
label = pp.Word(pp.alphas.upper(), pp.alphanums)

IDElement = constant('value') | accesskey('value') | freevar('value') | label('value')

IDTuple = pp.Suppress('(') + pp.ZeroOrMore(IDElement + pp.Optional(pp.Suppress(',')))('ids') + pp.Suppress(')')

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
except pp.ParseException as pe:
    print("Did not Match: ", pe)
