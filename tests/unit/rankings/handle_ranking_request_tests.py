from django.test import TestCase
from django.http import HttpRequest
from django.http import HttpResponseNotAllowed

from mock import patch, call

from rankings.views import handle_ranking_request


class HandleRankingRequestTest(TestCase):

    def test_should_not_accept_delete_request(self):
        mock_request = HttpRequest()
        mock_request.method = 'DELETE'

        actual_response = handle_ranking_request(mock_request)

        self.assertIsInstance(actual_response, HttpResponseNotAllowed)

    @patch('rankings.views.handle_update')
    def test_should_dispatch_post_request_to_update(self, mock_update):
        update_result = 'update result'
        mock_update.return_value = update_result
        mock_request = HttpRequest()
        mock_request.method = 'POST'

        actualResponse = handle_ranking_request(mock_request)

        self.assertEqual(mock_update.call_args, call(mock_request))
        self.assertEqual(update_result, actualResponse)

    @patch('rankings.views.retrieve_ranking')
    def test_should_dispatch_get_request_to_retrieve(self, mock_retrieve):
        retrieve_result = 'retrieve result'
        mock_retrieve.return_value = retrieve_result
        mock_request = HttpRequest()
        mock_request.method = 'GET'

        actualResponse = handle_ranking_request(mock_request)

        self.assertEqual(mock_retrieve.call_args, call(mock_request))
        self.assertEqual(retrieve_result, actualResponse)
