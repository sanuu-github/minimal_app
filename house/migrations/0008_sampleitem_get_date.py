# Generated by Django 4.1 on 2022-09-08 04:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0007_sampleitem_qty'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampleitem',
            name='get_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
