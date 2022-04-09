from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from ..serializer import FullMenuSerializer
from ..models import FullMenu


class GetFullMenus(APIView):
    queryset = FullMenu.objects.all()
    def get(self, request):
        fullmenus = [
            FullMenuSerializer(fm).data for fm in FullMenu.objects.all()
        ]
        return Response(fullmenus, status=status.HTTP_200_OK)