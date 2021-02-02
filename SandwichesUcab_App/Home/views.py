from django.shortcuts import render,get_object_or_404,redirect
from django.template import loader
from django.http import HttpResponse
from django.utils import timezone 
from django.db import connection
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

        print("Sandwich ID= "+ str(sandwich.id))
        for ingr in ingredientes:
            print("algo: " + str(ingr))
            i = Ingrediente.objects.get(pk=ingr)
            sandwich_ingrediente = sandwich.sandwich_ingrediente_set.create(sandwich_id=sandwich,ingrediente_id=i)

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
    cursor = connection.cursor()
    cursor.execute('''SELECT  ped.id Factura, ped.fecha_pedido Fecha, ped.cedula Cliente, 
(select count(*) 
    from Home_sandwich san 
        where san.pedido_id_id = ped.id) Cantidad_sandwiches,
(select sum(ingredientes.monto + tamanos.monto) || " Bs."
    from (select COALESCE (sum(ing.costo_ingrediente),0) as monto
             from Home_ingrediente ing, Home_sandwich san, Home_sandwich_ingrediente si
                 where ing.id = si.ingrediente_id_id and si.sandwich_id_id = san.id and san.pedido_id_id = ped.id)as ingredientes, 
         (select sum(tam.costo_tamano) as monto
             from Home_tamano tam, Home_sandwich san
                 where san.tamano_id_id = tam.id and san.pedido_id_id = ped.id) as tamanos) as Monto_sandwiches
from Home_pedido ped
where ped.cedula = %s
order by 5 desc ''', [request.POST["cedula"]])
    salida = dictfetchall(cursor)
    return render(request, 'ventasPorClientes.html', {
        'venta': salida
    })

def ventasPorDiaPage(request):
    cursor = connection.cursor()
    cursor.execute('''SELECT  ped.id Factura, ped.fecha_pedido Fecha, ped.cedula Cliente, 
(select count(*) 
    from Home_sandwich san 
        where san.pedido_id_id = ped.id) Cantidad_sandwiches,
(select sum(ingredientes.monto + tamanos.monto) || " Bs."
    from (select COALESCE (sum(ing.costo_ingrediente),0) as monto
             from Home_ingrediente ing, Home_sandwich san, Home_sandwich_ingrediente si
                 where ing.id = si.ingrediente_id_id and si.sandwich_id_id = san.id and san.pedido_id_id = ped.id)as ingredientes, 
         (select sum(tam.costo_tamano) as monto
             from Home_tamano tam, Home_sandwich san
                 where san.tamano_id_id = tam.id and san.pedido_id_id = ped.id) as tamanos) Monto_sandwiches
from Home_pedido ped
where ped.fecha_pedido = %s ''', [request.POST["fecha"]])
    salida = dictfetchall(cursor)
    return render(request, 'ventasPorDia.html', {
        'venta': salida
    })

def ventasPorIngredientesPage(request):
    print(request.POST["ingredienteselect"])
    cursor = connection.cursor()
    cursor.execute('''SELECT  ped.id Factura, ped.fecha_pedido Fecha, ped.cedula Cliente, 
(select count(*) 
    from Home_sandwich san 
        where san.pedido_id_id = ped.id and san.id in (select sand2.id 
                                                        from Home_sandwich sand2, Home_ingrediente ing, Home_sandwich_ingrediente si  
                                                            where si.sandwich_id_id = sand2.id and si.ingrediente_id_id in (select sing.id from Home_ingrediente i, Home_sandwich_ingrediente sing where i.nombre_ingrediente = %s and sing.ingrediente_id_id = i.id ))) Cantidad_sandwiches,
(select sum(ingredientes.monto + tamanos.monto) || " Bs."
    from (select COALESCE (sum(ing.costo_ingrediente),0) as monto
             from Home_ingrediente ing, Home_sandwich san, Home_sandwich_ingrediente si
                 where ing.id = si.ingrediente_id_id and si.sandwich_id_id = san.id and san.pedido_id_id = ped.id and san.id in (select sand2.id 
                                                        from Home_sandwich sand2, Home_ingrediente ing, Home_sandwich_ingrediente si  
                                                            where si.sandwich_id_id = sand2.id and si.ingrediente_id_id in (select sing.id from Home_ingrediente i, Home_sandwich_ingrediente sing where i.nombre_ingrediente = %s and sing.ingrediente_id_id = i.id )))as ingredientes, 
         (select sum(tam.costo_tamano) as monto
             from Home_tamano tam, Home_sandwich san
                 where san.tamano_id_id = tam.id and san.pedido_id_id = ped.id and san.id in (select sand2.id 
                                                        from Home_sandwich sand2, Home_ingrediente ing, Home_sandwich_ingrediente si  
                                                            where si.sandwich_id_id = sand2.id and si.ingrediente_id_id in (select sing.id from Home_ingrediente i, Home_sandwich_ingrediente sing where i.nombre_ingrediente = %s and sing.ingrediente_id_id = i.id ))) as tamanos) Monto_sandwiches
from Home_pedido ped 
where ped.id in (select pp.id from Home_pedido pp, Home_sandwich ss where ss.pedido_id_id = pp.id and ss.id in (select sand2.id 
                                                        from Home_sandwich sand2, Home_ingrediente ing, Home_sandwich_ingrediente si  
                                                            where si.sandwich_id_id = sand2.id and si.ingrediente_id_id in (select sing.id from Home_ingrediente i, Home_sandwich_ingrediente sing where i.nombre_ingrediente = %s and sing.ingrediente_id_id = i.id )))''', [request.POST["ingredienteselect"], request.POST["ingredienteselect"], request.POST["ingredienteselect"], request.POST["ingredienteselect"]])
    salida = dictfetchall(cursor)
    return render(request, 'ventasPorIngredientes.html', {
        'venta': salida,
        'ing': Ingrediente.objects.all(),
    })

