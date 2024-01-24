"""Property Graph transformation rule.

This module contains the `Rule` class for representation of a declarative 
property graph transformation rule.
"""
from dtgraph.parser import RuleParser, RightHandSide
from dtgraph.compiler import compile

class Rule(object):
    """ Class representing a declarative transformation rule.

    (TODO long description for this class)

    Methods
    -------
    apply(graph)
        Execute the query on the Neo4jGraph
    """

    _dict = None
    _compiled = None

    def __init__(self, raw = None, lhs = None, rhs = None, ascii = None):
        """Initializes a rule.

        The type of operation is defined by which arguments are provided.
        If an invalid combination of arguments is provided, raises an RuleInitializationError exception.
        Supported combinations: raw; lhs + rhs; lhs + ascii; ascii.

        Parameters
        ----------
        raw : str
            A string describing the rule as an executable openCypher script.
        lhs : str
            A string describing the lhs of the rule as an executable openCypher script.
        rhs : str
            A string describing the rhs of the rule in openCypher.
        ascii : str
            A string representing the rhs of the rule in ASCII-art style if `lhs` is provided. 
            If `lhs` is not provided, its contains a representation of the entire rule in ASCII-art style.
            In any case, it will be processed by the DSL, and an openCypher script will be obtained
            from it.
        """
        if raw:
            self._compiled = raw
        elif lhs and rhs:
            self._compiled = f"{lhs}\n{rhs}"
        elif lhs and ascii:
            rhs_dict = RightHandSide.parseString(ascii, parseAll=True).asDict()
            self._dict = {'lhs': lhs, 'constructors': rhs_dict['constructors']}
        elif ascii:
            self._dict = RuleParser.parseString(ascii, parseAll=True).asDict()
        else:
            raise Exception("Invalid rule initialiser")

    @classmethod
    def from_ascii(cls, ascii, lhs = None):
        """Creates a rule object from an ASCII representation. """
        if lhs:
            return cls(lhs = lhs, ascii = ascii)
        else:
            return cls(ascii = ascii)

    def _compile(self):
        self._compile = compile(self._dict)

    def apply(self, graph):
        """
        Applies the rule's corresponding openCypher script in the context of a graph transformation scenario.

        Parameters
        ----------
        graph : dtgraph.backend.neo4j.graph.Neo4jGraph
            Graph to be transformed by the rule.
        """
        return graph.query(self._compiled)

    def __str__(self):
        repr = ""
        if self._compiled:
            repr += "Compiled:\n" + self._compiled + "\n"
        if self._dict:
            repr += "Source dictionary:\n" + str(self._dict)
        return repr
        
