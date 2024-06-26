from urllib import response
from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'password', 'username', 'contact', 'ccm_number', 'created_at', 'is_active']
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data.pop('password', None)
        user = User.objects.create_user(
            fullname=validated_data['fullname'],
            email=email,
            contact=validated_data['contact'],
            ccm_number=validated_data['ccm_number'],
            password=password
        )
        return user
    
    def update(self, instance, validated_data):
        instance.fullname = validated_data.get('fullname', instance.fullname)
        instance.email = validated_data.get('email', instance.email)
        instance.contact = validated_data.get('contact', instance.contact)
        instance.ccm_number = validated_data.get('ccm_number', instance.ccm_number)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

