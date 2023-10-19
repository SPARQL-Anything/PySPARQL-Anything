"""
Script to unit test the ParameterHandler class of PySPARQL Anything.
@author Marco Ratta
@version 09/02/2023
"""

import unittest
from pysparql_anything.parameter_handler import transform_parameters

#  Test data:
data = {
    'q': 'my_query',
    'o': 'my_output',
    'f': 'my_format',
    'v': {
        '?_v1': 'a_value1',
        '?_v2': 'a_value2'
    }
}

output = [
    '-q', 'my_query', '-v', '?_v1=a_value1', '-v', '?_v2=a_value2',
    '-o', 'my_output', '-f', 'my_format'
]


class PySparqlHandlerTestCase(unittest.TestCase):

    def test_handler(self):
        test = transform_parameters(data)
        print(test)
        self.assertEqual(test, output)


#  Test script main:
if __name__ == '__main__':
    unittest.main(verbosity=2)
