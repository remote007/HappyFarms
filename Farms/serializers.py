from rest_framework import serializers
from .models import City, ComponentsData

class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ('pk', 'name')


class ComponentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ComponentsData
        fields = '__all__'
