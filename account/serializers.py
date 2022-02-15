from rest_framework import serializers

from account.models import Address


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        exclude = ('is_deleted', 'created_on', 'updated_on', 'id')
