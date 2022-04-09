from django.db import models
from address.models import AddressField
from djmoney.models.fields import MoneyField

DAY_OF_THE_WEEK = {
    '1': 'Monday',
    '2': 'Tuesday',
    '3': 'Wednesday',
    '4': 'Thursday',
    '5': 'Friday',
    '6': 'Saturday', 
    '7': 'Sunday',
}

class DayOfTheWeekField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['choices']=tuple(sorted(DAY_OF_THE_WEEK.items()))
        kwargs['max_length']=1 
        super(DayOfTheWeekField,self).__init__(*args, **kwargs)


class CentralHub(models.Model):
    name = models.CharField(max_length=200)
    address = AddressField()

    def __str__(self):
       return self.name 

class Eatery(models.Model):
    name = models.CharField(max_length=200)
    centralHub = models.ForeignKey(CentralHub, related_name='eateries', on_delete=models.CASCADE)
    address = AddressField()

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=200)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    eatery = models.ForeignKey(Eatery, related_name='items', on_delete=models.CASCADE)


class Menu(models.Model):
    day = DayOfTheWeekField()
    time = models.TimeField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

