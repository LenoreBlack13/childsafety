from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'date_posted')
    search_fields = ('user__username', 'review')
    list_filter = ('rating', 'date_posted')
    ordering = ('-date_posted',)
