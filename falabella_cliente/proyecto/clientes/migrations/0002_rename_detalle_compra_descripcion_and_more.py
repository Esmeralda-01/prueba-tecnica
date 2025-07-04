# Generated by Django 5.2 on 2025-05-06 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='compra',
            old_name='detalle',
            new_name='descripcion',
        ),
        migrations.AlterField(
            model_name='cliente',
            name='numero_documento',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='compra',
            name='monto',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
