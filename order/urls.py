from django.urls import path

from order.views import OrderCreateView, OrderListView, OrderUpdateView

urlpatterns = [
    path('', OrderCreateView.as_view(), name='create_order'),
    path('list', OrderListView.as_view(), name='list_order'),
    path('<str:id>', OrderUpdateView.as_view(), name='list_order'),
]