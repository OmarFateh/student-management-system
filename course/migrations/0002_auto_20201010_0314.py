# Generated by Django 3.1.2 on 2020-10-10 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='code',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='code',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
