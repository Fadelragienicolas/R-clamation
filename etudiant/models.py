from django.db import models

# TABLE URF
class UFR(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom

# TABLE ANNEE ACADEMIQUE
class AnneeAcademique(models.Model):
    annee_academique = models.CharField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.annee_academique}"

# TABLE FILIERE
class Filiere(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    ufr = models.ForeignKey(
        UFR,
        on_delete=models.CASCADE,
        related_name="filieres"
    )

    annee_academique = models.ForeignKey(
        AnneeAcademique,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return self.nom


# TABLE ETUDIANT
class Etudiant(models.Model):

    SEXE = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]

    OUI_NON = [
        ("oui", "Oui"),
        ("non", "Non"),
    ]

    NIVEAU = [
        ('L1', 'Licence 1'),
        ('L2', 'Licence 2'),
        ('L3', 'Licence 3'),
        ('M1', 'Master 1'),
        ('M2', 'Master 2'),
        ('D', 'Doctorat'),
    ]

    identifiant_permanent = models.CharField(max_length=100)
    photo_identite = models.ImageField(
        upload_to="images/",
        blank=True,
        null=True
    )

    nom = models.CharField(max_length=100)
    prenoms = models.CharField(max_length=150)

    date_naissance = models.DateField()

    sexe = models.CharField(
        max_length=1,
        choices=SEXE
    )

    telephone = models.CharField(max_length=20)

    filiere = models.ForeignKey(
        'Filiere',
        on_delete=models.CASCADE,
        related_name="etudiants"
    )

    niveau = models.CharField(
        max_length=2,
        choices=NIVEAU
    )

    date_inscription = models.DateField(auto_now_add=True)

    admissible = models.CharField(
        max_length=3,
        choices=OUI_NON,
        default = 'non'
    )
    
    def __str__(self):
        return f"{self.identifiant_permanent} - {self.nom} {self.prenoms}"
