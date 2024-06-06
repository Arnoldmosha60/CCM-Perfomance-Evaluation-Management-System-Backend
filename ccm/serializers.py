from rest_framework import serializers
from .models import *

class RepresentativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WilayaRepresentative
        fields = '__all__'

        