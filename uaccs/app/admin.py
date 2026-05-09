from django.contrib import admin
from .models import Staff, Child, Parent, Resource

# Register your models here.
"""
Admin Classes specify how models are layed out on Admin site.
"""

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'email', 'photo', 'bio']


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    pass


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    pass


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    pass
