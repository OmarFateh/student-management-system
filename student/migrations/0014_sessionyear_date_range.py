# Generated by Django 3.1.2 on 2020-11-04 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0013_auto_20201018_2256'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessionyear',
            name='date_range',
            field=models.CharField(max_length=24, null=True),
        ),
    ]
