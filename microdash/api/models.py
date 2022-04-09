from django.db import models
from django.contrib.auth.models import AbstractUser
from address.models import AddressField

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