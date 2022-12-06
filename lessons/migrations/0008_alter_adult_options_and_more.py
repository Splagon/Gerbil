# Generated by Django 4.1.1 on 2022-12-06 14:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0007_merge_20221206_1359'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='adult',
            options={'verbose_name': 'Adult'},
        ),
        migrations.AlterField(
            model_name='adultchildrelationship',
            name='adult',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adult', to='lessons.adult'),
        ),
        migrations.AlterField(
            model_name='adultchildrelationship',
            name='child',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_adult',
            field=models.BooleanField(default=True, verbose_name='Adult Status'),
        ),
    ]
