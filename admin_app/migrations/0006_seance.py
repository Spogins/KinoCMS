# Generated by Django 4.1.1 on 2022-12-01 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0005_alter_mailingtemplate_html_template'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True)),
                ('time', models.DateTimeField(null=True)),
                ('ticket_price', models.IntegerField(null=True)),
                ('halls_id', models.IntegerField(null=True)),
                ('films_id', models.IntegerField(null=True)),
            ],
        ),
    ]
