from rest_framework import serializers
from .models import *
from user_management.models import User

class RepresentativeSerializer(serializers.ModelSerializer):
    representative = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = WilayaRepresentative
        fields = ['id', 'wilaya', 'mkoa', 'date', 'status', 'wilaya_code', 'representative']


class ObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objective
        fields = ['objective', 'representative']

        