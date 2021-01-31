from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def homePage(request):
    return render(request, 'home.html')

def pedidosPage(request):
    return render(request, 'pedidos.html')

def totalizacionPage(request):
    return render(request, 'totalizacion.html')

def historialPage(request):
    return render(request, 'historial.html')

def graciasVuelvaProntoPage(request):
    return render(request, 'graciasVuelvaPronto.html')