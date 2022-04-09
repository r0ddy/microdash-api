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


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [ 'id', 'name', 'price']


class EateryItemsSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)
    class Meta:
        model = Eatery
        fields = [ 'id', 'name', 'items']

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class FullMenuSerializer(serializers.ModelSerializer):
    menus = MenuSerializer(many=True)
    class Meta:
        model = FullMenu
        fields = '__all__'
