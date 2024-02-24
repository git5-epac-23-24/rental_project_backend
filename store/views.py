from django.shortcuts import render
from rest_framework import viewsets, permissions
from store.serializers import *
from store.models import Rent, Product, ProductType
from users.models import User
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
        'list': getRentedSerialisers,
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
        permission_classes = [permissions.IsAuthenticated]
        # if self.action == 'create' or self.action == 'list' or self.action == 'list_by_product':
        #     permission_classes = [permissions.IsAuthenticated]
        # else:
        #     permission_classes = [permissions.IsAdminUser]
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
                if (data['product'].stock < 1):
                    isNotAvailable = data['product'].rents.filter(Q(start_date__range=(start_date_n, end_date_n))|Q(end_date__range=(start_date_n, end_date_n))|(Q(start_date__lt= start_date_n)&Q(end_date__gt =end_date_n))).exists()
                    if (isNotAvailable):
                        return Response({
                            "status": "error",
                            "message": "This intervalle of date is not available",
                        })
                qte = 1
                if data['quantity']:
                    if data['product'].stock < data['quantity']:
                        return Response({
                            "status": "error",
                            "message": "the quantity available is not sufficient",
                        })
                    else:
                        qte = data['quantity']
                        
                rent = Rent(**data)
                rent.duration = start_date_n - end_date_n
                rent.user = request.user
                rent.quantity = qte
                rent.save()
                product = rent.product
                product.stock = product.stock - rent.quantity
                product.save()
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
            
    def update_status(self, request, *args, **kwargs):
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
            recipient = [
                user.email,
            ]
            send_mail(
                subject=subject,
                message=message,
                from_email=emailFrom,
                recipient_list=recipient,
            )
            return Response(
                {
                    "status": "success",
                    "message": "Status updated successfully for the reservation",
                    "data": model_to_dict(rent),
                }
            )
        except Exception as e:
            return Response(
                {"status": "error", "message": "Something went wrong", "error": str(e)}
            )

    def list_by_product(self, request, *args, **kwargs):
        try:
            product = Product.objects.filter(pk=kwargs['pk']).first()
            if (product is None):
                return Response({
                    "status": "error",
                    "message": "Something went wrong",
                    "error": "Product not found"
                }, status=404)
            rents = product.rents.all()
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


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializers

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create' or self.action =='update' or self.action =='destroy' :
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Product.objects.all().order_by("-created_at")

    def create(self, request):
        # try:
        data = request.data
        # data['owner'] = request.user
        data_copy = data.copy()
        product_type = ProductType.objects.get(pk=data['type'])
        # data_copy['type'] = product_type
        # The code is removing the 'type' key from the dictionary `data_copy` and assigning its value
        # to the variable `type`.
        # type = data_copy.pop('type')
       
        # user = request.user
        data_copy["owner"] = request.user.id
        # product = Product.objects.create(**data_copy)
        # product.owner = request.user
        # product.save()
        # print(data)
        serializer = ProductSerializers(data=data_copy, partial=True)
        
        if serializer.is_valid():
            product = serializer.save()
            serialized = ProductSerializers(product)
            
            # data = serializer.save()
            # product = Product(**data_sec)
            # print(product.picture)
            
            return Response(
                {
                    "status": "success",
                    "message": "Your product has been added successfully",
                    "data": serialized.data
                }
            )
        else:
            return Response(
                {
                    "status": "error",
                    "message": "Serialization fails",
                    "error": serializer.errors,
                }
            )
        # except Exception as e:
        #     return Response(
        #         {"status": "errors", "message": "Something went wrong", "error": str(e)}
        #     )

    def update(self, request, *args, **kwargs):
        try:
            data = request.data
            product = get_object_or_404(Product, pk=kwargs["pk"])
            serializer = ProductSerializers(product, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "status": "success",
                        "message": "Your product has been updated successfully",
                        "data": serializer.data,
                    }
                )
            else:
                return Response(
                    {
                        "status": "error",
                        "message": "Serialization fails",
                        "error": serializer.errors,
                    }
                )
        except Exception as e:
            return Response(
                {"status": "errors", "message": "Something went wrong", "error": str(e)}
            )

    def destroy(self, request, *args, **kwargs):
        try:
            product = get_object_or_404(Product, pk=kwargs["pk"])
            product.delete()
            return Response(
                {
                    "status": "success",
                    "message": "Your product has been deleted successfully",
                }
            )
        except Exception as e:
            return Response(
                {"status": "errors", "message": "Something went wrong", "error": str(e)}
            )

    def list(self, request):
        try:
            products = Product.objects.all().order_by("-created_at")
            serializer = ProductSerializers(products, many=True)
            return Response(
                {
                    "status": "success",
                    "message": "Products retrieved successfully",
                    "data": serializer.data,
                }
            )
        except Exception as e:
            return Response(
                {"status": "errors", "message": "Something went wrong", "error": str(e)}
            )

    def list_for_owner(self, request, *args, **kwargs):
        try:
            owner = get_object_or_404(User, pk=kwargs["pk"])
            products = Product.objects.filter(owner=owner).order_by("-created_at")
            serializer = ProductSerializers(products, many=True)
            return Response(
                {
                    "status": "success",
                    "message": "Products retrieved successfully",
                    "data": serializer.data,
                }
            )
        except Exception as e:
            return Response(
                {"status": "errors", "message": "Something went wrong", "error": str(e)}
            )

    def retrieve(self, request, *args, **kwargs):
        try:
            product = get_object_or_404(Product, pk=kwargs["pk"])
            serializer = ProductSerializers(product)
            return Response(
                {
                    "status": "success",
                    "message": "Product retrieved successfully",
                    "data": serializer.data,
                }
            )
        except Exception as e:
            return Response(
                {"status": "errors", "message": "Something went wrong", "error": str(e)}
            )

    def filter(self, request):
        try:
            data = request.data
            products = Product.objects.filter(
                Q(price__lte=data["price"] if "price" in data else 1000000)
                | Q(stock__gte=data["stock"] if "stock" in data else 0)
                | Q(rooms__gte=data["rooms"] if "rooms" in data else 0)
                | Q(superficie__gte=data["superficie"] if "superficie" in data else 0)
                | Q(speed__gte=data["speed"] if "speed" in data else 0)
                | Q(weight__gte=data["weight"] if "weight" in data else 0)
                | Q(length__gte=data["length"] if "length" in data else 0)
                | Q(width__gte=data["width"] if "width" in data else 0)
                | Q(type__name__icontains=data["type"] if "type" in data else "")
                | Q(description__icontains=data["description"] if "description" in data else "")
                | Q(name__icontains=data["name"] if "name" in data else "")
            ).order_by("-created_at")
            serializer = ProductSerializers(products, many=True)
            return Response(
                {
                    "status": "success",
                    "message": "Products retrieved successfully",
                    "data": serializer.data,
                }
            )
        except Exception as e:
            return Response(
                {"status": "errors", "message": "Something went wrong", "error": str(e)}
            )


