from django.contrib.auth.models import User as BaseUser
from django.db import models

from util.models import TimeStampedModel


class User(BaseUser, TimeStampedModel):
    OWNER = 'owner'
    WORKER = 'worker'
    ADMIN = 'admin'

    USER_TYPE = (
        (OWNER, 'owner'),
        (WORKER, 'worker'),
        (ADMIN, 'admin')
    )

    mobile = models.CharField(max_length=10)
    type = models.CharField(max_length=10, default='owner', choices=USER_TYPE)


class Address(TimeStampedModel):
    PERMANENT = 'permanent'
    CURRENT = 'current'
    RESTAURANT = 'restaurant'

    ADDRESS_TYPE = (
        (PERMANENT, 'owner'),
        (CURRENT, 'worker'),
        (RESTAURANT, 'admin')
    )

    address_line_1 = models.CharField(max_length=300, null=False)
    address_line_2 = models.CharField(max_length=300)
    lat = models.DecimalField(max_digits=8, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    pin_code = models.DecimalField(max_digits=6, decimal_places=0, null=False)
    locality = models.CharField(max_length=50)
    landmark = models.CharField(max_length=100)
    city = models.CharField(max_length=50, null=False)
    state = models.CharField(max_length=50, null=False)
    address_type = models.CharField(max_length=100, null=False, default='permanent', choices=ADDRESS_TYPE)
    country = models.CharField(max_length=3, null=False, default='IN')


class UserAddressMapping(TimeStampedModel):

    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='user', blank=False)
    address = models.ForeignKey(Address, null=False, on_delete=models.CASCADE, related_name='address', blank=False)
