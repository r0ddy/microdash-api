from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from ..models import CentralHub
from ..serializer import CentralHubSerializer

class GetEateriesByCentralHubs(APIView):
    queryset = CentralHub.objects.all()
    def get(self, request):
        eateries = [
            CentralHubSerializer(ch).data for ch in CentralHub.objects.all()
        ]
        return Response(eateries, status=status.HTTP_200_OK)
