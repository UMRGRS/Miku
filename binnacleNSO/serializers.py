from rest_framework import serializers

from .models import Alias, Entry
from users.serializers import UserProfileSerializer

# Alias serializer
class AliasSerializer(serializers.ModelSerializer):
    profile = serializers.CharField(source='profile.name', read_only=True)
    image = serializers.ImageField(required=False, max_length=None, use_url=True)
    owner = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Alias
        fields = '__all__'
        read_only_fields = ['id']

# Entry serializers

# Used to create entries
class EntrySerializer(serializers.ModelSerializer):
    profile = serializers.CharField(source='profile.name', read_only=True)
    alias = serializers.PrimaryKeyRelatedField(queryset=Alias.objects.all())
    owner = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Entry
        fields = ['id', 'content', 'image', 'profile', 'alias', 'owner']
        read_only_fields = ['id']

# Used to display the whole information about an entry
class CompleteEntrySerializer(serializers.ModelSerializer):
    alias = AliasSerializer(data='alias')
    owner = UserProfileSerializer(data='owner')
    class Meta:
        model = Entry
        fields = '__all__'