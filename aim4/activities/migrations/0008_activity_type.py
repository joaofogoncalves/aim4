# Generated by Django 3.1.7 on 2021-03-08 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0007_auto_20210308_0956'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='type',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
