# Generated by Django 5.0.7 on 2024-10-07 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppRepuestos', '0003_remove_repuestos_machine_is_repuestos_machines'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repuestos',
            name='name_spare_part',
            field=models.CharField(max_length=20, verbose_name='Nombre Repuesto'),
        ),
    ]
