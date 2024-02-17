from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework import routers


router = DefaultRouter()
router.register(r"users", views.UserTestViewSet, basename="user")


urlpatterns = [
    # path("api/", include(router.urls)),
    path("customer/register/", views.register_customer), #good
    path("owner/complete_register/", views.register_owner_complete), #good
    path("owner/partial_register/", views.register_owner_partial), #good
    path("login/", views.login_user), #good
    path("logout/", views.logout_user), #good
    path("customers/", views.UserViewSet.as_view({"get": "list"})), #good
    path("customers/<int:pk>/", views.UserViewSet.as_view({"get": "retrieve","post": "update", "delete": "destroy"})), #good partial
    path("owners/", views.OwnerViewSet.as_view({"get": "list"})), #good
    path("owners/<int:pk>/", views.OwnerViewSet.as_view({"get": "retrieve","post": "update", "delete": "destroy"})), #good partial
]