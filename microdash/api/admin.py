from csv import list_dialects
from django.contrib import admin
from address.models import AddressField
from address.forms import AddressWidget
from .models import CentralHub, Eatery

# admin.site.register(CentralHub)

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

