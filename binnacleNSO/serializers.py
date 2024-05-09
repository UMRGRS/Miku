from rest_framework import serializers

from .models import Profile, Alias, Entry

#P->Post G->Get D->Delete Pa->Patch 

#Profile serializers
class ProfileGDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class ProfilePPaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['streak', 'numberOfEntries', 'lastEntryDate']
        read_only_fields = ['id']

#Alias serializer
class AliasPDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alias
        fields = '__all__'

class AliasGPaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alias
        exclude = ['profile']
        read_only_fields = ['id']

#Entry serializers
class EntryPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        exclude = ['stars', 'shares', 'day']

class EntryGPaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        exclude = ['stars', 'shares', 'day', 'alias']
        read_only_fields = ['id']
        
class EntryListSerializer(serializers.ModelSerializer):
    profileName = serializers.SerializerMethodField()
    aliasName = serializers.SerializerMethodField()
    streak = serializers.SerializerMethodField()
    
    def get_supUName(self, obj):
        return obj.profile.name
    
    def get_subUName(self, obj):
        return obj.alias.name
    
    def get_streak(self, obj):
        return obj.profile.streak
      
    class Meta:
        model = Entry
        exclude = ['profile', 'alias']
        read_only_fields = ['id']