# Generated by Django 3.1.7 on 2021-03-08 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0008_auto_20210308_0945'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membership',
            name='approved',
        ),
        migrations.AddField(
            model_name='challenge',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='distance',
            field=models.FloatField(default=0, verbose_name='Distance in m'),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='velocity',
            field=models.FloatField(default=0, verbose_name='Velocity in m/s'),
        ),
    ]
