import os
import openpyxl
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from .models import *
from django.contrib import messages
from .forms import *
from django.db.models import Q
from django.core.paginator import Paginator
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.db.models import Count




# Create your views here.

def Presentation_app(request):
    return render(request, 'Presentation_app.html')



# Debut fonction Tableau de bord
@login_required(login_url='connexion')
def tableau_de_bord(request):
    # Statistiques par sexe
    stats_sexe = Etudiant.objects.values('sexe').annotate(total=Count('id'))
    
    # Statistiques par filière
    stats_filiere = Etudiant.objects.values('filiere__nom').annotate(total=Count('id'))
    
    # Statistiques par UFR
    stats_ufr = Etudiant.objects.values('filiere__ufr__nom').annotate(total=Count('id'))
    
    # Statistiques par admissible / non admissible
    stats_admissible = Etudiant.objects.values('admissible').annotate(total=Count('id'))

    annee = AnneeAcademique.objects.first()

    context = {
        'stats_sexe': stats_sexe,
        'stats_filiere': stats_filiere,
        'stats_ufr': stats_ufr,
        'stats_admissible': stats_admissible,
        'annee': annee
    }

    return render(request, 'index.html', context)

# Debut fonction Annee academique
@login_required (login_url='connexion')
def Annee_academique (request):
    liste_annee = AnneeAcademique.objects.all()
    page = 'Annees Academiques'
    bouton = '+ Annee Academique'
    lien = ''
    return render(request, 'liste_annee.html', {
        'page': page, 
        'bouton': bouton,
        'liste_annee': liste_annee
        })

# Debut fonction Classe
@login_required (login_url='connexion')
def Liste_ufr (request):
    liste_ufr = UFR.objects.all()
    page = 'Liste des UFR' 
    bouton = '+ Une UFR'                             
    return render(request, 'liste_urf.html', {
        'page': page, 
        'bouton': bouton,
        'liste_ufr': liste_ufr
        })

@login_required (login_url='connexion')
#liste etudiant
def Liste_etudiant(request):

    etudiants = Etudiant.objects.all()

    ufrs = UFR.objects.all()
    filieres = Filiere.objects.all()

    nom = request.GET.get("nom")
    sexe = request.GET.get("sexe")
    niveau = request.GET.get("niveau")
    admissible = request.GET.get('admissible')
    date = request.GET.get("date")
    ufr = request.GET.get("ufr")
    filiere = request.GET.get("filiere")

    if nom:
        etudiants = etudiants.filter(
            Q(nom__icontains=nom) |
            Q(prenoms__icontains=nom)
        )

    if sexe:
        etudiants = etudiants.filter(sexe=sexe)

    if niveau:
        etudiants = etudiants.filter(niveau=niveau)

    if admissible:
        etudiants = etudiants.filter(admissible=admissible)

    if date:
        etudiants = etudiants.filter(date_inscription=date)

    if ufr:
        etudiants = etudiants.filter(filiere__ufr_id=ufr)

    if filiere:
        etudiants = etudiants.filter(filiere_id=filiere)

    paginator = Paginator(etudiants, 10)
    page = request.GET.get('page')
    etudiants = paginator.get_page(page)

    return render(request,"liste_etudiant.html",{
        "etudiants":etudiants,
        "ufrs":ufrs,
        "filieres":filieres,
    })





# Debut fonction Liste matiere
@login_required (login_url='connexion')
def Liste_filiere(request):
    filieres = Filiere.objects.all()
    ufrs = UFR.objects.all()

    nom = request.GET.get("nom")
    ufr = request.GET.get("ufr")

    if nom:
        filieres = filieres.filter(nom__icontains=nom)

    if ufr:
        filieres = filieres.filter(ufr_id=ufr)

    paginator = Paginator(filieres, 10)
    page = request.GET.get('page')
    filieres = paginator.get_page(page)

    return render(request, "liste_filiere.html", {
        "filieres": filieres,
        "ufrs": ufrs
    })

@login_required (login_url="connexion")
def Ajout_ufr(request):
    titre = "Ajout UFR"
    if request.method == 'POST':
        form = UFRForm(request.POST)

        if form.is_valid():
            nom = form.cleaned_data.get('nom')
            #Verifié si UFR existe deja 
            if UFR.objects.filter(nom__iexact=nom).exists():
                messages.error(request, "Cette UFR existe déja")
            else:
                form.save()
                messages.success(request, 'UFR ajouter avec success')
                return redirect('ajout_ufr')
    else:
        form = UFRForm()
    return render(request, 'ajout.html', {
            'form': form,
            'titre': titre
    })


