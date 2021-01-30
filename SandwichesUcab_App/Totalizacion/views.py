from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def totalizacionPage(request):
    return render(request, 'totalizacion.html')