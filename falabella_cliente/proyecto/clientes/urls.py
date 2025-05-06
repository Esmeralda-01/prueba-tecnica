from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ping/', views.ping, name='ping'),
    path('buscar-cliente/', views.buscar_cliente, name='buscar_cliente'),
    path('exportar-cliente/', views.exportar_cliente_excel, name='exportar_cliente_excel'),
    path('reporte-fidelizacion/', views.reporte_fidelizacion, name='reporte_fidelizacion'),
    path('consultar-clientes-compras/', views.consultar_clientes_compras, name='consultar_clientes_compras'),
]
