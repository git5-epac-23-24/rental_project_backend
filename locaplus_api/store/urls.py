from django.urls import path, include
from . import views
from rest_framework import routers
from store import views


router = routers.SimpleRouter()

router.register('rented', views.RentedViewSet, basename='rented')


urlpatterns = [
    path('', include(router.urls)),
    path("products/<int:pk>/rented/", views.RentedViewSet.as_view({'get': 'list_by_product'})),
    path("rented/<int:pk>/update/status/", views.RentedViewSet.as_view({'patch': 'partial_update'})),
    path("products/", views.ProductViewSet.as_view({"get": "list", "post": "create"})),
    path("products/<int:pk>/", views.ProductViewSet.as_view({"get": "retrieve", "post": "update", "delete": "destroy"})),
    path("owner_products/<int:pk>/", views.ProductViewSet.as_view({"get": "list_for_owner"})),
    path("product_types/", views.ProductTypeViewSet.as_view({"get": "list", "post": "create"})),
    path("product_types/<int:pk>/", views.ProductTypeViewSet.as_view({"get": "retrieve", "post": "update", "delete": "destroy"})),
]