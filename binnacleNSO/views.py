from django.shortcuts import render

from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from .models import Superuser, Subuser, Entry
from .serializers import SuperuserGDSerializer, SuperuserPPaSerializer, SubuserPDSerializer, SubuserGPaSerializer, EntryPSerializer, EntryGPaSerializer, EntryGallSerializer
from .authentication import ExampleAuthentication

# Create your views here.

#P->Post G->Get D->Delete Pa->Patch 
#Superuser views
class PSuperuser(generics.CreateAPIView):
    queryset = Superuser.objects.all()
    serializer_class = SuperuserPPaSerializer

class PaSuperuser(generics.UpdateAPIView):
    queryset = Superuser.objects.all()
    serializer_class = SuperuserPPaSerializer

class GDSuperuser(generics.RetrieveDestroyAPIView):
    queryset = Superuser.objects.all()
    serializer_class = SuperuserGDSerializer

#Subuser views
class PSubuser(generics.CreateAPIView):
    queryset = Subuser.objects.all()
    serializer_class = SubuserPDSerializer
    
class GPaSubuser(generics.RetrieveUpdateAPIView):
    queryset = Subuser.objects.all()
    serializer_class = SubuserGPaSerializer

class DSubuser(generics.DestroyAPIView):
    queryset = Subuser.objects.all()
    serializer_class = SubuserPDSerializer

#Entry views
class PEntry(generics.CreateAPIView):
    queryset = Entry.objects.all()
    serializer_class = EntryPSerializer

class GPaEntry(generics.RetrieveUpdateAPIView):
    
    queryset = Entry.objects.all()
    serializer_class = EntryGPaSerializer
    
class GallEntries(APIView):
    def get(self, request, pk):
        superuser = Superuser.objects.get(pk=pk)
        queryset = superuser.entry.all()
        serializer = EntryGallSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)