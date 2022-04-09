# Generated by Django 4.0.3 on 2022-04-09 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_fullmenu'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='time',
        ),
        migrations.AddField(
            model_name='menu',
            name='meal_period',
            field=models.IntegerField(choices=[(1, 'Breakfast'), (2, 'Lunch'), (3, 'Dinner')], default=None, null=True),
        ),
    ]
