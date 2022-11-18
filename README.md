# SPyRQL Anything
###### A Python CLI for SPARQL Anything.

## User Guide

<<<<<<< HEAD
Open the command prompt with the current working directory set to the main folder of a SPARQL Anything project.

Launch Python, ```$ python ```.
=======
###### INSTALLATION

Navigate to the folder where Python is installed on the machine. 

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

4) Initialise SpyrqlAnything object:
``` 
path = 'localPathToJar'
sp = spy.SpyrqlAnything(path)
```

5) Run the query:
```
sp.run(**kwargs)
```
The keyword argument to be set are the same as the regular Sparql Anything CLI, minus the hyphen. 

For example:
```
sp.run(q='queries/getFacade.sparql', f='TTL', o='C:/Users/Marco/Desktop/facade.ttl')
```
>>>>>>> f8935dccc1345cefb154435fff1e9f5268bb50f7
