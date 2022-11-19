from django.db import models


class City(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

    class Meta: 
        verbose_name_plural = 'cities'


class ComponentsData(models.Model):
    city = models.CharField(max_length=25)
    date = models.IntegerField()
    co = models.FloatField()
    no = models.FloatField()
    so2 = models.FloatField()
    nh3 = models.FloatField()

    class Meta:
        unique_together = ('city', 'date',)
