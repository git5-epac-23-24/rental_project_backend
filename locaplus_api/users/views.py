from django.shortcuts import render

from django.contrib.auth.models import Group
from users.models import User, Customer, Owner
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.serializers import UserSerializer, CustomerSerializer, OwnerSerializer, UserCreationTestSerializer, UserCreationSerializer, UserLoginSerializer, UserUpdateSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.models import User, Customer
from users.serializers import CustomerSerializer

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserUpdateSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


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
    # serializer = UserCreationSerializer(data=data)
    serializer = UserSerializer(data=data, partial=True)
    if serializer.is_valid():
        # serializer.save
        data = serializer.data
        user = User.objects.create_user(**data)
        customer = Customer(user=user)
        customer.save()
        return Response({
            "status": "success",
            "message": "Customer created successfully"
        })
    else:
        return Response({
            "status": "error",
            "message": "Something went wrong"
        })
    
    
    
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }    

    
@api_view(["POST"])
def login_user(request):
    data = request.data
    serializer = UserSerializer(data=data, partial=True)
    # serializer = UserLoginSerializer(data=data)
    if serializer.is_valid():
        # serializer.save
        data = serializer.data
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            tokens = get_tokens_for_user(user)
            return Response({
                "status": "success",
                "message": "Customer logged in successfully",
                "tokens": tokens
            })
        else:
            return Response({
                "status": "error",
                "message": "Invalid credentials"
            })
    else:
        return Response({
            "status": "error",
            "message": "Something went wrong",
            "errors": serializer.errors
        })
 
    
    
@api_view(["POST"])
def logout_user(request):
    token = RefreshToken(request.data['token'])
    token.blacklist()
