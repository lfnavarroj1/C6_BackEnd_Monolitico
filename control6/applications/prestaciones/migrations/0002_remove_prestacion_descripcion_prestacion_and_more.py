# Generated by Django 4.2.5 on 2023-11-30 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prestaciones', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prestacion',
            name='descripcion_prestacion',
        ),
        migrations.AlterField(
            model_name='prestacion',
            name='alcance',
            field=models.TextField(),
        ),
    ]