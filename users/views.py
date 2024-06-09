from django.shortcuts import render, get_object_or_404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


from .models import CustomUser
from .serializers import GDPaCustomUserSerializer, PCustomUserSerializer, PaCustomUserPasswordSerializer

# Create your views here.
#P->Post G->Get D->Delete Pa->Patch Pu->Put
class PCustomUser(generics.CreateAPIView):
    serializer_class = PCustomUserSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        #Returns 400 if data isn't valid
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        response = {"Message": "User created successfully"}
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)
        
class GDPaCustomUser(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = GDPaCustomUserSerializer

@api_view(http_method_names=['PUT'])
@permission_classes([IsAuthenticated])
def PuCustomUserPassword(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    serializer = PaCustomUserPasswordSerializer(user, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"Message": "Password updated successfully"})
        