#!/bin/env python3
import os
from dtgraph import Neo4jGraph, Rule, Transformation

if __name__ == "__main__":
    # Defaults for local development
    scheme = "bolt"
    hostname = "localhost"
    port = "7687"
    username = "neo4j"
    password = "password"
    database = "neo4j"
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
    if d := os.getenv('DTG_DATABASE'):
        database = d

    uri = f"{scheme}://{hostname}:{port}"
    graph = Neo4jGraph(uri, database=database, username=username, password=password)

    graph.output_all_nodes()

    from dtgraph.scenarios.movies import Movies
    Movies.load(graph)

    my_rule = Rule('''
        MATCH (n:Person)-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(o:Person)
        WHERE n.name < o.name
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

    my_transform = Transformation([my_rule])
    my_transform.apply_on(graph)

    my_second_rule = Rule('''
        MATCH (d:Person)-[:DIRECTED]->(m:Movie)<-[:ACTED_IN]-(a:Person)
        =>
        (x = (d) : Director {
            name = d.name,
            born = d.born
        })-[(m) : SUPERVISED {
            movie = m.title
        }]->(y = (a) : Actor {
            name = a.name,
            born = a.born
        })
    ''')
    my_transform.add(my_second_rule)
    ## We can see that `James Marshall is both a Director and an Actor.
    my_transform.eject()

    # second round
    graph.output_all_nodes()
    my_transform.exec(graph)

    # abort round
    graph.output_all_nodes()
    my_transform.apply_on(graph)
    my_transform.abort()

    # third round
    graph.output_all_nodes()
    my_transform(graph)

    # fourth round
    graph.output_all_nodes()
    my_transform(graph, destructive=True)

    # fifth round
    graph.output_all_nodes()
    my_transform(graph)

    # final printing
    graph.output_all_nodes()
