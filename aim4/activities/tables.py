import django_tables2 as tables

class ActivityTable(tables.Table):

    class Meta:
        # model = Activity
        template_name = "django_tables2/bootstrap4.html"

    member = tables.Column(verbose_name='User')
    type = tables.Column(orderable=True)
    name = tables.Column(orderable=True)
    distance = tables.Column(orderable=True, attrs={'td':{'class':'right'}})
    duration = tables.Column(orderable=True)
    date = tables.Column(orderable=True)

    def render_member(self, value):
        return value.get_full_name()
