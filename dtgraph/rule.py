"""Property Graph transformation rule.

This module contains the `Rule` class for representation of a declarative 
property graph transformation rule.
"""

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

    def __init__(self, lhs = None, rhs = None, json = None, ascii = None):
        """Initializes a rule.

        Parameters
        ----------
        lhs : string
            A string representing the lhs of a rule as an executable script.
        rhs : string
            A string representing the rhs of a rule as an executable script.
        json : json
            A json object representing the rhs of the rule. It will be
            processed and an openCypher script will be obtained from it.
        ascii : string
            A string representing the rhs of the rule in ASCII-art style.
            It will be processed and an openCypher script will be obtained
            from it.
        """
        self.lhs = lhs
        if rhs is not None:
            self.rhs = rhs

    def to_json(self):
        """Convert the rule to JSON repr."""
        pass

    @classmethod
    def from_json(cls, json_data):
        """Create a rule obj from JSON repr."""
        pass

    def to_ascii(self):
        """Convert the rule to ASCII repr."""
        pass

    @classmethod
    def from_ascii(cls, ascii_string):
        """Create a rule obj from ASCII repr."""
        pass

    def apply(self, graph):
        """Perform graph transformation with the rule.

        Parameters
        ----------
        graph : dtgraph.backend.neo4j.graph.Neo4jGraph
            Graph to transform with the rule.
        """
        return graph.query(self.lhs + "\n" + self.rhs) 

    def __str__(self):
        return f"{self.lhs}\n{self.rhs}"
        
