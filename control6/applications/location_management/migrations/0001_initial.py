# Generated by Django 4.2.5 on 2024-04-18 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Municipality',
            fields=[
                ('code', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TerritorialUnit',
            fields=[
                ('id', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Sidewalk',
            fields=[
                ('code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60)),
                ('cft', models.CharField(max_length=7)),
                ('dispersion_factor', models.CharField(max_length=2)),
                ('municipality', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='location_management.municipality')),
            ],
        ),
        migrations.AddField(
            model_name='municipality',
            name='territorial_unit',
            field=models.ManyToManyField(to='location_management.territorialunit'),
        ),
    ]
