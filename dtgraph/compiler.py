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
    # handle first node constructors; including node constructors found in edge constructors
    for constructor in dict.get('constructors'):
        print(constructor)
        src, edge, tgt = constructor.get('src'), constructor.get('edge'), constructor.get('tgt')
        if(src):
            script += processNodeConstructor(src, aliases, missing_aliases)
            script += processNodeConstructor(tgt, aliases, missing_aliases)
        else:
            script += processNodeConstructor(constructor, aliases, missing_aliases)
    print(script)
    print(aliases)
    print(missing_aliases)

def processNodeConstructor(node, aliases, missing_aliases):
    alias = node.get('alias')
    ids = node.get('ids')
    script = ""
    print(f'processNodeConstructor call with {node}')
    if alias and ids is None:
        # this is when an alias is referenced; for flexibility we allow to reference an alias before it is defined
        if alias not in aliases and alias not in missing_aliases:
            missing_aliases.append(alias)
    else:
        if alias:
            aliases.append(alias)
            if alias in missing_aliases:
                missing_aliases.remove(alias)
        else:
            alias = f"x_{len(aliases)}"
        labels = node.get('ids')
        properties = node.get('properties')
        script += f'MERGE ({alias}:_dummy {{\n    _id: "(" + { """ + "," + """.join(ids)  } + ")" \n}})\n'
    return script

if __name__ == "__main__":
    from dtgraph import Rule
    dico = Rule.from_ascii('''
        MATCH (n) 
        RETURN n
        => (("c") : Dummy),
        (x = (n) : Person {
            name = "SK1(" + n.name + ")" 
        })-[(): Knows]->(y = (n) : Person {
            name = "SK2(" + n.name + ")" 
        }), 
        (x)-[() : Likes]->(y)
    ''')._dict
    compile(dico)