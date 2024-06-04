from urllib import response
from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'password', 'username', 'contact', 'membership_number', 'created_at', 'is_active']
        extra_kwargs = {'password': {'write_only': True}, 'username': {'required': False}}

    def create(self, validated_data):
        email = validated_data['email']
        user = User.objects.create_user(
            fullname=validated_data['fullname'],
            email=email,
            username=email,  # Set email as the username
            contact=validated_data['contact'],
            membership_number=validated_data['membership_number'],
            password=validated_data['password']
        )
        return user

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

