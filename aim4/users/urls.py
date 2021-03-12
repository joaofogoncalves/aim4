from django.conf.urls import url, include
from django.urls import path


from .views import home, profile, settings

urlpatterns = [

    path('profile', profile, name='profile'),
    path('settings', settings, name='settings'),

]

