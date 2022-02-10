from django.urls import path

from account.views import CreateUserView, AuthenticateUser

urlpatterns = [
    path('add', CreateUserView.as_view(), name='menu_detail'),
    path('login', AuthenticateUser.as_view(), name='menu_detail'),
]