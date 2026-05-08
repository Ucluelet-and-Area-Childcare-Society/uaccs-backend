from rest_framework import serializers
from .models import Staff, Child, Parent, Resource

## JSON Serialization of Django models for REST API conversion

## Staff Serializer
class StaffSerializer(serializers.ModelSerializer):
    # Note: fields can be set to __all__, not done to prevent information leaks
    class Meta:
        model = Staff
        fields = ['name', 'bio', 'email', 'role', 'photo', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

## Parent Serializer
class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = ['name', 'phone_number', 'email', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
