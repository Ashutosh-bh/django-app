from django.db import models

# Create your models here.
from account.models import User
from restaurant.models import Restaurant
from util.models import TimeStampedModel


class Order(TimeStampedModel):

    class Meta:
        db_table = "order"

    CREATED = 'created'
    CANCELLED = 'cancelled'
    PAID = 'paid'
    COMPLETED = 'completed'

    STATUS = (
        (CREATED, 'created'),
        (PAID, 'paid'),
        (CANCELLED, 'cancelled'),
        (COMPLETED, 'completed')
    )

    restaurant = models.ForeignKey(Restaurant, null=False, on_delete=models.CASCADE, related_name='order_retaurant')
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='order_user', blank=False)
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=100, null=False, choices=STATUS)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0, null=False)
    details = models.JSONField(null=False, default=dict)
