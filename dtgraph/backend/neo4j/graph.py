from neo4j import GraphDatabase, basic_auth

class Neo4jGraph(object):
    """Class reflecting a Neo4j graph instance.

    This class encapsulates a neo4j.GraphDatabase object.
    Note that it also supports other openCypher compatible backends such as Memgraph.
    """

    def __init__(self, uri, database, username=None, password=None, verbose=False):
        if username is None:
            self.driver = GraphDatabase.driver(
                uri, 
                auth=None)
        else:
            self.driver = GraphDatabase.driver(
                uri, 
                auth=basic_auth(username, password))
        self.database = database
        self.verbose = verbose

    def close(self):
        self.driver.close

    def print_query_stats(self, records, summary, keys):
        print("The query `{query}` returned {records_count} records in {time} ms.".format(
            query=summary.query, 
            records_count=len(records),
            time=summary.result_available_after))

    def flush_database(self):
        flush_query = """
        MATCH (n) DETACH DELETE(n)
        """
        records, summary, keys = self.driver.execute_query(
            flush_query,
            database=self.database)
        if(self.verbose):
            self.print_query_stats(records, summary, keys)
        print(f"Flushed database: Deleted {summary.counters.nodes_deleted} nodes, deleted {summary.counters.relationships_deleted} relationships, completed after {summary.result_available_after} ms.")

    def abort(self, stats=False):
        abort_query = """
        MATCH (n:`_dummy`)
        DETACH DELETE n
        """
        records, summary, keys = self.driver.execute_query(
            abort_query,
            database=self.database)
        if(self.verbose):
            self.print_query_stats(records, summary, keys)
        if(stats):
            print(f"Abort: Deleted {summary.counters.nodes_deleted} nodes, deleted {summary.counters.relationships_deleted} relationships, completed after {summary.result_available_after} ms.")
    
    def destruct_input(self, stats = False):
        destruct_query = """
        MATCH (n)
        WHERE NOT n:`_dummy`
        DETACH DELETE n
        """
        records, summary, keys = self.driver.execute_query(
            destruct_query,
            database=self.database)
        if(self.verbose):
            self.print_query_stats(records, summary, keys)
        if(stats):
            print(f"Destruct: Deleted {summary.counters.nodes_deleted} nodes, deleted {summary.counters.relationships_deleted} relationships, completed after {summary.result_available_after} ms.")

    def remove_bookkeeping(self, stats=False):
        remove_query = """
        MATCH ()-[r]->()
        REMOVE r._id, r._hasConflict
        WITH *
        MATCH (n:`_dummy`)
        REMOVE n:_dummy, n:_hasConflict, n._id
        """
        records, summary, keys = self.driver.execute_query(
            remove_query,
            database=self.database)
        if(self.verbose):
            self.print_query_stats(records, summary, keys)
        if(stats):
            print(f"Eject: Removed {summary.counters.labels_removed} labels, erased {summary.counters.properties_set} properties, completed after {summary.result_available_after} ms.")

    def populate_with_csv(self, path_to_csv_file, mergeCMD, fieldterminator="|", stats=False):
        populate_query = f"LOAD CSV FROM '{path_to_csv_file}' as row FIELDTERMINATOR '{fieldterminator}' " + mergeCMD
        records, summary, keys = self.driver.execute_query(
            populate_query,
            database=self.database)
        if(self.verbose):
            self.print_query_stats(records, summary, keys)
        if(self.verbose or stats):    
            print(f"CSV:    Added {summary.counters.labels_added} labels, created {summary.counters.nodes_created} nodes, " 
                  f"set {summary.counters.properties_set} properties, created {summary.counters.relationships_created} relationships, completed after {summary.result_available_after} ms.")

    def output_all_nodes(self, stats=True):
        count_all_query = """
        MATCH (n)
        RETURN COUNT(n) as count
        """
        records, summary, keys = self.driver.execute_query(
            count_all_query,
            database=self.database)
        if(self.verbose):
            self.print_query_stats(records, summary, keys)
        if(self.verbose or stats):
            print(f"Info: There are currently {records[0]['count']} node(s) in the database.")

    def query(self, query):
        records, summary, keys = self.driver.execute_query(
            query,
            database=self.database)
        if(self.verbose):
            self.print_query_stats(records, summary, keys)
            print(f"Query:  Added {summary.counters.labels_added} labels, created {summary.counters.nodes_created} nodes, " 
                  f"set {summary.counters.properties_set} properties, created {summary.counters.relationships_created} relationships, completed after {summary.result_available_after} ms.")
        return summary.result_available_after
    
    def load_scenario_script(self, query, stats=False):
        records, summary, keys = self.driver.execute_query(
            query,
            database=self.database)
        if(self.verbose):
            self.print_query_stats(records, summary, keys)
        if(self.verbose or stats):
            print(f"Load scenario: Added {summary.counters.labels_added} labels, created {summary.counters.nodes_created} nodes, " 
                  f"set {summary.counters.properties_set} properties, created {summary.counters.relationships_created} relationships, completed after {summary.result_available_after} ms.")
        return summary
    
    def exec_rule(self, query, stats=False):
        records, summary, keys = self.driver.execute_query(
            query,
            database=self.database)
        if(self.verbose):
            self.print_query_stats(records, summary, keys)
        if(self.verbose or stats):
            print(f"Rule: Added {summary.counters.labels_added} labels, created {summary.counters.nodes_created} nodes, " 
                  f"set {summary.counters.properties_set} properties, created {summary.counters.relationships_created} relationships, completed after {summary.result_available_after} ms.")
        return summary

    def diagnose_nodes(self, stats=True):
        diagnose_nodes_query = """
        MATCH (n:_hasConflict)
        RETURN n
        """
        records, summary, keys = self.driver.execute_query(
            diagnose_nodes_query,
            database=self.database)
        if(self.verbose):
            self.print_query_stats(records, summary, keys)
        if(self.verbose or stats):
            print(f"NodeConflicts: There are currently {len(records)} nodes in the database which have a conflict.")
        for r in records:
            print(" ", self._pretty_print_node(r['n']))

    def _pretty_print_node(self, node, print_conflict = True):
        str_ = "(" 
        if node.labels:
            str_ += ":"
        str_ += ":".join([l for l in node.labels if l != "_hasConflict" and l != "_dummy"])
        str_ += " {"
        str_ += ", ".join([k + ": " + str(v) for k, v in node.items() if k != '_id' and v != "Conflict Detected!"])
        str_ += "})"
        if(print_conflict):
            str_ += " has a conflict on attributes ['"
            str_ += "', '".join([k for k, v in node.items() if v == "Conflict Detected!"])
            str_ += "']." # It has been generated with parameters: " + node['_id']
        return str_

    def diagnose_edges(self, stats=True):
        diagnose_nodes_query = """
        MATCH (i)-[r]->(o)
        WHERE r._hasConflict IS NOT NULL
        RETURN i, r, o
        """
        records, summary, keys = self.driver.execute_query(
            diagnose_nodes_query,
            database=self.database)
        if(self.verbose):
            self.print_query_stats(records, summary, keys)
        if(self.verbose or stats):
            print(f"EdgeConflicts: There are currently {len(records)} edges in the database which have a conflict.")
        for r in records:
            print(" ",self._pretty_print_node(r['i'], print_conflict=False), end="")
            print(self._pretty_print_edge(r['r']), end="")
            print(self._pretty_print_node(r['o'], print_conflict=False), end=" ")
            print(self._pretty_print_edge_conflicts(r['r']))

    def _pretty_print_edge(self, edge):
        str_ = "-[:" + edge.type
        str_ += " {"
        str_ += ", ".join([k + ": " + str(v) for k, v in edge.items() if k != '_id' and k != "_hasConflict" and v != "Conflict Detected!"])
        str_ += "}]->" # It has been generated with parameters: " + node['_id']
        return str_

    def _pretty_print_edge_conflicts(self, edge):
        str_ = "has a conflict on attributes ['"
        str_ += "', '".join([k for k, v in edge.items() if v == "Conflict Detected!"])
        str_ += "']"
        return str_

    # TODO refactor the code below by pushing into the following functions the logic to handle the differences in how backends define their indexes
    # rename funtions according to PEP8, i.e., add_index
    def addIndex(self, query, stats=False):
        records, summary, keys = self.driver.execute_query(
                query,
                database=self.database,
                )
        if(self.verbose):
            self.print_query_stats(records, summary, keys)
        if(self.verbose or stats):
            print(f"Index: Added {summary.counters.indexes_added} index, completed after {summary.result_available_after} ms.")

    def dropIndex(self, query, stats=False):
        records, summary, keys = self.driver.execute_query(
                query,
                database=self.database,
                )
        if(self.verbose):
            self.print_query_stats(records, summary, keys)
        if(self.verbose or stats):
            print(f"Index: Removed {summary.counters.indexes_removed} index, completed after {summary.result_available_after} ms.") 

    def addConstraint(self, query, stats=False):
        records, summary, keys = self.driver.execute_query(
                query,
                database=self.database,
                )
        if(self.verbose):
            self.print_query_stats(records, summary, keys)
        if(self.verbose or stats):
            print(f"Cns:    Added {summary.counters.constraints_added} constraint, completed after {summary.result_available_after} ms.")

    def dropConstraint(self, query, stats=False):
        records, summary, keys = self.driver.execute_query(
                query,
                database=self.database,
                )
        if(self.verbose):
            self.print_query_stats(records, summary, keys)
        if(self.verbose or stats):
            print(f"Cns:    Removed {summary.counters.constraints_removed} constraint, completed after {summary.result_available_after} ms.") 