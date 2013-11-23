from django.test import TestCase
from django.test.client import Client

from tests.fixtures.factory import create, delete_all


class RankingServiceRetrieveTest(TestCase):

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
        response = Client().get('/rankings/?limit=2&metric=mid1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '[["uid2", "mid1", 2.5], ["uid3", "mid1", 1]]')


class RankingServiceUpdateTest(TestCase):

    @classmethod
    def setUpClass(cls):
        delete_all('score')

    @classmethod
    def tearDownClass(cls):
        delete_all('score')

    def test_should_return_success_created(self):
        response = Client().post('/rankings/', {'username': 'uid1', 'metric': 'mid1', 'value': 1.5})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'score created')

    def test_should_return_success_updated(self):
        create('score', username='uid1', metric='mid1', value=1.5)
        response = Client().post('/rankings/', {'username': 'uid1', 'metric': 'mid1', 'value': 2.5})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'score updated')


class RankingServiceSanityTest(TestCase):

    @classmethod
    def setUpClass(cls):
        delete_all('score')

    @classmethod
    def tearDownClass(cls):
        delete_all('score')

    def test_should_retrieve_the_highest_updated_score_for_given_metric(self):
        Client().post('/rankings/', {'username': 'uid1', 'metric': 'mid1', 'value': 1.5})
        Client().post('/rankings/', {'username': 'uid2', 'metric': 'mid1', 'value': 2})
        Client().post('/rankings/', {'username': 'uid1', 'metric': 'mid1', 'value': 3.5})
        Client().post('/rankings/', {'username': 'uid3', 'metric': 'mid2', 'value': 10})

        response = Client().get('/rankings/?limit=1&metric=mid1')

        self.assertEqual(response.content, '[["uid1", "mid1", 3.5]]')
