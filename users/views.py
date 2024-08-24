from django.shortcuts import render
from knox.views import LoginView as KnoxLoginView
from rest_framework.authentication import BasicAuthentication


from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import CustomUser
from . import serializers
# Create your views here.

#Signup view
class Signup(APIView):
    def post(self, request):
        serializer = serializers.SignupSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#Get view

#Update view

#Delete view

#Update password view -> No serializer

#Overwrite knox view to only use token auth in the other views
class LoginView(KnoxLoginView):
    authentication_classes = [BasicAuthentication]
