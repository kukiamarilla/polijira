# Generated by Django 2.1.4 on 2021-09-20 06:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_miembro_horario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='miembro',
            name='horario',
        ),
        migrations.AddField(
            model_name='horario',
            name='miembro',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Miembro'),
        ),
    ]