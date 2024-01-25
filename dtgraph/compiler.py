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
        An openCypher script implementing the transformation described by the input dictionary.
    """
    aliases = []
    missing_aliases = []
    script = dict['lhs'].strip() + "\n"
    # handle first the node constructors; including node constructors found in edge constructors
    for constructor in dict.get('constructors'):
        src, tgt = constructor.get('src'), constructor.get('tgt')
        if(src):
            script += _process_node_constructor(src, aliases, missing_aliases)
            script += _process_node_constructor(tgt, aliases, missing_aliases)
        else:
            script += _process_node_constructor(constructor, aliases, missing_aliases)
    if missing_aliases:
        raise CompileError("The following aliases are not defined: " + ",".join(missing_aliases))
    # handle edge constructors
    for constructor in dict.get('constructors'):
        src, edge, tgt = constructor.get('src'), constructor.get('edge'), constructor.get('tgt')
        if edge:
            script += _process_edge_constructor(edge, aliases, src.get('alias'), tgt.get('alias'))
    return script

def _process_edge_constructor(edge, aliases, src_alias, tgt_alias):
    alias = edge.get('alias')
    ids = edge.get('ids')
    script = ""
    if alias:
        raise CompileError("Using alias in edge constructor is forbidden.")
    alias = f"x_{len(aliases)}"
    aliases.append(alias)
    edge['alias'] = alias
    labels = edge.get('labels')
    properties = edge.get('properties')
    if labels is None or len(labels) != 1:
        raise CompileError("Relationships should be of only one type in openCypher.")
    script += f'MERGE ({src_alias})-[{alias}:{labels[0]} {{\n    ' 
    idsE = [labels[0]]
    idsE.extend(ids)
    idsE.extend([src_alias, tgt_alias])
    script += _process_ids(idsE)
    script += f' \n}}]->({tgt_alias})\n'
    script += _process_properties(alias, labels, properties, setLabels=False)
    return script

def _process_node_constructor(node, aliases, missing_aliases):
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
                raise CompileError("Redefinition of the following alias: " + alias)
            aliases.append(alias)
            if alias in missing_aliases:
                missing_aliases.remove(alias)
        else:
            alias = f"x_{len(aliases)}"
            aliases.append(alias)
            node['alias'] = alias
        labels = node.get('labels')
        properties = node.get('properties')
        script += f'MERGE ({alias}:_dummy {{\n    '
        script += _process_ids(ids)
        script += f' \n}})\n'
        script += _process_properties(alias, labels, properties)
    return script

def _process_ids(ids):
    script = f'_id: "("'
    if ids:
        script += ' + '
    script += f'{ """ + "," + """.join(map(_wrap_id, ids)) } + ")"'
    return script

def _wrap_id(id: str):
    # id[0].islower() rules out both Labels and "constants"; the last check rules out access.keys
    if id[0].islower() and '.' not in id:
        return "elementID(" + id + ")"
    # labels should get enclosed into quotes; we add leading and trailing colons for labels
    elif id[0].isupper():
        return '":' + id + ':"'
    else:
        return id

def _process_properties(alias, labels, properties, setLabels = True):
    script = ""
    if setLabels or properties:
        script += f'ON CREATE\n'
        if setLabels:
            script += f'    SET { ",".join([alias + ":" + l for l in labels]) }'
        if properties:
            if setLabels:
                script += ",\n        "
            else:
                script += f'    SET '
            script += ",\n        ".join([alias + "." + p['key'] + " = " + p['value'] for p in properties])
        script += "\nON MATCH\n"
        if setLabels:
            script += f'    SET { ",".join([alias + ":" + l for l in labels]) }'
        if properties:
            if setLabels:
                script += ",\n        "
            else:
                script += f'    SET '
            script += ",\n        ".join([_conflict_detection(alias, p) for p in properties])
        script += "\n"
    return script

def _conflict_detection(alias, p):
    return (
        alias + "." + p['key'] + " = \n        CASE WHEN " 
        + alias + "." + p['key'] + " <> " + p['value'] 
        + '\n            THEN "Conflict Detected!"\n            ELSE ' 
        + p["value"]
    )

if __name__ == "__main__":
    from dtgraph import Rule
    dico = Rule.from_ascii('''
        MATCH (n) 
        RETURN n
        => (("c", v.fff, w) : Dummy),
        (x = (n) : Person {
            name = "SK1(" + n.name + ")",
            city = "test"
        })-[(): Knows]->(y = (n) : Person {
            name = "SK2(" + n.name + ")" 
        }), 
        (x)-[(v) : Likes {
            since = "01/01/1970"
        }]->(y),
        (() : Test)
    ''')._dict
    print(compile(dico))

    ## Wrap the identifiers in an argument list to elementID
    ## include identifiers of the source and the target into the list of arguments of the edge
    ## avoid having two '+' that follows each other when the argument list is empty