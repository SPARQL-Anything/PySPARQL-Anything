"""
Script to unit test the ParameterHandler class of PySPARQL Anything.
@author Marco Ratta
@version 09/02/2023
"""

import unittest
from pysparql_anything.parameter_handler import ParameterHandler


class PySparqlHandlerTestCase(unittest.TestCase):

    def test_combine(self):
        test = handler.combine()
        print(test)
        self.assertEqual(test, output)

#  Test data:
data = {
    'q' : 'my_query',
    'o' : 'my_output',
    'f' : 'my_format',
    'v' : {
        '?_v1' : 'a_value1',
        '?_v2' : 'a_value2'
    }
}

output = [
    '-q', 'my_query', '-v', '?_v1=a_value1', '-v', '?_v2=a_value2',
    '-o', 'my_output', '-f', 'my_format'
]

#  Test script main:
if __name__ == '__main__':
    handler = ParameterHandler(data)
    unittest.main(verbosity=2)