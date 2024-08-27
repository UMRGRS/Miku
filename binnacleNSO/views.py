from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .models import Profile, Alias, Entry
from .permissions import IsProfileOwner, IsAliasOrEntryOwner, NoProfileCreated, HasLessThanTenAliases
from .serializers import ProfileSerializer, AliasSerializer, EntrySerializer, CompleteEntrySerializer

# Create your views here.

# Profile views
class CreateProfile(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, NoProfileCreated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SeeUpdateDeleteProfile(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]

# Alias views
class CreateAlias(generics.CreateAPIView):
    serializer_class = AliasSerializer
    permission_classes = [IsAuthenticated, HasLessThanTenAliases]

    def perform_create(self, serializer):
        try:
            profile = self.request.user.profile
        except:
            return Response({"detail": "You need to have a profile to create aliases"}, status=status.HTTP_404_NOT_FOUND)

        serializer.save(profile=profile)

class SeeUpdateDeleteAlias(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alias.objects.all()
    serializer_class = AliasSerializer
    permission_classes = [IsAuthenticated, IsAliasOrEntryOwner]

class ListAlias(APIView):
    serializer_class = AliasSerializer
    def get(self, request):
        try:
            profile = request.user.profile
        except:
            return Response({"detail": "You need to have a profile to see aliases"}, status=status.HTTP_404_NOT_FOUND)

        aliases = profile.alias.all()
        serializer = AliasSerializer(aliases, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Entry views
class CreateEntry(generics.CreateAPIView):
    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            profile = request.user.profile
        except:
            return Response({"detail": "No profile found for this user"}, status=status.HTTP_404_NOT_FOUND)
        serializer = EntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(profile=profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_201_CREATED)

class UpdateEntry(generics.UpdateAPIView):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticated, IsAliasOrEntryOwner]

class SeeDeleteEntry(generics.RetrieveDestroyAPIView):
    queryset = Entry.objects.all()
    serializer_class = CompleteEntrySerializer
    permission_classes = [IsAuthenticated, IsAliasOrEntryOwner]

class ListEntries(APIView):
    permission_classes = [IsAuthenticated, IsAliasOrEntryOwner]
    serializer_class = CompleteEntrySerializer
    def get(self, request):
        limit = request.GET.get('limit')
        filter_by_entry = request.GET.get('by_entry')
        alias_pk = request.GET.get('alias')
        if limit is None:
            limit = -1
        else:
            try:
                limit = int(limit)
            except:
                return Response({"limit": "This query parameter has to be a number"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            profile = request.user.profile
        except:
            return Response({"detail": "No profile found for this user"}, status=status.HTTP_404_NOT_FOUND)
        
        if filter_by_entry is not None:
            if filter_by_entry == "True":
                try:
                    alias_pk = int(alias_pk)
                except:
                    return Response({"alias_pk": "This query parameter has to be a number"}, status=status.HTTP_400_BAD_REQUEST)
                entries = Entry.objects.filter(profile=profile, alias=alias_pk)
            else:
                return Response({"by_entry": "by_entry has to be either True or blank (Case sensitive)"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            entries = Entry.objects.filter(profile=profile)
        
        if limit != -1:
           entries = entries[:limit]
           
        if len(entries) == 0:
            return Response({"detail": "No entries match the given query."}, status=status.HTTP_404_NOT_FOUND)
           
        serializer = CompleteEntrySerializer(entries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
