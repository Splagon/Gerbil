# Generated by Django 4.1.2 on 2022-11-30 17:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='availability_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
