from django.contrib import admin
from .models import Staff, Child, Parent, Resource

# Register your models here.

"""
Admin Classes specify how models are layed out on Admin site.
"""

class ParentInline(admin.TabularInline):
    pass

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'email', 'photo', 'bio']


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ['name', 'dob', 'starting_date', 'parents']


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_dsiplay = ['name', 'email', 'phone_number']


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['resource_type', 'description', 'file', 'image', 'url']
