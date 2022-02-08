from rest_framework import generics

from restaurant.models import Restaurant
from restaurant.serializers import RestaurantMenuSerializer
from util.common import send_response


class GetMenuView(generics.ListAPIView):
    serializer_class = RestaurantMenuSerializer
    queryset = Restaurant.objects.filter(is_deleted=False).all()
    lookup_url_kwarg = 'id'

    def list(self, request, *args, **kwargs):
        data = self.serializer_class(self.get_object()).data
        print(data)
        return send_response(response_code=200, data=data, message='success', error=None)
