from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from aim4.challenges.models import Challenge

@login_required
def challenges(request):
    context = {}

    challenges = request.user.challenges.all()

    public_challenges = Challenge.objects.filter(public=True).exclude(id__in=challenges )


    context['challenges'] = challenges
    context['public_challenges'] = public_challenges

    return render(request, 'list.html',  context=context)

@login_required
def challenge_detail(request, challenge_id):
    try:
        challenge = Challenge.objects.get(pk=challenge_id)
        user_challenges_ids = request.user.challenges.all().values_list('id', flat=True)

        if not challenge.public:
            if challenge.id not in user_challenges_ids:
                return redirect(to='/challenges/')
        else:
            if challenge.id in user_challenges_ids:
                is_member = True
            else:
                is_member = False

        if challenge.owner and challenge.owner.id == request.user.id:
            is_owner = True
        else:
            is_owner = False

    except Challenge.DoesNotExist:
        # If no Post has id post_id, we raise an HTTP 404 error.
        raise Http404
    return render(request, 'challenge/detail.html', {'challenge': challenge, 'is_member': is_member, 'is_owner': is_owner})

@login_required
def challenge_join(request, challenge_id):
    try:
        challenge = Challenge.objects.get(pk=challenge_id)

        challenge.join_member(request.user)

    except Challenge.DoesNotExist:
        # If no Post has id post_id, we raise an HTTP 404 error.
        raise Http404

    return redirect(to=f'/challenges/{challenge.id}')

@login_required
def challenge_refresh(request, challenge_id):
    try:
        challenge = Challenge.objects.get(pk=challenge_id)

        if challenge.owner and challenge.owner.id == request.user.id:
            challenge.refresh()

    except Challenge.DoesNotExist:
        # If no Post has id post_id, we raise an HTTP 404 error.
        raise Http404

    return redirect(to=f'/challenges/{challenge.id}')

