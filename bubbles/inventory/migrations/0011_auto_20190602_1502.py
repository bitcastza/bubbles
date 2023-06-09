# Generated by Django 2.1.5 on 2019-06-02 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0010_auto_20190219_0841"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bcd",
            name="size",
            field=models.CharField(
                choices=[
                    ("2XS", "Extra extra small"),
                    ("XS", "Extra small"),
                    ("S", "Small"),
                    ("M", "Medium"),
                    ("ML", "Medium large"),
                    ("L", "Large"),
                ],
                max_length=3,
                verbose_name="Size",
            ),
        ),
    ]
