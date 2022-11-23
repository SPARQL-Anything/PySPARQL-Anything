# SPyRQL Anything
###### A Python CLI for SPARQL Anything

## User Guide

###### INSTALLATION

1) Install PyJNIus:
```
https://pyjnius.readthedocs.io/en/stable/installation.html
```

2) Navigate to the folder where Python is installed on the machine. 

Then, do -> Lib -> site-packages and drop the spyrql_anything.py file in that folder.

Windows 10 example:
```
C:\Users\aUser\AppData\Local\Programs\Python\Python310\Lib\site-packages
```

###### USAGE

1) Open the command prompt with the current working directory set to the main folder of a SPARQL Anything project.

2) Launch Python: 
```
$ python 
```
   
3) Import SPyRQL Anything: 
```
import spyrql_anything as spy
```

4) Initialise a SpyrqlAnything object:
``` 
jar = 'localPathToJar'
engine = spy.SpyrqlAnything(jar)
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

IN PROGRESS: the option f='dict' allows a SELECT query to be returned as a Python dictionary:
```
aDictionary = engine.run(q='myQuery.sparql',..., f='dict')
```