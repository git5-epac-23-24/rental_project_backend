from django.shortcuts import render
from rest_framework import viewsets, permissions
from store.serializers import RentedSerializers, CreateRentedSerializers, updateRentedSerializers, getRentedSerialisers
from store.models import Rent, Product
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.forms.models import model_to_dict
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail

class RentedViewSet(viewsets.ModelViewSet):
    serializer_class = RentedSerializers
    
    serializer_action_classes = {
        'list': getRentedSerialisers
    }
    
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
 
    def get_queryset(self):
        return Rent.objects.all().order_by('-start_date')
    
    def create(self, request):
        try:
            data = request.data
            serializer = CreateRentedSerializers(data=data)
            if (serializer.is_valid()):
                data = serializer.data
                data['product'] = Product.objects.get(pk=data['product'])
                formatDate = "%Y-%m-%dT%H:%M:%SZ"
                start_date_n = datetime.strptime(data['end_date'], formatDate)
                end_date_n = datetime.strptime(data['start_date'], formatDate)
                isNotAvailable = data['product'].rents.filter(Q(start_date__range=(start_date_n, end_date_n))|Q(end_date__range=(start_date_n, end_date_n))|(Q(start_date__lt= start_date_n)&Q(end_date__gt =end_date_n))).exists()
                if (isNotAvailable):
                    return Response({
                        "status": "error",
                        "message": "This intervalle of date is not available",
                    })
                rent = Rent(**data)
                rent.duration = start_date_n - end_date_n
                rent.user = request.user
                rent.save()
                owner = rent.product.owner
                subject = "Demande de location"
                message = f"Chers {owner.username}, cet email vous a été envoyé en raison d'une récente demande de location de votre produit : {rent.product.name}.\nEn effet un client nommé {rent.user.username} a effectué une réservation de votre produit.\n Connectez-vous à votre compte pour plus d'information."
                emailFrom = settings.EMAIL_HOST_USER
                recipient = [owner.email,]
                send_mail(subject=subject, message=message, from_email=emailFrom, recipient_list=recipient)
                return Response({
                    "status": "success",
                    "message": "Your reservation has been added successfully",
                    "data": model_to_dict(rent)
                })
            else:
                return Response({
                    "status": "error",
                    "message": "Serialization fails",
                    "error": serializer.errors
                })
        except Exception as e:
            return Response({
                    "status": "errors",
                    "message": "Something went wrong",
                    "error": str(e)
                })
            
    def partial_update(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = updateRentedSerializers(data=data)
            if (not serializer.is_valid()):
                return Response({
                    "status": "error",
                    "message": "Something went wrong",
                    "error": serializer.errors
                })
            rent = get_object_or_404(Rent, pk=kwargs['pk'])
            rent.status = serializer.data['status']
            rent.save()
            subject = "Confirmation de location"
            user = rent.user
            message = f"Chers {user.username}, cet email vous a été envoyé pour vous informer que votre demande de location du produit {rent.product.name} a été validé par le propritaire.\n Connectez-vous à votre compte pour plus d'informations."
            emailFrom = settings.EMAIL_HOST_USER
            recipient = [user.email,]
            send_mail(subject=subject, message=message, from_email=emailFrom, recipient_list=recipient)
            return Response({
                "status": "success",
                "message": "Status updated successfully for the reservation",
                "data": model_to_dict(rent)
            })
        except Exception as e:
            return Response({
                "status": "error",
                "message": "Something went wrong",
                "error": str(e)
            })