from django.db import models
from aim4.mixins import BaseModel

# Create your models here.

TYPE_To_KMH = {
    "WeightTraining": 4,
    "Workout": 4,
    "Walk": 5,
    "Hike": 4,
    "Ride": 20
}


class Activity(BaseModel):
    class Meta:
        verbose_name_plural = 'Activities'
        ordering = ['date']

    member = models.ForeignKey('users.User', related_name='activities', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(null=False, blank=False)
    distance = models.FloatField(default=0, null=False, blank=False)
    duration = models.DurationField(default=0, null=False, blank=False)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    used_internal_conversion = models.BooleanField('Internal Distance Converted', default=False)
    internal_conversion_metric = models.FloatField(default=0, null=False, blank=False)

    #to detect and prevent duplicates
    provider = models.CharField(max_length=250, default='')
    original_id = models.BigIntegerField(unique=True)

    def __str__(self):
        return f'{self.name} - {self.date}'



    def update_distances(self, distance, force=False):


        if distance == 0 and TYPE_To_KMH[self.type]:
            print(f'update distance {TYPE_To_KMH[self.type]} {self.duration.seconds / 3600} ')
            self.used_internal_conversion = True
            self.internal_conversion_metric = TYPE_To_KMH[self.type]
            self.distance =  self.internal_conversion_metric * (self.duration.seconds / 3600)
        else:
            print(f'DONT update distance {distance}')
            self.distance = distance
            used_internal_conversion = False

        if force:
            print('---- saving')
            self.save()