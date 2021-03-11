from django.contrib import admin

from .models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['member', 'name', 'date', 'distance', 'created', 'updated']
    list_filter = ['member']
