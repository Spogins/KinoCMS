# Generated by Django 4.1.5 on 2023-01-04 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0036_alter_cinemacontact_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cinemacontact',
            name='location',
            field=models.URLField(max_length=1000),
        ),
    ]
