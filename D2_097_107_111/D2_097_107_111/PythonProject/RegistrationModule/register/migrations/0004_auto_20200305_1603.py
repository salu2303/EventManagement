# Generated by Django 3.0.2 on 2020-03-05 10:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0003_customerevent_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerevent',
            name='event_ID',
        ),
        migrations.DeleteModel(
            name='Event',
        ),
    ]