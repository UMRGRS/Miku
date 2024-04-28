from django.shortcuts import render

from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Superuser, Subuser, Entry
from .serializers import SuperuserDSerializer, SuperuserPPaSerializer, SubuserPDSerializer, SubuserGPaSerializer, EntryPSerializer, EntryGPaSerializer, EntryGallSerializer

# Create your views here.

#P->Post G->Get D->Delete Pa->Patch 
#Superuser views

#Subuser views
    
#Entry views