from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from ..models import CentralHub, Eatery
from ..serializer import CentralHubSerializer, EateryItemsSerializer

class GetEateriesByCentralHubs(APIView):
    queryset = CentralHub.objects.all()
    def get(self, request):
        eateries = [
            CentralHubSerializer(ch).data for ch in CentralHub.objects.all()
        ]
        return Response(eateries, status=status.HTTP_200_OK)

class GetEateryItems(APIView):
    queryset = Eatery.objects.all()
    def get(self, request, **kwargs):
        eatery = Eatery.objects.get(pk=kwargs['pk'])
        return Response(EateryItemsSerializer(eatery).data, status=status.HTTP_200_OK)