from django.test import TestCase

from mock import Mock, patch, call

from rankings.models import Score


@patch('rankings.models.Score.objects.get_or_create')
class ScoreUpdateOrCreateTest(TestCase):

    def test_should_call_get_or_create(self, mock_get_or_create):
        mock_get_or_create.return_value = (Mock(), True)
        Score.update_or_create(value=1.0, username='uid1', metric='mid1')

        self.assertEqual(mock_get_or_create.call_args, call(defaults={'value': 1.0}, username='uid1', metric='mid1'))

    def test_should_return_true_if_created(self, mock_get_or_create):
        mock_get_or_create.return_value = (Mock(), True)

        created = Score.update_or_create(value=1.0, username='uid1', metric='mid1')

        self.assertEqual(created, True)

    def test_should_return_false_if_updated(self, mock_get_or_create):
        mock_get_or_create.return_value = (Mock(), False)

        created = Score.update_or_create(value=1.0, username='uid1', metric='mid1')

        self.assertEqual(created, False)
