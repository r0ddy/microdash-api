# Generated by Django 4.0.3 on 2022-04-10 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryagent',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=5.0, max_digits=4),
        ),
    ]
