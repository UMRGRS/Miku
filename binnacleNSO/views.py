from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import Alias, Entry
from .permissions import IsAliasOrEntryOwner, HasLessThanTenAliases
from .serializers import AliasSerializer, EntrySerializer, CompleteEntrySerializer
from .pagination import EntriesResultsSetPagination
# Create your views here.

# Alias views
class CreateAlias(generics.CreateAPIView):
    serializer_class = AliasSerializer
    permission_classes = [IsAuthenticated, HasLessThanTenAliases]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SeeUpdateDeleteAlias(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alias.objects.all()
    serializer_class = AliasSerializer
    permission_classes = [IsAuthenticated, IsAliasOrEntryOwner]

class ListAlias(APIView):
    serializer_class = AliasSerializer
    def get(self, request):
        aliases = request.user.alias.all()
        
        if len(aliases) == 0:
            return Response({"detail": "No aliases found for the current user."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AliasSerializer(aliases, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Entry views
class CreateEntry(generics.CreateAPIView):
    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class UpdateEntry(generics.UpdateAPIView):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticated, IsAliasOrEntryOwner]

class SeeDeleteEntry(generics.RetrieveDestroyAPIView):
    queryset = Entry.objects.all()
    serializer_class = CompleteEntrySerializer
    permission_classes = [IsAuthenticated, IsAliasOrEntryOwner]

class ListUserEntries(generics.ListAPIView):
    serializer_class = CompleteEntrySerializer
    pagination_class = EntriesResultsSetPagination
    def get_queryset(self):
        user = self.request.user
        return Entry.objects.filter(owner=user)

class ListAliasEntries(generics.ListAPIView):
    serializer_class = CompleteEntrySerializer
    pagination_class = EntriesResultsSetPagination
    def get_queryset(self):
        alias_pk = self.request.query_params.get("alias_pk", None)
        if alias_pk is None:
            raise ValidationError(detail='alias_pk is required')
        
        try:
            alias_pk = int(alias_pk)
        except:
            raise ValidationError(detail='alias_pk should be a number')
        
        return Entry.objects.filter(alias=alias_pk)