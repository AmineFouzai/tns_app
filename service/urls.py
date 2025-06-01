from django.urls import path, include

from service.api.dynamic_api import DynamicAPIRouter
from service.models import *

dynamic_api = DynamicAPIRouter(
    included_models=[Campaign, Template, Merchant, Recipient],
)

urlpatterns = [
    path("api/v1/", include(dynamic_api.get_urls())),
]
