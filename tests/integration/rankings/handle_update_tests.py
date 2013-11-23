from django.test import TestCase
from django.http import HttpRequest, HttpResponseBadRequest, QueryDict

from tests.fixtures.factory import create, delete_all
from rankings.views import handle_update


class HandleUpdateTest(TestCase):

    @classmethod
    def setUpClass(cls):
        delete_all('score')

    @classmethod
    def tearDownClass(cls):
        delete_all('score')

    def test_should_return_response_with_success_create(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST = QueryDict('username=uid1&metric=mid1&value=1.5')

        response = handle_update(request)
        self.assertEqual(response.content, 'score created')

    def test_should_return_response_with_success_update(self):
        create('score', username='uid1', metric='mid1', value=1.5)

        request = HttpRequest()
        request.method = 'POST'
        request.POST = QueryDict('username=uid1&metric=mid1&value=2.5')

        response = handle_update(request)

        self.assertEqual(response.content, 'score updated')

    def test_should_return_bad_request_if_invalid_parameters(self):
        request = HttpRequest()
        request.method = 'POST'
        request.GET = QueryDict('invalid')

        response = handle_update(request)

        self.assertIsInstance(response, HttpResponseBadRequest)
