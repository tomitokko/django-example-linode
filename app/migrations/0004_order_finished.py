# Generated by Django 4.0.3 on 2022-03-12 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_order_amount_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='finished',
            field=models.BooleanField(default=False),
        ),
    ]
