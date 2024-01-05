import setuptools

with open("README.md", "r") as fh:
    long_descr = fh.read()

setuptools.setup(
    name = "DTGraph",
    description = "Framework for specifying transformations of property graphs",
    author = "Yann Ramusat",
    author_address = "yann.ramusat@gmail.com",
    license = "MIT License",
    long_description = long_descr,
    long_description_content_type = "text/markdown",
    url = "https://github.com/yannramusat/DTGraph",
    packages = [
        "dtgraph",
        "dtgraph.backend.neo4j",
    ],
    package_dir = {
        "dtgraph": "dtgraph"
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        "neo4j",
    ],
)
