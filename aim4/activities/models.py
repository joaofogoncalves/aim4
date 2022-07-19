from django.db import models
from aim4.mixins import BaseModel
from stravalib import unithelper

# Create your models here.

TYPE_To_KMH = {
    "WeightTraining": 4,
    "Workout": 4,
    "Walk": 5,
    "Hike": 4,
    "Ride": 20,
    "Surfing": 2,
    "Swim": 2,
    "Yoga": 2,
    "Run": 10
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

        distance_num_value = float(unithelper.meters(activity.distance))

        if distance_num_value == 0.0 and TYPE_To_KMH[self.type]:
            print(f'update distance {TYPE_To_KMH[self.type]} {self.duration.seconds / 3600} ')
            self.used_internal_conversion = True
            self.internal_conversion_metric = TYPE_To_KMH[self.type] #km/h

            #conversion is on km/h so need to convert to m/h and then get duration in hours
            self.distance = (self.internal_conversion_metric*1000) * (self.duration.seconds / 3600)
        else:
            print(f'DONT update distance {distance_num_value}')
            self.distance = distance_num_value
            used_internal_conversion = False

        if force:
            print('---- saving')
            self.save()