from rest_framework import serializers
from .models import Staff, Child, Parent, Resource
from drf_writable_nested.serializers import WritableNestedModelSerializer
from drf_writable_nested.mixins import UniqueFieldsMixin

## JSON Serialization of Django models for REST API conversion

## Staff Serializer
class StaffSerializer(serializers.ModelSerializer):
    # Note: fields can be set to __all__, not done to prevent information leaks
    class Meta:
        model = Staff
        fields = ['name', 'bio', 'email', 'role', 'photo', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


## Parent Serializer
class ParentSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    # UniqueFieldsMixin handles serialization issue with Unique fields in m2m.

    class Meta:
        model = Parent
        fields = ['id', 'name', 'phone_number', 'email', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


## Child Serializer
class ChildSerializer(WritableNestedModelSerializer):
    # Nested serializer to produce many-to-many relationship
    parents = ParentSerializer(many = True)

    class Meta:
        model = Child
        fields = ['name', 'dob', 'starting_date', 'parents', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


## Resource Serializer
class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['description', 'url', 'image', 'file', 'resource_type', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']