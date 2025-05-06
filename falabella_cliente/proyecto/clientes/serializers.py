from rest_framework import serializers
from .models import Cliente, TipoDocumento, Compra

class TipoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDocumento
        fields = '__all__'
class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = ['monto', 'descripcion', 'fecha']

# Serializador para el cliente
class ClienteSerializer(serializers.ModelSerializer):
    compras = CompraSerializer(many=True)  # Agregar las compras del cliente

    class Meta:
        model = Cliente
        fields = ['numero_documento', 'nombre', 'apellido', 'correo', 'telefono', 'compras']
