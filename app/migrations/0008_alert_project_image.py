# Generated by Django 4.0.3 on 2022-05-28 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alert_project_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='project_image',
            field=models.CharField(default='https://i.imgur.com/iFgvQva.png', max_length=1000),
            preserve_default=False,
        ),
    ]
