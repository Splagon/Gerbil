# Generated by Django 3.2.5 on 2022-11-28 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0006_alter_request_duration_of_lessons_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_number', models.CharField(max_length=12)),
                ('invoice_number', models.CharField(max_length=12)),
            ],
        ),
    ]
