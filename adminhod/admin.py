from django.contrib import admin

from .models import AdminHOD

class AdminHODAdmin(admin.ModelAdmin):
    """
    Override the AdminHOD admin and customize the AdminHOD display.
    """
    class Meta:
        model = AdminHOD

# models admin site registeration. 
admin.site.register(AdminHOD, AdminHODAdmin)
