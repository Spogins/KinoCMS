# Generated by Django 4.1.1 on 2022-11-10 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_customuser_ch_mail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='ch_mail',
        ),
    ]
