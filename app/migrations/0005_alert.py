# Generated by Django 4.0.3 on 2022-05-28 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_order_finished'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('above_or_below', models.CharField(max_length=1000)),
                ('price', models.FloatField()),
                ('email', models.CharField(max_length=1000)),
            ],
        ),
    ]