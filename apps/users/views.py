from django.shortcuts import get_object_or_404
from knox.views import LoginView as KnoxLoginView
from rest_framework.authentication import BasicAuthentication

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from apps.users.models import CustomUser
from .serializers import UserSerializer, UserProfileSerializer
from .permissions import IsOwner
# Create your views here.

#Signup view
class Signup(APIView):
    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = []
    @extend_schema(
        description='Create a new user to authenticate into the API'
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            response_data = serializer.data
            response_data.pop('password', None)
            return Response(response_data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#Get view
class SeeUser(APIView):
    @extend_schema(
        responses={200: UserProfileSerializer},
        description='Get basic user data with current token'
    )
    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

#Update, delete view
@extend_schema(
    description='Delete user via ID'
)
class UpdateDeleteUser(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    def getUser(self, pk):
        user =  get_object_or_404(CustomUser, pk=pk)
        self.check_object_permissions(self.request, user)
        return user
    
    def setPassword(self, user, password):
        user.set_password(password)
        user.save()
    
    @extend_schema(
        description='Update user data via ID'
    )
    def patch(self, request, pk):
        user = self.getUser(pk)
        if 'password' in  request.data:
            request.data._mutable = True
            self.setPassword(user, request.data.pop('password', None)[0])
            request.data._mutable = False
        serializer = UserSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            response_data = serializer.data
            response_data.pop('password', None)
            return Response(response_data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#Overwrite knox view to only use token auth in the other views
@extend_schema(
    description='Get auth token with basic auth'
)
class LoginView(KnoxLoginView):
    authentication_classes = [BasicAuthentication]