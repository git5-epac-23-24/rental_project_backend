from django.shortcuts import render

from django.contrib.auth.models import Group
from users.models import User, Customer, Owner
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.serializers import UserSerializer, CustomerSerializer, OwnerSerializer, UserCreationTestSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.models import User, Customer
from users.serializers import CustomerSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows customers to be viewed or edited.
    """

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]


class OwnerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows owners to be viewed or edited.
    """

    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(["POST"])
def register_customer(request):
    data = request.data
    serializer = UserCreationTestSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save
        customer = Customer.objects.create(user=user)
        return Response({
            "status": "success",
            "message": "Customer created successfully"
        })
    else:
        return Response({
            "status": "error",
            "message": "Something went wrong"
        })
    # try:
    #     user = User.objects.create_user(
    #         username=data["username"],
    #         email=data["email"],
    #         password=data["password"]
    #     )
    #     customer = Customer.objects.create(user=user)
    #     return Response({
    #         "status": "success",
    #         "message": "Customer created successfully"
    #     })
    # except:
    #     return Response({
    #         "status": "error",
    #         "message": "Something went wrong"
    #     })
