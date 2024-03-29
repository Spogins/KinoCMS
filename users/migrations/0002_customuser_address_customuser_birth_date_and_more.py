# Generated by Django 4.1.1 on 2022-11-05 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='address',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='birth_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='card_number',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='gender',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='language',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
