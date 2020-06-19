# Generated by Django 3.0.2 on 2020-03-07 05:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0008_customerevent_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManagerEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_event_status', models.CharField(max_length=15)),
                ('event_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Event')),
                ('m_username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Manager')),
            ],
        ),
    ]
