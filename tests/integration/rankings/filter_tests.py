from decimal import Decimal
from django.test import TestCase

from tests.fixtures.factory import create, delete_all, MODEL


class ScoreFilterTest(TestCase):

    @classmethod
    def setUpClass(cls):
        delete_all('score')
        create('score', username='uid1', metric='mid1', value=0.0)
        create('score', username='uid1', metric='mid2', value=3.0)
        create('score', username='uid2', metric='mid1', value=2.0)
        create('score', username='uid3', metric='mid1', value=1.0)

    @classmethod
    def tearDownClass(cls):
        delete_all('score')

    def test_should_return_filtered_ordered_limited_queryset_for_positive_limit(self):
        expected_list = [('uid2', 'mid1', Decimal('2')),
                         ('uid3', 'mid1', Decimal('1'))]
        actual_list = list(MODEL['score'].filter(limit=2, metric='mid1').values_list('username', 'metric', 'value'))

        self.assertEqual(actual_list, expected_list)

    def test_should_return_filtered_ordered_queryset_for_zero_limit(self):
        expected_list = [('uid2', 'mid1', Decimal('2')),
                         ('uid3', 'mid1', Decimal('1')),
                         ('uid1', 'mid1', Decimal('0'))]
        actual_list = list(MODEL['score'].filter(limit=0, metric='mid1').values_list('username', 'metric', 'value'))

        self.assertEqual(actual_list, expected_list)
