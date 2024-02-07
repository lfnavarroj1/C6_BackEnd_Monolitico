# Generated by Django 4.2.5 on 2024-02-06 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspecciones_tqi', '0005_metasinspectores_cantidad_meta_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Maniobras',
            fields=[
                ('codigo', models.CharField(max_length=25, primary_key=True, serialize=False, unique=True)),
                ('tipo', models.CharField()),
                ('fecha_trabajo_inicio', models.DateField()),
                ('hora_trabajo_inicio', models.TimeField()),
                ('fecha_trabajo_fin', models.DateField()),
                ('hora_trabajo_fin', models.TimeField()),
                ('fecha_programacion', models.DateField()),
                ('estado', models.CharField(max_length=150)),
                ('pdl_asociado', models.CharField(max_length=25)),
                ('circuito', models.CharField(max_length=50)),
                ('causal', models.CharField(max_length=50)),
                ('descripcion', models.TextField()),
                ('unidad_territorial', models.CharField(max_length=80)),
                ('unidad_territorial_std', models.CharField(max_length=80)),
                ('fecha_actualizacion', models.DateField()),
                ('ubicacion', models.CharField(max_length=128)),
                ('localidad_municipio', models.CharField(max_length=128)),
                ('nombre_responsable', models.CharField(max_length=255)),
                ('unidad_responsable', models.CharField(max_length=255)),
                ('telefono_reponsable', models.CharField(max_length=255)),
                ('firma', models.CharField(max_length=255)),
                ('co', models.CharField(max_length=255)),
            ],
        ),
    ]