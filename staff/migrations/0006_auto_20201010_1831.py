# Generated by Django 3.1.2 on 2020-10-10 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0005_auto_20201010_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='birth_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='recruitment_date',
            field=models.DateField(null=True),
        ),
    ]
