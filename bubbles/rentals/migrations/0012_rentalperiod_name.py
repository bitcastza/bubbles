# Generated by Django 2.1.5 on 2019-03-07 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0011_fix_item_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentalperiod',
            name='name',
            field=models.CharField(default='', max_length=255, verbose_name='Name'),
            preserve_default=False,
        ),
    ]