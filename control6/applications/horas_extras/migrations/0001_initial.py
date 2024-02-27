# Generated by Django 5.0.2 on 2024-02-26 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CalendarioFestivo',
            fields=[
                ('id_festivo', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('celebracion', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='CodigoConcepto',
            fields=[
                ('codigo_concepto', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=150)),
                ('recargo', models.CharField(max_length=150)),
                ('observacion', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='HoraExtra',
            fields=[
                ('id_hora_extra', models.CharField(default='N/A', editable=False, max_length=25, primary_key=True, serialize=False, unique=True)),
                ('fecha', models.DateField()),
                ('hora_entrada', models.TimeField()),
                ('hora_salida', models.TimeField()),
                ('observacion', models.TextField()),
                ('estado', models.CharField(choices=[('0', 'Pendientes por aprobación'), ('1', 'Aprobadas'), ('2', 'Rechazadas')], max_length=1)),
                ('cod_4185', models.FloatField(default=0.0)),
                ('cod_4215', models.FloatField(default=0.0)),
                ('cod_4225', models.FloatField(default=0.0)),
                ('cod_4230', models.FloatField(default=0.0)),
                ('cod_4235', models.FloatField(default=0.0)),
                ('cod_4240', models.FloatField(default=0.0)),
                ('cod_4245', models.FloatField(default=0.0)),
                ('cod_4270', models.FloatField(default=0.0)),
                ('cod_4275', models.FloatField(default=0.0)),
                ('cod_4280', models.FloatField(default=0.0)),
                ('cod_9050', models.FloatField(default=0.0)),
                ('cod_9054', models.FloatField(default=0.0)),
            ],
        ),
    ]
