from django.apps import apps
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.urls import path, include


class DynamicModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that dynamically generates fields based on the model.
    """

    @classmethod
    def create_for_model(cls, model):
        meta_attrs = {"model": model, "fields": "__all__"}

        serializer_name = f"{model.__name__}Serializer"
        meta_class = type("Meta", (), meta_attrs)

        return type(serializer_name, (cls,), {"Meta": meta_class})


class DynamicModelViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet that dynamically generates queryset and serializer_class.
    """

    @classmethod
    def create_for_model(cls, model, serializer_class):
        viewset_name = f"{model.__name__}ViewSet"

        return type(
            viewset_name,
            (cls,),
            {"queryset": model.objects.all(), "serializer_class": serializer_class},
        )


class DynamicAPIRouter:
    """
    Creates dynamic API endpoints for specific models only.
    """

    def __init__(self, included_models=None, custom_config=None):
        self.router = routers.DefaultRouter()
        self.included_models = included_models or []  # List of model instances or (app_label, model_name) tuples
        self.custom_config = custom_config or {}
        self.registered_models = {}

    def register_model(self, model):
        """Register a single model with the router."""
        model_name = model.__name__

        # Skip if already registered
        if model_name in self.registered_models:
            return None

        # Check if there's custom configuration for this model
        config = self.custom_config.get(model_name, {})

        # Create serializer class
        if "serializer" in config:
            serializer_class = config["serializer"]
        else:
            serializer_class = DynamicModelSerializer.create_for_model(model)

        # Create viewset class
        if "viewset" in config:
            viewset_class = config["viewset"]
        else:
            viewset_class = DynamicModelViewSet.create_for_model(
                model, serializer_class
            )

        # Register with the router
        base_name = config.get("base_name", model._meta.model_name)
        self.router.register(base_name, viewset_class)

        self.registered_models[model_name] = {
            "serializer": serializer_class,
            "viewset": viewset_class,
            "base_name": base_name,
        }

        return self.registered_models[model_name]

    def register_specified_models(self):
        for model_identifier in self.included_models:
            if hasattr(model_identifier, '_meta'):
                model = model_identifier
            elif isinstance(model_identifier, tuple) and len(model_identifier) == 2:
                app_label, model_name = model_identifier
                try:
                    model = apps.get_model(app_label, model_name)
                except LookupError:
                    continue
            elif isinstance(model_identifier, str) and '.' in model_identifier:
                app_label, model_name = model_identifier.split('.')
                try:
                    model = apps.get_model(app_label, model_name)
                except LookupError:
                    continue
            else:
                continue
                
            self.register_model(model)
                
        return self.registered_models

    def get_urls(self):
        self.register_specified_models()

        @api_view(["GET"])
        def api_root(request, format=None):
          
            return Response(
                {
                    model_name: reverse(
                        f'{config["base_name"]}-list', request=request, format=format
                    )
                    for model_name, config in self.registered_models.items()
                }
            )

        return [
            path("", include(self.router.urls)),
        ]


# Example usage in urls.py
"""
from django.urls import path, include
from .dynamic_api import DynamicAPIRouter
from myapp.models import Product, Category, Order

# Optional custom configurations for specific models
custom_config = {
    'Product': {
        'base_name': 'products',
        # You can provide custom serializers or viewsets if needed
        # 'serializer': ProductSerializer,
        # 'viewset': ProductViewSet,
    }
}

# Method 1: Pass model classes directly
dynamic_api = DynamicAPIRouter(
    included_models=[Product, Category, Order],
    custom_config=custom_config
)

# Method 2: Specify models by app_label and model_name
dynamic_api = DynamicAPIRouter(
    included_models=[
        ('myapp', 'Product'),
        ('myapp', 'Category'),
        ('shop', 'Order')
    ],
    custom_config=custom_config
)

# Method 3: Specify models as strings
dynamic_api = DynamicAPIRouter(
    included_models=[
        'myapp.Product',
        'myapp.Category',
        'shop.Order'
    ],
    custom_config=custom_config
)

urlpatterns = [
    # ... your other URL patterns
    path('api/', include(dynamic_api.get_urls())),
]
"""