# Generated by Django 4.1.1 on 2022-11-21 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0002_alter_user_dateofbirth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dateOfBirth',
            field=models.DateField(blank=True, max_length=10, null=True),
        ),
    ]