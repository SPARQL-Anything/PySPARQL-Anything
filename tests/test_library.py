"""
Unit testing script for the PySPARQL Anything API.
For the construction of this script, files from the book 'Learning SPARQL'
by Bob DuCharme have been used.

@author Marco Ratta
@version 16/01/2023
"""

import unittest
import pysparql_anything as sa
from rdflib import Graph


class PySparqlAPITestCase(unittest.TestCase):

    def test_ask(self):
        self.assertTrue(engine.ask(q='queries/ask/ex199.rq', l='ex198.ttl'))
        self.assertTrue(engine.ask(q='queries/ask/ex202.rq', l='ex198.ttl'))
        self.assertFalse(engine.ask(q='queries/ask/ex199.rq', l='ex012.ttl'))
        self.assertFalse(engine.ask(q='queries/ask/ex199.rq', l='ex012.ttl'))

    def test_construct(self):
        g_1 = Graph().parse('ex189.txt', format='ttl')
        x_1 = engine.construct(q='queries/construct/ex188.rq', l='ex187.ttl')
        g_2 = Graph().parse('ex191.txt', format='ttl')
        x_2 = engine.construct(q='queries/construct/ex190.rq', l='ex187.ttl')
        self.assertEqual(len(x_1 - g_1), 0)
        self.assertEqual(len(x_2 - g_2), 0)

    def test_select(self):
        d_1 = {
            'head': {'vars': ['seriesName']},
            'results': {
                'bindings': [{
                        'seriesName': {
                            'type': 'literal',
                            'value': 'Friends'
                        }
                    },
                    {'seriesName': {'type': 'literal', 'value': 'Cougar Town'}}
                ]
            }
        }
        d_2 = {
            'head': {'vars': ['first', 'last', 'workTel']},
            'results': {
                'bindings': [{
                    'first': {'type': 'literal', 'value': 'Craig'},
                    'last': {'type': 'literal', 'value': 'Ellis'},
                    'workTel': {'type': 'literal', 'value': '(245) 315-5486'}
                }]
            }
        }
        self.assertEqual(
            engine.select(q='queries/select/testSelect.sparql'), d_1
        )
        self.assertEqual(
            engine.select(q='queries/select/ex055.rq', l='ex054.ttl'), d_2
        )


if __name__ == '__main__':
    engine = sa.SparqlAnything()
    unittest.main(verbosity=2)
