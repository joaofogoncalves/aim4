from django.db import models
from aim4.mixins import BaseModel
from aim4.users.models import User
from aim4.activities.models import Activity
from django.utils import timezone
from django.conf import settings

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

    def __str__(self):
        return self.target_name

    def create_activities_for_member(self, member, refresh=False):
        activities = member.get_activities_from_date(from_date=self.start_date, refresh=refresh)

        for activity in activities:
            self.activities.add(activity)

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

            self.velocity = velocity
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

    class Meta:
        verbose_name_plural = 'Memberships'

    def __str__(self):
        return f'{self.member} - {self.challenge}'

class Contribution(BaseModel):

    challenge = models.ForeignKey(Challenge, related_name='contributions', on_delete=models.CASCADE, null=False, blank=False)
    activity = models.ForeignKey(Activity, related_name='contributions', on_delete=models.CASCADE, null=False, blank=False)


    class Meta:
        verbose_name_plural = 'Contributions'

    def __str__(self):
        return f'{self.activity} - {self.challenge}'