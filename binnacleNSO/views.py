from django.shortcuts import render

from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Profile, Alias, Entry
from .permissions import IsOwner
from .serializers import ProfileGDSerializer, ProfilePPaSerializer, AliasPDSerializer, AliasGPaSerializer, EntryPSerializer, EntryGPaSerializer, EntryListSerializer

# Create your views here.

#P->Post G->Get D->Delete Pa->Patch 
#Profile views
class PProfile(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfilePPaSerializer
    permission_classes = [permissions.IsAuthenticated]

class PaProfile(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfilePPaSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]#object level permission

class GDProfile(generics.RetrieveDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileGDSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]#object level permission

#Alias views
class PAlias(generics.CreateAPIView):
    queryset = Alias.objects.all()
    serializer_class = AliasPDSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class GPaAlias(generics.RetrieveUpdateAPIView):
    queryset = Alias.objects.all()
    serializer_class = AliasGPaSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]#object level permission

class DAlias(generics.DestroyAPIView):
    queryset = Alias.objects.all()
    serializer_class = AliasPDSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]#object level permission

#Entry views
class PEntry(generics.CreateAPIView):
    queryset = Entry.objects.all()
    serializer_class = EntryPSerializer
    permission_classes = [permissions.IsAuthenticated]

class GPaEntry(generics.RetrieveUpdateAPIView):
    queryset = Entry.objects.all()
    serializer_class = EntryGPaSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]#object level permission
    
class GallEntries(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]#object level permission
    def get(self, request, pk):
        profile = Profile.objects.get(pk=pk)
        queryset = profile.entry_set.all()
        serializer = EntryListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)