"""Property Graph transformations.

This module contains the `Transformation` class for representation of declarative 
property graph transformations.

An instance manages a set of transformation rules, and provide several facilities for dealing with property graph trasnformations:
- Rules can be applied and reverted;
- New rules can be added to a current transformation;
- Efficient lookup and investigation of conflicts;
- Ejection mechanism: when a transformation is validated, removes internal bookeeping data.
"""
from dtgraph.rule import Rule
from dtgraph.exceptions import TransformationActivationError

class Transformation(object):
    """This class represents a declarative transformation. It manages a set of rules.

    (TODO long description for this class)

    Methods
    -------
    add(rule)
        Add this rule to the transformation. If the transformation is active, this rule is executed.
    apply_on(graph)
        Execute the query on the Neo4jGraph. The transformation is activated.
    diagnose
        Print information about conflicts.
    eject
        Removes internal bookeeping data (if any). The transformation is deactivated.
        This is useful if you want to keep both the input and output for later use.
    revert
        Revert the transformation and removes output data from the underlying graph. The transformation is deactivated.
    validate
        Delete source data and eject internal data. The transformation is deactivated.
    """

    _graph = None # when not none the transformation is active

    def __init__(self, rules):
        """Initializes a transformation.

        The type of operation is defined by which arguments are provided.
        If an invalid combination of arguments is provided, raises an RuleInitializationError exception.
        Supported combinations: raw; lhs + rhs; lhs + ascii; ascii.

        Parameters
        ----------
        rules : list[dtgraph.rule.Rule]
            A list of rules.
        """
        self._rules = rules

    def add(self, rule):
        """Add this rule to the transformation. If the transformation is active, this rule is executed.

        Parameters:
        -----------
        rule : dtgraph.rule.Rule
            New rule to add to the transformation.
        """
        self._rules.append(rule)
        if self._graph:
            rule.apply_on(self._graph)

    def apply_on(self, graph):
        """
        Applies all the rule on the given graph.
        Sets the transformation in active state.

        Parameters
        ----------
        graph : dtgraph.backend.neo4j.graph.Neo4jGraph
            Graph to be transformed by the rules.
        """
        if self._graph:
            raise TransformationActivationError("The transformation is already active on another graph.")
        else:
            self._graph = graph
        self._pre_apply()
        for r in self._rules:
            r.apply_on(self._graph)

    def _pre_apply(self):
        """
        Sets-up the environment for executing the transformation.
        """
        indexDummy = """
        CREATE INDEX idx_dummy IF NOT EXISTS
        FOR (n:_dummy)
        ON (n._id)
        """
        self._graph.addIndex(indexDummy, stats=True)

    def eject(self):
        dropDummy = """
        DROP INDEX idx_dummy IF EXISTS
        """
        self._graph.dropIndex(dropDummy, stats=True)
        self._graph.remove_bookkeeping(stats=True)
        # finally, set the transformation to be inactive
        self._graph = None