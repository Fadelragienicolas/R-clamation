from django import forms
from .models import *

# Formulaire pour UFR
class UFRForm(forms.ModelForm):
    class Meta:
        model = UFR
        fields = ['nom', 'description']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Ex: UFR Sciences et Technologies"
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': "Décrivez brièvement l'UFR"
            }),
        }

# Formulaire pour Année Académique
class AnneeAcademiqueForm(forms.ModelForm):
    class Meta:
        model = AnneeAcademique
        fields = ['annee_academique']
        widgets = {
            'annee_academique': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Ex: 2025-2026"
            }),
        }

# Formulaire pour Filiere
class FiliereForm(forms.ModelForm):
    class Meta:
        model = Filiere
        fields = ['nom', 'description', 'ufr', 'annee_academique']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Ex: Informatique"
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': "Description de la filière"
            }),
            'ufr': forms.Select(attrs={
                'class': 'form-control'
            }),
            'annee_academique': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

# Formulaire pour Etudiant
class EtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = [
            'identifiant_permanent', 'nom', 'prenoms', 'date_naissance',
            'sexe', 'telephone', 'filiere',
            'niveau',
        ]
        widgets = {
            'identifiant_permanent': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Nom de l'étudiant"
            }),

            'photo_identite': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Nom de l'étudiant"
            }),
            'prenoms': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Prénoms de l'étudiant"
            }),
            'date_naissance': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'sexe': forms.Select(attrs={
                'class': 'form-control'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Ex: 0700000000"
            }),
            'filiere': forms.Select(attrs={
                'class': 'form-control'
            }),
            'niveau': forms.Select(attrs={
                'class': 'form-control'
            }),
        }



        
# Formulaire pour Etudiant
class EtudiantAdminForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = [
            'identifiant_permanent', 'nom', 'prenoms', 'date_naissance',
            'sexe', 'telephone', 'filiere',
            'niveau'
        ]
        widgets = {
            'identifiant_permanent': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Nom de l'étudiant"
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Nom de l'étudiant"
            }),
            'prenoms': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Prénoms de l'étudiant"
            }),
            'date_naissance': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'sexe': forms.Select(attrs={
                'class': 'form-control'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Ex: 0700000000"
            }),
            'filiere': forms.Select(attrs={
                'class': 'form-control'
            }),
            'niveau': forms.Select(attrs={
                'class': 'form-control'
            }),
        }