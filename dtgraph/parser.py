import pyparsing as pp

# Some known differences with Cypher's syntax: https://neo4j.com/docs/cypher-manual/current/syntax/naming/
#   - We require variables to begin with a lowercase character
#   - We require node labels and relationship types to start with an uppercase character
#   - We disallow underscores in node labels, relationship types, property names, variables

constant = pp.Combine(pp.Literal('"') + pp.Word(pp.alphanums) + pp.Literal('"'))
freevar = pp.Word(pp.alphas.lower(), pp.alphanums)
attribute = pp.Word(pp.alphas, pp.alphanums)
accesskey = pp.Combine(freevar.set_results_name("freevar") + pp.Literal('.')  + attribute.set_results_name("key"))
label = pp.Word(pp.alphas.upper(), pp.alphanums)

IDElement = constant | freevar | accesskey | label

print(constant.parse_string(' "test" '))
print(freevar.parse_string(' x '))
print(accesskey.parse_string(' x1.de1 '))
print(accesskey.parse_string(' x2.de2 ')['freevar'])
print(accesskey.parse_string(' x3.de3 ')['key'])

print(IDElement.parse_string(' "test" '))
print(IDElement.parse_string(' x '))
print(IDElement.parse_string(' x1.de1 '))
#print(IDElement.parse_string(' x2.de2 ')['freevar'])
#print(IDElement.parse_string(' x3.de3 ')['key'])
