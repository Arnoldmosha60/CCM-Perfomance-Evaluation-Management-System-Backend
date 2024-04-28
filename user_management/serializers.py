from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'membership_number', 'contact', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        groups_data = validated_data.pop('groups', None)
        user = User.objects.create_user(**validated_data)
        if groups_data:
            user.groups.set(groups_data)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

