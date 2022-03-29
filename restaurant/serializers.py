from rest_framework import serializers

from account.models import Address, User
from account.serializers import AddressSerializer
from restaurant.models import MenuCategory, MenuSubCategory, MenuItem, Restaurant


class RestaurantSerializer(serializers.ModelSerializer):

    address = serializers.SerializerMethodField()
    dist = serializers.FloatField(required=False)

    class Meta:
        model = Restaurant
        exclude = ('is_deleted', 'lat', 'lon')

    @staticmethod
    def get_address(obj):
        return AddressSerializer(Address.objects.filter(id=obj.address_id, is_deleted=False).all(), many=True).data


class RestaurantMenuSerializer(serializers.ModelSerializer):
    menu_categories = serializers.SerializerMethodField()
    restaurant_id = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        exclude = ('is_deleted', )

    @staticmethod
    def get_menu_categories(obj):
        return MenuSerializer(MenuCategory.objects.filter(restaurant_id=obj.id, is_deleted=False), many=True).data

    @staticmethod
    def get_restaurant_id(obj):
        return obj.id

    @staticmethod
    def get_address(obj):
        return AddressSerializer(Address.objects.filter(id=obj.address_id, is_deleted=False).first()).data


class MenuSerializer(serializers.ModelSerializer):
    category_id = serializers.SerializerMethodField()
    sub_categories = serializers.SerializerMethodField()

    class Meta:
        model = MenuCategory
        exclude = ('is_deleted', 'id')

    @staticmethod
    def get_sub_categories(obj):
        return SubCategorySerializer(MenuSubCategory.objects.filter(category_id=obj.id, is_deleted=False),
                                     many=True).data

    @staticmethod
    def get_category_id(obj):
        return obj.id


class SubCategorySerializer(serializers.ModelSerializer):
    sub_category_id = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    class Meta:
        model = MenuSubCategory
        exclude = ('is_deleted', 'id')

    @staticmethod
    def get_items(obj):
        return ItemSerializers(MenuItem.objects.filter(sub_category_id=obj.id, is_deleted=False), many=True).data

    @staticmethod
    def get_sub_category_id(obj):
        return obj.id


class ItemSerializers(serializers.ModelSerializer):
    item_id = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        exclude = ('is_deleted', 'id')

    @staticmethod
    def get_item_id(obj):
        return obj.id
