# Generated by Django 2.2.4 on 2019-11-19 14:47

import bubbles.inventory.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [
        ("inventory", "0001_initial"),
        ("inventory", "0002_auto_20180701_1342"),
        ("inventory", "0003_item_description"),
        ("inventory", "0004_auto_20180704_2133"),
        ("inventory", "0005_auto_20180711_1334"),
        ("inventory", "0006_auto_20181009_1252"),
        ("inventory", "0007_item_hidden"),
        ("inventory", "0008_auto_20181112_2338"),
        ("inventory", "0009_auto_20190107_1517"),
        ("inventory", "0010_auto_20190219_0841"),
        ("inventory", "0011_auto_20190602_1502"),
        ("inventory", "0012_item_free"),
    ]

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "number",
                    models.CharField(
                        default=bubbles.inventory.models.Item.get_next_number,
                        max_length=5,
                        verbose_name="Number",
                    ),
                ),
                (
                    "manufacturer",
                    models.CharField(max_length=255, verbose_name="Manufacturer"),
                ),
                ("date_of_purchase", models.DateField(verbose_name="Date of purchase")),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("A", "Available"),
                            ("U", "In use"),
                            ("B", "Broken"),
                            ("R", "Repair"),
                            ("M", "Missing"),
                            ("C", "Condemned"),
                        ],
                        default=("A", "Available"),
                        max_length=1,
                        verbose_name="State",
                    ),
                ),
                ("description", models.CharField(max_length=255, verbose_name="Type")),
                (
                    "hidden",
                    models.BooleanField(
                        blank=True, default=False, verbose_name="Hidden"
                    ),
                ),
                (
                    "free",
                    models.BooleanField(blank=True, default=False, verbose_name="Free"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Weight",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("total_weight", models.IntegerField(verbose_name="Total weight")),
                (
                    "available_weight",
                    models.IntegerField(verbose_name="Available weight"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="WeightBelt",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_of_purchase", models.DateField(verbose_name="Date of purchase")),
                (
                    "state",
                    models.CharField(
                        choices=[("U", "In use"), ("B", "Broken"), ("C", "Condemned")],
                        max_length=1,
                        verbose_name="State",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Cylinder",
            fields=[
                (
                    "item_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        to="inventory.Item",
                    ),
                ),
                (
                    "serial_num",
                    models.CharField(
                        max_length=255,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Serial number",
                    ),
                ),
                ("material", models.CharField(max_length=255, verbose_name="Material")),
                (
                    "capacity",
                    models.DecimalField(
                        decimal_places=2, max_digits=4, verbose_name="Capacity"
                    ),
                ),
                ("last_viz", models.DateField(verbose_name="Last visual inspection")),
                (
                    "last_hydro",
                    models.DateField(verbose_name="Last hydro-static inspection"),
                ),
                (
                    "viz_period",
                    models.DurationField(
                        default=datetime.timedelta(days=364),
                        verbose_name="Visual inspection validity period",
                    ),
                ),
                (
                    "hydro_period",
                    models.DurationField(
                        default=datetime.timedelta(days=728),
                        verbose_name="Hydro-static test validity period",
                    ),
                ),
            ],
            bases=("inventory.item",),
        ),
        migrations.CreateModel(
            name="Regulator",
            fields=[
                (
                    "item_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="inventory.Item",
                    ),
                ),
                ("last_service", models.DateField(verbose_name="Last service")),
                (
                    "serial_num",
                    models.CharField(
                        default="", max_length=255, verbose_name="Serial number"
                    ),
                ),
            ],
            bases=("inventory.item",),
        ),
        migrations.CreateModel(
            name="Booties",
            fields=[
                (
                    "item_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="inventory.Item",
                    ),
                ),
                (
                    "size",
                    models.CharField(
                        choices=[
                            ("XS", "Extra small"),
                            ("S", "Small"),
                            ("M", "Medium"),
                            ("L", "Large"),
                            ("XL", "Extra large"),
                        ],
                        max_length=2,
                        verbose_name="Size",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Booties",
            },
            bases=("inventory.item",),
        ),
        migrations.CreateModel(
            name="Wetsuit",
            fields=[
                (
                    "item_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="inventory.Item",
                    ),
                ),
                (
                    "size",
                    models.CharField(
                        choices=[
                            ("XS", "Extra small"),
                            ("S", "Small"),
                            ("M", "Medium"),
                            ("ML", "Medium large"),
                            ("L", "Large"),
                            ("XL", "Extra large"),
                        ],
                        max_length=2,
                        verbose_name="Size",
                    ),
                ),
            ],
            bases=("inventory.item",),
        ),
        migrations.CreateModel(
            name="ItemValue",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "description",
                    models.CharField(max_length=255, unique=True, verbose_name="Type"),
                ),
                ("cost", models.IntegerField(default=0, verbose_name="Value")),
            ],
        ),
        migrations.CreateModel(
            name="Fins",
            fields=[
                (
                    "item_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="inventory.Item",
                    ),
                ),
                (
                    "size",
                    models.CharField(
                        choices=[
                            ("XS", "Extra small"),
                            ("S", "Small"),
                            ("M", "Medium"),
                            ("L", "Large"),
                            ("XL", "Extra large"),
                        ],
                        max_length=2,
                        verbose_name="Size",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Fins",
            },
            bases=("inventory.item",),
        ),
        migrations.CreateModel(
            name="BCD",
            fields=[
                (
                    "item_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="inventory.Item",
                    ),
                ),
                ("last_service", models.DateField(verbose_name="Last service")),
                (
                    "size",
                    models.CharField(
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
                (
                    "serial_num",
                    models.CharField(
                        default="", max_length=255, verbose_name="Serial number"
                    ),
                ),
            ],
            options={
                "verbose_name": "BCD",
            },
            bases=("inventory.item",),
        ),
    ]
