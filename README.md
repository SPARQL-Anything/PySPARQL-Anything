# PySPARQL Anything
###### A Python CLI for SPARQL Anything

## User Guide

###### INSTALLATION 

To install PySPARQL Anything on your machine type the following in your command prompt:
```
pip install -i https://test.pypi.org/simple/ pysparql-anything --extra-index-url https://pypi.org/simple PyGithub
```

To remove PySPARQL Anything from your machine, do the following.

In your command prompt execute
```
$ python
>>> import pysparql_anything as cli
>>> cli.config.remove_jar()
>>> exit()
$ pip uninstall pysparql-anything
```

###### USAGE

1) Open the command prompt with the current working directory set to the main folder of a SPARQL Anything project.

2) Launch Python: 
```
$ python 
```
   
3) Import PySPARQL Anything: 
```
>>> import pysparql_anything as cli
```

If the SPARQL Anything jar isn't installed in the API's folder it will now be downloaded there automatically.

4) Initialise a ```pysparql_anything.sparql_anything.SparqlAnything``` object:
``` 
>>> engine = cli.SparqlAnything()
```

5) Run the query:
```
>>> engine.run(**kwargs)
```
The keyword arguments to be set are the same as those of the regular Sparql Anything CLI, minus the hyphen. 

For example:
```
>>> engine.run(q='queries/getFacade.sparql', f='TTL', o='C:/Users/Marco/Desktop/facade.ttl')
```

All of the keyword arguments except for ```v``` want to be assigned a string literal. 

```v``` requires to be assigned a Python dictionary, as in the following example.

To execute the following query from the SPARQL Anything MusicXML showcase,
```
java -jar sparql-anything-0.8.0-SNAPSHOT.jar -q queries/populateOntology.sparql -v filePath="./musicXMLFiles/AltDeu10/AltDeu10-017.musicxml" -v fileName="AltDeu10-017" -f TTL
```

with PySPARQL Anything, do
```
>>> engine.run(
    	q='queries/populateOntology.sparql',
    	f='ttl',
    	v={
            'filePath' : './musicXMLFiles/AltDeu10/AltDeu10-017.musicxml',
            'fileName' : 'AltDeu10-017'
    	}
    )
```

## API

All of PySPARQL Anything functionalities can be accessed via the following four methods of the class 
```pysparql_anything.sparql_anything.SparqlAnything```.

All keyword arguments to be set are the same as those of the regular Sparql Anything CLI, minus the hyphen.

See https://github.com/SPARQL-Anything/sparql.anything#command-line-interface-cli  and above for some particular
examples.

``` run(**kwargs) -> None ```

Reflects the functionalities of the original SPARQL Anything CLI. This can be used to run a query the output of
which is to be printed on the command line or saved to a file. (See example above)

``` ask(**kwargs) -> bool ```

Executes an ASK query and returns a Python boolean True or False.

``` construct(**kwargs) -> rdflib.Graph ```

Executes a CONSTRUCT query and returns a rdflib graph object.

``` select(**kwargs) -> dict ```

Executes a SELECT query and returns the result as a Python dictionary. 