from django.contrib import admin
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'project', 'create_at')
    list_filter = ('project',)
    search_fields = ('name', 'email', 'phone')


