# Generated by Django 5.1.3 on 2024-11-28 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registro_paradas', '0003_alter_operationtime_total_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operationtime',
            name='total_time',
            field=models.CharField(blank=True, null=True),
        ),
    ]
