# Generated by Django 5.0.2 on 2024-02-28 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('codigo_material', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=50)),
                ('unidad_medida', models.CharField(max_length=5)),
                ('aportacion', models.BooleanField()),
                ('precio', models.FloatField()),
            ],
        ),
    ]
