# Generated by Django 4.2.5 on 2024-01-25 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspecciones_tqi', '0002_alter_pdltqi_pdl_asociado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdltqi',
            name='pdl_asociado',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]