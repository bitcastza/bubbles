# Generated by Django 2.2.7 on 2019-11-19 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rentals", "0014_auto_20191028_1052"),
    ]

    operations = [
        migrations.AlterField(
            model_name="requestitem",
            name="item_number",
            field=models.CharField(
                blank=True, max_length=5, null=True, verbose_name="Number"
            ),
        ),
    ]
