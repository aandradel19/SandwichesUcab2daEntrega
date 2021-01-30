from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def historialPage(request):
    return render(request, 'historial.html')