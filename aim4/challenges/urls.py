from django.conf.urls import url, include
from django.urls import path


from .views import challenges, challenge_detail, challenge_join, challenge_refresh

urlpatterns = [

    path('', challenges, name='challenges',),

    url(r'^(?P<challenge_id>\d+)$', challenge_detail, name='challenge_detail'),
    url(r'^(?P<challenge_id>\d+)/join$', challenge_join, name='challenge_join'),
    url(r'^(?P<challenge_id>\d+)/refresh$', challenge_refresh, name='challenge_refresh'),

]



