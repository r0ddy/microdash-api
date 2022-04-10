from django.db import models
from address.models import AddressField
from djmoney.models.fields import MoneyField
from django.contrib.auth import get_user_model

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


class Customer(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    firstName = models.CharField(max_length=20, default='Tommy')
    lastName = models.CharField(max_length=20, default='Banana')

    def name(self):
        return "%s %s." % (self.firstName, self.lastName[0])

    def __str__(self):
        return self.name()


class DeliveryAgent(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=2, default=5.00)
    firstName = models.CharField(max_length=20, default='Bobby')
    lastName = models.CharField(max_length=20, default='Apples')

    def name(self):
        return "%s %s." % (self.firstName, self.lastName[0])



class Batch(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    centralHub = models.ForeignKey(CentralHub, on_delete=models.CASCADE, blank=True, null=True)
    deliveryAgent = models.ForeignKey(DeliveryAgent, related_name='orders', on_delete=models.CASCADE, blank=True, null=True)


class Order(models.Model):
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)
    isPaid = models.BooleanField(default=False)
    isDelivered = models.BooleanField(default=False)
    isReceived = models.BooleanField(default=False)
    code = models.CharField(max_length=6)
    # can be general pickup or direct location of customer
    destination = AddressField()
    # contains the item price and origin
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    # if this is is part of a meal plan then the item is free
    isPartOfMealPlan = models.BooleanField(default=False)
    # if the user is not using pickup location, then charge more
    usingPickupLocation = models.BooleanField(default=True)
    expectedArrival = models.DateTimeField()
    batch = models.ForeignKey(Batch, related_name='orders', on_delete=models.CASCADE)

    def origin(self):
        return self.item.eatery


class Invoice(models.Model):
    order = models.ForeignKey(Order, related_name='invoice', on_delete=models.CASCADE)

