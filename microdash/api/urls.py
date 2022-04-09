from re import I
from django.urls import path

from .views.central_hub_views import CreateCentralHub

urlpatterns = [
    path('central_hub/', CreateCentralHub.as_view(), name='create central hub'),
]
