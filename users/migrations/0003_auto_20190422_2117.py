# Generated by Django 2.2 on 2019-04-22 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_weightgoal_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weightgoal',
            name='start_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
