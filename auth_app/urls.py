

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('inscription/', views.Inscription, name= 'inscription'), 
    path('connexion/', views.Connexion, name= 'connexion'),  
    path('deconnexion/', views.Deconnexion, name= 'deconnexion'),
]