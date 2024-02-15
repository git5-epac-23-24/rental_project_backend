from django.shortcuts import render

from django.contrib.auth.models import Group
from users.models import User, Customer, Owner, Role
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.serializers import UserSerializer, UserCreationSerializer, CustomerSerializer, OwnerGetSerializer, OwnerUpgradeSerializer, UserRetrieveSerializer, OwnerCreationSerializer, UserCreationTestSerializer, UserCreationSerializer, UserLoginSerializer, UserUpdateSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.models import User, Customer
from users.serializers import CustomerSerializer

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser



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

    queryset = User.objects.filter(role__name = "CLIENT")
    serializer_class = UserRetrieveSerializer
    permission_classes = [permissions.IsAuthenticated]


class OwnerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows owners to be viewed or edited.
    """
    serializer_action_classes = {
        'list': OwnerGetSerializer,
        'partial_update': OwnerUpgradeSerializer
    }
    parser_classes = (MultiPartParser, FormParser)
    
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
        
    parser_classes = (MultiPartParser, FormParser)
    queryset = User.objects.all()
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'upgrade':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = []
            
        return [permission() for permission in permission_classes]
 
    def get_queryset(self):
        return User.objects.all()
    
    def create(self, request):
        try:
            data = request.data
            # print(data)
            # serializer = UserCreationSerializer(data=data)
            print(request.FILES.dict())
            serializer = OwnerCreationSerializer(data=data)
            if serializer.is_valid():
                # serializer.save
                data = serializer.data
                # data['profil_picture'] = request.data.images[0]
                # data['id_card'] = request.data.images[1]
                user = User.objects.create_user(**data)
                user.role_set.add(Role.objects.get(name="OWNER"))
                
                return Response({
                    "status": "success",
                    "message": "Owner created successfully"
                })
            else:
                return Response({
                    "status": "error",
                    "message": "Something went wrong",
                    "error": serializer.errors
                })
        except Exception as e:
            return Response({
                "status": "error",
                "message": "Something went wrong",
                "error": str(e)
            })

@api_view(["POST"])
def register_customer(request):
    # try:
    data = request.data
    profile = data['profil_picture']
    # serializer = UserCreationSerializer(data=data)
    serializer = UserCreationSerializer(data=data, partial=True)
    if serializer.is_valid():
        # serializer.save
        data = serializer.data
        data['profil_picture'] = profile
        user = User.objects.create_user(**data)
        user.role_set.add(Role.objects.get(name="CLIENT"))
        # user.profil_picture = profile
        # user.save()
        # customer = Customer(user=user)
        # customer.save()
        return Response({
            "status": "success",
            "message": "Customer created successfully"
        })
    else:
        return Response({
            "status": "error",
            "message": "Serialization failed",
            "error": serializer.errors
        })
    # except Exception as e:
    #     return Response({
    #             "status": "errors",
    #             "message": "Something went wrong",
    #             "error": str(e)
    #         })
        

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }    

    
@api_view(["POST"])
def login_user(request):
    try:
        data = request.data
        serializer = UserLoginSerializer(data=data, partial=True)
        # serializer = UserLoginSerializer(data=data)
        if serializer.is_valid():
            # serializer.save
            data = serializer.data
            user = authenticate(username=data['username'], password=data['password'])
            print(data)
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
    except Exception as e:
        return Response({
            "status": "error",
            "message": "Something went wrong",
            "errors": str(e)
        })
    
    
@api_view(["POST"])
def logout_user(request):
    token = RefreshToken(request.data['token'])
    token.blacklist()
