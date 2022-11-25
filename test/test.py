from pysparql_anything import PySparqlAnything as spy
# jar must be user defined to run the test.
jar = '/Users/ed4565/Development/sparql-anything/sparql.anything/sparql-anything-cli/target/sparql-anything-0.9.0-SNAPSHOT.jar'
engine = spy(jar)

engine.run(q='test.sparql')
#
#
#
out = engine.select(q='test.sparql')
print(out)
