"""Property Graph transformation rule.

This module contains the `Rule` class for representation of a declarative 
property graph transformation rule.
"""
from dtgraph.parser import RuleParser, RightHandSide
from dtgraph.compiler import Compiler
from dtgraph.exceptions import RuleInitializationError

class Rule(object):
    """ Class representing a declarative transformation rule.

    (TODO long description for this class)

    Methods
    -------
    apply_on(graph)
        Execute the query on the Neo4jGraph.
    """

    _dict = None
    _compiled = None

    def __init__(self, ascii = None, raw = None, lhs = None, rhs = None):
        """Initializes a rule.

        The type of operation is defined by which arguments are provided.
        If an invalid combination of arguments is provided, raises an RuleInitializationError exception.
        Supported combinations: raw; lhs + rhs; lhs + ascii; ascii.

        Parameters
        ----------
        ascii : str
            A string representing the rhs of the rule in ASCII-art style if `lhs` is provided. 
            If `lhs` is not provided, its contains a representation of the entire rule in ASCII-art style.
            In any case, it will be processed by the DSL, and an openCypher script will be obtained
            from it.
        raw : str
            A string describing the rule as an executable openCypher script.
        lhs : str
            A string describing the lhs of the rule as an executable openCypher script.
        rhs : str
            A string describing the rhs of the rule in openCypher.
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
            raise RuleInitializationError("Invalid set of parameters.")

    @classmethod
    def from_ascii(cls, ascii, lhs = None):
        """Creates a rule object from an ASCII representation. """
        if lhs:
            return cls(lhs = lhs, ascii = ascii)
        else:
            return cls(ascii = ascii)
    
    @classmethod
    def from_raw(cls, raw):
        """Creates a rule object from a raw representation. """
        return cls(raw = raw)

    def _compile(self, database="neo4j", with_diagnose = True, explain = False, profile = False):
        # the compilation step is not idempotent
        if self._compiled is None:
            compiler = Compiler(database, with_diagnose=with_diagnose, explain = explain, profile = profile)
            self._compiled = compiler.compile(self._dict)

    def apply_on(self, graph, with_diagnose = True, explain = False, profile = False):
        """
        Applies the rule on the given graph, in the context of a graph transformation scenario.

        Parameters
        ----------
        graph : dtgraph.backend.neo4j.graph.Neo4jGraph
            Graph to be transformed by the rule.
        """
        if self._compiled is None:
            self._compile(graph.database, with_diagnose=with_diagnose, explain = explain, profile = profile)
        _ = graph.exec_rule(self._compiled, stats=True)

    def __str__(self):
        repr = ""
        if self._compiled:
            repr += "Compiled:\n" + self._compiled + "\n"
        if self._dict:
            repr += "Source dictionary:\n" + str(self._dict)
        return repr
        
