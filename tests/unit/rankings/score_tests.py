from django.test import TestCase
from django.db.models import fields

from rankings.models import Score


class ScoreModelTest(TestCase):

    def test_should_contain_decimal_value_field(self):
        value_field = Score._meta.get_field(name='value', many_to_many=False)
        self.assertIsInstance(value_field, fields.DecimalField)
