# Generated by Django 3.0.2 on 2020-04-25 20:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0028_auto_20200426_0138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerevent',
            name='c_username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Customer'),
        ),
    ]
