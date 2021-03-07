from django.db import models
from aim4.mixins import BaseModel
from aim4.users.models import User
from aim4.activities.models import Activity

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
    target_date = models.DateField('Target date', null=True, blank=True)
    target_distance = models.IntegerField(default=0, null=False, blank=False)
    start_date = models.DateField('Start date', null=False, blank=False)
    public = models.BooleanField('Public', default=False)

    join_type = models.CharField(max_length=2, choices=JoinTypes.choices,default=JoinTypes.OPEN )

    members = models.ManyToManyField(User, through='Membership', related_name='challenges')

    distance = models.IntegerField(default=0, null=False, blank=False)
    eta = models.DateField('ETA', null=True, blank=True)


    def __str__(self):
        return self.target_name

class Membership(BaseModel):

    member = models.ForeignKey(User, related_name='memberships', on_delete=models.CASCADE, null=False, blank=False)
    challenge = models.ForeignKey(Challenge, related_name='memberships', on_delete=models.CASCADE, null=False, blank=False)
    approved = models.BooleanField(default=True)

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