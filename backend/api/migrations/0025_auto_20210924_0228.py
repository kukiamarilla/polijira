# Generated by Django 2.1.4 on 2021-09-24 02:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_auto_20210924_0227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstory',
            name='desarrollador',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_stories', to='api.Miembro'),
        ),
    ]