from django.urls import path
from . import views

urlpatterns = [

    path('',views.historialPage, name='historialPage'),

]