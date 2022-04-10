from csv import list_dialects
from django.contrib import admin
from address.models import AddressField
from address.forms import AddressWidget
from .models import (
    Batch,
    CentralHub,
    Customer,
    DeliveryAgent,
    Eatery,
    FullMenu,
    Item,
    Menu,
    Order,
    OrderInvoice
)

@admin.register(CentralHub)
class CentralHubAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "address",
    )

    formfield_overrides = {AddressField: {"widget": AddressWidget(attrs={"style": "width: 300px;"})}}


@admin.register(Eatery)
class EateryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "address",
        "centralHub",
    )

    formfield_overrides = {AddressField: {"widget": AddressWidget(attrs={"style": "width: 300px;"})}}


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price"
    )


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "day",
        "meal_period",
        "item",
    )


@admin.register(FullMenu)
class FullMenuAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )

admin.site.register(Customer)
admin.site.register(DeliveryAgent)
admin.site.register(Order)
admin.site.register(Batch)
admin.site.register(OrderInvoice)