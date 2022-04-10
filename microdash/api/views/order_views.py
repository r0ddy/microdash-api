import googlemaps
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ..serializer import BatchSerializer, CustomerOrderSerializer, DeliveryAgentOrderSerializer
from ..models import Batch, DeliveryAgent, Order, Customer, Item
import random
import string
from datetime import date, datetime, timedelta

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class GetOrdersAsCustomer(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    queryset = Order.objects.all()

    def get(self, request):
        customer = Customer.objects.get(user__pk=request.user.pk)
        orders = [CustomerOrderSerializer(order).data for order in customer.orders.all()]
        return Response(orders, status=status.HTTP_200_OK)


class GetOrdersAsDeliveryAgent(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    queryset = Order.objects.all()

    def get(self, request):
        deliveryAgent = DeliveryAgent.objects.get(pk=request.user.pk)
        orders = [DeliveryAgentOrderSerializer(order).data for order in deliveryAgent.orders]
        return Response(orders, status=status.HTTP_200_OK)


def getAddressDictionary(geocoded_addr):
    addr_dict = {
        'raw': geocoded_addr['formatted_address'],
        'lat': geocoded_addr['geometry']['location']['lat'],
        'lng': geocoded_addr['geometry']['location']['lng']
    }
    for addr_comp in geocoded_addr['address_components']:
        for addr_comp_type in addr_comp['types']:
            if addr_comp_type in ['street_number', 'route', 'locality', 'postal_code']:
                addr_dict[addr_comp_type] = addr_comp['short_name']
                break
            elif addr_comp_type == 'administrative_area_level_1':
                addr_dict['state'] = addr_comp['long_name']
                addr_dict['state_code'] = addr_comp['short_name']
                break
            elif addr_comp_type == 'country':
                addr_dict['country'] = addr_comp['long_name']
                addr_dict['country_code'] = addr_comp['short_name']
                break
    return addr_dict

class CreateOrder(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    queryset = Order.objects.all()
    def post(self, request):
        customer = Customer.objects.get(user__pk=request.user.pk)
        item = Item.objects.get(pk=request.data['item_id'])
        gmaps = googlemaps.Client(key='AIzaSyBbw-o73PjRI5SJAj9gPVB3dxEriBVCOE0')
        geocode_results = gmaps.geocode(request.data['destination'])
        batch = Batch.objects.filter(centralHub__pk=item.eatery.centralHub.pk, deliveryAgent=None).first()
        if batch is None:
            batch = Batch(centralHub=item.eatery.centralHub)
            batch.save()
        order = Order(
            customer=customer,
            code=id_generator(),
            destination=getAddressDictionary(geocode_results[0]),
            item=item,
            expectedArrival=datetime.now() + timedelta(minutes=15),
            batch=batch
        )
        order.save()
        return Response(CustomerOrderSerializer(order).data, status=status.HTTP_201_CREATED)

class DeliverBatch(APIView): 
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    def post(self, request):
        time_threshold = datetime.now() - timedelta(minutes=5)
        batches = Batch.objects.filter(createdAt__lt=time_threshold, deliveryAgent=None)
        for batch in batches:
            batch.deliveryAgent = random.choice(DeliveryAgent.objects.all())
            batch.save()
        return Response(BatchSerializer(batches, many=True).data, status=status.HTTP_200_OK)