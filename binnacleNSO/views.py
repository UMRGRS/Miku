from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .models import Profile, Alias, Entry
from .permissions import IsProfileOwner, IsAliasOwner, IsEntryOwner, NoProfileCreated, HasLessThanTenAliases
from .serializers import ProfileSerializer, AliasSerializer, EntrySerializer, CompleteEntrySerializer

# Create your views here.

#P->Post G->Get D->Delete Pa->Patch 
#Profile views
class PProfile(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, NoProfileCreated]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class GDPaProfile(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfileOwner]
    
#Alias views
class PAlias(generics.CreateAPIView):
    serializer_class = AliasSerializer
    permission_classes = [permissions.IsAuthenticated, HasLessThanTenAliases]
    def perform_create(self, serializer):
        try:
            profile = self.request.user.profile
        except:
            return Response({"detail": "No profile found for this user"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer.save(profile=profile)

class GDPaAlias(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alias.objects.all()
    serializer_class = AliasSerializer
    permission_classes = [permissions.IsAuthenticated, IsAliasOwner]

class GAllAlias(APIView):
    def get(self, request):
        try:
            profile = request.user.profile
        except:
            return Response({"detail": "No profile found for this user"}, status=status.HTTP_404_NOT_FOUND)
        
        aliases = profile.alias_set.all()
        serializer = AliasSerializer(aliases, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
#Entry views
class PEntry(generics.CreateAPIView):
    serializer_class = EntrySerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        alias_pk = request.POST.get('alias_pk')
        if alias_pk is None:
            return Response({"alias_pk": "This field is required"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                alias_pk = int(alias_pk)
            except:
                return Response({"alias_pk": "This field has to be a number"}, status=status.HTTP_400_BAD_REQUEST)
        alias = get_object_or_404(Alias, pk=alias_pk)
        try:
            profile = request.user.profile
        except:
            return Response({"detail": "No profile found for this user"}, status=status.HTTP_404_NOT_FOUND)
        serializer = EntrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(profile=profile, alias=alias)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PaEntry(generics.UpdateAPIView):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = [permissions.IsAuthenticated, IsEntryOwner]
    
class GDEntry(generics.RetrieveDestroyAPIView):
    queryset = Entry.objects.all()
    serializer_class = CompleteEntrySerializer
    permission_classes = [permissions.IsAuthenticated, IsEntryOwner]
    
class GEntries(APIView):
    def get(self, request):
        limit = request.GET.get('limit')
        if limit is None:
            return Response({"limit": "This field is required"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                limit = int(limit)
            except:
                return Response({"limit": "This field has to be a number"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            profile = request.user.profile
        except:
            return Response({"detail": "No profile found for this user"}, status=status.HTTP_404_NOT_FOUND)
        entries = Entry.objects.filter(profile=profile).order_by('entryDate')[:limit]
        serializer = CompleteEntrySerializer(entries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        