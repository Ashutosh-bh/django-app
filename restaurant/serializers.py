from rest_framework import serializers

from restaurant.models import MenuCategory, MenuSubCategory, MenuItem, Restaurant


class RestaurantMenuSerializer(serializers.ModelSerializer):
    menu_categories = serializers.SerializerMethodField()
    restaurant_id = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        exclude = ('is_deleted', )

    def get_menu_categories(self, obj):
        return MenuSerializer(MenuCategory.objects.filter(restaurant_id=obj.id, is_deleted=False), many=True).data

    def get_restaurant_id(self, obj):
        return obj.id


class MenuSerializer(serializers.ModelSerializer):
    category_id = serializers.SerializerMethodField()
    sub_categories = serializers.SerializerMethodField()

    class Meta:
        model = MenuCategory
        exclude = ('is_deleted', 'id')

    def get_sub_categories(self, obj):
        return SubCategorySerializer(MenuSubCategory.objects.filter(category_id=obj.id, is_deleted=False),
                                     many=True).data

    def get_category_id(self, obj):
        return obj.id


class SubCategorySerializer(serializers.ModelSerializer):
    sub_category_id = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    class Meta:
        model = MenuSubCategory
        exclude = ('is_deleted', 'id')

    def get_items(self, obj):
        return ItemSerializers(MenuItem.objects.filter(sub_category_id=obj.id, is_deleted=False), many=True).data

    def get_sub_category_id(self, obj):
        return obj.id


class ItemSerializers(serializers.ModelSerializer):
    item_id = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        exclude = ('is_deleted', 'id')

    def get_item_id(self, obj):
        return obj.id
