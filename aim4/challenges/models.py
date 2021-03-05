from django.db import models
from aim4.mixins import BaseModel
from aim4.users.models import User

class Challenge(BaseModel):

    class Meta:
        verbose_name_plural = 'Challenges'
        ordering = ['target_name']

    target_name = models.CharField('Target', max_length=250, null=False, blank=False)
    start_date = models.DateField('Start date', null=False, blank=False)
    target_date = models.DateField('Target date', null=True, blank=True)

    members = models.ManyToManyField(User, through='Membership', related_name='challenges')

    distance = models.IntegerField(default=0, null=False, blank=False)
    eta = models.DateField('ETA', null=True, blank=True)


    def __str__(self):
        return self.target_name

class Membership(BaseModel):

    member = models.ForeignKey(User, related_name='memberships', on_delete=models.CASCADE, null=True)
    challenge = models.ForeignKey(Challenge, related_name='memberships', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Memberships'

    def __str__(self):
        return f'{self.member} - {self.challenge}'
