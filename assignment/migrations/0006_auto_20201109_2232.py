# Generated by Django 3.1.2 on 2020-11-09 20:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0014_sessionyear_date_range'),
        ('assignment', '0005_studentassignment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentassignment',
            name='assignment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assignment.assignment'),
        ),
        migrations.AlterField(
            model_name='studentassignment',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='student.student'),
        ),
    ]
