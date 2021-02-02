from django.urls import path
from . import views
app_name = 'Home'
urlpatterns = [
    path('',views.homePage, name='homePage'),
    path('pedidos/',views.pedidosPage, name='pedidosPage'),
    path('totalizacion/',views.totalizacionPage, name='totalizacionPage'),
    path('historial/',views.historialPage, name='historialPage'),
    path('graciasVuelvaPronto/',views.graciasVuelvaProntoPage, name='graciasVuelvaProntoPage'),
    path('ventasPorClientes/',views.ventasPorClientesPage, name='ventasPorClientesPage'),
    path('ventasPorDia/',views.ventasPorDiaPage, name='ventasPorDiaPage'),
    path('ventasPorIngredientes/',views.ventasPorIngredientesPage, name='ventasPorIngredientesPage'),
    path('ventasPorTamano/',views.ventasPorTamanoPage, name='ventasPorTamanoPage'),
    path('ventasTotales/',views.ventasTotalesPage, name='ventasTotalesPage'),
    path('ventasPorClientesEmpty/',views.ventasPorClientesPageEmpty, name='ventasPorClientesPageEmpty'),
    path('ventasPorDiaEmpty/',views.ventasPorDiaPageEmpty, name='ventasPorDiaPageEmpty'),
    path('ventasPorIngredientesEmpty/',views.ventasPorIngredientesPageEmpty, name='ventasPorIngredientesPageEmpty'),
    path('ventasPorTamanoEmpty/',views.ventasPorTamanoPageEmpty, name='ventasPorTamanoPageEmpty'),
    path('agrupadosPorCliente/',views.agrupadosPorClientePage, name='agrupadosPorCliente'),
    path('agrupadosPorIngrediente/',views.agrupadosPorIngredientePage, name='agrupadosPorIngrediente'),
    path('agrupadosPorTamano/',views.agrupadosPorTamanoPage, name='agrupadosPorTamano'),
    
]