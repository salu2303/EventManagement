# Generated by Django 3.0.2 on 2020-03-14 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0023_bookevent'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BookEvent',
        ),
        migrations.RemoveField(
            model_name='event',
            name='ticket_price',
        ),
        migrations.DeleteModel(
            name='CustomerEvent',
        ),
    ]