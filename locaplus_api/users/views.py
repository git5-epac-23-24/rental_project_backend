from django.shortcuts import render

from django.contrib.auth.models import Group
from users.models import User
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
@api_view(['POST'])
def register(request):
    data = request.data
    try:
        user = User.objects.create_user(
            data['username'], data['email'], data['password'])
        return Response({'status': 'success', 'message': 'User created successfully'})
    except:
        return Response({'status': 'error', 'message': 'Something went wrong'})
    return Response({'status': 'error', 'message': 'User already exists'})
    return Response(data)