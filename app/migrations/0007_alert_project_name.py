# Generated by Django 4.0.3 on 2022-05-28 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alert_current_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='project_name',
            field=models.CharField(default='trippin_ape_tribe', max_length=1000),
            preserve_default=False,
        ),
    ]
