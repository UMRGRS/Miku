from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import Alias, Entry
from .permissions import IsAliasOrEntryOwner, HasLessThanTenAliases
from .serializers import AliasSerializer, EntrySerializer, CompleteEntrySerializer
from .pagination import EntriesResultsSetPagination
# Create your views here.

# Alias views
@extend_schema(
    description='Create a new alias tied to an existing user'
)
class CreateAlias(generics.CreateAPIView):
    serializer_class = AliasSerializer
    permission_classes = [IsAuthenticated, HasLessThanTenAliases]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
@extend_schema(
    description="Access, edit or delete current user's aliases"
)
class SeeUpdateDeleteAlias(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alias.objects.all()
    serializer_class = AliasSerializer
    permission_classes = [IsAuthenticated, IsAliasOrEntryOwner]
    
@extend_schema(
    description='Get all the alias corresponding to the current user'
)
class ListAlias(APIView):
    serializer_class = AliasSerializer
    def get(self, request):
        aliases = request.user.alias.all()
        
        if len(aliases) == 0:
            return Response({"detail": "No aliases found for the current user."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AliasSerializer(aliases, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Entry views
@extend_schema(
    description='Create a new entry'
)
class CreateEntry(generics.CreateAPIView):
    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

@extend_schema(
    description='Update entry data'
)
class UpdateEntry(generics.UpdateAPIView):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticated, IsAliasOrEntryOwner]

class SeeDeleteEntry(generics.RetrieveDestroyAPIView):
    queryset = Entry.objects.all()
    serializer_class = CompleteEntrySerializer
    permission_classes = [IsAuthenticated, IsAliasOrEntryOwner]
    
    @extend_schema(
        description='Get all the info corresponding to one entry'
    )
    def get(self, request, pk):
        return super().get(request, pk)
    
    @extend_schema(
        description='Delete entry via ID'
    )
    def delete(self, request, pk):
        return super().delete(request, pk)
    
@extend_schema(
    description='Get all the entries corresponding to the current user'
)
class ListUserEntries(generics.ListAPIView):
    serializer_class = CompleteEntrySerializer
    pagination_class = EntriesResultsSetPagination
    def get_queryset(self):
        user = self.request.user
        return Entry.objects.filter(owner=user)

@extend_schema(
    description='Get all the entries corresponding to a single alias',
    parameters=[
        OpenApiParameter(
            name='alias_pk', 
            type=OpenApiTypes.INT, 
            location=OpenApiParameter.QUERY, 
            description='ID of the alias you want to filter'
        )
    ]
)
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