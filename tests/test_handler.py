"""
Script to unit test the ParameterHandler class of PySPARQL Anything.
Author: Marco Ratta
Date: 01/03/2024
"""

import unittest
from pysparql_anything.args_handlers import transform_args

#  Test data:
data1 = {
    'query': 'my_query',
    'output': 'my_output',
    'format': 'my_format',
    'values': {
        '?_v1': 'a_value1',
        '?_v2': 'a_value2'
    }
}

data2 = {
    'q': 'my_query',
    'o': 'my_output',
    'f': 'my_format',
    'v': {
        '?_v1': 'a_value1',
        '?_v2': 'a_value2'
    }
}

output1 = [
    '--query', 'my_query', '--output', 'my_output', '--format', 'my_format',
    '-v', '?_v1=a_value1', '-v', '?_v2=a_value2'
]

output2 = [
    '-q', 'my_query', '-o', 'my_output', '-f', 'my_format',
    '-v', '?_v1=a_value1', '-v', '?_v2=a_value2',
]


class PySparqlHandlerTestCase(unittest.TestCase):

    def test_handler(self):
        test1 = transform_args(data1)
        test2 = transform_args(data2)
        print(test1)
        self.assertEqual(test1, output1)
        print(test2)
        self.assertEqual(test2, output2)


#  Test script main:
if __name__ == '__main__':
    unittest.main(verbosity=2)
