from django.contrib import admin

from .models import Challenge, Membership



@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['target_name', 'start_date', 'distance', 'created', 'updated']
    readonly_fields = ['distance', 'eta']


@admin.register(Membership)
class Membership(admin.ModelAdmin):
    list_display = ['member', 'challenge', 'created', 'updated']
    list_filter = ['challenge']
