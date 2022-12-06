# Generated by Django 4.1.1 on 2022-12-03 17:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0003_adultchildrelationship'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='unique_reference_number',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='term',
            name='endDate',
            field=models.DateField(default=datetime.date.today, unique=True),
        ),
        migrations.AlterField(
            model_name='term',
            name='startDate',
            field=models.DateField(default=datetime.date.today, unique=True),
        ),
    ]
