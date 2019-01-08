# Generated by Django 2.1.5 on 2019-01-07 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0008_fix_item_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeightRequestItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField(blank=True, null=True, verbose_name='Weight')),
                ('rental', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rentals.Rental')),
            ],
        ),
    ]