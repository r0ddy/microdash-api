from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from ..models import CentralHub
from ..serializer import CentralHubSerializer

class CreateCentralHub(APIView):
    permission_classes = [IsAdminUser, ]

    def post(self, request, *args, **kwargs):
        ch = CentralHub.objects.create(name=request.data['name'])
        return Response(data=CentralHubSerializer(ch).data, status=status.HTTP_201_CREATED)
