# Generated by Django 2.0.6 on 2018-06-29 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

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
                ("number", models.CharField(max_length=5, verbose_name="Number")),
                (
                    "manufacturer",
                    models.CharField(max_length=255, verbose_name="Manufacturer"),
                ),
                ("date_of_purchase", models.DateField(verbose_name="Date of purchase")),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("U", "In use"),
                            ("B", "Broken"),
                            ("R", "Repair"),
                            ("C", "Condemned"),
                        ],
                        max_length=1,
                        verbose_name="State",
                    ),
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
                            ("S", "Small"),
                            ("M", "Medium"),
                            ("ML", "Medium large"),
                            ("L", "Large"),
                        ],
                        max_length=2,
                        verbose_name="Size",
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
            bases=("inventory.item",),
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
                    models.IntegerField(
                        default=1, verbose_name="Visual inspection validity period"
                    ),
                ),
                (
                    "hydro_period",
                    models.IntegerField(
                        default=2, verbose_name="Hydro-static test validity period"
                    ),
                ),
            ],
            bases=("inventory.item",),
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
            ],
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
    ]
