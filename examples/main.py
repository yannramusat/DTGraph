#!/bin/env python3
from dtgraph import Neo4jGraph

if __name__ == "__main__":
    scheme = "bolt"
    hostname = "localhost"
    port = "7687"
    uri = f"{scheme}://{hostname}:{port}"
    graph = Neo4jGraph(uri, "neo4j", verbose=True)

    print(graph.output_all_nodes())
