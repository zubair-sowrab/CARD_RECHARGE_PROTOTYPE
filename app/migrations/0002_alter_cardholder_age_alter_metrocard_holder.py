# Generated by Django 5.1 on 2024-08-23 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardholder',
            name='age',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='metrocard',
            name='holder',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