# def Ajout_etudiant(request):
#     titre = "Ajout Etudiant"
#     if request.method == "POST":
#         form = EtudiantForm(request.POST)
#         if form.is_valid():
#             form.save()
#             nom = form.cleaned_data['nom']
#             messages.success(request, 'Etudiant ajouter avec success')
#             return redirect('merci', nom=nom)
#     else:
#         form = EtudiantForm()
#     return render(request, 'ajout.html', {
#         'form': form,
#         'titre': titre
#     })


def Ajout_etudiant(request):
    titre = "Déposer une réclamation"

    if request.method == "POST":
        form = EtudiantForm(request.POST)

        if form.is_valid():

            identifiant = form.cleaned_data['identifiant_permanent']
            nom = form.cleaned_data['nom']
            prenoms = form.cleaned_data['prenoms']
            date_naissance = form.cleaned_data['date_naissance']

            # Vérification doublon
            existe = Etudiant.objects.filter(
                identifiant_permanent=identifiant,
                nom=nom,
                prenoms=prenoms,
                date_naissance=date_naissance
            ).exists()

            if existe:
                messages.error(
                    request,
                    "Cet étudiant existe déjà dans la base !"
                )

            else:
                # Enregistrer et récupérer l'étudiant créé
                etudiant = form.save()

                # Redirection vers la page Merci avec son ID
                return redirect(
                    'merci',
                    etudiant_id=etudiant.id
                )

    else:
        form = EtudiantForm()

    return render(request, 'ajout.html', {
        'form': form,
        'titre': titre,
    })


from django.shortcuts import render, get_object_or_404
from .models import Etudiant


def merci_view(request, etudiant_id):
    return render(request, 'merci.html', {'etudiant_id': etudiant_id})

@login_required (login_url="connexion")
def Ajout_filiere(request):
    titre = "Ajout Filiere"
    if request.method == 'POST':
        form = FiliereForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data.get('nom')
            #Verifié si Etudiant existe deja
            if Filiere.objects.filter(nom__iexact=nom).exists():
                messages.error(request, "Cette filiere existe déja")
            else:
                form.save()
                messages.success(request, 'Filiere ajouter avec success')
                return redirect('ajout_filiere')
    else:
        form = FiliereForm()
    return render(request, 'ajout.html',{
        'form': form,
        'titre': titre
    })



@login_required(login_url='connexion')
def Modifier_ufr(request, id):
    titre = "Modification de l'ufr"
    ufr = get_object_or_404(UFR, id=id)
    if request.method == 'POST':
        form = UFRForm(request.POST, instance=ufr)
        if form.is_valid():
            form.save()
            messages.success(request, 'Modification Enregistrée avec succès')
            return redirect('modifier_ufr', id=id)
    else:
        form = UFRForm(instance=ufr)
    return render(request, 'ajout.html', {
    'form': form,
    'titre': titre
    })



