# Generated by Django 2.0.6 on 2018-07-27 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0003_auto_20180727_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentalperiod',
            name='end_date',
            field=models.DateField(null=True, verbose_name='End date'),
        ),
    ]