# Generated by Django 3.1.2 on 2020-10-27 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('announcement', '0003_announcement_is_seen'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnnouncementSeenGroup',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('announcement.announcement',),
        ),
    ]