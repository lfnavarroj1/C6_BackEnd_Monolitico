# Generated by Django 4.2.5 on 2023-10-11 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_management', '0003_alter_trazabilidad_fecha_trazabilidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='trabajo',
            name='ticket',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]