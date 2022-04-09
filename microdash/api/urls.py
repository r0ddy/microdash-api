from re import I
from django.urls import path
from .views.eatery_views import GetEateriesByCentralHubs

urlpatterns = [
    path('eateries/', GetEateriesByCentralHubs.as_view())
]
