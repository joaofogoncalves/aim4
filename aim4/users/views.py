from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect

from social_django.utils import load_strategy
from datetime import datetime
from social_django.models import UserSocialAuth

import requests
from stravalib.client import Client

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from datetime import datetime

from units import scaled_unit

@login_required
def home(request):

    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    activities = []
    strava_connected = True

    try:
        strava_social = request.user.social_auth.get(provider='strava')
    except UserSocialAuth.DoesNotExist:
        strava_connected = False


    if from_date or to_date:
        if from_date:
            from_datetime = datetime.strptime(from_date + " 00:00:00", "%d/%m/%Y %H:%M:%S")
        if to_date:
            to_datetime = datetime.strptime(to_date + " 23:59:59", "%d/%m/%Y %H:%M:%S")

        page = request.GET.get('page')

        # get access token
        strava_social = request.user.social_auth.get(provider='strava')
        token = strava_social.get_access_token(load_strategy())

        # get activity details
        client = Client()
        client.access_token = token


        if from_date and to_date:
            query = client.get_activities(before=to_datetime, after=from_datetime)
        elif from_date:
            query = client.get_activities(after=from_datetime)
        else: # to_date
            query = client.get_activities(before=to_datetime)

        km = scaled_unit('km', 'm', 1000) # define a new unit

        for activity in query:
            if from_date and not to_date:
                index = 0
            else:
                index = len(activities)

            activities.insert(index,
                {
                    "id": activity.id,
                    "name": activity.name,
                    "distance": km(activity.distance),
                    "type": activity.type,
                    "link": "https://www.strava.com/activities/{}".format(activity.id),
                    "date": activity.start_date_local,
                }
            )

        paginator = Paginator(activities, 20) # Show n results per page
        try:
            activities = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            activities = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            activities = paginator.page(paginator.num_pages)

    return render(request, 'home.html',
                            context={
                                'activities': activities,
                                'from_date': from_date,
                                'to_date': to_date,
                                'strava_connected': strava_connected,
                            })


@login_required
def profile(request):
    context = {}
    if request.GET:
        pass
    elif request.POST:
        pass

    return render(request, 'profile.html',context=context)

@login_required
def settings(request):
    context = {}
    if request.GET:
        pass
    elif request.POST:
        pass

    return render(request, 'settings.html',context=context)