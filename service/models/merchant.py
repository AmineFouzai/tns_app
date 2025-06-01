from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission


class Merchant(User):
    class Meta:
        proxy = True
        verbose_name = "Merchant"
        verbose_name_plural = "Merchants"
