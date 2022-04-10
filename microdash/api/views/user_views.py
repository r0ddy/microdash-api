from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..serializer import CustomerSerializer, DeliveryAgentSerializer
from ..models import Customer, DeliveryAgent

class RegisterNameAndRole(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    queryset = Customer.objects.all()
    def post(self, request):
        res = {}
        if request.data['is_customer']:
            customer = Customer(user=request.user, firstName=request.data['firstname'], lastName=request.data['lastname'])
            customer.save()
            res = CustomerSerializer(res).data
        else:
            da = DeliveryAgent(user=request.user, firstName=request.data['firstname'], lastName=request.data['lastname'])
            da.save()
            res = DeliveryAgentSerializer(da).data
        return Response(res, status=status.HTTP_201_CREATED)
