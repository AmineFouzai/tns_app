from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.apps import apps

from service.api.dynamic_api import DynamicAPIRouter
from service.models import *

# Create the dynamic API router instance
dynamic_api = DynamicAPIRouter(
    included_models=[
       Campaign
    ],
)

urlpatterns = [
    # Your other URL patterns
    path("api/v1/", include(dynamic_api.get_urls())),
]