# Generated by Django 3.1.2 on 2020-10-27 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0002_auto_20201026_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedbackstaff',
            name='is_replied',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feedbackstudent',
            name='is_replied',
            field=models.BooleanField(default=False),
        ),
    ]