from django.test import TestCase
from django.http import HttpRequest, HttpResponseBadRequest, QueryDict

from tests.fixtures.factory import create, delete_all
from rankings.views import retrieve_ranking


class RetrieveRankingTest(TestCase):

    @classmethod
    def setUpClass(cls):
        delete_all('score')
        create('score', username='uid1', metric='mid1', value=0.0)
        create('score', username='uid1', metric='mid2', value=3.0)
        create('score', username='uid2', metric='mid1', value=2.5)
        create('score', username='uid3', metric='mid1', value=1.0)

    @classmethod
    def tearDownClass(cls):
        delete_all('score')

    def test_should_return_ranking_in_json_response(self):
        request = HttpRequest()
        request.method = 'GET'
        request.GET = QueryDict('limit=2&metric=mid1')

        response = retrieve_ranking(request)

        self.assertEqual(response.content, '[["uid2", "mid1", 2.5], ["uid3", "mid1", 1]]')

    def test_should_return_bad_request_if_invalid_parameters(self):
        request = HttpRequest()
        request.method = 'GET'
        request.GET = QueryDict('invalid')

        response = retrieve_ranking(request)

        self.assertIsInstance(response, HttpResponseBadRequest)

    def test_should_return_empty_list_in_json_response_if_no_match(self):
        request = HttpRequest()
        request.method = 'GET'
        request.GET = QueryDict('limit=2&metric=mid3')

        response = retrieve_ranking(request)

        self.assertEqual(response.content, '[]')
