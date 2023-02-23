from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            'Custom Fields',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'phone',
                    'long',
                    'lat',
                ),
            },
        ),
    )
  

admin.site.register(User, CustomUserAdmin)

from django.contrib.admin.models import LogEntry
admin.site.register(LogEntry)