from random import shuffle

from django.contrib.auth.decorators import login_required
from django.http.response import Http404
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.db.models.functions import TruncDate
#from aim4.aim4.activities.tables import ActivityTable
from chartjs.views.lines import BaseLineChartView
from chartjs.colors import COLORS, next_color

from aim4.activities.models import Activity
from aim4.activities.tables import ActivityTable
from aim4.challenges.models import Challenge, Membership


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
        print(challenge.owner, challenge.owner.id, request.user.id)

        if not challenge.public:
            if challenge.id not in user_challenges_ids:
                return redirect(to='/challenges/')

        is_member = challenge.id in user_challenges_ids

        if challenge.owner and challenge.owner.id == request.user.id:
            is_owner = True
        else:
            is_owner = False

        if is_member:
            #table=MembersTable(challenge.activities.all())
            table = ActivityTable(challenge.activities.all())
            table.order_by = request.GET.get('sort', '-date')
            table.paginate(page=request.GET.get("page", 1), per_page=25)
        else:
            table = ActivityTable(Activity.objects.none())

    except Challenge.DoesNotExist:
        # If no Post has id post_id, we raise an HTTP 404 error.
        raise Http404

    return render(request, 'challenge/detail.html',
            {
                'challenge': challenge,
                'is_member': is_member,
                'is_owner': is_owner,
                'table': table,
            }
        )

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

@login_required
def challenge_refresh_membership(request, challenge_id, membership_id):
    try:
        challenge = Challenge.objects.get(pk=challenge_id)


        if challenge.owner and challenge.owner.id == request.user.id:
            challenge.refresh_membership(membership_id)

    except Challenge.DoesNotExist:
        # If no Post has id post_id, we raise an HTTP 404 error.
        raise Http404


    return redirect(to=f'/challenges/{challenge.id}')

class LineChartJSONView(BaseLineChartView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dist_data = challenge_distance_chart_data(Challenge.objects.get(id=1))

        context["labels"] = dist_data[0]
        context["datasets"] = self.set_dataset_data([dist_data[1]])
        return context

    def set_dataset_data(self, data):
        """ overwrite default method to pass the data"""
        datasets = []
        color_generator = self.get_colors()
        providers = self.get_providers()
        num = len(providers)
        for i, entry in enumerate(data):
            color = tuple(next(color_generator))
            dataset = {"data": entry}
            dataset.update(self.get_dataset_options(i, color))
            if i < num:
                dataset["label"] = providers[i]  # series labels for Chart.js
                dataset["name"] = providers[i]  # HighCharts may need this
            datasets.append(dataset)
        return datasets

    def get_colors(self):
        """Return a new shuffle list of color so we change the color
        each time."""
        colors = COLORS[:]
        shuffle(colors)
        return next_color(colors)

    def get_providers(self):
        """Return names of datasets."""
        return ["Daily distance"]

    def get_labels(self):
        """Return empty list, more efficient to get labels and data in the same function"""
        return []

    def get_data(self):
        """Return empty list, more efficient to get labels and data in the same function"""
        return []


line_chart_json = LineChartJSONView.as_view()

def challenge_distance_chart_data(challenge):
    """
    lineChart data
    """
    distance_by_date = challenge.activities.annotate(day=TruncDate('date')).\
        values('day').order_by('day').annotate(tot_dist=Sum('distance'))
    xdata = []
    ydata = []
    for data in distance_by_date:
        xdata += [data['day']]
        ydata += [data['tot_dist']]

    return xdata, ydata
