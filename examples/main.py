#!/bin/env python3
from dtgraph import Neo4jGraph, Rule

if __name__ == "__main__":
    # local development
    scheme = "bolt"
    hostname = "localhost"
    port = "7687"
    username = None
    password = None
    ## Neo4j sandbox
    #hostname = "34.200.233.111"
    #username = "neo4j"
    #password = "breakdown-certificates-navigations"

    uri = f"{scheme}://{hostname}:{port}"
    graph = Neo4jGraph(uri, "neo4j", username=username, password=password, verbose=True)

    print(graph.output_all_nodes())

    rule = Rule(lhs="MATCH (n)", rhs="RETURN n")
    print(rule.apply(graph))
