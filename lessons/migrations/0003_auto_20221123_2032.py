# Generated by Django 3.2.5 on 2022-11-23 20:32

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
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]