def ventasPorTamanoPage(request):
    cursor = connection.cursor()
    cursor.execute('''SELECT ped.id Factura, ped.fecha_pedido Fecha, ped.cedula Cliente, 
(select count(*) 
    from Home_sandwich san 
        where san.pedido_id_id = ped.id and san.tamano_id_id in (select t.id from Home_tamano t where t.nombre_tamano = %s)) Cantidad_sandwiches,
(select sum(ingredientes.monto + tamanos.monto) || " Bs."
    from (select COALESCE (sum(ing.costo_ingrediente),0) as monto
             from Home_ingrediente ing, Home_sandwich san, Home_sandwich_ingrediente si
                 where ing.id = si.ingrediente_id_id and si.sandwich_id_id = san.id and san.pedido_id_id = ped.id and san.tamano_id_id in (select t.id from Home_tamano t where t.nombre_tamano = %s))as ingredientes, 
         (select sum(tam.costo_tamano) as monto
             from Home_tamano tam, Home_sandwich san
                 where san.tamano_id_id = tam.id and san.pedido_id_id = ped.id and san.tamano_id_id in (select t.id from Home_tamano t where t.nombre_tamano = %s)) as tamanos) Monto_sandwiches
from Home_pedido ped 
where ped.id in (select pp.id from Home_pedido pp, Home_sandwich ss where ss.pedido_id_id = pp.id and ss.tamano_id_id in (select t.id from Home_tamano t where t.nombre_tamano = %s))''', [request.POST["tamanoselect"], request.POST["tamanoselect"], request.POST["tamanoselect"], request.POST["tamanoselect"]])
    salida = dictfetchall(cursor)
    return render(request, 'ventasPorTamano.html', {
        'venta': salida,
        'tamano': Tamano.objects.all(),
    })

def ventasTotalesPage(request):
    cursor = connection.cursor()
    cursor.execute('''SELECT  ped.id Factura, ped.fecha_pedido Fecha, ped.cedula Cliente, 
                            (SELECT count(*) 
                                from Home_sandwich san 
                                where san.pedido_id_id = ped.id) Cantidad_sandwiches,
                                (select sum(ingredientes.monto + tamanos.monto) || " Bs."
                                from (select COALESCE (sum(ing.costo_ingrediente),0) as monto
                            from Home_ingrediente ing, Home_sandwich san, Home_sandwich_ingrediente si
                            where ing.id = si.ingrediente_id_id and si.sandwich_id_id = san.id and san.pedido_id_id = ped.id)as ingredientes, 
                                (select sum(tam.costo_tamano) as monto
                                from Home_tamano tam, Home_sandwich san
                                where san.tamano_id_id = tam.id and san.pedido_id_id = ped.id) as tamanos) Monto_sandwiches
                from Home_pedido ped''')
    salida = dictfetchall(cursor)
    return render(request, 'ventasTotales.html', {
        'venta': salida
    })
    
    
def ventasPorTamanoPageEmpty(request):
    return render(request, 'ventasPorTamano.html', {
        'tamano': Tamano.objects.all(),
    })

def ventasPorClientesPageEmpty(request):
    return render(request, 'ventasPorClientes.html')

def ventasPorIngredientesPageEmpty(request):
    return render(request, 'ventasPorIngredientes.html', {
        'ing': Ingrediente.objects.all(),
    })         

def ventasPorDiaPageEmpty(request):
    return render(request, 'ventasPorDia.html')
    
def dictfetchall(cursor):
    desc = cursor.description
    return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
    ]