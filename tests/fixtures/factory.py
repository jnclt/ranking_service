from rankings.models import Score

"""
Factories for fixtures
"""
MODEL = {}
MODEL['score'] = Score


def create(object_name, **kwargs):
    return MODEL[object_name].objects.create(**kwargs)


def delete_all(object_name):
    MODEL[object_name].objects.all().delete()
