# Generated by Django 4.2.5 on 2023-11-14 16:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
            name='HoraExtra',
            fields=[
                ('id_hora_extra', models.CharField(default='N/A', editable=False, max_length=25, primary_key=True, serialize=False, unique=True)),
                ('fecha', models.DateField()),
                ('hora_entrada', models.TimeField()),
                ('hora_salida', models.TimeField()),
                ('observacion', models.TextField()),
                ('estado', models.CharField(choices=[('0', 'Pendientes por aprobación'), ('1', 'Aprobadas')], max_length=1)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]