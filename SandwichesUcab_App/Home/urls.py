from django.urls import path
from . import views

urlpatterns = [
    

    path('',views.homePage, name='homePage'),
    path('pedidos/',views.pedidosPage, name='pedidosPage'),
    path('totalizacion/',views.totalizacionPage, name='totalizacionPage'),
    path('historial/',views.historialPage, name='historialPage'),
    path('graciasVuelvaPronto/',views.graciasVuelvaProntoPage, name='graciasVuelvaProntoPage'),
]