# Generated by Django 4.1.1 on 2022-11-06 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_customuser_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='card_number',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='language',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
