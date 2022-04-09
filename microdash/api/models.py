from django.db import models
from django.contrib.auth.models import AbstractUser

class CentralHub(models.Model):
    name = models.CharField(max_length=200)


class Eatery(models.Model):
    name = models.CharField(max_length=200)
    placeId = models.CharField(max_length=30)
    centralHub = models.ForeignKey(CentralHub, related_name='eateries', on_delete=models.CASCADE)
