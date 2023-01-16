# PySPARQL Anything
###### A Python CLI for SPARQL Anything

## User Guide

###### INSTALLATION (provisional)

To install the beta on your machine type the following in your command prompt:
```
pip install -i https://test.pypi.org/simple/ pysparql-anything
```

###### USAGE

1) Open the command prompt with the current working directory set to the main folder of a SPARQL Anything project.

2) Launch Python: 
```
$ python 
```
   
3) Import PySPARQL Anything: 
```
import pysparql_anything as cli
```

If the SPARQL Anything jar isn't installed in the API's folder it will now be downloaded there automatically.

4) Initialise a PySpyrqlAnything object:
``` 
engine = cli.SparqlAnything()
```

5) Run the query:
```
engine.run(**kwargs)
```
The keyword arguments to be set are the same as those of the regular Sparql Anything CLI, minus the hyphen. 

For example:
```
engine.run(q='queries/getFacade.sparql', f='TTL', o='C:/Users/Marco/Desktop/facade.ttl')
```

## API

All keyword arguments to be set are the same as those of the regular Sparql Anything CLI, minus the hyphen.

See https://github.com/SPARQL-Anything/sparql.anything#command-line-interface-cli .

###### engine.run(**kwargs)

Reflects the functionalities of the original SPARQL Anything CLI. This can be used to run a query the output of
which is to be printed on the command line or saved to a file. (See example above)

###### engine.ask(**kwargs)

Executes an ASK query and returns a Python boolean True or False.

###### engine.construct(**kwargs)

Executes a CONSTRUCT query and returns a rdflib graph object.

###### engine.select(**kwargs)

Executes a SELECT query and returns the result as a Python dictionary. 