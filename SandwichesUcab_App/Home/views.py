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
    try:
        pedidoID = request.POST['pedidoID']
        select_tamano = '-1'
        if 'select_tamano' in request.POST:
            select_tamano = request.POST['select_tamano']
        else:
            return render(request, 'pedidos.html', {
                'pedido_id': pedidoID,
                'tamano': Tamano.objects.all(),
                'ing': Ingrediente.objects.all(),
                'error_message': "Error, debes seleccionar un tamaño",
            })

        ingredientes = list()
        if 'ingredientes' in request.POST:
            ingredientes = request.POST.getlist('ingredientes')

        boton = request.POST['action']

        if pedidoID == "":
            return render(request, 'pedidos.html', {
                'error_message': "Error, vuelve a intentarlo.",
            })

        print("ID= "+str(pedidoID))
        print("Tamano= "+str(select_tamano))
        print("Ingrediente= "+str(ingredientes))
        print("Boton= "+str(boton))

        pedido = Pedido.objects.get(pk=pedidoID)
        tamano = Tamano.objects.get(pk=select_tamano)

        sandwich = pedido.sandwich_set.create(pedido_id=pedido,tamano_id=tamano)
        # pizza.save()

        print("Sandwich ID= "+ str(sandwich.id))
        for ingr in ingredientes:
            print("algo: " + str(ingr))
            i = Ingrediente.objects.get(pk=ingr)
            sandwich_ingrediente = sandwich.sandwich_ingrediente_set.create(sandwich_id=sandwich,ingrediente_id=i)
            # pizza_ing.save()

        if boton == "agregar":
            return render(request, 'pedidos.html', {
                'pedido_id': pedidoID,
                'tamano': Tamano.objects.all(),
                'ing': Ingrediente.objects.all(),
            })
            
        if boton == "finalizar":
            return render(request, 'graciasVuelvaPronto.html', {
                'pedido': pedido,
            })

    except:
        if pedidoID != "":
            return render(request, 'pedidos.html', {
                'error_message': "Error, vuelve a intentarlo.",
            })
    else:
        return render(request, 'pedidos.html', {
            'pedido_id': pedidoID,
            'tamano': Tamano.objects.all(),
            'ing': Ingrediente.objects.all(),
        })


def historialPage(request):
    return render(request, 'historial.html')

def graciasVuelvaProntoPage(request):
    return render(request, 'graciasVuelvaPronto.html')
    
def ventasPorClientesPage(request):
    return render(request, 'ventasPorClientes.html')

def ventasPorDiaPage(request):
    return render(request, 'ventasPorDia.html')

def ventasPorIngredientesPage(request):
    return render(request, 'ventasPorIngredientes.html')

def ventasPorTamanoPage(request):
    return render(request, 'ventasPorTamano.html')

def ventasTotalesPage(request):
    return render(request, 'ventasTotales.html')