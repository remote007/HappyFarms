# Generated by Django 4.1.3 on 2022-11-18 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
            options={
                'verbose_name_plural': 'cities',
            },
        ),
        migrations.CreateModel(
            name='CityDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('lat', models.FloatField()),
                ('long', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ComponentsData',
            fields=[
                ('date', models.DateTimeField(primary_key=True, serialize=False)),
                ('co', models.FloatField()),
                ('no', models.FloatField()),
                ('no2', models.FloatField()),
                ('o3', models.FloatField()),
                ('so2', models.FloatField()),
                ('pm2_5', models.FloatField()),
                ('pm10', models.FloatField()),
                ('nh3', models.FloatField()),
            ],
        ),
    ]
