# Generated by Django 4.1.1 on 2022-12-13 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0018_alter_seance_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seance',
            name='date',
            field=models.DateField(max_length=300, null=True),
        ),
    ]
