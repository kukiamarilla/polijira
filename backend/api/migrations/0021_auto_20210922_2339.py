# Generated by Django 2.1.4 on 2021-09-22 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_auto_20210920_0720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plantillarolproyecto',
            name='nombre',
            field=models.CharField(default='', max_length=255, unique=True),
        ),
    ]
