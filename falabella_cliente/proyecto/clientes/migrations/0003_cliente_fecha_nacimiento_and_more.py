# Generated by Django 5.2 on 2025-05-06 01:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0002_rename_detalle_compra_descripcion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='fecha_nacimiento',
            field=models.DateField(default='2000-01-01'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='numero_documento',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefono',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='compra',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compras', to='clientes.cliente'),
        ),
        migrations.AlterField(
            model_name='compra',
            name='descripcion',
            field=models.CharField(default='Sin descripción', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='compra',
            name='fecha',
            field=models.DateTimeField(),
        ),
    ]
