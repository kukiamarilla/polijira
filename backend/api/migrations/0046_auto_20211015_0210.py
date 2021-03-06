# Generated by Django 2.1.4 on 2021-10-15 02:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0045_merge_20211015_0206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstory',
            name='desarrollador',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_stories', to='api.MiembroSprint'),
        ),
        migrations.AlterField(
            model_name='userstory',
            name='estado_estimacion',
            field=models.CharField(choices=[('N', 'No estimado'), ('p', 'Parcial'), ('C', 'Completo'), ('P', 'Pendiente')], default='P', max_length=1),
        ),
        migrations.AlterField(
            model_name='userstory',
            name='horas_estimadas',
            field=models.IntegerField(default=0),
        ),
    ]
