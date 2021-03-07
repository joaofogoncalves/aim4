from django.db import models
from aim4.mixins import BaseModel
from aim4.users.models import User

# Create your models here.

class Activity(BaseModel):
    class Meta:
        verbose_name_plural = 'Activities'
        ordering = ['date']

    member = models.ForeignKey(User, related_name='activities', on_delete=models.SET_NULL, null=True)
    date = models.DateField(null=False, blank=False)
    distance = models.IntegerField(default=0, null=False, blank=False)
    duration = models.DurationField(default=0, null=False, blank=False)
    name = models.CharField(max_length=250, null=True, blank=True)

    #to detect and prevent duplicates
    provider = models.CharField(max_length=250, default='')
    original_id = models.CharField(max_length=250, default='')

    def __str__(self):
        return f'{self.name} - {self.date}'