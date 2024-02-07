# Generated by Django 4.2.5 on 2023-12-06 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horas_extras', '0003_horaextra_cod_4185_horaextra_cod_4190_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodigoConcepto',
            fields=[
                ('codigo_concepto', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=150)),
                ('recargo', models.CharField(max_length=150)),
                ('observacion', models.CharField(max_length=250)),
            ],
        ),
        migrations.RenameField(
            model_name='horaextra',
            old_name='cod_4190',
            new_name='cod_4280',
        ),
        migrations.RenameField(
            model_name='horaextra',
            old_name='cod_4195',
            new_name='cod_9050',
        ),
        migrations.RemoveField(
            model_name='horaextra',
            name='cod_4200',
        ),
        migrations.RemoveField(
            model_name='horaextra',
            name='cod_4205',
        ),
        migrations.RemoveField(
            model_name='horaextra',
            name='cod_4210',
        ),
        migrations.RemoveField(
            model_name='horaextra',
            name='cod_4220',
        ),
    ]