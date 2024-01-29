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

#### Memgraph (WIP)

## Tutorials

We provide some tutorials in the form of *Jupyter notebooks* (.ipynb files). To open these files, you will need to install **Jupyter labs**:
```
pip install jupyterlab
```

The tutorials are located in the `examples` folder, at the root of this repository.
