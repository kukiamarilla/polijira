# Generated by Django 2.1.4 on 2021-08-14 03:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_usuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='admin',
        ),
    ]
