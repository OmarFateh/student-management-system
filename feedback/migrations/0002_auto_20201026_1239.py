# Generated by Django 3.1.2 on 2020-10-26 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedbackstaff',
            name='is_seen',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feedbackstudent',
            name='is_seen',
            field=models.BooleanField(default=False),
        ),
    ]
