# Generated by Django 2.1.4 on 2021-09-26 01:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_auto_20210925_0714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productbacklog',
            name='proyecto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_backlogs', to='api.Proyecto'),
        ),
    ]