class ProductTypeViewSet(viewsets.ModelViewSet):
    serializer_class = ProductTypeSerializers

    # def get_permissions(self):
    #     """
    #     Instantiates and returns the list of permissions that this view requires.
    #     """
    #     if self.action == "create":
    #         permission_classes = [permissions.IsAuthenticated]
    #     else:
    #         permission_classes = [permissions.IsAdminUser]
    #     return [permission() for permission in permission_classes]

    def get_queryset(self):
        return ProductType.objects.all().order_by("-created_at")

    def create(self, request):
        try:
            data = request.data
            serializer = ProductTypeSerializers(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "status": "success",
                        "message": "Your product type has been added successfully",
                        "data": serializer.data,
                    }
                )
            else:
                return Response(
                    {
                        "status": "error",
                        "message": "Serialization fails",
                        "error": serializer.errors,
                    }
                )
        except Exception as e:
            return Response(
                {"status": "errors", "message": "Something went wrong", "error": str(e)}
            )

    def update(self, request, *args, **kwargs):
        try:
            data = request.data
            productType = get_object_or_404(ProductType, pk=kwargs["pk"])
            serializer = ProductTypeSerializers(productType, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "status": "success",
                        "message": "Your product type has been updated successfully",
                        "data": serializer.data,
                    }
                )
            else:
                return Response(
                    {
                        "status": "error",
                        "message": "Serialization fails",
                        "error": serializer.errors,
                    }
                )
        except Exception as e:
            return Response(
                {"status": "errors", "message": "Something went wrong", "error": str(e)}
            )

    def destroy(self, request, *args, **kwargs):
        try:
            productType = get_object_or_404(ProductType, pk=kwargs["pk"])
            productType.delete()
            return Response(
                {
                    "status": "success",
                    "message": "Your product type has been deleted successfully",
                }
            )
        except Exception as e:
            return Response(
                {"status": "errors", "message": "Something went wrong", "error": str(e)}
            )

    def list(self, request):
        try:
            productTypes = ProductType.objects.all().order_by("-created_at")
            serializer = ProductTypeSerializers(productTypes, many=True)
            return Response(
                {
                    "status": "success",
                    "message": "Product types retrieved successfully",
                    "data": serializer.data,
                }
            )
        except Exception as e:
            return Response(
                {"status": "errors", "message": "Something went wrong", "error": str(e)}
            )

    def retrieve(self, request, *args, **kwargs):
        try:
            productType = get_object_or_404(ProductType, pk=kwargs["pk"])
            serializer = ProductTypeSerializers(productType)
            return Response(
                {
                    "status": "success",
                    "message": "Product type retrieved successfully",
                    "data": serializer.data,
                }
            )
        except Exception as e:
            return Response(
                {"status": "errors", "message": "Something went wrong", "error": str(e)}
            )
