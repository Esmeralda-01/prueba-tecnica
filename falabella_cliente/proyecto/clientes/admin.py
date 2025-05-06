from django.contrib import admin
from .models import TipoDocumento, Cliente, Compra

admin.site.register(TipoDocumento)
admin.site.register(Cliente)
admin.site.register(Compra)
