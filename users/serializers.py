from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Adiciona dados extras na resposta do login
        data['role'] = self.user.role
        data['username'] = self.user.username
        data['must_change_password'] = self.user.must_change_password
        return data

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

from .models import PasswordResetRequest

class PasswordResetRequestSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = PasswordResetRequest
        fields = ['id', 'username', 'email', 'status', 'created_at']

class RequestResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class ApproveResetSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['APPROVE', 'REJECT'])
