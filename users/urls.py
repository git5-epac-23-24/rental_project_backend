from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework import routers


router = DefaultRouter()
router.register(r"users", views.UserTestViewSet, basename="user")

routerSimple = routers.SimpleRouter()
routerSimple.register('subscribers', views.SubscriberViewSet, basename='subscriber')


urlpatterns = [
    # path("api/", include(router.urls)),
    path("customer/register/", views.register_customer),
    path("owner/complete_register/", views.register_owner_complete),
    path("owner/partial_register/", views.register_owner_partial),
    path("login/", views.login_user),
    path("logout/", views.logout_user),
    path("customers/", views.UserViewSet.as_view({"get": "list", "put": "update"})),
    path("customers/<int:pk>/", views.UserViewSet.as_view({"get": "retrieve", "delete": "destroy"})),
    path("owners/", views.UserViewSet.as_view({"get": "list", "put": "update"})),
    path("owners/<int:pk>/", views.UserViewSet.as_view({"get": "retrieve","post": "update", "delete": "destroy"})),
    path("<int:pk>/rented/", views.UserViewSet.as_view({'get': 'list_by_user'})),
    path("owners/<int:pk>/rented/", views.UserViewSet.as_view({'get': 'list_by_owner'})),
    path('', include(routerSimple.urls)),
    path('subscribers/message', views.SubscriberViewSet.as_view({'post': 'send_mail'})),
    path("adminemail/", views.receive_email)
]