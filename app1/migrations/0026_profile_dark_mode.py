# Generated by Django 3.0.3 on 2020-06-29 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0025_profile_default_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='dark_mode',
            field=models.BooleanField(default=False),
        ),
    ]
