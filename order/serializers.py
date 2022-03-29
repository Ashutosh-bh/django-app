from rest_framework import serializers

from order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ('is_deleted',)
