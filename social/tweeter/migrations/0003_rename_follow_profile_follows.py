# Generated by Django 5.1.2 on 2024-10-23 00:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweeter', '0002_profile_date_modified'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='follow',
            new_name='follows',
        ),
    ]
