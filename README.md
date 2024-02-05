# DTGraph

A tool for performing declarative transformations of property graphs.

## About project

The **DTGraph** library is a generic framework for transforming property graphs.
Transformations are written in our own declarative rule-based DSL (Domain Specific Language) and are compiled into efficient and scalable openCypher scripts.
This library supports a wide range of openCypher's compatible backends.

## Installation

You can install the **DTGraph** library from the source by cloning the repository using SSH:
```
git@github.com:yannramusat/DTGraph.git
```
or using HTTPS:
```
https://github.com/yannramusat/DTGraph.git
```

Then, install the library using Python's setup tools:
```
pip install .
```
or install it in *development mode* (the recommended way if you plan to contribute to the project):
```
pip install -r requirements.txt
```

### Database installation and configuration

There are several supported ways to connect to a database instance:

#### Neo4j Sandbox

#### Local Neo4j instance

#### Neo4j (Docker image)

The following command retrieves and runs a Docker container serving a Neo4j database locally:
```
sudo docker run --name neo4j5.16 --env=NEO4J_AUTH=none -p 7687:7687 -p 7474:7474 neo4j:5.16.0-community
```

To connect to this instance, you can refer to the example notebook at `examples/Tutorial_Connecting_Neo4j_Docker.ipynb`.

#### Memgraph (Docker image)

The following command retrieves and runs a Docker container serving a Memgraph database locally:
```
sudo docker run --name memgraph2.14.0 -p 7687:7687 -p 7444:7444 -p 3000:3000 memgraph/memgraph-platform:2.14.0-memgraph2.14.0-lab2.11.1
```

To connect to this instance, you can refer to the example notebook at `examples/Tutorial_Connecting_Memgraph_Docker.ipynb`.

## Tutorials

We provide some tutorials in the form of *Jupyter notebooks* (.ipynb files). 
To open these files, you will need to install **Jupyter labs**:
```
pip install jupyterlab
```

The tutorials are located in the `examples` folder, at the root of this repository.
You can start serving the Jupyter notebooks with the following query:
```
jupyter lab --notebook-dir=examples
```
