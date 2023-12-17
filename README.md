# PySPARQL Anything
###### The SPARQL Anything Python Library

## Table of Contents
1. [User Guide](#user_guide)
   1. [Installation](#installation)
   2. [Basic Usage](#basic_usage)
   3. [Keyword Arguments](#kwargs)
3. [API](#api)

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

The keyword arguments to be passed to any of the PySPARQL Anything methods are the same as those of the regular SPARQL Anything CLI [1]

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

[1] See https://github.com/SPARQL-Anything/sparql.anything#command-line-interface-cli for more information.

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

### 2.1. METHODS
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
