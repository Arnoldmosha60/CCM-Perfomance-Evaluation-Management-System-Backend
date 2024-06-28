from rest_framework import serializers
from .models import *
from user_management.models import User

class RepresentativeSerializer(serializers.ModelSerializer):
    representative = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = WilayaRepresentative
        fields = ['id', 'wilaya', 'mkoa', 'date', 'status', 'wilaya_code', 'representative']


class ObjectiveSerializer(serializers.ModelSerializer):
    representative = serializers.PrimaryKeyRelatedField(queryset=WilayaRepresentative.objects.all())
    
    class Meta:
        model = Objective
        fields = ['id','objective', 'representative', 'objective_code', 'created_by', 'created_at']


class TargetSerializer(serializers.ModelSerializer):
    objective = serializers.PrimaryKeyRelatedField(queryset=Objective.objects.all())

    class Meta:
        model = Target
        fields = '__all__'


class IndicatorSerializer(serializers.ModelSerializer):
    target = serializers.PrimaryKeyRelatedField(queryset=Target.objects.all())

    class Meta:
        model = Indicator
        fields = '__all__'


class ActivitySerializer(serializers.ModelSerializer):
    indicator = serializers.PrimaryKeyRelatedField(queryset=Indicator.objects.all())

    class Meta:
        model = Activity
        fields = '__all__'

        
