from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from account.models import User
from util.common import send_response


class CreateUserView(generics.CreateAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        print('request received to create user is', request.data)
        password = request.data.pop('password')
        user = User(**request.data, is_active=True, is_staff=False, date_joined=timezone.localtime())
        user.set_password(password)
        user.save()
        print('user created', user)
        return send_response(response_code=201, data={}, message='success', error=None)


class AuthenticateUser(generics.CreateAPIView):

    def create(self, request, *args, **kwargs):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            print(user)
            token = Token.objects.create(user=user)
            return send_response(response_code=201, data={'token': token.key}, message='success', error=None)
        else:
            return send_response(response_code=401, data={}, message='invalid username or password', error=None)
