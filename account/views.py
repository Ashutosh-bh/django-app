from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from account.models import User, Address, UserAddressMapping
from util.common import send_response


class CreateUserView(generics.CreateAPIView):

    def create(self, request, *args, **kwargs):
        print('request received to create user is', request.data)
        password = request.data.pop('password')
        addresses = request.data.pop('address')
        user = User(**request.data, is_active=True, is_staff=False, date_joined=timezone.localtime(),
                    username=request.data['mobile'])
        user.set_password(password)
        user.save()
        for address in addresses:
            obj = Address(**address)
            obj.save()
            UserAddressMapping(user_id=user.id, address_id=obj.id).save()
        print('user created', user)
        return send_response(response_code=201, data={}, message='success', error=None)


class AuthenticateUserView(generics.CreateAPIView):

    def create(self, request, *args, **kwargs):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            print(user)
            token, is_created = Token.objects.get_or_create(user=user)
            print('new token created')
            return send_response(response_code=201, data={'token': token.key}, message='success', error=None)
        else:
            return send_response(response_code=401, data={}, message='invalid username or password', error=None)
