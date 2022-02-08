from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.
from util.models import TimeStampedModel


class Restaurant(TimeStampedModel):

    name = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=50, unique=True)
    address_line = models.CharField(max_length=200, unique=True)
    lat = models.DecimalField(max_digits=8, decimal_places=6, default=0)
    lon = models.DecimalField(max_digits=9, decimal_places=6, default=0)


class MenuCategory(TimeStampedModel):

    restaurant = models.ForeignKey(Restaurant, null=False, on_delete=models.CASCADE, related_name='restaurant')
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, unique=True)
    is_available = models.BooleanField(default=True)


class MenuSubCategory(TimeStampedModel):

    category = models.ForeignKey(MenuCategory, null=False, on_delete=models.CASCADE, related_name='menu_category',
                                 blank=False)
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, unique=True)
    is_available = models.BooleanField(default=True)


class MenuItem(TimeStampedModel):

    sub_category = models.ForeignKey(MenuSubCategory, null=False, on_delete=models.CASCADE,
                                     related_name='menu_sub_category')
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, unique=True)
    images = ArrayField(models.CharField(max_length=500))
    is_available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
