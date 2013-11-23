from django.test import TestCase
from django.http import HttpRequest, HttpResponseBadRequest, QueryDict

from mock import Mock, patch, call
import simplejson as json

from rankings.views import retrieve_ranking


@patch('rankings.views.is_valid_retrieve_request')
class RetrieveRankingTest(TestCase):

    def test_should_call_is_valid_retrieve_request(self, mock_request_check):
        mock_request = HttpRequest()
        mock_request_check.return_value = False

        retrieve_ranking(mock_request)

        self.assertEqual(mock_request_check.call_args, call(mock_request))

    def test_should_return_bad_request_when_invalid_retrieve_request(self, mock_request_check):
        mock_request = HttpRequest()
        mock_request_check.return_value = False

        response = retrieve_ranking(mock_request)

        self.assertIsInstance(response, HttpResponseBadRequest)

    @patch('rankings.views.Score.filter')
    def test_should_call_scores_filter(self, mock_score_filter, mock_request_check):
        mock_request = HttpRequest()
        mock_request.GET = QueryDict('username=uid1&metric=mid1&limit=10')
        mock_request_check.return_value = True

        retrieve_ranking(mock_request)

        self.assertEqual(mock_score_filter.call_args, call(limit=10, username='uid1', metric='mid1'))

    @patch('rankings.views.Score.filter')
    def test_should_call_scores_filter_with_zero_limit_if_no_limit_in_request(self,
                                                                              mock_score_filter,
                                                                              mock_request_check):
        mock_request = HttpRequest()
        mock_request.GET = QueryDict('metric=mid1')
        mock_request_check.return_value = True

        retrieve_ranking(mock_request)

        self.assertEqual(mock_score_filter.call_args, call(limit=0, metric='mid1'))

    @patch('rankings.views.Score.filter')
    def test_should_return_json_with_filtered_scores(self,
                                                     mock_score_filter,
                                                     mock_request_check):
        mock_request = HttpRequest()
        mock_request.GET = QueryDict('limit=1&metric=mid1')
        mock_request_check.return_value = True
        mock_query_set = Mock(values_list=Mock(return_value=[('uid1', 1.0)]))
        mock_score_filter.return_value = mock_query_set

        response = retrieve_ranking(mock_request)
        content = json.loads(response.content)

        self.assertEqual(content, [['uid1', 1.0]])
