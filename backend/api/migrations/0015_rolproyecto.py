# Generated by Django 2.1.4 on 2021-09-09 04:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_permisoproyecto_plantillarolproyecto'),
    ]

    operations = [
        migrations.CreateModel(
            name='RolProyecto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='', max_length=255)),
                ('permisos', models.ManyToManyField(to='api.PermisoProyecto')),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proyecto', to='api.Proyecto')),
            ],
        ),
    ]
