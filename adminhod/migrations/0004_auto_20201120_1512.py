# Generated by Django 3.1.2 on 2020-11-20 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminhod', '0003_auto_20201120_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminhod',
            name='education',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='adminhod',
            name='skills',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]