from django.urls import path, include
from . import views
from rest_framework import routers
from store import views


router = routers.SimpleRouter()

router.register('rented', views.RentedViewSet, basename='rented')


urlpatterns = [
    path('', include(router.urls)),
    path("rented/<int:pk>/update/status/", views.RentedViewSet.as_view({'patch': 'partial_update'}))
]