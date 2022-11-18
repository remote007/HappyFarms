from django.db import models

class City(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self): #show the actual city name on the dashboard
        return self.name

    class Meta: #show the plural of city as cities instead of citys
        verbose_name_plural = 'cities'

class CityDetails(models.Model):
    name = models.CharField(max_length=25)
    lat = models.FloatField()
    long = models.FloatField()

    def __str__(self):
        return self.name

class ComponentsData(models.Model):
    city = models.CharField(max_length=25)
    date = models.DateTimeField()
    co = models.FloatField()
    no = models.FloatField()
    no2 = models.FloatField()
    o3 = models.FloatField()
    so2 = models.FloatField()
    pm2_5 = models.FloatField()
    pm10 = models.FloatField()
    nh3 = models.FloatField()

    class Meta:
        unique_together = ('city', 'date',)