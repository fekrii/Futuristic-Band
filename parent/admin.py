from django.contrib import admin
from .models import ParentProfile


class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'firstName', 'lastName', 'parent_type', 'birthDate',
                    'address', 'jobTitle', 'nationality', 'created_at', 'updated_at')

admin.site.register(ParentProfile, ParentProfileAdmin)