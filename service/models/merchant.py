# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import Group, Permission


# class Merchant(AbstractUser):
#     organization = models.CharField(max_length=255, blank=True, null=True)
#     api_key = models.CharField(max_length=64, unique=True)
#     groups = models.ManyToManyField(Group, related_name='merchant_groups')
#     user_permissions = models.ManyToManyField(Permission, related_name='merchant_user_permissions')
#     def __str__(self):
#         return self.username
