# Generated by Django 2.2 on 2019-05-05 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_caloriecount_exercise_food'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caloriecount',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
