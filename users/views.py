from django.shortcuts import render

from django.contrib.auth.models import Group
from users.models import User, Role, Subscribers, Email
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
from rest_framework_simplejwt.tokens import RefreshToken


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
        'list_by_owner': UserSerializer,
        'list': UserSerializer
    }
    
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def update(self, request, *args, **kwargs):
        # instance = self.get_object()
        # serializer = UserSerializer(instance, data=request.data, partial=True)
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)
    
    def list(self, request, *args, **kwargs):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data, status=200)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = User(instance)
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
            serializer_class = UserSerializer
            owner = User.objects.filter(pk=kwargs['pk']).first()
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
                subject = "Abonnement à la newsletter de Rental_app"
                message = f"Votre abonnement à la newsletter de Rental app a été enregistré avec succès.\nVous serez informés de toutes les actualités."
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
            

# class OwnerViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows owners to be viewed or edited.
#     """

#     queryset = Owner.objects.all()
#     serializer_class = OwnerSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = OwnerSerializer(instance)
#         return Response(serializer.data, status=200)

#     def list(self, request, *args, **kwargs):
#         queryset = Owner.objects.all()
#         serializer = OwnerSerializer(queryset, many=True)
#         return Response(serializer.data, status=200)

#     def update(self, request, *args, **kwargs):
#         # instance = self.get_object()
#         # serializer = OwnerSerializer(instance, data=request.data, partial=True)
#         user = request.user
#         user_data = request.data.pop("user") if "user" in request.data else {}
#         serializer = UserSerializer(user, data=user_data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         owner = request.user.owner
#         serializer2 = OwnerSerializer(owner, data=request.data, partial=True)
#         serializer2.is_valid(raise_exception=True)
#         serializer2.save()
#         return Response(serializer2.data, status=200)

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response(status=204)


@api_view(["POST"])
def register_customer(request):
    try:
        data = request.data
        # profile = data['profil_picture'] if 'profil_picture' in data else None
        serializer = UserSerializer(data=data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            # user.role_set.add(Role.objects.get_or_create(name="CLIENT")[0])
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
                }
            )
    except Exception as e:
        return Response(
            {"status": "errors", "message": "Something went wrong", "error": str(e)}
        )


@api_view(["POST"])
def register_owner_complete(request):
    try:
        data = request.data
        # profile = data['profil_picture'] if 'profil_picture' in data else None
        serializer = UserSerializer(data=data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            # user.role_set.add(Role.objects.get_or_create(name="CLIENT")[0])
            owner_group = Group.objects.get_or_create(name="Owner")[0]
            user.groups.add(owner_group)
            send_user_serializer = UserSerializer(user)
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
                }
            )
    except Exception as e:
        return Response(
            {"status": "errors", "message": "Something went wrong", "error": str(e)}
        )


@api_view(["POST"])
def register_owner_partial(request):
    try :
        data = request.data
        user = request.user
        id_card = data["id_card"]
        user.id_card = id_card
        # owner.user.role_set.add(Role.objects.get_or_create(name="OWNER")[0])
        user.save()
        owner_group = Group.objects.get_or_create(name="Owner")[0]
        user.groups.add(owner_group)
        owner_data = UserSerializer(user).data
        return Response(
            {
                "status": "success",
                "message": "Owner created successfully",
                "user": owner_data,
            }
        )
    except Exception as e:
        return Response(
            {"status": "errors", "message": "Something went wrong", "error": str(e)}
        )


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
                return Response(
                    {
                        "status": "success",
                        "message": "Owner logged in successfully",
                        "tokens": tokens,
                        "user": send_user_serializer.data,
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
    try:
        token = RefreshToken(request.data["token"])
        token.blacklist()
        return Response({'message': 'User logged out successfully.'})
    except Exception as e:
        return Response(
            {
                "status": "error",
                "message": "Something went wrong",
                "errors": str(e),
            }
        )


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
