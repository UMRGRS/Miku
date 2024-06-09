from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import CustomUser
from .serializers import GDPaCustomUserSerializer, PCustomUserSerializer, PaCustomUserPasswordSerializer
from .permissions import IsOwner

# Create your views here.
#P->Post G->Get D->Delete Pa->Patch Pu->Put

#See a way to protect post endpoints
class PCustomUser(APIView):
    def post(self, request):
        serializer = PCustomUserSerializer(data=request.data)
        #Returns 400 if data isn't valid
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {"detail": "User created successfully"}
        return Response(response, status=status.HTTP_201_CREATED)

class GDPaCustomUser(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = GDPaCustomUserSerializer
    permission_classes = [IsAuthenticated, IsOwner]

#Made another class to change password to be able to add more functions in the future
class PuCustomUserPassword(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    def put(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = PaCustomUserPasswordSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password updated successfully"}, status=status.HTTP_200_OK)        