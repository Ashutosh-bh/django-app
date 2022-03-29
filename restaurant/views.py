from django.db.models import F, ExpressionWrapper, FloatField
from django.db.models.functions import Power, Cos
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from account.models import Address
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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        print('request received to create restaurant is', request.data)
        address = request.data.pop('address')
        add_obj = Address(**address, address_type=Address.RESTAURANT)
        add_obj.save()
        restaurant = Restaurant(**request.data, user_id=request.user.id, address_id=add_obj.id)
        restaurant.save()
        data = self.serializer_class(restaurant).data
        print('returning response', data)
        return send_response(response_code=201, data=data, message='success', error=None)


class GetAllRestaurantView(generics.ListAPIView):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        print('request received to get all restaurant ')
        query_set = self.add_filters(request)
        data = self.serializer_class(query_set.all(), many=True).data
        print('returning response', data)
        return send_response(response_code=200, data=data, message='success', error=None)

    def add_filters(self, request):
        queryset = self.get_queryset()
        print(request.GET)
        if 'loc' in request.GET:
            lat, lon = request.GET['loc'].split(',')
            queryset = queryset.annotate(dist=ExpressionWrapper(
                Power(69.1 * (float(lat) - F('lat')), 2) +
                Power(69.1 * (F('lon') - float(lon)) * Cos(float(lon) / 57.3), 2),
                output_field=FloatField())).filter(dist__lte=request.GET.get('dist', 5))
        if 'name' in request.GET:
            queryset = queryset.filter(name__icontains=request.GET['name'])
        queryset = queryset.filter(is_deleted=False)
        return queryset


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
