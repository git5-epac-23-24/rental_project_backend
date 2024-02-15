from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.SimpleRouter()

router.register('owners', views.OwnerViewSet, basename='owner')
urlpatterns = [
    path("customer/register/", views.register_customer),
    path("login/", views.login_user),
    path("customers/", views.CustomerViewSet.as_view({"get": "list"})),
    path('', include(router.urls)),
    # path("owners/<pk:int>/upgrade/", views.OwnerViewSet.as_view({'patch': 'partial_update'}))
    
]