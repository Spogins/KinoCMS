# Generated by Django 4.1.1 on 2022-11-08 12:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_customuser_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterUniqueTogether(
            name='customuser',
            unique_together=set(),
        ),
    ]
