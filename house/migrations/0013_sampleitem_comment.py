# Generated by Django 4.1 on 2022-09-08 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0012_remove_sampleitem_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampleitem',
            name='comment',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]