# Generated by Django 4.1.2 on 2022-12-07 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0007_alter_adult_options_alter_term_enddate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='instrument',
            field=models.CharField(blank=True, choices=[('Violin', 'Violin'), ('Double Bass', 'Double Bass'), ('Cello', 'Cello'), ('Keyboard', 'Keyboard'), ('Piano', 'Piano'), ('Trumpet', 'Trumpet'), ('Other', 'Other')], max_length=180),
        ),
    ]
