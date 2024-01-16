"""Property Graph transformation rule.

This module contains the `Rule` class for representation of a declarative 
property graph transformation rule.
"""

class Rule(object):
    """ Class TODO
    
    TODO
    """

    def __init__(self, lhs = None, rhs = None, json = None, ascii = None):
        """Initializes a rule.

        Attributes:
        -----------
        lhs : string
            A string representing the lhs of a rule as an openCypher script.
        rhs : string
            A string representing the rhs of a rule as an openCypher script.
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

    def apply(self, graph):
        return graph.query(self.lhs + "\n" + self.rhs) 

    def __str__(self):
        return f"{self.lhs}\n{self.rhs}"
        
