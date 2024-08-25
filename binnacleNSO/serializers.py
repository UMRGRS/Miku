from rest_framework import serializers

from .models import Profile, Alias, Entry

# Profile serializers
class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Profile
        exclude = ['streak', 'lastEntryDate']
        read_only_fields = ['id']

# Alias serializer
class AliasSerializer(serializers.ModelSerializer):
    profile = serializers.CharField(source='profile.name', read_only=True)
    image = serializers.ImageField(required=False, max_length=None, use_url=True)

    class Meta:
        model = Alias
        fields = '__all__'
        read_only_fields = ['id']

# Entry serializers

# Used to create entries
class EntrySerializer(serializers.ModelSerializer):
    profile = serializers.CharField(source='profile.name', read_only=True)
    alias = serializers.PrimaryKeyRelatedField(queryset=Alias.objects.all())
    image = serializers.ImageField(required=False, max_length=None, use_url=True)

    class Meta:
        model = Entry
        fields = ['id', 'content', 'image', 'profile', 'alias']
        read_only_fields = ['id']

# Used to display the whole information about an entry
class CompleteEntrySerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(data='profile')
    alias = AliasSerializer(data='alias')

    class Meta:
        model = Entry
        fields = '__all__'