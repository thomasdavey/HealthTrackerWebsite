# Generated by Django 2.2 on 2019-05-05 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_auto_20190505_0311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caloriecount',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]