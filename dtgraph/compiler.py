from dtgraph.exceptions import CompileError

class Compiler:
    def __init__(self, database):
        self._database = database

    def compile(self, dict) -> str:
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
                script += self._process_node_constructor(src, aliases, missing_aliases)
                script += self._process_node_constructor(tgt, aliases, missing_aliases)
            else:
                script += self._process_node_constructor(constructor, aliases, missing_aliases)
        if missing_aliases:
            raise CompileError("The following aliases are not defined: " + ",".join(missing_aliases))
        # handle edge constructors
        for constructor in dict.get('constructors'):
            src, edge, tgt = constructor.get('src'), constructor.get('edge'), constructor.get('tgt')
            if edge:
                script += self._process_edge_constructor(edge, aliases, src.get('alias'), tgt.get('alias'))
        return script

    def _process_edge_constructor(self, edge, aliases: list[str], src_alias: str, tgt_alias: str) -> str:
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
        script += self._process_ids(idsE)
        script += f' \n}}]->({tgt_alias})\n'
        script += self._process_properties(alias, labels, properties, setLabels=False)
        return script

    def _process_node_constructor(self, node, aliases: list[str], missing_aliases: list[str]) -> str:
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
            script += self._process_ids(ids)
            script += f' \n}})\n'
            script += self._process_properties(alias, labels, properties)
        return script

    def _process_ids(self, ids: list[str]) -> str:
        script = f'_id: "("'
        if ids:
            script += ' + '
        script += f'{ """ + "," + """.join(map(self._wrap_id, ids)) } + ")"'
        return script

    def _wrap_id(self, id: str) -> str:
        # id[0].islower() rules out both Labels and "constants"; the last check rules out access.keys
        if id[0].islower() and '.' not in id:
            return ("element" if self._database == "neo4j" else "") + "ID(" + id + ")"
        # labels should get enclosed into quotes; we add leading and trailing colons for labels
        elif id[0].isupper():
            return '":' + id + ':"'
        else:
            return id

    def _process_properties(self, alias: str, labels: list[str], properties: list[dict[str, str]], setLabels: bool = True) -> str:
        script = ""
        if (setLabels and labels) or properties:
            script += f'ON CREATE\n'
            if setLabels and labels:
                script += f'    SET { ",".join([alias + ":" + l for l in labels]) }'
            if properties:
                if setLabels and labels:
                    script += ",\n        "
                else:
                    script += f'    SET '
                script += ",\n        ".join([alias + "." + p['key'] + " = " + p['value'] for p in properties])
            script += "\nON MATCH\n"
            if setLabels and labels:
                script += f'    SET { ",".join([alias + ":" + l for l in labels]) }'
            if properties:
                if setLabels and labels:
                    script += ",\n        "
                else:
                    script += f'    SET '
                script += ",\n        ".join([self._conflict_detection(alias, p) for p in properties])
            script += "\n"
        return script

    def _conflict_detection(self, alias: str, p: dict[str, str]) -> str:
        return (
            alias + "." + p['key'] + " = \n        CASE\n            WHEN " 
            + alias + "." + p['key'] + " <> " + p['value'] 
            + ' THEN\n                "Conflict Detected!"\n            ELSE\n                ' 
            + p["value"] + "\n        END"
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
    compiler = Compiler("neo4j")
    print(compiler.compile(dico))

    # because dico is modified in place during the compilation step, 
    # we need to create a new dictionary
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
    compiler = Compiler("memgraph")
    print(compiler.compile(dico))