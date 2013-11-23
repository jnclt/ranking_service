from django.test import TestCase
from django.http import HttpRequest, HttpResponseBadRequest, QueryDict

from mock import patch, call

from rankings.views import handle_update


@patch('rankings.views.is_valid_update_request')
class HandleUpdateTest(TestCase):

    def test_should_call_is_valid_update_request(self, mock_request_check):
        mock_request = HttpRequest()
        mock_request_check.return_value = False

        handle_update(mock_request)

        self.assertEqual(mock_request_check.call_args, call(mock_request))

    def test_should_return_bad_request_when_invalid_update_request(self, mock_request_check):
        mock_request = HttpRequest()
        mock_request_check.return_value = False

        response = handle_update(mock_request)

        self.assertIsInstance(response, HttpResponseBadRequest)

    @patch('rankings.models.Score.update_or_create')
    def test_should_call_score_update_or_create(self, mock_update_or_create_score, mock_request_check):
        mock_request = HttpRequest()
        mock_request.POST = QueryDict('username=uid1&metric=mid1&value=1.0')
        mock_request_check.return_value = True

        handle_update(mock_request)

        self.assertEqual(mock_update_or_create_score.call_args, call(username='uid1',
                                                                     metric='mid1',
                                                                     value='1.0'))

    @patch('rankings.models.Score.update_or_create')
    def test_should_return_score_created_if_created(self, mock_update_or_create_score, mock_request_check):
        mock_request = HttpRequest()
        mock_request.POST = QueryDict('username=uid1&metric=mid1&value=1.0')
        mock_request_check.return_value = True
        mock_update_or_create_score.return_value = True

        response = handle_update(mock_request)

        self.assertEqual(response.content, 'score created')

    @patch('rankings.models.Score.update_or_create')
    def test_should_return_score_updated_if_updated(self, mock_update_or_create_score, mock_request_check):
        mock_request = HttpRequest()
        mock_request.POST = QueryDict('username=uid1&metric=mid1&value=1.0')
        mock_request_check.return_value = True
        mock_update_or_create_score.return_value = False

        response = handle_update(mock_request)

        self.assertEqual(response.content, 'score updated')
