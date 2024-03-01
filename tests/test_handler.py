"""
Script to unit test the ParameterHandler class of PySPARQL Anything.
Author: Marco Ratta
Date: 01/03/2024
"""

import unittest
from pysparql_anything.args_handlers import transform_args

#  Test data:
data = {
    'query': 'my_query',
    'output': 'my_output',
    'format': 'my_format',
    'values': {
        '?_v1': 'a_value1',
        '?_v2': 'a_value2'
    }
}

output = [
    '-q', 'my_query', '-v', '?_v1=a_value1', '-v', '?_v2=a_value2',
    '--output', 'my_output', '--format', 'my_format'
]


class PySparqlHandlerTestCase(unittest.TestCase):

    def test_handler(self):
        test = transform_args(data)
        print(test)
        self.assertEqual(test, output)


#  Test script main:
if __name__ == '__main__':
    unittest.main(verbosity=2)
