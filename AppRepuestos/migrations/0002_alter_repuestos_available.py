# Generated by Django 5.0.7 on 2024-10-07 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppRepuestos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repuestos',
            name='available',
            field=models.BooleanField(null=True),
        ),
    ]
