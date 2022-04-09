from rest_framework import serializers
from .models import *

class CentralHubSerializer(serializers.ModelSerializer):
    class Meta:
        model = CentralHub
        fields = '__all__'
