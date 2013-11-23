from django.test import TestCase
from django.http import HttpRequest, QueryDict

from rankings.views import is_valid_retrieve_request


class IsValidRetrieveRequestTest(TestCase):

    def test_should_reject_post_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST = QueryDict('metric=mid1')

        check = is_valid_retrieve_request(request)

        self.assertFalse(check)

    def _valid_with_parameter(self, parameter):
        request = HttpRequest()
        request.method = 'GET'
        request.GET = QueryDict(parameter)

        return is_valid_retrieve_request(request)

    def test_should_allow_metric_parameter(self):
        self.assertTrue(self._valid_with_parameter('metric=mid1'))

    def test_should_allow_username_parameter(self):
        self.assertTrue(self._valid_with_parameter('username=uid1'))

    def test_should_allow_limit_parameter(self):
        self.assertTrue(self._valid_with_parameter('limit=3'))

    def test_should_not_allow_noninteger_limit_parameter(self):
        self.assertFalse(self._valid_with_parameter('limit=bla'))

    def test_should_check_for_unsupported_parameters(self):
        self.assertFalse(self._valid_with_parameter('metric=mid1&unsupported=param'))
