# Generated by Django 2.2.19 on 2021-05-17 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20210517_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
