from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def realizarPedidosPage(request):
    return render(request, 'realizarPedidos.html')