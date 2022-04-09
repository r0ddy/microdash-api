from rest_framework import serializers
from .models import *


class EaterySerializer(serializers.ModelSerializer):
    class Meta:
        model = Eatery
        fields = '__all__'


class CentralHubSerializer(serializers.ModelSerializer):
    eateries = EaterySerializer(many=True)
    class Meta:
        model = CentralHub
        fields = '__all__'
