# Generated by Django 2.2.7 on 2019-11-19 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0015_auto_20190909_1527"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bcd",
            name="serial_num",
            field=models.CharField(max_length=255, verbose_name="Serial number"),
        ),
        migrations.AlterField(
            model_name="regulator",
            name="serial_num",
            field=models.CharField(max_length=255, verbose_name="Serial number"),
        ),
    ]
