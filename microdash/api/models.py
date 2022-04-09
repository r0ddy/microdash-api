from distutils.command.upload import upload
from email.policy import default
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
    photo = models.ImageField(default='', upload_to="eatery_photos/", null=True, blank=True)
    address = AddressField()

    def __str__(self):
        return self.name

    def photo_url(self):
        return self.photo.url if self.photo else ""


class Item(models.Model):
    name = models.CharField(max_length=200)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    eatery = models.ForeignKey(Eatery, related_name='items', on_delete=models.CASCADE)
    photo = models.ImageField(default='', upload_to="item_photos/", null=True, blank=True)
    description = models.CharField(max_length=500)
    ubereats_price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    doordash_price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')

    def __str__(self):
        return "%s: %s" % (self.eatery.name, self.name)

    def photo_url(self):
        return self.photo.url if self.photo else ""


class Menu(models.Model):
    MEAL_PERIODS = [
        (1, 'Breakfast'),
        (2, 'Lunch'),
        (3, 'Dinner'),
    ]
    day = DayOfTheWeekField()
    meal_period = models.IntegerField(choices=MEAL_PERIODS, default=None, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s %s" % (self.day, self.meal_period, self.item.name)
    
    def meal_period_str(self):
        return self.MEAL_PERIODS[self.meal_period-1][1]
    
    def day_str(self):
        return DAY_OF_THE_WEEK[self.day]


class FullMenu(models.Model):
    name = models.CharField(max_length=200)
    menus = models.ManyToManyField(Menu)

    def __str__(self):
        return "%s" % (self.name)
