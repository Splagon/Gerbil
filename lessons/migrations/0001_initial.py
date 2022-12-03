# Generated by Django 3.2.5 on 2022-12-03 18:56

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.EmailField(max_length=254, unique=True, validators=[django.core.validators.EmailValidator(message='Invalid email')], verbose_name='email')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('dateOfBirth', models.DateField(blank=True, max_length=8, null=True, verbose_name='Date of Birth')),
                ('is_staff', models.BooleanField(verbose_name='Admin Status')),
                ('is_superuser', models.BooleanField(verbose_name='Director Status')),
                ('balance', models.FloatField(default=0.0)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_reference_number', models.CharField(max_length=100)),
                ('invoice_number', models.CharField(max_length=50)),
                ('student_id', models.IntegerField(default=0)),
                ('paid', models.BooleanField(default=False)),
                ('amount', models.FloatField(default=0.0)),
                ('currently_paid', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='SchoolBankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDate', models.DateField(default=datetime.date.today, unique=True)),
                ('endDate', models.DateField(default=datetime.date.today, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('availability_date', models.DateField(default=django.utils.timezone.now)),
                ('availability_time', models.TimeField(default='08:00')),
                ('number_of_lessons', models.CharField(max_length=3)),
                ('interval_between_lessons', models.CharField(max_length=3)),
                ('duration_of_lessons', models.CharField(choices=[('30', '30'), ('45', '45'), ('60', '60')], max_length=4)),
                ('instrument', models.CharField(blank=True, choices=[('violin', 'violin'), ('double bass', 'double bass'), ('cello', 'cello')], max_length=180)),
                ('teacher', models.CharField(blank=True, max_length=50)),
                ('status', models.CharField(default='In Progress', max_length=50)),
                ('totalPrice', models.CharField(default=0, max_length=50)),
                ('requesterId', models.IntegerField(default=0)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BankTransfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(max_length=50)),
                ('amount', models.FloatField(default=0)),
                ('student_id', models.IntegerField(default=0)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
