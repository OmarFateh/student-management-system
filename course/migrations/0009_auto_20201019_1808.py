# Generated by Django 3.1.2 on 2020-10-19 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0009_auto_20201012_1830'),
        ('course', '0008_auto_20201018_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='staff',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subject', to='staff.staff'),
        ),
    ]
