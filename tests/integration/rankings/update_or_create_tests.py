from django.test import TestCase

from tests.fixtures.factory import create, delete_all, MODEL


class ScoreUpdateOrCreateTest(TestCase):

    @classmethod
    def setUpClass(cls):
        delete_all('score')

    @classmethod
    def tearDownClass(cls):
        delete_all('score')

    def test_should_create_score(self):
        MODEL['score'].update_or_create(username='uid1', metric='mid1', value=1.5)
        scores = MODEL['score'].objects.all()

        self.assertEqual(len(scores), 1)
        score = scores[0]
        self.assertEqual(score.value, 1.5)
        self.assertEqual(score.username, 'uid1')
        self.assertEqual(score.metric, 'mid1')

    def test_should_update_score(self):
        create('score', username='uid1', metric='mid1', value=1.5)

        MODEL['score'].update_or_create(username='uid1', metric='mid1', value=2.5)
        scores = MODEL['score'].objects.all()

        self.assertEqual(len(scores), 1)
        score = scores[0]
        self.assertEqual(score.value, 2.5)
        self.assertEqual(score.username, 'uid1')
        self.assertEqual(score.metric, 'mid1')
