# Generated by Django 2.1.4 on 2021-09-24 06:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_auto_20210924_0239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrouserstory',
            name='user_story',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='registro_user_story', to='api.UserStory'),
        ),
    ]
