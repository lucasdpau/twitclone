# Generated by Django 3.0.3 on 2020-06-25 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0024_profile_is_private'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='default_page',
            field=models.CharField(default='all', max_length=20),
        ),
    ]
