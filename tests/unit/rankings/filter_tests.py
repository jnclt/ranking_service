from django.test import TestCase

from mock import patch, call

from rankings.models import Score


@patch('rankings.models.Score.objects.filter')
class ScoreFilterTest(TestCase):

    def test_should_call_filter(self, mock_filter):
        mock_key = {'metric': 'mid1', 'username': 'uid1'}

        Score.filter(limit=5, **mock_key)

        self.assertEqual(mock_filter.call_args, call(metric='mid1', username='uid1'))
