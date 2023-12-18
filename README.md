# PySPARQL Anything
###### The SPARQL Anything Python Library

## Table of Contents
1. [User Guide](#user_guide)
   1. [Installation](#installation)
   2. [Basic Usage](#basic_usage)
   3. [Keyword Arguments](#kwargs)
2. [API](#api)
   1. [Methods](#methods)
3. [Development and Maintanance](#dev_guide)
   1. [Building PySPARQL Anything](#build)
   2. [SPARQL Anything Updates](#sa_updates)
      
## 1. USER GUIDE <a name="user_guide"></a>

### 1.1. INSTALLATION <a name="installation"></a>

To install PySPARQL Anything on your machine type the following in your command prompt:
```powershell
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

### 1.2. BASIC USAGE <a name="basic_usage"></a>

1) Open the command prompt with the current working directory set to the main folder of a SPARQL Anything project.

2) Launch Python: 
```
$ python 
```
   
3) Import PySPARQL Anything: 
```python
>>> import pysparql_anything as sa
```

If the SPARQL Anything jar isn't installed in the API's folder it will now be downloaded there automatically.

4) Initialise a ```pysparql_anything.sparql_anything.SparqlAnything``` object:
```python
>>> engine = sa.SparqlAnything()
```

5) Run the query:
```python
>>> engine.run(**kwargs)
```

### 1.3. KEYWORD ARGUMENTS <a name="kwargs"></a>

The keyword arguments to be passed to any of the PySPARQL Anything methods are the same as those of the regular SPARQL Anything CLI (See [here](https://github.com/SPARQL-Anything/sparql.anything#command-line-interface-cli) for more info).

For example:
```python
>>> engine.run(q='queries/getFacade.sparql', f='TTL', o='C:/Users/Marco/Desktop/facade.ttl')
```

All of the keyword arguments except for ```v``` must be assigned a string literal. 

```v``` requires to be assigned a Python dictionary, as in the following example.

To execute the following query from the SPARQL Anything MusicXML showcase,
```powershell
java -jar sparql-anything-0.8.0-SNAPSHOT.jar -q queries/populateOntology.sparql -v filePath="./musicXMLFiles/AltDeu10/AltDeu10-017.musicxml" -v fileName="AltDeu10-017" -f TTL
```

with PySPARQL Anything, do
```python
>>> engine.run(
    	q='queries/populateOntology.sparql',
    	f='ttl',
    	v={
            'filePath' : './musicXMLFiles/AltDeu10/AltDeu10-017.musicxml',
            'fileName' : 'AltDeu10-017'
    	}
    )
```

The currently supported arguments are as follows.

```
 q: str - The path to the file storing the query to execute or the query itself.

 o: str - OPTIONAL - The path to the output file. [Default: STDOUT]

 l: str - OPTIONAL - The path to one RDF file or a folder including a set of
          files to be loaded. When present, the data is loaded in memory and
          the query executed against it.

 f: str - OPTIONAL -  Format of the output file. Supported values: JSON, XML,
          CSV, TEXT, TTL, NT, NQ. [Default:TEXT or TTL]

 v: dict[str, str] - OPTIONAL - Values passed as input parameter to a query template.
                     When by substituting variable names with the values provided.
                     The argument can be used in two ways:
                     (1) Providing a single SPARQL ResultSet file. In this case,
                     the query is executed for each set of bindings in the input result set.
                     Only 1 file is allowed.
                     (2) Named variable bindings: the argument value must follow the syntax:
                     var_name=var_value. The argument can be passed multiple times and
                     the query repeated for each set of values.
```

## 2. API <a name="api"></a>

All of PySPARQL Anything functionalities can be accessed via the following four methods of the class 
``` pysparql_anything.sparql_anything.SparqlAnything ```.

The constructor for this class is
``` python
pysparql_anything.SparqlAnything(*jvm_options: str) -> pysparql_anything.sparql_anything.SparqlAnything
```
where ```*jvm_options``` are the optional string arguments representing the user's preferred JVM options.

As an example, one may have
```python
engine = sa.SparqlAnything('-Xrs', '-Xmx6g')
```
NOTE: the ```*jvm_options``` are final. Once they are set they cannot be changed without starting a new process.
This limitation is unfortunately due to the nature of the interaction between the JVM and the Python environment.
Please see [#6](https://github.com/SPARQL-Anything/PySPARQL-Anything/issues/6) for more information on this issue.

### 2.1. METHODS <a name="methods"></a>
``` python
SparqlAnything.run(**kwargs) -> None
```

Reflects the functionalities of the original SPARQL Anything CLI. This can be used to run a query the output of
which is to be printed on the command line or saved to a file. (See example above)

```python
SparqlAnything.ask(**kwargs) -> bool
```

Executes an ASK query and returns a Python boolean True or False.

```python
SparqlAnything.construct(**kwargs) -> rdflib.graph.Graph
```

Executes a CONSTRUCT query and returns a rdflib graph object.

```python
SparqlAnything.select(**kwargs) -> dict
```

Executes a SELECT query and returns the result as a Python dictionary. 

## 3. DEVELOPMENT AND MAINTAINANCE <a name="dev_guide"></a>

### 3.1. Building PySPARQL Anything <a name="build"></a>

To build the source distribution and binary distribution we proceed as follows. 

First, the tools we require are ```hatch``` as the build frontend (which comes with ```hatchling``` as its backend tool) and ```twine``` to upload the distribution files to PyPI.

All of these can be installed via ```pip install hatch``` or ```pip install twine``` if required.

Once the tools are ready, the build metadata can be configured in the ```pyproject.toml``` file. 

NOTE: it is not needed to amend anything in this file for versioning the software, as this is set dynamically (see below for how to perform this).

After the build metadata has been defined, one can proceed to build the distribution archives.

To do this, open the command prompt on the directory containing the ```pyproject.toml``` file and run
```powershell
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
```powershell
twine upload dist/*
```
and enter the relevant PyPI credentials for this project. 

NOTE: this process is not exclusive, and other frontend tools like ```build``` together with ```hatchling``` may be similarly used to generate the distributions. The only limit currently is on sticking with ```hatchling``` as the build backend.

### 3.2. SPARQL Anything Updates <a name="sa_updates"></a>

Each version of PySPARQL Anything is tied to a released version of SPARQL Anything. Therefore, when a new version of the latter is released a new release of PySPARQL Anything should follow. 

This process simply involves updating the ```__about__.py``` module of the source code. To do this, set the ```__version__```, ```__SparqlAnything__```  and ```__jarMainPath__``` variables to the new values following the given structure.

As an example, to update from ```0.9.0``` to say ```0.9.1``` of SPARQL Anything, we would have
```python
# PySPARQL ANYTHING METADATA
# PySPARQL version for the build process:
__version__ = '0.9.0.1' # --> '0.9.1.1'

# SPARQL ANYTHING METADATA
# Version of SPARQL Anything to download:
__SparqlAnything__ = '0.9.0'  # --> '0.9.1'
# Path to the SPARQL Anything main class within the executable jar:
__jarMainPath__ = 'io.github.sparqlanything.cli.SPARQLAnything'  # Check is this path is still valid for 0.9.1
# SPARQL Anything GitHub URI:
__uri__ = 'SPARQL-Anything/sparql.anything'
```
After this build the new distribution files and upload them to PyPI.
