from django.contrib.auth.models import User as BaseUser
from django.db import models

from util.models import TimeStampedModel


class User(BaseUser, TimeStampedModel):

    mobile = models.CharField(max_length=10)
