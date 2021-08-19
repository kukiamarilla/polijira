# Generated by Django 2.1.4 on 2021-08-18 23:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('api', '0006_usuario_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permiso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='', max_length=255)),
                ('codigo', models.CharField(default='', max_length=255)),
                ('permission', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.Permission')),
            ],
        ),
    ]
