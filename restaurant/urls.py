from django.urls import path

from restaurant.views import GetMenuView, GetAllRestaurantView, SaveRestaurantView, SaveMenuView

urlpatterns = [
    path('<str:id>/menu', GetMenuView.as_view(), name='menu_detail'),
    path('', SaveRestaurantView.as_view(), name='SaveRestaurant'),
    path('list', GetAllRestaurantView.as_view(), name='GetAllRestaurant'),
    path('<str:id>/menu/add', SaveMenuView.as_view(), name='SaveMenuView'),
]