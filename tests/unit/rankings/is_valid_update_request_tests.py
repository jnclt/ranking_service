from django.test import TestCase
from django.http import HttpRequest, QueryDict

from rankings.views import is_valid_update_request


class IsValidUpdateRequestTest(TestCase):

    def test_should_reject_get_request(self):
        request = HttpRequest()
        request.method = 'GET'
        request.POST = QueryDict('username=uid1&metric=mid1&value=1.0')

        check = is_valid_update_request(request)

        self.assertFalse(check)

    def _valid_with_parameters(self, parameters):
        request = HttpRequest()
        request.method = 'POST'
        request.POST = QueryDict(parameters)

        return is_valid_update_request(request)

    def test_should_allow_valid_request(self):
        self.assertTrue(self._valid_with_parameters('username=uid1&metric=mid1&value=1.0'))

    def test_should_not_allow_missing_metric_parameter(self):
        self.assertFalse(self._valid_with_parameters('username=uid1&value=1.0'))

    def test_should_not_allow_missing_username_parameter(self):
        self.assertFalse(self._valid_with_parameters('metric=mid1&value=1.0'))

    def test_should_not_allow_missing_value_parameter(self):
        self.assertFalse(self._valid_with_parameters('username=uid1&metric=mid1'))

    def test_should_not_allow_nondecimal_value_parameter(self):
        self.assertFalse(self._valid_with_parameters('username=uid1&metric=mid1&value=bla'))

    def test_should_not_allow_unsupported_parameters(self):
        self.assertFalse(self._valid_with_parameters('username=uid1&metric=mid1&value=1.0&unsupported=param'))
