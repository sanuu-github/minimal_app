# Generated by Django 4.1 on 2022-09-08 04:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0005_sampleitem_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sampleitem',
            name='comment',
        ),
    ]
