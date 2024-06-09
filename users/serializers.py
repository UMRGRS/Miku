from rest_framework import serializers

from .models import CustomUser

#P->Post G->Get D->Delete Pa->Patch 
class PCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email']

class GDPaCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']
        
class PaCustomUserPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(label="Password", required=True, allow_blank=False, allow_null=False)
    class Meta:
        model = CustomUser
        fields = ['password']