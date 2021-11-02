# Generated by Django 3.2.8 on 2021-10-20 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postings', '0002_rename_user_posting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posting',
            name='text',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='posting',
            name='title',
            field=models.CharField(default='', max_length=128),
        ),
    ]
