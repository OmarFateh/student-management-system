# Generated by Django 3.1.2 on 2020-10-09 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='admission_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]