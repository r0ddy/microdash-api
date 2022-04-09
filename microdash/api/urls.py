from re import I
from django.urls import path

from .views.full_menu_views import GetFullMenus
from .views.eatery_views import GetEateriesByCentralHubs, GetEateryItems

urlpatterns = [
    path('eateries/', GetEateriesByCentralHubs.as_view()),
    path('eateries/<int:pk>', GetEateryItems.as_view()),
    path('menus/', GetFullMenus.as_view()),
]
