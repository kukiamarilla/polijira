# Generated by Django 2.1.4 on 2021-10-11 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0042_merge_20211011_1216'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sprint',
            name='capacidad',
        ),
    ]
