# Generated by Django 2.0.6 on 2018-10-24 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_auto_20181009_1252'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='hidden',
            field=models.BooleanField(default=False, verbose_name='Hidden'),
        ),
    ]