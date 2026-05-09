from django.contrib import admin
from .models import Staff, Child, Parent, Resource

# Register your models here.

"""
Admin Classes specify how models are layed out on Admin site.
"""

class ParentInline(admin.TabularInline):
    model = Child.parents.through
    extra = 2   # no. of extra forms to display

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'email', 'photo', 'bio']


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ['name', 'dob', 'starting_date']
    inlines = [ParentInline]


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_number']


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['resource_type', 'description', 'file', 'image', 'url']
