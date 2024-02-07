# Generated by Django 4.2.5 on 2024-02-07 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspecciones_tqi', '0008_alter_maniobras_causal_alter_maniobras_circuito_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdltqi',
            name='criticidad_maniobra',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pdltqi',
            name='direccion',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pdltqi',
            name='fecha_actualizacion',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pdltqi',
            name='municipio',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pdltqi',
            name='vereda_localidad',
            field=models.CharField(blank=True, null=True),
        ),
    ]
