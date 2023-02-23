from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.PositiveBigIntegerField(blank=True,null=True)
    long = models.DecimalField(max_digits=9, decimal_places=6,blank=True,null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6,blank=True,null=True)
    