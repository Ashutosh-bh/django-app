from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from order.models import Order
from order.serializers import OrderSerializer
from util.common import send_response


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        print('request received to create order is', request.data)
        order = request.data
        order_obj = Order(**order, status=Order.CREATED, user_id=request.user.id)
        order_obj.save()
        data = self.serializer_class(order_obj).data
        print('returning response', data)
        return send_response(response_code=201, data=data, message='success', error=None)
