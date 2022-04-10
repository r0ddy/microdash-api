from django.urls import path

from .views.order_views import GetOrdersAsCustomer, GetOrdersAsDeliveryAgent
from .views.full_menu_views import GetFullMenus
from .views.eatery_views import GetEateriesByCentralHubs, GetEateryItems
from .views.user_views import RegisterNameAndRole

urlpatterns = [
    path('eateries/', GetEateriesByCentralHubs.as_view()),
    path('eateries/<int:pk>', GetEateryItems.as_view()),
    path('user/register', RegisterNameAndRole.as_view()),
    path('menus/', GetFullMenus.as_view()),
    path('orders/customer', GetOrdersAsCustomer.as_view()),
    path('orders/delivery_agent', GetOrdersAsDeliveryAgent.as_view())
]
