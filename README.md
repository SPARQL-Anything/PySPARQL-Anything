Python CLI for SPARQL Anything.

Current usage is as follows.

1) Open the command prompt with the current working directory set to the main folder of a SPARQL Anything project.

2) Launch Python: 
```
$ python 
```

3) Add the path to this module to the runtime environment:
```
import sys
sys.path.insert(0, 'pathToModule') 
```
   
4) Import SPyRQL Anything: 
```
import spyrql_anything as spy
```

5) (Optional) Set: 
```
path = 'pathToJar'
```

6) Initialise SpyrqlAnything object:
``` 
sp = spy.SpyrqlAnything(path)
```

7) Run the query:
```
sp.run(['-q', 'myQuery.sparql', ... ])
```
