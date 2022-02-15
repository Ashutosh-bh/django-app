from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.
from account.models import User, Address
from util.models import TimeStampedModel


class Restaurant(TimeStampedModel):

    name = models.CharField(max_length=50, null=False)
    type = models.CharField(max_length=50, null=False)
    address = models.ForeignKey(Address, null=False, on_delete=models.CASCADE, related_name='rest_address', blank=False)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='rest_user', blank=False)


class MenuCategory(TimeStampedModel):

    restaurant = models.ForeignKey(Restaurant, null=False, on_delete=models.CASCADE, related_name='restaurant')
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=200)
    is_available = models.BooleanField(default=True)


class MenuSubCategory(TimeStampedModel):

    category = models.ForeignKey(MenuCategory, null=False, on_delete=models.CASCADE, related_name='menu_category',
                                 blank=False)
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=200)
    is_available = models.BooleanField(default=True)


class MenuItem(TimeStampedModel):

    sub_category = models.ForeignKey(MenuSubCategory, null=False, on_delete=models.CASCADE,
                                     related_name='menu_sub_category')
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=200)
    images = ArrayField(models.CharField(max_length=500), null=False)
    is_available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0, null=False)
    variations = models.JSONField(null=True)
    add_ons = models.JSONField(null=True)
