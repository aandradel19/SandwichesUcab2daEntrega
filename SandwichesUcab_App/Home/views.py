from django.shortcuts import render,get_object_or_404,redirect
from django.template import loader
from django.http import HttpResponse
from django.utils import timezone 
from .models import *
# Create your views here.

def homePage(request):
    return render(request, 'home.html')

def pedidosPage(request):
    try:
        campo_cedula = request.POST['campo_cedula']
        if campo_cedula == "":
            return render(request, 'home.html', {
                'error_message': "Error, cedula no puede estar vacio.",
            })
    except:
        return render(request, 'home.html', {
            'error_message': "Error, no existe el campo cedula.",
        })
    else:
        pedido = Pedido(fecha_pedido=timezone.now(),cedula=campo_cedula)
        pedido.save()
        return render(request, 'pedidos.html', {
            'pedido_id': pedido.id,
            'tamano': Tamano.objects.all(),
            'ing': Ingrediente.objects.all(),
        })

def totalizacionPage(request):
    return render(request, 'totalizacion.html')

def historialPage(request):
    return render(request, 'historial.html')

def graciasVuelvaProntoPage(request):
    return render(request, 'graciasVuelvaPronto.html')