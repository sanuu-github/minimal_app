# Generated by Django 4.1 on 2022-09-08 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0010_remove_sampleitem_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampleitem',
            name='Comment',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
    ]
