# Generated by Django 3.1.2 on 2020-10-12 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0007_auto_20201012_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='recruitment_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
