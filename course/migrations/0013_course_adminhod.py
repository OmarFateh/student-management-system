# Generated by Django 3.1.2 on 2020-11-18 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminhod', '0001_initial'),
        ('course', '0012_auto_20201109_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='adminhod',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses', to='adminhod.adminhod'),
        ),
    ]