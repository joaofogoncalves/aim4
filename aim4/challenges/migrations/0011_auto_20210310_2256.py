# Generated by Django 3.1.7 on 2021-03-10 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0010_challenge_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='slack_channel',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='challenge',
            name='slack_endpoint_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
