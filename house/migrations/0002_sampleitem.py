# Generated by Django 4.1 on 2022-09-07 05:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sampleitem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itemname', models.CharField(max_length=35)),
                ('originalsize', models.IntegerField(default=10)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('sampleroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='house.sampleroom')),
            ],
        ),
    ]
