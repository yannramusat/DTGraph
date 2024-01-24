from dtgraph.exceptions import CompileError

def compile(dict):
    """Compiles a rule.

    Raises a CompileError if something went wrong.

    Parameters
    ----------
    dict : dict
        A string describing the rule as an executable openCypher script.

    Returns:
    --------
    str
        An openCypher script implementing the transformation described by dict.
    """
    aliases = []
    missing_aliases = []
    script = dict['lhs'] + "\n"
    # handle first the node constructors; including node constructors found in edge constructors
    for constructor in dict.get('constructors'):
        print(constructor)
        src, tgt = constructor.get('src'), constructor.get('tgt')
        if(src):
            script += processNodeConstructor(src, aliases, missing_aliases)
            script += processNodeConstructor(tgt, aliases, missing_aliases)
        else:
            script += processNodeConstructor(constructor, aliases, missing_aliases)
    print(script)
    print(aliases)
    if missing_aliases:
        CompileError("Missing a definition for the following aliases: " + missing_aliases)
    # handle edge constructors
    return script

def processNodeConstructor(node, aliases, missing_aliases):
    alias = node.get('alias')
    ids = node.get('ids')
    script = ""
    if alias and ids is None:
        # this is when an alias is referenced; for flexibility, we allow an alias to be referenced before its definition
        if alias not in aliases and alias not in missing_aliases:
            missing_aliases.append(alias)
    else:
        if alias:
            if alias in aliases:
                raise CompileError("Multiple definitions of the following alias: " + alias)
            aliases.append(alias)
            if alias in missing_aliases:
                missing_aliases.remove(alias)
        else:
            alias = f"x_{len(aliases)}"
        labels = node.get('labels')
        properties = node.get('properties')
        script += f'MERGE ({alias}:_dummy {{\n    _id: "(" + { """ + "," + """.join(ids) } + ")" \n}})\n'
        script += f'ON CREATE\n    SET { ",".join([alias + ":" + l for l in labels]) }'
        if(properties):
            script += ",\n        "
            script += ",\n        ".join([ p['key'] + " = " + p['value'] for p in properties])
        script += "\n"
    return script

if __name__ == "__main__":
    from dtgraph import Rule
    dico = Rule.from_ascii('''
        MATCH (n) 
        RETURN n
        => (("c") : Dummy),
        (x = (n) : Person {
            name = "SK1(" + n.name + ")",
            city = "test"
        })-[(): Knows]->(y = (n) : Person {
            name = "SK2(" + n.name + ")" 
        }), 
        (x)-[() : Likes]->(y)
    ''')._dict
    compile(dico)