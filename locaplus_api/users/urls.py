from django.urls import path
from . import views


urlpatterns = [
    path("customer/register/", views.register_customer),
    path("login/", views.login_user),
    path("customers/", views.CustomerViewSet.as_view({"get": "list"})),
]