# Generated by Django 4.1.2 on 2022-11-30 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='status',
            field=models.CharField(default='In Progress', max_length=50),
        ),
        migrations.AddField(
            model_name='request',
            name='totalPrice',
            field=models.CharField(default=0, max_length=50),
        ),
    ]