from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from aim4.challenges.models import Challenge

@login_required
def challenges(request):
    context = {}

    challenges = request.user.challenges.all()
    public_challenges = Challenge.objects.filter(public=True)


    context['challenges'] = challenges
    context['public_challenges'] = public_challenges

    return render(request, 'list.html',  context=context)