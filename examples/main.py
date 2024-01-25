#!/bin/env python3
import os
from dtgraph import Neo4jGraph, Rule

if __name__ == "__main__":
    # Defaults for local development
    scheme = "bolt"
    hostname = "localhost"
    port = "7687"
    username = "neo4j"
    password = "password"
    # Using env. Useful for overriding previous
    # values when using a Neo4j sandbox
    if s := os.getenv('DTG_SCHEME'):
        scheme = s
    if h := os.getenv('DTG_HOSTNAME'):
        hostname = h
    if po := os.getenv('DTG_PORT'):
        port = po
    if u := os.getenv('DTG_USERNAME'):
        username = u
    if pa := os.getenv('DTG_PASSWORD'):
        password = pa

    uri = f"{scheme}://{hostname}:{port}"
    graph = Neo4jGraph(uri, "neo4j", username=username, password=password, verbose=True)

    graph.output_all_nodes()

    my_query = Rule.from_ascii('''
        MATCH (n:Person)-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(o:Person)
        => 
        (x = (n) : Actor {
            name = n.name,
            born = n.born
        })-[(m) : COLLEAGUE {
            movie = m.title
        }]->(y = (o) : Actor {
            name = o.name,
            born = o.born
        })
    ''')
    my_query.apply_on(graph)

    """ print(Rule.from_ascii('''
        MATCH (n)
        => 
        (x = (n) : Person {
            name = "SK1(" + n.name + ")" 
        })-[(): Knows]->(y = (n) : Person {
            name = "SK2(" + n.name + ")" 
        })
    '''))

    print(Rule.from_ascii( '''
        (x = (n) : Person {
            name = "SK1(" + n.name + ")" 
        })-[(): Knows]->(y = (n) : Person {
            name = "SK2(" + n.name + ")" 
        })
        ''', lhs = ''' 
        MATCH (n) 
    ''')) """
