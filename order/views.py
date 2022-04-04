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


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.filter(is_deleted=False)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        print('request received to get all restaurant ')
        print(request.GET)
        query_set = self.get_queryset().filter(**{k: v[0] for k, v in request.GET.items()})
        data = self.serializer_class(query_set.all(), many=True).data
        amounts = {}
        [amounts.update({item['status']: amounts.get(item['status'], 0) + float(item['amount'])}) for item in data]
        print('returning response', data)
        return send_response(response_code=200, data={'orders': data,
                                                      'count': query_set.count(),
                                                      'amount': amounts}, message='success', error=None)


class OrderUpdateView(generics.UpdateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.filter(is_deleted=False).all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = 'id'

    def put(self, request, *args, **kwargs):
        print('request received to update order')
        order = self.get_object()
        order.status = request.data['status'] if 'status' in request.data else order.status
        order.save()
        data = self.serializer_class(order).data
        return send_response(response_code=201, data=data, message='success', error=None)
