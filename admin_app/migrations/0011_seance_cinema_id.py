# Generated by Django 4.1.1 on 2022-12-02 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0010_alter_seance_date_alter_seance_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='seance',
            name='cinema_id',
            field=models.IntegerField(null=True),
        ),
    ]
