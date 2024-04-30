# Generated by Django 4.2.5 on 2024-04-14 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ModuloBandeja',
            fields=[
                ('id', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=350)),
            ],
        ),
        migrations.CreateModel(
            name='StateWork',
            fields=[
                ('id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=350)),
            ],
        ),
        migrations.CreateModel(
            name='WorkFlow',
            fields=[
                ('id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('step', models.CharField(max_length=2)),
                ('modules', models.ManyToManyField(to='process_management.modulobandeja')),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='process_management.process')),
                ('state_work', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='process_management.statework')),
            ],
        ),
    ]