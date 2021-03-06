# Generated by Django 3.1.2 on 2020-10-09 11:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import student.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(default='user_default.jpg', upload_to=student.models.student_image)),
                ('birth_date', models.DateField()),
                ('nationality', django_countries.fields.CountryField(max_length=2)),
                ('phone', models.CharField(max_length=14, unique=True)),
                ('address', models.CharField(max_length=256)),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female')], max_length=8)),
                ('admission_date', models.DateField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
            },
        ),
    ]
