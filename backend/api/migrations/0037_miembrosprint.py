# Generated by Django 2.1.4 on 2021-10-03 22:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0036_sprintbacklog'),
    ]

    operations = [
        migrations.CreateModel(
            name='MiembroSprint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('miembro_proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='miembro_sprints', to='api.Miembro')),
                ('sprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='miembro_sprints', to='api.Sprint')),
            ],
        ),
    ]
