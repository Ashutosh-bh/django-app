from django.urls import path

from restaurant.views import GetMenuView

urlpatterns = [
    path('<str:id>/menu', GetMenuView.as_view(), name='menu_detail'),
]