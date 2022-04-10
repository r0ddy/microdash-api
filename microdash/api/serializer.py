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


class EateryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eatery
        fields = [ 'id', 'name', 'photo_url' ]


class ItemSerializer(serializers.ModelSerializer):
    eatery = EateryNameSerializer()
    class Meta:
        model = Item
        fields = [ 
            'id',
            'name',
            'price',
            'eatery',
            'photo_url',
            'description',
            'ubereats_price',
            'doordash_price',
        ]


class EateryItemsSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)
    class Meta:
        model = Eatery
        fields = [ 'id', 'name', 'items' ]


class MenuSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    class Meta:
        model = Menu
        fields = [ 'id', 'day', 'meal_period', 'meal_period_str', 'item', ]


class FullMenuSerializer(serializers.ModelSerializer):
    menus = MenuSerializer(many=True)
    class Meta:
        model = FullMenu
        fields = [ 'name', 'menus', 'total']


class DeliveryAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAgent
        fields = [ 'id', 'name', 'rating' ]


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [ 'id', 'name', 'rating' ]

class CustomerOrderSerializer(serializers.ModelSerializer):
    deliveryAgent = DeliveryAgent()
    item = ItemSerializer()
    class Meta:
        model = Order
        fields = [ 'id', 'item', 'expectedArrival', 'deliveryAgent']

class DeliveryAgentOrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    class Meta:
        model = Order
        fields = [ 'id', 'item', 'customer', 'destination', 'origin']

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = '__all__'