# Generated by Django 2.1.4 on 2021-09-18 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20210915_0518'),
    ]

    operations = [
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lunes', models.IntegerField(default=0)),
                ('martes', models.IntegerField(default=0)),
                ('miercoles', models.IntegerField(default=0)),
                ('jueves', models.IntegerField(default=0)),
                ('viernes', models.IntegerField(default=0)),
                ('sabado', models.IntegerField(default=0)),
                ('domingo', models.IntegerField(default=0)),
            ],
        ),
    ]
