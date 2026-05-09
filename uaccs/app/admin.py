from django.contrib import admin
from .models import Staff, Child, Parent, Resource

# Register your models here.


class StaffAdmin(admin.ModelAdmin):
    pass

admin.site.register(Staff, StaffAdmin)


class ChildAdmin(admin.ModelAdmin):
    pass


admin.site.register(Child, ChildAdmin)


class ParentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Parent, ParentAdmin)


class ResourceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Resource, ResourceAdmin)