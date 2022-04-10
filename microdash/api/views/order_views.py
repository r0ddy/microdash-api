import googlemaps
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, time
from ..serializer import BatchSerializer, CustomerOrderSerializer, DeliveryAgentOrderSerializer
from ..models import Batch, DeliveryAgent, MealPlan, OrderInvoice, Order, Customer, Item, Menu
from django.conf import settings
import random
import string
from datetime import datetime, timedelta
import decimal

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

def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

# class CreateMealPlanOrders(APIView):
#     authentication_classes = [TokenAuthentication, ]
#     permission_classes = [IsAuthenticated, ]
#     queryset = Order.objects.all()
#     def post(self, request):
#         day = str(datetime.today().weekday() + 1)
#         period = None
#         if is_time_between(time(7,00), time(9,00)):
#             period = 1
#         elif is_time_between(time(12,00), time(2,00)):
#             period = 2
#         elif is_time_between(time(5,00), time(7,00)):
#             period = 3
#         todays_menus = Menu.objects.filter(day=day, meal_period=period)
        


def get_addr_dict(destination):
    gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
    geocoded_addr = gmaps.geocode(destination)[0]
    addr_dict = {
        'raw': geocoded_addr['formatted_address'],
        'latitude': geocoded_addr['geometry']['location']['lat'],
        'longitude': geocoded_addr['geometry']['location']['lng']
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

def estimate_travel_time(origin, dest):
    gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
    res = gmaps.distance_matrix([origin], [dest])
    time_seconds = res['rows'][0]['elements'][0]['duration']['value']
    return timedelta(seconds=time_seconds)

def estimate_distance(origin, dest):
    gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
    res = gmaps.distance_matrix([origin], [dest])
    dist_meters = res['rows'][0]['elements'][0]['distance']['value']
    return dist_meters * 0.000621371 # meters to miles

DEFAULT_PICKUP_LOCATION = '343 Campus Rd, Ithaca, NY 14853'
AVERAGE_MILES_PER_GALLON = 24.9
AVERAGE_PRICE_OF_GALLON = 4.12

class CreateOrder(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    queryset = Order.objects.all()
    def post(self, request):
        customer = Customer.objects.get(user__pk=request.user.pk)
        item = Item.objects.get(pk=request.data['item_id'])
        batch = Batch.objects.filter(centralHub__pk=item.eatery.centralHub.pk, deliveryAgent=None).first()
        if batch is None:
            batch = Batch(centralHub=item.eatery.centralHub)
            batch.save()
        dest_dict = None
        if request.data['destination']:
            dest_dict = get_addr_dict(request.data['destination'])
        else:
            dest_dict = get_addr_dict(DEFAULT_PICKUP_LOCATION)
        travel_time = estimate_travel_time(item.eatery.centralHub.address.raw, request.data['destination'])
        order = Order(
            customer=customer,
            code=id_generator(),
            destination=dest_dict,
            item=item,
            expectedArrival=datetime.now() + timedelta(minutes=7) + travel_time,
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
            dist_miles = estimate_distance(batch.centralHub.address.raw, DEFAULT_PICKUP_LOCATION)
            fuel_cost = decimal.Decimal(dist_miles * AVERAGE_MILES_PER_GALLON * AVERAGE_PRICE_OF_GALLON)
            ordersToInvoice = [order for order in batch.orders.all() if not order.isPartOfMealPlan]
            totalCost = sum([order.item.price for order in ordersToInvoice])
            for order in ordersToInvoice:
                deliveryFee = fuel_cost * order.item.price / totalCost + decimal.Decimal(0.05)
                newInvoice = OrderInvoice(order=order, deliveryFee=deliveryFee, serviceFee=deliveryFee)
                newInvoice.save()
            batch.deliveryAgent = random.choice(DeliveryAgent.objects.all())
            batch.save()
        return Response(BatchSerializer(batches, many=True).data, status=status.HTTP_200_OK)