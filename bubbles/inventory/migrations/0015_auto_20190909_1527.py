# Generated by Django 2.2.4 on 2019-09-09 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0014_fix_cylinder_hydro'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cylinder',
            old_name='capacity',
            new_name='size',
        ),
    ]
