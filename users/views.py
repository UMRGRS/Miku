from django.shortcuts import render
from knox.views import LoginView as KnoxLoginView
from rest_framework.authentication import BasicAuthentication

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users.models import CustomUser
from . import serializers
from .permissions import IsOwner
# Create your views here.

#Signup view
class Signup(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        serializer = serializers.SignupSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#Get, update, delete view
class User(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = serializers.UserSerializer
    queryset = CustomUser.objects.all()
    
#Update password view -> No serializer
class UpdatePassword(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    def put(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        self.check_object_permissions(self.request, user)
        if 'password' not in request.data:
            return Response({"password": "This field is required"}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(request.data["password"])
        user.save()
        return Response({"success": "password updated successfully"})
        
#Overwrite knox view to only use token auth in the other views
class LoginView(KnoxLoginView):
    authentication_classes = [BasicAuthentication]