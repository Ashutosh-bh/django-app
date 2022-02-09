from rest_framework import generics

from restaurant.models import Restaurant, MenuCategory, MenuSubCategory, MenuItem
from restaurant.serializers import RestaurantMenuSerializer, RestaurantSerializer
from util.common import send_response


class GetMenuView(generics.ListAPIView):
    serializer_class = RestaurantMenuSerializer
    queryset = Restaurant.objects.filter(is_deleted=False).all()
    lookup_url_kwarg = 'id'

    def list(self, request, *args, **kwargs):
        data = self.serializer_class(self.get_object()).data
        print(data)
        return send_response(response_code=200, data=data, message='success', error=None)


class SaveRestaurantView(generics.CreateAPIView):
    serializer_class = RestaurantSerializer

    def create(self, request, *args, **kwargs):
        print('request received to create restaurant is', request.data)
        restaurant = Restaurant(**request.data)
        restaurant.save()
        data = self.serializer_class(restaurant).data
        print('returning response', data)
        return send_response(response_code=201, data=data, message='success', error=None)


class GetAllRestaurantView(generics.ListAPIView):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.filter(is_deleted=False).all()

    def list(self, request, *args, **kwargs):
        print('request received to get all restaurant ')
        data = self.serializer_class(self.get_queryset(), many=True).data
        print('returning response', data)
        return send_response(response_code=200, data=data, message='success', error=None)


class SaveMenuView(generics.CreateAPIView):
    serializer_class = RestaurantMenuSerializer
    queryset = Restaurant.objects.filter(is_deleted=False).all()
    lookup_url_kwarg = 'id'

    def create(self, request, *args, **kwargs):
        print('request received to add menu to restaurant ', kwargs['id'], 'with data', request.data)
        restaurant = self.get_object()
        for category in request.data['menu_categories']:
            sub_categories = category.pop('sub_categories')
            mc = MenuCategory(**category, restaurant_id=restaurant.id)
            mc.save()
            for sub_category in sub_categories:
                items = sub_category.pop('items')
                sc = MenuSubCategory(**sub_category, category_id=mc.id)
                sc.save()
                for item in items:
                    mi = MenuItem(**item, sub_category_id=sc.id)
                    mi.save()
        print('menu saved')
        data = self.serializer_class(restaurant).data
        return send_response(response_code=201, data=data, message='success', error=None)
