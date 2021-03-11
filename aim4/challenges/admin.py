from django.contrib import admin

from .models import Challenge, Membership, Contribution



@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['target_name', 'start_date', 'distance', 'created', 'updated']
    readonly_fields = ['distance', 'eta', 'velocity']


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ['member', 'challenge', 'created', 'updated']
    list_filter = ['challenge', ]
    search_fields = ['member']

@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ['activity', 'challenge', 'notified', 'created', 'updated']
    list_filter = ['challenge']
    search_fields = ['activity']