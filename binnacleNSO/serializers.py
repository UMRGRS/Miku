from rest_framework import serializers

from .models import Superuser, Subuser, Entry

#P->Post G->Get D->Delete Pa->Patch 

#Superuser serializers
class SuperuserGDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Superuser
        fields = '__all__'

class SuperuserPPaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Superuser
        exclude = ['streak', 'numberOfEntries', 'lastEntryDate']
        read_only_fields = ['id']

#Subuser serializer
class SubuserPDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subuser
        fields = '__all__'

class SubuserGPaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subuser
        exclude = ['superuser']
        read_only_fields = ['id']

#Entry serializers
class EntryPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        exclude = ['stars', 'shares', 'day']

class EntryGPaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        exclude = ['stars', 'shares', 'day', 'subuser']
        read_only_fields = ['id']
        
class EntryGallSerializer(serializers.ModelSerializer):
    supUName = serializers.SerializerMethodField()
    subUName = serializers.SerializerMethodField()
    streak = serializers.SerializerMethodField()
    
    def get_supUName(self, obj):
        return obj.superuser.name
    
    def get_subUName(self, obj):
        return obj.subuser.name
    
    def get_streak(self, obj):
        return obj.superuser.streak
      
    class Meta:
        model = Entry
        exclude = ['superuser', 'subuser']
        read_only_fields = ['id']