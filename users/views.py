from django.shortcuts import render

from django.contrib.auth.models import Group
from users.models import User, Owner, Role, Subscribers, Email
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.core.mail import send_mail
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.models import Rent
from users.serializers import (
    UserSerializer,
    OwnerSerializer,
    UserLoginSerializer,
    UserUpdateSerializer,
    UserCreationSerializer,
    UserTestSerializer,
    SubscriberSerializer,
    MailSerializer
)
from store.serializers import getRentedSerialisers
from django.conf import settings
from django.core.mail import send_mail


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
    
    serializer_action_classes = {
        'list_by_owner': OwnerSerializer,
    }
    
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

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
    
    def list_by_user(self, request, *args, **kwargs):
        try:
            user = User.objects.filter(pk=kwargs['pk']).first()
            if (user is None):
                return Response({
                    "status": "error",
                    "message": "Something went wrong",
                    "error": "User not found"
                }, status=404)
            rents = user.rents.all()
            list_rents = []
            for rent in rents:
                list_rents.append(getRentedSerialisers(rent).data)
            # print(rents.__class__.objects.all())
            return Response({
                "status": "success",
                "message": "",
                "data": list_rents
            })
        except Exception as e:
            return Response({
                "status": "error",
                "message": "Something went wrong",
                "error": str(e)
            })

    def list_by_owner(self, request, *args, **kwargs):
        try:
            serializer_class = OwnerSerializer
            owner = Owner.objects.filter(pk=kwargs['pk']).first()
            if (owner is None):
                return Response({
                    "status": "error",
                    "message": "Something went wrong",
                    "error": "Owner not found"
                }, status=404)
            rents = Rent.objects.filter(product__owner=owner).all()
            list_rents =  []
            for rent in rents:
                list_rents.append(getRentedSerialisers(rent).data)
            return Response({
                "status": "success",
                "message": "",
                "data": list_rents
            })
        except Exception as e:
            return Response({
                "status": "error",
                "message": "Something went wrong",
                "error": str(e)
            })

# class CustomerViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows customers to be viewed or edited.
#     """

    # queryset = User.objects.filter(role__name = "CLIENT")
    # serializer_class = UserRetrieveSerializer
    # permission_classes = [permissions.IsAuthenticated]


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
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer
#     permission_classes = [permissions.IsAuthenticated]
class SubscriberViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows subscribers to be viewed or edited.
    """
    queryset = Subscribers.objects.all()
    serializer_class = SubscriberSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = []
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = SubscriberSerializer(data=request.data)
            if (serializer.is_valid()):
                subscriber = Subscribers.objects.create(email= serializer.data['email'])
                subject = "Abonnement à newsletter de Rental_app"
                message = f"Votre abbonnement à la newsletter de Rental app a été enregistré avec succès.\nVous serez informés de toutes les actualités."
                emailFrom = settings.EMAIL_HOST_USER
                recipient = [serializer.data['email'],]
                send_mail(subject=subject, message=message, from_email=emailFrom, recipient_list=recipient)
                return Response({
                    "status": "success",
                    "message": "You have been subscribed successfully",
                    "data": SubscriberSerializer(subscriber).data
                })
            else:
                return Response({
                    "status": "error",
                    "message": "Serialization failed",
                    "error": serializer.errors
                }, status=200)     
        except Exception as e:
            return Response({
                    "status": "error",
                    "message": "Serialization failed",
                    "error": str(e)
                }, status=500)
    
    def send_mail(self, request, *args, **kwargs):
        try:
            mailSerializer = MailSerializer(data=request.data)
            if (mailSerializer.is_valid()):
                subject = mailSerializer.data['subject']
                message = mailSerializer.data['message']
                emailFrom = settings.EMAIL_HOST_USER
                recipient = []
                subscribers = Subscribers.objects.all()
                for subscriber in subscribers:
                    recipient.append(subscriber.email)
                send_mail(subject=subject, message=message, from_email=emailFrom, recipient_list=recipient)
                return Response({
                    "status": "success",
                    "message": "Email sended succesfully to all subscribers",
                    "data": ""
                }, status=200)
            else:
                return Response({
                    "status": "error",
                    "message": "Serialization failed",
                    "error": mailSerializer.errors
                }, status=200)     
        except Exception as e:
            return Response({
                    "status": "error",
                    "message": "Serialization failed",
                    "error": str(e)
                }, status=500)
            

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


@api_view(["POST"])
def register_customer(request):
    try:
        data = request.data
        # profile = data['profil_picture'] if 'profil_picture' in data else None
        serializer = UserSerializer(data=data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            user.role_set.add(Role.objects.get_or_create(name="CLIENT")[0])
            customer_group = Group.objects.get_or_create(name="Customer")[0]
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
                    "message": "Serialization failed",
                    "errors": serializer.errors,
                })
    except Exception as e:
        return Response({
                "status": "errors",
                "message": "Something went wrong",
                "error": str(e)
            })


@api_view(["POST"])
def register_owner_complete(request):
    data = request.data
    profile = data['profil_picture'] if 'profil_picture' in data else None
    id_card = data['id_card'] if 'id_card' in data else None
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
            user.profil_picture = profile
            user.set_password(user_data['password'])
            owner = Owner(
                user=user, id_card=data["id_card"] if "id_card" in data else None
            )
            owner.id_card = id_card
            owner.save()
            owner_group = Group.objects.get_or_create(name="Owner")[0]
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
    owner.id_card = id_card
    owner.save()
    owner_group = Group.objects.get_or_create(name="Owner")[0]
    user.groups.add(owner_group)
    return Response({"status": "success", "message": "Owner created successfully"})


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@api_view(["POST"])
def login_user(request):
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


@api_view(["POST"])
def logout_user(request):
    token = RefreshToken(request.data["token"])
    token.blacklist()


@api_view(["POST"])
def receive_email(request):
    try:
        data = request.data
        sender = data["sender"]
        name = data["name"]
        # subject = data["subject"]
        body = data["body"]


        email = Email.objects.create(sender=sender, name = name,  body=body)
        
        
        # envoyer_email_admin(name, sender, body)   
        return Response({'message': 'Message enregistré avec succès.'})
    
    except Exception as e:
        return Response(
            {
                "status": "error",
                "message": "Something went wrong",
                "errors": str(e),
            }
        )
    

# @api_view(["POST"])
# def suscribe_to_newsletter(request):
#     try:
#         data = request.data
#         mail = data["mail"]

#         mail = NewsLetter.objects.create(mail = mail)

#         return Response({'message': 'Vous avez été enregistré avec succès dans la newletter'})
    
#     except Exception as e:
#         return Response({'message': "Désolé!, nous n'avons pas pu vous enregistrez."})
    

def envoyer_email_admin(nom_utilisateur, email_utilisateur, contenu_email):
    sujet = f"Nouveau mail de {nom_utilisateur}"
    message = contenu_email
    adresse_email_admin = settings.EMAIL_HOST_USER  # Remplacez par l'adresse e-mail de l'administrateur
    send_mail(sujet, message, email_utilisateur, adresse_email_admin)
