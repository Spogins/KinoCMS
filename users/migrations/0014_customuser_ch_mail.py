# Generated by Django 4.1.1 on 2022-11-08 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_alter_customuser_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='ch_mail',
            field=models.BooleanField(default=False),
        ),
    ]
