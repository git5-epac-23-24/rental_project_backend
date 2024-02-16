from django.shortcuts import render

from django.contrib.auth.models import Group
<<<<<<< HEAD
from users.models import User, Customer, Owner, Role
=======
from users.models import User, Owner
>>>>>>> haricrim
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

<<<<<<< HEAD
from users.serializers import UserSerializer, UserCreationSerializer, CustomerSerializer, OwnerGetSerializer, OwnerUpgradeSerializer, UserRetrieveSerializer, OwnerCreationSerializer, UserCreationTestSerializer, UserCreationSerializer, UserLoginSerializer, UserUpdateSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.models import User, Customer
from users.serializers import CustomerSerializer
=======
from users.serializers import (
    UserSerializer,
    OwnerSerializer,
    UserLoginSerializer,
    UserUpdateSerializer,
    UserTestSerializer,
)

>>>>>>> haricrim

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser


class UserTestViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserTestSerializer
    # permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserSerializer(instance)
        return Response(serializer.data, status=200)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)


# class CustomerViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows customers to be viewed or edited.
#     """

<<<<<<< HEAD
    queryset = User.objects.filter(role__name = "CLIENT")
    serializer_class = UserRetrieveSerializer
    permission_classes = [permissions.IsAuthenticated]


# class OwnerViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows owners to be viewed or edited.
#     """
#     serializer_action_classes = {
#         'list': OwnerGetSerializer,
#         'partial_update': OwnerUpgradeSerializer
#     }
#     parser_classes = (MultiPartParser, FormParser)
    
#     def get_serializer_class(self):
#         try:
#             return self.serializer_action_classes[self.action]
#         except (KeyError, AttributeError):
#             return super().get_serializer_class()
        
#     parser_classes = (MultiPartParser, FormParser)
#     queryset = User.objects.all()
    
#     def get_permissions(self):
#         """
#         Instantiates and returns the list of permissions that this view requires.
#         """
#         if self.action == 'upgrade':
#             permission_classes = [permissions.IsAuthenticated]
#         else:
#             permission_classes = []
            
#         return [permission() for permission in permission_classes]
 
#     def get_queryset(self):
#         return User.objects.all()
    
#     def create(self, request):
#         try:
#             data = request.data
#             # print(data)
#             # serializer = UserCreationSerializer(data=data)
#             print(request.FILES.dict())
#             serializer = OwnerCreationSerializer(data=data)
#             if serializer.is_valid():
#                 # serializer.save
#                 data = serializer.data
#                 # data['profil_picture'] = request.data.images[0]
#                 # data['id_card'] = request.data.images[1]
#                 data['is_active'] = False
#                 user = User.objects.create_user(**data)
#                 user.role_set.add(Role.objects.get(name="OWNER"))
                
#                 return Response({
#                     "status": "success",
#                     "message": "Owner created successfully"
#                 })
#             else:
#                 return Response({
#                     "status": "error",
#                     "message": "Something went wrong",
#                     "error": serializer.errors
#                 })
#         except Exception as e:
#             return Response({
#                 "status": "error",
#                 "message": "Something went wrong",
#                 "error": str(e)
#             })
=======
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer
#     permission_classes = [permissions.IsAuthenticated]


class OwnerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows owners to be viewed or edited.
    """

    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = OwnerSerializer(instance)
        return Response(serializer.data, status=200)

    def list(self, request, *args, **kwargs):
        queryset = Owner.objects.all()
        serializer =  OwnerSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = OwnerSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)

>>>>>>> haricrim

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
<<<<<<< HEAD
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
        
=======
        if User.objects.filter(username=data["username"]).exists():
            return Response({"status": "error", "message": "Username already exists"})
        elif User.objects.filter(email=data["email"]).exists():
            return Response({"status": "error", "message": "Email already exists"})
        elif User.objects.filter(phone=data["phone"]).exists():
            return Response({"status": "error", "message": "Phone already exists"})
        else:
            user = User.objects.create_user(**data)
            user.save()
            customer_group = Group.objects.get(name="Customer")
            user.groups.add(customer_group)
            send_user_serializer = UserSerializer(user)
            # customer = Customer(user=user)
            # customer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Customer created successfully",
                    "user": send_user_serializer.data,
                }
            )
    else:
        return Response(
            {
                "status": "error",
                "message": "Something went wrong",
                "errors": serializer.errors,
            }
        )


@api_view(["POST"])
def register_owner_complete(request):
    data = request.data
    user_data = {
        "username": data["username"] if "username" in data else None,
        "email": data["email"] if "email" in data else None,
        "password": data["password"],
        "first_name": data["first_name"] if "first_name" in data else None,
        "last_name": data["last_name"] if "last_name" in data else None,
        "phone": data["phone"] if "phone" in data else None,
        "profil_picture": data["profil_picture"] if "profil_picture" in data else None,
        "address": data["address"] if "address" in data else None,
        "city": data["city"] if "city" in data else None,
        "country": data["country"] if "country" in data else None,
    }
    data = {
        "user": user_data,
        "id_card": data["id_card"] if "id_card" in data else None,
    }
    serializer =  OwnerSerializer(data=data, partial=True)
    if serializer.is_valid():
        # serializer.save
        data = serializer.data
        if User.objects.filter(username=data["user"]["username"]).exists():
            return Response({"status": "error", "message": "Username already exists"})
        elif User.objects.filter(email=data["user"]["email"]).exists():
            return Response({"status": "error", "message": "Email already exists"})
        elif User.objects.filter(phone=data["user"]["phone"]).exists():
            return Response({"status": "error", "message": "Phone already exists"})
        else:
            # user = User.objects.create_user(**data)

            user = User.objects.create_user(**user_data)
            owner = Owner(
                user=user, id_card=data["id_card"] if "id_card" in data else None
            )
            owner.save()
            owner_group = Group.objects.get(name="Owner")
            user.groups.add(owner_group)
            # owner_data = {
            #     "id": owner.id,
            #     "user": user.id,
            #     "id_card": owner.id_card.url if owner.id_card else None,
            #     "username": user.username,
            #     "email": user.email,
            #     "first_name": user.first_name,
            #     "last_name": user.last_name,
            #     "phone": user.phone,
            #     "profil_picture": (
            #         user.profil_picture.url if user.profil_picture else None
            #     ),
            #     "address": user.address,
            #     "city": user.city,
            #     "country": user.country,
            # }
            owner_data =  OwnerSerializer(owner).data
            return Response(
                {
                    "status": "success",
                    "message": "Owner created successfully",
                    "owner": owner_data,
                }
            )
    else:
        return Response(
            {
                "status": "error",
                "message": "Something went wrong",
                "errors": serializer.errors,
            }
        )


@api_view(["POST"])
def register_owner_partial(request):
    data = request.data
    user_id = data["customer_id"]
    id_card = data["id_card"]
    user = User.objects.get(id=user_id)
    owner = Owner(user=user, id_card=id_card)
    owner.save()
    owner_group = Group.objects.get(name="Owner")
    user.groups.add(owner_group)
    return Response({"status": "success", "message": "Owner created successfully"})

>>>>>>> haricrim

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@api_view(["POST"])
def login_user(request):
<<<<<<< HEAD
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
    
    
=======
    data = request.data
    # serializer = UserSerializer(data=data, partial=True)
    serializer = UserLoginSerializer(data=data)
    if serializer.is_valid():
        # serializer.save
        data = serializer.data
        user = authenticate(username=data["username"], password=data["password"])
        if user is not None:
            send_user_serializer = UserSerializer(user)

            tokens = get_tokens_for_user(user)

            if user.groups.filter(name="Owner").exists():
                owner = Owner.objects.get(user=user)
                owner_data = {
                    "id": owner.id,
                    "user": send_user_serializer.data,
                    "id_card": owner.id_card.url if owner.id_card else None,
                }
                return Response(
                    {
                        "status": "success",
                        "message": "Owner logged in successfully",
                        "tokens": tokens,
                        "user": send_user_serializer.data,
                        "owner": owner_data,
                    }
                )
            else:
                return Response(
                    {
                        "status": "success",
                        "message": "Customer logged in successfully",
                        "tokens": tokens,
                        "user": send_user_serializer.data,
                    }
                )
        else:
            return Response({"status": "error", "message": "Invalid credentials"})
    else:
        return Response(
            {
                "status": "error",
                "message": "Something went wrong",
                "errors": serializer.errors,
            }
        )


>>>>>>> haricrim
@api_view(["POST"])
def logout_user(request):
    token = RefreshToken(request.data["token"])
    token.blacklist()
