from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

# Admin pour UFR
@admin.register(UFR)
class UFRAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description')
    search_fields = ('nom',)

# Admin pour Année Académique
@admin.register(AnneeAcademique)
class AnneeAcademiqueAdmin(admin.ModelAdmin):
    list_display = ('annee_academique', 'active')
    list_filter = ('active',)
    ordering = ('-annee_academique',)

# Admin pour Filiere
@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ufr', 'annee_academique')
    list_filter = ('ufr', 'annee_academique')
    search_fields = ('nom',)

# Admin pour Etudiant
@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenoms', 'filiere', 'niveau')
    list_filter = ('filiere', 'niveau')
    search_fields = ('nom', 'prenoms', 'telephone')
    readonly_fields = ('date_inscription',)
