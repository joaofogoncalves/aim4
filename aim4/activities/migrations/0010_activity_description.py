# Generated by Django 3.1.7 on 2021-07-05 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0009_auto_20210309_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
