from django.db import models
from aim4.mixins import BaseModel
from aim4.users.models import User
from aim4.activities.models import Activity
from django.utils import timezone
from django.conf import settings
import requests
import json

from datetime import timedelta
class Challenge(BaseModel):

    class JoinTypes(models.TextChoices):
        OPEN = 'OP', 'Open'
        APPROVAL = 'AP', 'Approval'
        INVITE = 'IN', 'Invite'
        CLOSED = 'CL', 'Closed'

    class Meta:
        verbose_name_plural = 'Challenges'
        ordering = ['target_name']

    target_name = models.CharField('Target', max_length=250, null=False, blank=False)
    target_date = models.DateTimeField('Target date', null=True, blank=True)
    target_distance = models.IntegerField('Target distance in Km', default=0, null=False, blank=False)
    start_date = models.DateTimeField('Start date', null=False, blank=False)
    public = models.BooleanField('Public', default=False)
    description = models.TextField('Description', null=True, blank=True)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='challenges_owner', null=True, blank=True, on_delete=models.SET_NULL,)

    join_type = models.CharField(max_length=2, choices=JoinTypes.choices,default=JoinTypes.OPEN )

    members = models.ManyToManyField(User, through='Membership', related_name='challenges')
    activities = models.ManyToManyField(Activity, through='Contribution', related_name='challenges')

    distance = models.FloatField('Distance in m', default=0, null=False, blank=False)
    eta = models.DateTimeField('ETA', null=True, blank=True)
    velocity = models.FloatField('Velocity in m/s', default=0, null=False, blank=False)

    # Slack fields
    slack_channel = models.CharField(max_length=255, null=True, blank=True)
    slack_endpoint_url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.target_name

    def create_activities_for_member(self, member, refresh=False):
        activities = member.get_activities_from_date(from_date=self.start_date, refresh=refresh)

        self.activities.add(*activities)

    def update_distance(self, force=False):
        inicial_distance = 0
        for activity in self.activities.all():
            inicial_distance += activity.distance

        self.distance = inicial_distance
        if force:
            self.save()

    def update_needed_velocity(self, force=False):
        #TODO calculate needed speed going forward
        if force:
            self.save()

    def update_eta(self, force=False):
        if self.distance > 0:
            seconds_gone = (timezone.now()-self.start_date).total_seconds()
            velocity = self.distance/seconds_gone #in m/s

            missing_distance = (self.target_distance*1000)-self.distance #Bad but needed for now untill target can be set in different units

            seconds_to_target =  missing_distance/velocity

            self.velocity = round(velocity, 5)
            self.eta = self.start_date+timedelta(seconds=seconds_to_target)
        else:
            self.velocity = 0
            self.eta = None

        if force:
            self.save()

    def update_calculated_fields(self, force=True):
        self.update_distance()
        self.update_eta()

        if self.target_date:
            self.update_needed_velocity()

        if force:
            self.save()

    def join_member(self, member):
        if self.join_type == self.JoinTypes.CLOSED:
            return

        if self.join_type == self.JoinTypes.OPEN:
            self.members.add(member)
            self.create_activities_for_member(member)
            self.update_calculated_fields()

        #TODO other join methods

    def refresh(self):
        for member in self.members.all():
            self.create_activities_for_member(member, refresh=True)

        self.update_calculated_fields()

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)



class Membership(BaseModel):

    member = models.ForeignKey(User, related_name='memberships', on_delete=models.CASCADE, null=False, blank=False)
    challenge = models.ForeignKey(Challenge, related_name='memberships', on_delete=models.CASCADE, null=False, blank=False)

    #TODO fields to save invite and approval logic
    # TODO fields to have member/admin logic

    class Meta:
        verbose_name_plural = 'Memberships'

    def __str__(self):
        return f'{self.member} - {self.challenge}'

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

class Contribution(BaseModel):

    challenge = models.ForeignKey(Challenge, related_name='contributions', on_delete=models.CASCADE, null=False, blank=False)
    activity = models.ForeignKey(Activity, related_name='contributions', on_delete=models.CASCADE, null=False, blank=False)
    notified = models.BooleanField('Notification Sent', default=False)

    class Meta:
        verbose_name_plural = 'Contributions'

    def __str__(self):
        return f'{self.activity} - {self.challenge}'


from django.dispatch import receiver
from django.db.models.signals import m2m_changed, post_save


@receiver(post_save, sender=Contribution)
def authorship_changed(sender, instance, **kwargs):
    print("authors changed")

@receiver(m2m_changed, sender=Challenge.activities.through, dispatch_uid='notify_slack')
def notify_slack(sender, instance, action, reverse, model, pk_set, **kwarg):
    """"""
    if action in ["post_add"] :
        activities = Activity.objects.filter(id__in = pk_set)
        for activity in activities:
            challenge = instance

            if challenge and activity and challenge.slack_endpoint_url:
                message_dict = {
                    "channel": challenge.slack_channel,
                    "attachments": [
                        {
                            "color": "#36a64f",
                            "author_name": activity.member.get_full_name() if activity.member else '',
                            "title": activity.name,
                            "text": f"on {aim4_date_format(activity.date)}",
                            "fields": [
                                { "title": "Type",  "value": activity.type, "short": True },
                                { "title": "Distance",  "value": f"{activity.distance}m", "short": True },
                                { "title": "Duration",  "value": aim4_duration_format(activity.duration), "short": True }
                            ],
                            "footer": "<https://aim4.live|aim4.live>"
                        }
                    ]

                }
                reponse = requests.post(url=challenge.slack_endpoint_url, data=json.dumps(message_dict))


def aim4_date_format(date):
    return date.strftime('%A, %B %d, %Y at %H:%M')

def aim4_duration_format(td):

    total_seconds = int(td.total_seconds())

    days = total_seconds // 86400
    remaining_hours = total_seconds % 86400
    remaining_minutes = remaining_hours % 3600
    hours = remaining_hours // 3600
    minutes = remaining_minutes // 60
    seconds = remaining_minutes % 60

    days_str = f'{days}d ' if days else ''
    hours_str = f'{hours}h ' if hours else ''
    minutes_str = f'{minutes}m ' if minutes else ''
    seconds_str = f'{seconds}s' if seconds and not hours_str else ''

    return f'{days_str}{hours_str}{minutes_str}{seconds_str}'
