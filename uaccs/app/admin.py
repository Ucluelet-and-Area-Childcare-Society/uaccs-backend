from django.contrib import admin
from .models import Staff, Child, Parent, Resource

# Register your models here.

class StaffAdmin(admin.ModelAdmin):
    pass

class ChildAdmin(admin.ModelAdmin):
    pass

class ParentAdmin(admin.ModelAdmin):
    pass

class ResourceAdmin(admin.ModelAdmin):
    pass