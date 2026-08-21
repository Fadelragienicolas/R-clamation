from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Presentation_app, name= 'presentation_app'),
    path('tableau_de_bord/', views.tableau_de_bord, name= 'accueil'),
    path('annee_academique/', views.Annee_academique, name='annee_academique'),
    # path('statistique/', views.Statistique, name='statistique'),
    #LISTE
    path('liste_ufr/', views.Liste_ufr, name='liste_ufr'),
    path('liste_filiere/', views.Liste_filiere, name='liste_filiere'),
    path('liste_etudiant/', views.Liste_etudiant, name='liste_etudiant'),
    #AJOUT
    path('ajout_ufr/', views.Ajout_ufr, name='ajout_ufr'),
    path('ajout_etudiant/', views.Ajout_etudiant, name='ajout_etudiant'),
    path('ajout_filiere/', views.Ajout_filiere, name='ajout_filiere'),
    path('merci/<int:etudiant_id>/', views.merci_view, name='merci'),
    #MODIFIER
    path('modifier_ufr/<int:id>/', views.Modifier_ufr, name='modifier_ufr'),
    path('modifier_etudiant/<int:id>/', views.Modifier_etudiant, name='modifier_etudiant'),
    path('modifier_filiere/<int:id>/', views.Modifier_filiere, name='modifier_filiere'),
    path('modifier_annee/<int:id>/', views.Modifier_annee, name='modifier_annee'),
    #fichier a telecharger excel et pdf
    path('etudiants/pdf/', views.export_pdf, name='export_pdf'),
    path('etudiants/excel/', views.export_excel, name='export_excel'),

    #suppression
    path('etudiant/supprimer/<int:id>/', views.supprimer_etudiant, name='supprimer_etudiant'),
    path('filiere/supprimer/<int:id>/', views.supprimer_filiere, name='supprimer_filiere'),
    path('ufr/supprimer/<int:id>/', views.supprimer_UFR, name='supprimer_ufr'),
    path('fiche_reclamation/<int:etudiant_id>/',views.fiche_reclamation_pdf,name='fiche_reclamation_pdf'),    

] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)