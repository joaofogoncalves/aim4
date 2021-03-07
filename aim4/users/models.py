from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from social_django.utils import load_strategy
from datetime import datetime
from social_django.models import UserSocialAuth

import requests
from stravalib.client import Client

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from datetime import datetime

from units import scaled_unit

from aim4.activities.models import Activity


# -----------------------------------------------------------------------------
# User
# -----------------------------------------------------------------------------
class User(AbstractUser):
    """
    User based on the abstract base class that implements a fully
    featured User model with admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """

    relate_activities = models.BooleanField(default=True)

    def get_activities_from_date(self, from_date=None, refresh = True):
        if not refresh or not self.relate_activities:
            return self.activities.filter(date__gte=from_date)

        social_activities = []
        # FOR EACH SOCIAL ACCOUNT
        sport_providers = ['strava'] #Maybe later define somewhere else

        for social in self.social_auth.all():
            get_social_activities = getattr(self, f'get_{social.provider}_activities', None)
            if callable(get_social_activities):
                social_activities += get_social_activities(social, from_date)


        return social_activities

    def get_strava_activities(self, strava_social, from_date=None):
        new_activities = []
        provider_name = 'strava'
        existing_ids = self.activities.filter(provider=provider_name).values_list('original_id', flat=True)

        print(existing_ids)

        # get access token
        token = strava_social.get_access_token(load_strategy())

        # get activity details
        client = Client()
        client.access_token = token

        query = client.get_activities(after=from_date)

        km = scaled_unit('km', 'm', 1000) # define a new unit

        for strava_activity in query:
            print(strava_activity.id)
            strava_id = strava_activity.id
            if not strava_id in existing_ids:

                new_activity = Activity()

                new_activity.original_id = strava_id
                new_activity.provider = provider_name
                new_activity.date = strava_activity.start_date_local
                new_activity.distance = km(strava_activity.distance)
                new_activity.duration = strava_activity.elapsed_time
                new_activity.name = strava_activity.name


                if self.relate_activities:
                    new_activity.member = self

                new_activity.save()
            else:
                new_activity = self.activities.get(original_id=strava_id)

            new_activities.append(new_activity)

        return new_activities


    def has_read_permission(self, user):
        return user.is_staff or self.id == user.id

    def has_write_permission(self, user):
        """IMPORTANT: Only staff users can edit data from users."""
        return user.is_staff

