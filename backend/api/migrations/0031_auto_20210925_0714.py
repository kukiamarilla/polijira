# Generated by Django 2.1.4 on 2021-09-25 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_auto_20210924_0656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrouserstory',
            name='user_story',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registros', to='api.UserStory'),
        ),
    ]
