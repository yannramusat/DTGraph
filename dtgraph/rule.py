"""Property Graph transformation rule.

This module contains the `Rule` class for representation of a declarative 
property graph transformation rule.
"""
import json
from dtgraph.parser import RuleParser, RightHandSide

class Rule(object):
    """ Class representing a declarative transformation rule.

    (TODO long description for this class)
    
    Attributes
    ----------
    lhs : string
        A string representing the lhs of a rule as an executable script.
    rhs : string
        A string representing the rhs of a rule as an executable script.

    Methods
    -------
    apply(graph)
        Execute the query on the Neo4jGraph
    """

    _dict = None
    _compiled = None

    def __init__(self, raw = None, lhs = None, rhs = None, ascii = None):
        """Initializes a rule.

        Parameters
        ----------
        raw : string
            A string describing the rule as an executable openCypher script.
        lhs : string
            A string describing the lhs of the rule as an executable openCypher script.
        rhs : string
            A string describing the rhs of the rule in openCypher.
        ascii : string
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
        """Create a rule object from an ASCII representation """
        if lhs:
            return cls(lhs = lhs, ascii = ascii)
        else:
            return cls(ascii = ascii)

    def _compile(self):
        pass

    def apply(self, graph):
        """Perform graph transformation with the rule.

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
        
