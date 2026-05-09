from django.contrib import admin
from .models import Staff, Child, Parent, Resource

# Register your models here.

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    pass


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    pass


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    pass


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    pass
