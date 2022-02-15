from django.urls import path

from account.views import CreateUserView, AuthenticateUserView

urlpatterns = [
    path('add', CreateUserView.as_view(), name='menu_detail'),
    path('login', AuthenticateUserView.as_view(), name='menu_detail'),
]