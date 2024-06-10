from rest_framework import serializers

from .models import Profile, Alias, Entry

#P->Post G->Get D->Delete Pa->Patch 

#Profile serializers
class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    class Meta:
        model = Profile
        exclude = ['streak', 'lastEntryDate']
        read_only_fields = ['id']

#Alias serializer
class AliasSerializer(serializers.ModelSerializer):
    profile = serializers.CharField(source='profile.name', read_only=True)
    image = serializers.ImageField(max_length=None, use_url=True)
    class Meta:
        model = Alias
        fields = '__all__'
        read_only_fields = ['id']

#Entry serializers
class EntrySerializer(serializers.ModelSerializer):
    profile = serializers.CharField(source='profile.name', read_only=True)
    alias = serializers.CharField(source='alias.name', read_only=True)
    class Meta:
        model = Entry
        fields = ['content', 'image', 'profile', 'alias']
        
#Used to display the whole information about an entry
class CompleteEntrySerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(data='profile')
    alias = AliasSerializer(data='alias')
    class Meta:
        model   = Entry
        fields = '__all__'
        