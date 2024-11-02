from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'can_create_posts')
    list_filter = ('can_create_posts',)

admin.site.register(Profile)