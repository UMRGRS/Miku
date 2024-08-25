from rest_framework import serializers

from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        return CustomUser.objects.create_standard_user(**validated_data)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password']
        read_only_fields = ['id']