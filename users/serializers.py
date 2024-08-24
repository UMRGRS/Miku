from rest_framework import serializers

from .models import CustomUser

class SignupSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        return CustomUser.objects.create_standard_user(**validated_data)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']