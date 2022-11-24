import spyrql_anything as spy

jar = '/Users/ed4565/Development/sparql-anything/sparql.anything/sparql-anything-cli/target/sparql-anything-0.9.0-SNAPSHOT.jar'
engine = spy.SpyrqlAnything(jar)
engine.run(q='test.sparql')
#
#
#
out = engine.select(q='test.sparql')
print(out)