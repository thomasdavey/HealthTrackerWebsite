# Generated by Django 2.2 on 2019-05-07 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190422_2117'),
    ]

    operations = [
        migrations.AddField(
            model_name='weightgoal',
            name='start_weight',
            field=models.IntegerField(null=True),
        ),
    ]