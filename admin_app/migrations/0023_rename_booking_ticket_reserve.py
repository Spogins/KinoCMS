# Generated by Django 4.1.1 on 2022-12-17 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0022_ticket'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='booking',
            new_name='reserve',
        ),
    ]
