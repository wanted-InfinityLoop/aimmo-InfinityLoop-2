# Generated by Django 3.2.8 on 2021-10-20 00:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('postings', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='Posting',
        ),
    ]
