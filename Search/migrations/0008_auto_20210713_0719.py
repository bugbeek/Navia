# Generated by Django 3.0.5 on 2021-07-13 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Search', '0007_auto_20210713_0656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='price_per_unit',
            field=models.FloatField(blank=True, null=True),
        ),
    ]