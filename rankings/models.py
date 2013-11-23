from django.db import models


class Key(models.Model):
    username = models.CharField(max_length=50)
    metric = models.CharField(max_length=50)

    class Meta:
        abstract = True


class Score(Key):
    value = models.DecimalField(max_digits=15, decimal_places=5)

    @classmethod
    def update_or_create(cls, value, **kwargs):
        score, created = cls.objects.get_or_create(defaults={'value': value}, **kwargs)
        if not created:
            score.value = value
            score.save()
        return created

    @classmethod
    def filter(cls, limit, **kwargs):
        ranking = cls.objects.filter(**kwargs).order_by('-value')
        if limit:
            ranking = ranking[:limit]
        return ranking
