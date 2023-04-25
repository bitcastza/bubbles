# Generated by Django 3.2.18 on 2023-03-23 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0017_auto_20220920_0841"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="id",
            field=models.SmallAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="itemvalue",
            name="id",
            field=models.SmallAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="weight",
            name="id",
            field=models.SmallAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="weightbelt",
            name="id",
            field=models.SmallAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]