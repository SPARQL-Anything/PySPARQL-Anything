[![How to](https://img.shields.io/badge/How%20to-use-green.svg)](#basic_usage)
[![How to](https://img.shields.io/badge/How%20to-join-blue.svg)](https://forms.gle/t1paTLz7jVu3RYnu8)
# PySPARQL Anything
###### The SPARQL Anything Python Library

## Table of Contents
1. [Introduction](#intro)
   1. [Façade-X](#fx)
   2. [Querying Anything](#query_anything)
2. [User Guide](#user_guide)
   1. [Installation](#installation)
   2. [Basic Usage](#basic_usage)
   3. [Tutorial](#tutorial)
3. [API](#api)
   1. [Methods](#methods)
4. [Development & Maintanance](#dev_guide)
   1. [Building PySPARQL Anything](#build)
   2. [SPARQL Anything Updates](#sa_updates)

## 1. Introduction <a name="intro"></a>

SPARQL Anything is a data integration and Semantic Web re-engineering system that implements the Façade-X meta-model, resolving the heterogeneity of sources by structurally mapping them onto a set of RDF components, upon
which semantic mappings can be constructed.

PySPARQL Anything is a python wrapper for the SPARQL Anything tool. It purports to offer to Python users dealing with tasks of data integration and RDF data construction and analysis access to the capabilities offered by SPARQL Anything.
Furthermore, it enables developers to inject RDF graphs into their Python RDFlib, NetworkX  or pandas-powered data science processes, opening new opportunities for developing complex, data- intensive pipelines for generating and manipulating RDF data.

### 1.1. Façade-X <a name="fx"></a>
Facade-X is a simplistic meta-model used by SPARQL Anything transformers to generate RDF data from diverse data sources. Intuitively, Facade-X uses a subset of RDF as a general approach to represent the source content as-it-is but in RDF. The model combines two types of elements: containers and literals. Facade-X always has a single root container. Container members are a combination of key-value pairs, where keys are either RDF properties or container membership properties. Instead, values can be either RDF literals or other containers. 

This is a generic example of a Facade-X data object (more examples below):
```sparql
@prefix fx: <http://sparql.xyz/facade-x/ns/> .
@prefix xyz: <http://sparql.xyz/facade-x/data/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
[] a fx:root ; rdf:_1 [
    xyz:someKey "some value" ;
    rdf:_1 "another value with unspecified key" ;
    rdf:_2 [
        rdf:type xyz:MyType ;
        rdf:_1 "another value"
    ]
] .
```
More details on the Facade-X metamodel can be found [here](https://github.com/SPARQL-Anything/sparql.anything/blob/v1.0-DEV/Facade-X.md).

### 1.2. Querying anything <a name="query_anything"></a>
SPARQL Anything extends the Apache Jena ARQ processors by overloading the SERVICE operator, as in the following example:

Suppose having this JSON file as input (also available at https://sparql-anything.cc/example1.json)
```json
[
  {
    "name": "Friends",
    "genres": [
      "Comedy",
      "Romance"
    ],
    "language": "English",
    "status": "Ended",
    "premiered": "1994-09-22",
    "summary": "Follows the personal and professional lives of six twenty to thirty-something-year-old friends living in Manhattan.",
    "stars": [
      "Jennifer Aniston",
      "Courteney Cox",
      "Lisa Kudrow",
      "Matt LeBlanc",
      "Matthew Perry",
      "David Schwimmer"
    ]
  },
  {
    "name": "Cougar Town",
    "genres": [
      "Comedy",
      "Romance"
    ],
    "language": "English",
    "status": "Ended",
    "premiered": "2009-09-23",
    "summary": "Jules is a recently divorced mother who has to face the unkind realities of dating in a world obsessed with beauty and youth. As she becomes older, she starts discovering herself.",
    "stars": [
      "Courteney Cox",
      "David Arquette",
      "Bill Lawrence",
      "Linda Videtti Figueiredo",
      "Blake McCormick"
    ]
  }
]
```
With SPARQL Anything you can select the TV series starring "Courteney Cox" with the SPARQL query
```sparql
PREFIX xyz: <http://sparql.xyz/facade-x/data/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX fx: <http://sparql.xyz/facade-x/ns/>

SELECT ?seriesName
WHERE {

    SERVICE <x-sparql-anything:https://sparql-anything.cc/example1.json> {
        ?tvSeries xyz:name ?seriesName .
        ?tvSeries xyz:stars ?star .
        ?star fx:anySlot "Courteney Cox" .
    }

}
```
and get this result without caring of transforming JSON to RDF.
```powershell
seriesName
"Cougar Town"
"Friends"
```
      
## 2. User Guide <a name="user_guide"></a>

### 2.1. Installation <a name="installation"></a>

PySPARQL Anything is released on PyPI. To install it on your machine type the following in your command prompt:
```
$ pip install pysparql-anything 
```

To remove PySPARQL Anything from your machine, do the following.

In your command prompt execute
```python
$ python
>>> import pysparql_anything as sa
>>> sa.utilities.remove_sparql_anything()
>>> exit()
$ pip uninstall pysparql-anything
```

### 2.2. Basic Usage <a name="basic_usage"></a>

PySPARQL Anything comes equipped with a CLI tool. Its functionalities can therefore either be accessed through the
command prompt or by importing the library into your scripts. Choosing the latter method will also enable the user
to return the results of their SPARQL queries as specific Python objects.

Below we show a few basic steps to illustrate usage.

1) To use the CLI tool, pen the command prompt with the current working directory set to the main folder of a SPARQL Anything project.
The CLI tool is accessed with the ```sparql-anything``` command. Executing
```
$ sparql-anything -h
```
will pull up the instructions on how to use the CLI:
```
Welcome to the PySPARQL Anything CLI. For the optional flags see below.

options:
  -h, --help            show this help message and exit
  -j [JAVA ...], --java [JAVA ...]
                        The JVM initialisation options.
  -q QUERY, --query QUERY
                        The path to the file storing the query to execute or the query itself.
  -o OUTPUT, --output OUTPUT
                        The path to the output file. [Default: STDOUT]
  -f FORMAT, --format FORMAT
                        Format of the output file. Supported values: JSON, XML, CSV, TEXT, TTL,
                        NT, NQ. [Default:TEXT or TTL]
  -l LOAD, --load LOAD  The path to one RDF file or a folder including a set of files to be
                        loaded. When present, the data is loaded in memory and the query executed
                        against it.
  -v [VALUES ...], --values [VALUES ...]
                        Values passed as input parameter to a query template. When present, the
                        query is pre-processed by substituting variable names with the values
                        provided. The argument can be used in two ways: (1) Providing a single
                        SPARQL ResultSet file. In this case, the query is executed for each set of
                        bindings in the input result set. Only 1 file is allowed. (2) Named
                        variable bindings: the argument value must follow the syntax:
                        var_name=var_value. The argument can be passed multiple times and the
                        query repeated for each set of values.
```

2) To import PySPARQL Anything in one's scripts simply import the library and initialise a ```pysparql_anything.sparql_anything.SparqlAnything``` object
```python
import pysparql_anything as sa
engine = sa.SparqlAnything()
```

Note that in both cases, if the SPARQL Anything jar isn't installed in the API's folder it will be downloaded there automatically the first time the module is imported or the CLI command has been executed.

3) As an example, to execute the following query from the SPARQL Anything MusicXML showcase with PySPARQL Anything,
```
java -jar sparql-anything-0.8.0-SNAPSHOT.jar -q queries/populateOntology.sparql -v filePath="./musicXMLFiles/AltDeu10/AltDeu10-017.musicxml" -v fileName="AltDeu10-017" -f TTL
```

one does
```
$ sparql-anything -q queries/populateOntology.sparql -v filePath=./musicXMLFiles/AltDeu10/AltDeu10-017.musicxml fileName=AltDeu10-017 -f TTL
```

or
```python
import pysparql_anything as sa
engine = sa.SparqlAnything()
engine.run(
    	query="queries/populateOntology.sparql",
    	format="ttl",
    	values={
            "filePath" : "./musicXMLFiles/AltDeu10/AltDeu10-017.musicxml",
            "fileName" : "AltDeu10-017"
    	}
    )
```

### 2.3. Tutorial <a name="tutorial"></a>
A live Google Colab demo demonstrating how to download, install and access the functionalities of PySPARQL Anything through its CLI and 
API can be found at the following link:

https://bit.ly/pysa-demo

## 3. API <a name="api"></a>

All of PySPARQL Anything functionalities can be accessed via the following four methods of the class 
``` pysparql_anything.sparql_anything.SparqlAnything ```.

The constructor for this class is
``` python
pysparql_anything.SparqlAnything(*jvm_options: str) -> pysparql_anything.sparql_anything.SparqlAnything
```
where ```*jvm_options``` are the optional string arguments representing the user's preferred JVM options.

As an example, one may have
```python
engine = sa.SparqlAnything("-Xrs", "-Xmx6g")
```
NOTE: the ```*jvm_options``` are final. Once they are set they cannot be changed without starting a new process.
This limitation is unfortunately due to the nature of the interaction between the JVM and the Python environment.
Please see [#6](https://github.com/SPARQL-Anything/PySPARQL-Anything/issues/6) for more information on this issue.

The keyword arguments to be passed to any of the PySPARQL Anything methods mirror the flags of SPARQL Anything CLI (See [here](https://github.com/SPARQL-Anything/sparql.anything#command-line-interface-cli) for more info).

All of the keyword arguments except for ```values```, requires to be assigned a ```dict```, must be assigned a string literal. 

Currently, the following arguments are supported:

```
 query: str - The path to the file storing the query to execute or the query itself.

 output: str - OPTIONAL - The path to the output file. [Default: STDOUT]

 load: str - OPTIONAL - The path to one RDF file or a folder including a set of
          files to be loaded. When present, the data is loaded in memory and
          the query executed against it.

 format: str - OPTIONAL -  Format of the output file. Supported values: JSON, XML,
          CSV, TEXT, TTL, NT, NQ. [Default:TEXT or TTL]

 values: dict[str, str] - OPTIONAL - Values passed as input parameter to a query template.
                     When present, the query is pre-processed by substituting variable
                     names with the values provided.
                     The argument can be used in two ways:
                     (1) Providing a single SPARQL ResultSet file. In this case,
                     the query is executed for each set of bindings in the input result set.
                     Only 1 file is allowed.
                     (2) Named variable bindings: the argument value must follow the syntax:
                     var_name=var_value. The argument can be passed multiple times and
                     the query repeated for each set of values.
```

### 3.1. Methods <a name="methods"></a>
``` python
SparqlAnything.run(**kwargs) -> None
```

Mirrors the functionalities of the CLI. This can be used to run a query the output of
which is to be printed on the command line or saved to a file. (See example above)

```python
SparqlAnything.ask(**kwargs) -> bool
```

Executes an ASK query and returns a Python boolean True or False.

```python
SparqlAnything.construct(graph_type: type=rdflib.graph.Graph, **kwargs) -> rdflib.graph.Graph | networkx.MultiDiGraph
```

Executes a CONSTRUCT query and returns a Python representation of a graph. 
The ```graph_type``` argument accepts ```rdflib.graph.Graph``` (default) or ```networkx.MultiDiGraph```.

```python
SparqlAnything.select(output_type: type=dict, **kwargs) -> dict | pandas.DataFrame
```

Executes a SELECT query and returns the result as a Python object.
The ```output_type``` argument accepts ```dict``` (default) or ```pandas.DataFrame```.

## 4. Development & Maintenance <a name="dev_guide"></a>

### 4.1. Building PySPARQL Anything <a name="build"></a>

To build the source distribution and binary distribution we proceed as follows. 

First, the tools we require are ```hatch``` as the build frontend (which comes with ```hatchling``` as its backend tool) and ```twine``` to upload the distribution files to PyPI.

All of these can be installed via ```pip install hatch``` or ```pip install twine``` if required.

Once the tools are ready, the build metadata can be configured in the ```pyproject.toml``` file. 

NOTE: it is not needed to amend anything in this file for versioning the software, as this is set dynamically (see below for how to perform this).

After the build metadata has been defined, one can proceed to build the distribution archives.

To do this, open the command prompt on the directory containing the ```pyproject.toml``` file and run
```
hatch build ./dist
```
This command should output some text and once completed should generate a ```dist``` directory containing two files:
```
dist/
├── pysparql_anything-0.8.1.2-py3-none-any.whl
└── pysparql_anything-0.8.1.2.tar.gz
```
for example. Here the ```tar.gz``` file is a source distribution whereas the ```.whl``` file is a binary distribution.

To upload the distributions one does 
```
twine upload dist/*
```
and enter the relevant PyPI credentials for this project. 

NOTE: this process is not exclusive, and other frontend tools like ```build``` together with ```hatchling``` may be similarly used to generate the distributions. The only limit currently is on sticking with ```hatchling``` as the build backend.

### 4.2. SPARQL Anything Updates <a name="sa_updates"></a>

Each version of PySPARQL Anything is tied to a released version of SPARQL Anything. Therefore, when a new version of the latter is released a new release of PySPARQL Anything should follow. 

This process simply involves updating the ```__about__.py``` module of the source code. To do this, set the ```__version__```, ```__SparqlAnything__```  and ```__jarMainPath__``` variables to the new values following the given structure.

As an example, to update from ```0.9.0``` to say ```0.9.1``` of SPARQL Anything, we would have
```python
# PySPARQL ANYTHING METADATA
# PySPARQL version for the build process:
__version__ = "0.9.0.1" # --> "0.9.1.1"

# SPARQL ANYTHING METADATA
# Version of SPARQL Anything to download:
__SparqlAnything__ = "0.9.0"  # --> "0.9.1"
# Path to the SPARQL Anything main class within the executable jar:
__jarMainPath__ = "io.github.sparqlanything.cli.SPARQLAnything"  # Check is this path is still valid for 0.9.1
# SPARQL Anything GitHub URI:
__uri__ = "SPARQL-Anything/sparql.anything"
```
After this build the new distribution files and upload them to PyPI.