@login_required(login_url='connexion')
def Modifier_etudiant(request, id):
    titre = "Modification de l'etudiant"
    etudiant = get_object_or_404(Etudiant, id=id)
    if request.method == 'POST':
        form = EtudiantAdminForm(request.POST, instance=etudiant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Modification Enregistrée avec succès')
            return redirect('merci', etudiant_id=id)
    else:
        form = EtudiantAdminForm(instance=etudiant)
    return render(request, 'ajout.html', {
    'form': form,
    'titre': titre
    })


@login_required(login_url='connexion')
def Modifier_filiere(request, id):
    titre = "Modification de la filiere"
    filiere = get_object_or_404(Filiere, id=id)
    if request.method == 'POST':
        form = FiliereForm(request.POST, instance=filiere)
        if form.is_valid():
            form.save()
            messages.success(request, 'Modification Enregistrée avec succès')
            return redirect('modifier_filiere', id=id)
    else:
        form = FiliereForm(instance=filiere)
    return render(request, 'ajout.html', {
    'form': form,
    'titre': titre
    })

@login_required(login_url='connexion')
def Modifier_annee(request, id):
    titre = "Modification de la chambre"
    annee = get_object_or_404(AnneeAcademique, id=id)
    if request.method == 'POST':
        form = AnneeAcademiqueForm(request.POST, instance=annee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Modification Enregistrée avec succès')
            return redirect('modifier_annee', id=id)
    else:
        form = AnneeAcademiqueForm(instance=annee)
    return render(request, 'ajout.html', {
    'form': form,
    'titre': titre
    })


@login_required(login_url='connexion')
#Suppression
def supprimer_etudiant(request, id):
    etudiant = get_object_or_404(Etudiant, id=id)
    if request.method == "POST":
        etudiant.delete()
        return redirect('liste_etudiant')
    return render(request, 'confirmer_supression.html',{
        "label": etudiant
    })


@login_required(login_url='connexion')
#Suppression
def supprimer_UFR(request, id):
    ufr = get_object_or_404(UFR, id=id)
    if request.method == "POST":
        ufr.delete()
        return redirect('liste_ufr')
    return render(request, 'confirmer_supression.html',{
        "label": ufr
    })

@login_required(login_url='connexion')
#Suppression
def supprimer_filiere(request, id):
    filiere = get_object_or_404(UFR, id=id)
    if request.method == "POST":
        filiere.delete()
        return redirect('liste_filiere')
    return render(request, 'confirmer_supression.html',{
        "label": filiere
    })


#fichier a telecharger pdf
def export_pdf(request):

    etudiants = Etudiant.objects.filter(admissible='nom')

    nom = request.GET.get("nom")
    sexe = request.GET.get("sexe")
    niveau = request.GET.get("niveau")
    resident = request.GET.get("resident")
    date = request.GET.get("date")
    ufr = request.GET.get("ufr")
    filiere = request.GET.get("filiere")

    if nom:
        etudiants = etudiants.filter(
            Q(nom__icontains=nom) |
            Q(prenoms__icontains=nom)
        )

    if sexe:
        etudiants = etudiants.filter(sexe=sexe)

    if niveau:
        etudiants = etudiants.filter(niveau=niveau)

    if resident:
        etudiants = etudiants.filter(resident=resident)

    if date:
        etudiants = etudiants.filter(date_inscription=date)

    if ufr:
        etudiants = etudiants.filter(filiere__ufr_id=ufr)

    if filiere:
        etudiants = etudiants.filter(filiere_id=filiere)

    # Chemin absolu vers le logo
    logo_path = os.path.join(settings.BASE_DIR, 'etudiant/static/img/logocrou.jpeg')

    template = get_template("pdf_etudiants.html")
    html = template.render({
        "etudiants": etudiants,
        "logo_path": logo_path  # passe le chemin au template
    })

    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename="liste_etudiants.pdf"'

    pisa.CreatePDF(html, dest=response)

    return response


        
#fichier a telecharger excel

def export_excel(request):
    etudiants = Etudiant.objects.all()

    nom = request.GET.get("nom")
    sexe = request.GET.get("sexe")
    niveau = request.GET.get("niveau")
    admissible = request.GET.get("admissible")
    date = request.GET.get("date")
    ufr = request.GET.get("ufr")
    filiere = request.GET.get("filiere")

    if nom:
        etudiants = etudiants.filter(
            Q(nom__icontains=nom) | Q(prenoms__icontains=nom)
        )

    if sexe:
        etudiants = etudiants.filter(sexe=sexe)

    if niveau:
        etudiants = etudiants.filter(niveau=niveau)

    if admissible:
        etudiants = etudiants.filter(admissible=admissible)

    if date:
        etudiants = etudiants.filter(date_inscription=date)

    if ufr:
        etudiants = etudiants.filter(filiere__ufr_id=ufr)

    if filiere:
        etudiants = etudiants.filter(filiere_id=filiere)

    # Création du workbook
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Etudiants"

    # Entêtes (note le petit bug avec "Resident""Chambre" collé corrigé)
    sheet.append([
        "Nom",
        "Prenoms",
        "Niveau",
        "Filiere",
        "UFR",
        "Téléphone",
        "Admis",

    ])

    for e in etudiants:


        sheet.append([
            e.nom,
            e.prenoms,
            e.niveau,
            e.filiere.nom,
            e.filiere.ufr.nom,
            e.telephone,
            "oui" if e.admissible else "non",
        ])

    # Réponse HTTP
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition'] = 'attachment; filename="liste_etudiants.xlsx"'
    workbook.save(response)
    return response


from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from .models import Etudiant


def fiche_reclamation_pdf(request, etudiant_id):

    etudiant = get_object_or_404(
        Etudiant,
        id=etudiant_id
    )

    template = get_template(
        'fiche_reclamation.html'
    )

    html = template.render({
        'etudiant': etudiant
    })

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; '
        f'filename="fiche_reclamation_'
        f'{etudiant.identifiant_permanent}.pdf"'
    )

    pisa_status = pisa.CreatePDF(
        html,
        dest=response
    )

    if pisa_status.err:
        return HttpResponse(
            'Une erreur est survenue lors de la génération du PDF.'
        )

    return response

