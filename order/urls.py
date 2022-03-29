from django.urls import path

from order.views import OrderCreateView

urlpatterns = [
    path('', OrderCreateView.as_view(), name='create_order'),
]