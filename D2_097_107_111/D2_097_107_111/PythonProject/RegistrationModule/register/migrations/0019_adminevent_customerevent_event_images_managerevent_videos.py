# Generated by Django 3.0.2 on 2020-03-08 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0018_auto_20200308_2152'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('event_ID', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('event_name', models.CharField(max_length=30)),
                ('event_type', models.CharField(max_length=20)),
                ('event_duration', models.IntegerField()),
                ('event_time', models.TimeField()),
                ('event_date', models.DateField()),
                ('event_venue', models.CharField(max_length=15)),
                ('event_description', models.TextField()),
                ('ticket_price', models.IntegerField()),
                ('event_image', models.ImageField(upload_to='event-images')),
                ('event_contact_no', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('more_videos', models.FileField(upload_to='more-videos')),
                ('event_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Event')),
            ],
        ),
        migrations.CreateModel(
            name='ManagerEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_event_status', models.CharField(max_length=15)),
                ('event_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Event')),
                ('m_username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Manager')),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('more_images', models.ImageField(upload_to='more-images')),
                ('event_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Event')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_status', models.CharField(max_length=15)),
                ('c_username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Customer')),
                ('event_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Event')),
            ],
        ),
        migrations.CreateModel(
            name='AdminEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AD_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Admin')),
                ('event_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Event')),
            ],
        ),
    ]
