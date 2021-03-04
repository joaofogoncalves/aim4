from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect

from social_django.models import UserSocialAuth

import requests


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



@login_required
def home(request):


    return render(request, 'home.html',
                            context={})