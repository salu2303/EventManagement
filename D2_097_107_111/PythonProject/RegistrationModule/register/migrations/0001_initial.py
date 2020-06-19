# Generated by Django 3.0.2 on 2020-03-02 16:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('AD_ID', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('AD_password', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('c_username', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('c_name', models.CharField(max_length=30)),
                ('c_address', models.CharField(max_length=50)),
                ('c_mobileno', models.IntegerField()),
                ('c_email', models.CharField(max_length=30)),
                ('c_password', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('event_ID', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('event_type', models.CharField(max_length=20)),
                ('event_duration', models.IntegerField()),
                ('event_time', models.TimeField()),
                ('event_date', models.DateField()),
                ('event_venue', models.CharField(max_length=15)),
                ('event_description', models.TextField()),
                ('ticket_price', models.IntegerField()),
                ('previous_event_image_filelocation', models.ImageField(height_field='65', upload_to='images', width_field='65')),
                ('event_video_filelocation', models.ImageField(upload_to='')),
                ('event_contact_no', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('m_username', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('m_name', models.CharField(max_length=30)),
                ('m_address', models.CharField(max_length=50)),
                ('m_mobileno', models.IntegerField()),
                ('m_email', models.CharField(max_length=30)),
                ('m_event_type', models.CharField(max_length=15)),
                ('m_password', models.CharField(max_length=20)),
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
    ]