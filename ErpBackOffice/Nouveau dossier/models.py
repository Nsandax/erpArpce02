# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.db.models import Max,Sum
from datetime import time, timedelta, datetime, date
import calendar
import json
from random import randint
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from ErpBackOffice.utils.separateur import AfficheEntier
from django.contrib.sessions.models import Session
from django.contrib.auth.signals import user_logged_in, user_logged_out
from dateutil.relativedelta import relativedelta


PlaceType =	(
    (1, "Pays"),
    (2, "Etat / Province"),
    (3, "Ville"),
    (4, "Commune"),
    (5, "Quartier")
)

natureActivite =    (
    (0, "Electronique"),
    (1, "Poste"),
)
Type_Mobilite = (
    (1, "Recrutement"),
    (2, "Promotion"),
    (3, "Mutation"),
    (4, "Détachement"),
    (5, "Démission"),
    (6, "Départ Définitif"),
    (7, "Départ provisoire")

)
statutOp =    (
    (0, "Générée"),
    (1, "En cours"),
    (2, "Traitée"),
    (3, "Annulée"),
)

TypeEntite =    (
    (1, "ARPCE"),
    (2, "Autre"),
)
TypeFacture = (
    (1, "Fournisseur"),
    (2, "Client")
)

natureLigneBgt=    (
    (0, "Active"),
    (1, "Inactive"),
)

natureCharge=    (
    (0, "Variable"),
    (1, "Fixe"),
    (2,"Budget"),
    (3, "Nature"),
)

localite=    (
    (0, "Brazzaville"),
    (1, "Pointe-Noire"),
    (2, "Ouesso"),
    (3, "Dolisie"),
)


TypeBudget =    (
    (1, "Recette"),
    (2, "Dépense"),
)

TypeArticle             =    (
    (1, "Consommable"),
    (2, "Service"),
    (3, "Stockable")
)

TypePaiement = (
    (1, "Règlement"),
    (2, "Envoyer de l'argent"),
    (3, "Transfert interne")
)

MoyenPaiement = (
    (1, "Cash"),
    (2, "Virement Banquaire"),
    (3, "Chèque")
)

MoisAnnee = (
    (1, "Janvier"),
    (2, "Février"),
    (3, "Mars"),
    (4, "Avril"),
    (5, "Mai"),
    (6, "Juin"),
    (7, "Juilllet"),
    (8, "Août"),
    (9, "Septembre"),
    (10, "Octobre"),
    (11, "Novembre"),
    (12, "Décembre")
)

#RH
TypeElementBulletin =    (
    (1, "Gain"),
    (2, "Retenue")
)
CategorieElementBulletin =    (
    (1, "imposable"),
    (2, "Non imposable")
)
TypeCalcul = (
    (1, "Montant fixe"),
    (2, "Pourcentage (%)"),
    (3, "Résultat calcul"),
    (4, "Résultat Barême"),
    (5, "Depend d'une variable"),
)
TypeResultat = (
    (1, "Brut imposable (BI)"),
    (2, "Net imposable (NI)"),
    (3, "Net à payer"),
    (4, "Somme éléments à payer"),
    (5, "Somme éléments à retenir"),
    (6, "HR Dependant")
)
TypeLotBulletin = (
    ("TOUS", "Pour tous agents"),
    ("CERTAINS", "Pour certains agents"),
    ("DEPARTEMENT", "Pour un département")
)
TypeModeleBulletin = (
    (1, "Individuel"),
    (2, "Pour tous")
)
TypeCondition = (
    ("aucun", "Toujours vrai"),
    ("plage", "Plage"),
    ("code", "Expression Python")
)
HorairePaye = (
    (1, "Mensuel"),
    (2, "Bi-mensuel"),
    (3, "Trimestriel"),
    (4, "Semestriel"),
    (5, "Hebdomadaire"),
    (6, "Bi-hebdomadaire"),
    (7, "Annuel")
)
TypeSalaire = (
    (1, "Mensuel"),
    (2, "Horaire")
)
CategoriePros =    (
    ("A", "A"),
    ("B", "B"),
    ("C", "C"),
    ("D", "D"),
    ("E", "E"),
    ("F", "F"),
    ("A'", "A'"),
    ("B'", "B'"),
    ("C'", "C'"),
    ("D'", "D'"),
    ("E'", "E'"),
    ("F'", "F'")
)
TypeRubrique =    (
    (1, "Brut"),
    (2, "Cotisation"),
    (3, "Non-soumise")
)
TypeFormule =    (
    (1, "Nombre x Base"),
    (2, "Nombre x Taux"),
    (3, "Nombre x Base x Taux"),
    (4, "Base x Taux"),
    (5, "Nombre / Base"),
    (6, "Nombre / Taux"),
    (7, "Nombre / Base / Taux"),
    (8, "Base / Taux"),
    (9, "Nombre / Base X Taux"),
    (10, "Nombre X Base / Taux"),
    (11, "Taux / Base"),
    (12, "Taux / Nombre"),
    (13, "Taux / Nombre / Base"),
    (14, "Taux / Nombre X Base"),
    (15, "Montant fixe"),
)

TypeConstante =    (
    (1, "Calcul"),
    (2, "Test"),
    (3, "Tranche"),
    (4, "Valeur"),
    (5, "Rubrique"),
    (6, "Prédefini"),
    (7, "Individuel"),
    (8, "Cumul"),
    (9, "Date")
)

PeriodeCumul =    (
    (1, "Paie en cours"),
    (2, "Mensuelle"),
    (3, "Trimestrielle"),
    (4, "Annuelle"),
    (5, "De date à date")
)

TypeOperationCalcul = (
    (1, "Début"),
    (2, "+"),
    (3, "-"),
    (4, "x"),
    (5, "/"),
    (6, "Mod")
)
TypeOperationTest = (
    (1, "<"),
    (2, "<="),
    (3, ">"),
    (4, ">="),
    (5, "=="),
    (6, "!=")
)
TypeConditionTest = (
    (1, "Début"),
    (2, "Ou"),
    (3, "Et"),
    (4, "sauf")
)

TypeDependant = (
    ("enfant", "Enfant"),
    ("conjoint", "Conjoint"),
    ("conjoint", "Conjointe")
)

StatutRH = (
    (1, "Régulier"),
    (2, "Retraité")
)

# COMPTABILITE
StatutTransaction     =    (
    (1, "Created"),
    (2, "Submitted"),
    (3, "Cancelled"),
    (4, "Success"),
    (5, "Error"),
)
EtatOperationTresorerie = (
    ("created","created"),
    ("closed","closed")
)
TypeJournal = (
    (1, "Ventes"),
    (2, "Achats"),
    (3, "Banque"),
    (4, "Caisse"),
    (5, "Divers")
)
TypeLocal = (
    (1, "Bureau"),
    (2, "Salle de réunion"),
    (3, "Entrepôt"),
    (4, "Bâtiment"),
)
TypeOfTypeCompte = (
    (1, "RECEVABLE"),
    (2, "PAYABLE"),
    (3, "BANQUE ET CAISSE"),
    (4, "AUTRE"),
)
TypeAmortissement=(
    (1,"Linéaire"),
    (2, "Dégressif")
)
UniteDuree = (
    (1,"Mois"),
    (2,"Année")
)
PorteeTaxe = (
    (1, "Ventes"),
    (2, "Achats"),
    (3, "Aucune")
)
TypeOperation = (
    ("Banque", "Banque"),
    ("Caisse", "Caisse")
)

LigneTypeOperation = (
    (1, "Dépôt"),
    (2, "Retrait")
)

TypeMontant = (
    (1, "Fixe"),
    (2, "Pourcentage du prix hors taxe"),
    (3, "Pourcentage du prix TTC")
)
TypeEvenementSocial = (
    (1, "Maternité"),
    (2, "Couverture Maladie"),
    (3, "Frais médicaux"),
    (4, "Evènement familiaux"),
    (5, "Accident de travail"),
    (6, "Enquêtes et Suivi"),
    (7, "Auditions "),
    (8, "Autres")
)
TypeStatus = (
    (1, "Haut Cadre"),
    (2, "Cadre"),
    (3, "Agent de maîtrise"),
    (4, "Agent d'exécution")
)
TypeEcritureAnalytique = (
    (1, "Engagement"),
    (2, "Réel")
)
OrigineCompte = (
    (1, "Natif"),
    (2, "Interne"),
)
#BUDGET
TypeCentre = (
    (1, "Vue Analytique"),
    (2, "Compte Analytique")
)
TypeTransactionBudgetaire = (
    (1, "Normal"),
    (2, "Rallonge"),
    (3, "Diminution"),
    (4, "Dotation")
)

TypeAppelOffre = (
    (0, "Restreint"),
    (1, "National"),
    (2, "International"),
    (3, "Gré à Gré")
)
#INVENTAIRE
TypeTraitement = (
    (1, "Cession"),
    (2, "Mise au rebut")
)
# CALENDRIER
StatutParticipation = (
    (1, "En attente"),
    (2, "Accepté"),
    (3, "Refusé"),
    (4, "Incertain")
)
Disponibilite = (
    (1, "Libre"),
    (2, "Occupé")
)
TypeAlarme = (
    (1, "Notification"),
    (2, "Email"),
    (3, "Notification et Email")
)
TypeIntervalle = (
    (1, "Munites"),
    (2, "Heures"),
    (3, "Jours")
)
TypeRecurrent = (
    (1, "Jours"),
    (2, "Semaines"),
    (3, "Mois"),
    (4, "Années")
)
TypeFinRecurrent = (
    (1, "Nombre de répétitions"),
    (2, "Date de fin")
)
Confidentialite = (
    (1, "Tout le monde"),
    (2, "Utilisateur interne seulement"),
    (3, "Moi seulement"),
)
JoursDelaSemaine = (
    ('1', 'Lundi'),
    ('2', 'Mardi'),
    ('3', 'Mercredi'),
    ('4', 'Jeudi'),
    ('5', 'Vendredi'),
    ('6', 'Samedi'),
    ('7', 'Dimanche')
)
ParMois = (
    (1, 'Date dans le mois'),
    (2, 'Jour du mois')
)
ParJour = (
    (1, 'Premier'),
    (2, 'Seconde'),
    (3, 'Troisième'),
    (4, 'Quatrième'),
    (5, 'Cinquième'),
    (-1, 'Dernier')
)
# RECOUVREMENT
StatutRecouvrement = (
    (1, "En cours"),
    (2, "fermé")
)
TypeRelance = (
    (1, "Email"),
    (2, "Visite"),
    (3, "Téléphonique"),
    (4, "Courrier")
)
#CONTRAT
TypeOperation = (
    (1, "Montant fixe"),
    (2, "Pourcentage"),
)
CategorieOperation = (
    (1, "Facture"),
    (2, "Avenant (+)"),
    (3, "Avenant (-)")
)

# WORKFLOW
TypeOperateur = (
    (1, "OR"),
    (2, "AND")
)
TypeCombinaison = (
    (1, "Exploitation"),
    (2, "Projet")
)

TypeDuree = (
    (1, "6 Mois"),
    (2, "12 Mois")
)

choixGraphique = (
    (0, "Graphiques recommandés"),
    (1, "Barchart"),
    (2, "Doughnut Chart"),
    (3, "Horizontal Chart")
)

# COMMON MODEL
class Model_Personne(models.Model):
    #Propriete commune à toutes personnes
    prenom                    =    models.CharField(max_length = 50, null = True, blank = True)
    nom                        =    models.CharField(max_length = 50, null = True, blank = True)
    nom_complet                =    models.CharField(max_length = 100, null = True, blank = True)
    image                    =    models.CharField(max_length = 700, null = True, blank = True, default="")
    email                    =    models.CharField(max_length = 150, null = True, blank = True, default="")
    phone                    =    models.CharField(max_length = 100, null = True, blank = True, default="")
    adresse                    =    models.CharField(max_length = 500, null = True, blank = True, default="")
    commune_quartier           =    models.ForeignKey("Model_Place", on_delete = models.SET_NULL, related_name="personnes", null = True, blank = True)
    est_actif                 =    models.BooleanField(default = True)
    creation_date            =     models.DateTimeField(auto_now_add = True,null=True,blank=True)
    auteur                    =     models.ForeignKey("Model_Personne", on_delete = models.SET_NULL, related_name="personnes_creees", null = True, blank = True)
    compte                    =    models.ForeignKey("Model_Compte", on_delete = models.SET_NULL, related_name="responsable_crees", null = True, blank = True)
    est_particulier            =    models.BooleanField(default=False)
    url                    =     models.CharField(max_length = 600, blank=True, null=True)
    #postnom                    =    models.CharField(max_length = 50, null = True, blank = True)
    #civilite                =    models.ForeignKey("Model_Civilite", on_delete=models.SET_NULL, null = True, blank = True)
    #langue                    =    models.CharField(max_length = 50, null = True, blank = True, default="")
    #type                    =    models.CharField(max_length = 30, null = True, blank = True)
    #bp                         =    models.CharField(max_length = 50, null = True, blank = True)
    #lieu_de_naissance         =    models.CharField(max_length = 50, blank=True, null=True)
    #date_de_naissance        =    models.DateField(max_length = 50, null = True, blank = True)


    def __str__(self):
        if self.nom_complet != None and self.nom_complet != "":
            return self.nom_complet
        else: return "%s %s" % (self.prenom, self.nom)

    @property
    def annee_naissance(self):
        return self.date_de_naissance.year



    @property
    def adresse_complete(self):
        place = Model_Place.objects.get(pk = self.commune_quartier_id)
        adresse = place.designation
        i = 1
        while place.parent_id != None and place.parent_id != 0:
            place = Model_Place.objects.get(pk = place.parent_id)
            if i % 2 == 0 : adresse = adresse + ', \n' + place.designation
            else : adresse = adresse + ', \n' + place.designation
        return self.adresse + ', \n' + adresse

    @property
    def utilisateur(self):
        if self.user_id == None: return None

        user = User.objects.get(pk = self.user_id)
        return user

class Model_Civilite(models.Model):
    designation                =    models.CharField(max_length = 20)
    designation_court        =    models.CharField(max_length = 5)
    auteur                    =    models.ForeignKey(Model_Personne, related_name="auteur_civilite", null = True, blank = True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.designation


class Model_Place(models.Model):
    designation                =    models.CharField(max_length = 50, null = True, blank = True)
    code_telephone            =    models.CharField(max_length = 5, null = True, blank = True)
    place_type                =    models.IntegerField(choices = PlaceType)
    code_pays                =    models.CharField(max_length=3, null = True, blank = True, default="")
    parent                    =    models.ForeignKey("Model_Place", null = True, blank = True, on_delete = models.CASCADE, related_name="fils")
    url                    =     models.CharField(max_length = 250, blank=True, null=True)
    auteur                    =    models.ForeignKey(Model_Personne, related_name="auteur_place", null = True, blank = True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.designation

    @property
    def places_filles(self):
        return Model_Place.objects.filter(parent_id = self.id)

#New way Of droit

class Model_Module(models.Model):
    nom_module                =    models.CharField(max_length = 50, null = True, blank = True)
    nom_application           =    models.CharField(max_length = 100, null = True, blank = True)
    code                    =    models.CharField(max_length = 5, null = True, blank = True)
    description                =    models.TextField(null = True, blank = True)
    est_installe            =    models.BooleanField(default = False)
    url_vers                =    models.CharField(max_length = 100, null = True, blank = True)
    numero_ordre            =    models.IntegerField()
    icon_module                =    models.CharField(max_length = 50, default = "", null = True, blank = True)
    couleur                    =    models.CharField(max_length = 15, default = "", null = True, blank = True)
    url =     models.CharField(max_length = 250, blank=True, null=True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    auteur                   =    models.ForeignKey(Model_Personne, related_name="auteur_module", null = True, blank = True, on_delete=models.SET_NULL)

    def __str__(self):
        return "Module %s" % self.nom_module

    @property
    def nombre_periode(self):
        return Model_Operationnalisation_module.objects.filter(module_id = self.id).count()
    @property
    def periode_active(self):
        return Model_Operationnalisation_module.objects.filter(module_id = self.id).filter(est_active = True).count()

    @property
    def periode_cloture(self):
        return Model_Operationnalisation_module.objects.filter(module_id = self.id).filter(est_cloture = True).count()

class Model_GroupeMenu(models.Model):
    designation        = models.CharField(max_length = 50, null = True, blank = True)
    icon_menu          = models.CharField(max_length = 150, null = True, blank = True)
    description        = models.CharField(max_length = 250, null = True, blank = True)
    module             = models.ForeignKey(Model_Module, related_name="module_of_groupemenu", on_delete=models.CASCADE)
    url                = models.CharField(max_length = 250, blank=True, null=True)
    numero_ordre       =    models.IntegerField()
    creation_date      =    models.DateTimeField(auto_now=True)
    auteur             = models.ForeignKey(Model_Personne, related_name="auteur_of_groupe_menu", null = True, blank = True, on_delete=models.SET_NULL)

    def __str__(self):
        return "Groupe %s / %s" % (self.designation, self.module.nom_module)


class Model_SousModule(models.Model):
    module                    =    models.ForeignKey(Model_Module, related_name="sous_modules", on_delete=models.CASCADE)
    nom_sous_module            =    models.CharField(max_length = 50, null = True, blank = True)
    description                =    models.TextField(null = True, blank = True)
    groupe                    =    models.CharField(max_length = 50, null = True, blank = True)
    icon_menu          = models.CharField(max_length = 150, null = True, blank = True)
    url_vers                =    models.CharField(max_length = 100, null = True, blank = True)
    numero_ordre            =    models.IntegerField()
    est_model               =    models.BooleanField(default = False)
    est_dashboard            =      models.BooleanField(default = False)
    est_actif            =      models.BooleanField(default = True)
    model_principal            =    models.ForeignKey(ContentType, on_delete=models.SET_NULL, blank=True, null=True)
    groupe_menu               =    models.ForeignKey(Model_GroupeMenu, related_name="groupe_menu",  blank=True, null=True, on_delete=models.SET_NULL)
    update_date                 =    models.DateTimeField(auto_now_add = True)
    #permissions        =    models.ManyToManyField("Model_Permission", related_name="permission_related_to_sous_module", blank = True)
    url                    =     models.CharField(max_length = 250, blank=True, null=True)
    creation_date            =    models.DateTimeField(auto_now=True)
    auteur                    =    models.ForeignKey(Model_Personne, related_name="auteur_sous_module", null = True, blank = True, on_delete=models.SET_NULL)

    def __str__(self):
        return "Module %s / %s" % (self.module.nom_module, self.nom_sous_module)

#Ex Equivalent à Model_Droit
class Model_Permission(models.Model):
    sous_module              =    models.ForeignKey(Model_SousModule, on_delete = models.SET_NULL, related_name="permission_of_sous_module", null = True, blank = True)
    designation              =    models.CharField(max_length = 50, null = True, blank = True)
    numero                   =    models.IntegerField(null = True, blank = True, unique = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    auteur                   =    models.ForeignKey(Model_Personne, related_name="auteur_permission", null = True, blank = True, on_delete=models.SET_NULL)

    def __str__(self):
        if self.sous_module:
            name = self.sous_module.module.nom_module
        else:
            name = "Rien"
        return "Permission %s / %s" % (self.designation, name)


#Ex Equivalent à Model_Role
class Model_GroupePermission(models.Model):
    designation              =    models.CharField(max_length = 100, null = True, blank = True)
    permissions              =    models.ManyToManyField("Model_Permission", related_name="permission_related_to_a_group", blank = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_of_groupe", null = True, blank = True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation


    def stat(self):
        stat = {}
        modules = []
        sous_modules = []
        try:
            permissions = self.permissions.all()
            for permission in permissions:
                if permission.sous_module:
                    sous_modules.append(permission.sous_module)
                    if permission.sous_module.module:
                        modules.append(permission.sous_module.module)
            modules = set(modules)
            modules = list(modules)
            sous_modules = set(sous_modules)
            sous_modules = list(sous_modules)
            stat["nombre_module"] = len(modules)
            stat["nombre_sous_module"] = len(sous_modules)
            return stat

        except Exception as e:
            #print("ERREUR")
            #print(e)
            return 0

class Model_GroupePermissionUtilisateur(models.Model):
    groupe_permission        =    models.ForeignKey(Model_GroupePermission, related_name="groupe_permission", null = True, blank = True, on_delete=models.CASCADE)
    utilisateur              =    models.ForeignKey(Model_Personne, on_delete=models.CASCADE)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    auteur                   =    models.ForeignKey(Model_Personne, related_name="auteur_groupe_permission_utilisateur", null = True, blank = True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.utilisateur.nom_complet + " / " + self.groupe_permission.designation

class Model_Regle(models.Model):
    designation             =    models.CharField(max_length = 100, null = True, blank = True)
    filtre                  =    models.CharField(max_length = 250, null = True, blank = True)
    #permission             =    models.ForeignKey(Model_Permission, related_name="regle_link_to_permission", on_delete=models.CASCADE,  blank = True, null = True)
    permissions             =    models.ManyToManyField(Model_Permission, related_name="regle_link_to_all_permission")
    groupe_permission       =    models.ForeignKey(Model_GroupePermission, related_name="regle_link_to_a_group", on_delete=models.CASCADE, null = True, blank = True)
    auteur                  =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_of_regle", null = True, blank = True)
    statut                  =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =    models.CharField(max_length=50, blank=True, null=True)
    update_date             =    models.DateTimeField(auto_now=True)
    creation_date           =    models.DateTimeField(auto_now_add=True)
    url                     =    models.CharField(max_length = 250, blank=True, null=True)
    def __str__(self):
        return " %s / %s" % (self.groupe_permission.designation, self.designation)

#End new way of droit

class Model_ActionUtilisateur(models.Model):
    nom_action               =    models.CharField(max_length = 200, null = True, blank = True)
    ref_action               =    models.CharField(max_length = 200, default = "", null = True, blank = True)
    description              =    models.TextField()
    permission               =    models.ForeignKey(Model_Permission, on_delete = models.SET_NULL, related_name="actions", null = True, blank = True)
    url                      =     models.CharField(max_length = 250, blank=True, null=True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    auteur                   =    models.ForeignKey(Model_Personne, related_name="auteur_action_utilisation", null = True, blank = True, on_delete=models.SET_NULL)

    def __str__(self):
        return "ACTION %s" % self.nom_action

class Model_ActionSousModule(models.Model):
    action                   =    models.ForeignKey(Model_ActionUtilisateur, on_delete=models.CASCADE)
    sous_module              =    models.ForeignKey(Model_SousModule, on_delete=models.CASCADE)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    auteur                   =    models.ForeignKey(Model_Personne, related_name="auteur_action_sous_module", null = True, blank = True, on_delete=models.SET_NULL)

    def __str__(self):
        return "Module %s / %s - %s" % (self.sous_module.module.nom_module, self.sous_module.nom_sous_module, self.action)

class Model_Role(models.Model):
    nom_role                 =    models.CharField(max_length = 50, null = True, blank = True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="roles_crees", null = True, blank = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    url                      =     models.CharField(max_length = 250, blank=True, null=True)


    def __str__(self):
        return self.nom_role

    def contient_module(self, module_id):
        module_id = int(module_id)
        try:
            role_module = Model_RoleModule.objects.filter(role_id = self.id).get(module_id = module_id)
            if role_module != None: return True
            else: return False
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return False

    def contient_sousmodule(self, sous_module_id):
        sous_module_id = int(sous_module_id)
        try:
            role_sousmodule = Model_RoleSousModule.objects.filter(role_id = self.id).get(sous_module_id = sous_module_id)
            if role_sousmodule != None: return True
            else: return False
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return False

    def contient_action(self, action_id):
        action_id = int(action_id)
        try:
            role_action = Model_RoleAction.objects.filter(role_id = self.id).get(action_id = action_id)
            if role_action != None: return True
            else: return False
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return False

class Model_RoleModule(models.Model):
    role                     =    models.ForeignKey(Model_Role, on_delete=models.CASCADE, related_name="modules_role")
    module                   =    models.ForeignKey(Model_Module, on_delete=models.CASCADE)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="attachements_role_module", null = True, blank = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return "%s a accès au %s" % (self.role, self.module)

class Model_RoleSousModule(models.Model):
    role                     =    models.ForeignKey(Model_Role, on_delete=models.CASCADE, related_name="sous_modules_role")
    sous_module              =    models.ForeignKey(Model_SousModule, on_delete=models.CASCADE)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="attachements_role_sous_module", null = True, blank = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return "%s a accès au %s" % (self.role, self.sous_module)

class Model_RoleAction(models.Model):
    role                     =    models.ForeignKey(Model_Role, on_delete=models.CASCADE, related_name="actions_role")
    action                   =    models.ForeignKey(Model_ActionSousModule, on_delete=models.CASCADE)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="actions_attribues", null = True, blank = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return "%s a accès au %s" % (self.role, self.action)


class Model_ModuleOverModel(models.Model):
    nom_modele               =    models.CharField(max_length = 100)
    module_id                =    models.ForeignKey(Model_Module, on_delete=models.SET_NULL, null=True)
    model_id                 =    models.ForeignKey(ContentType, on_delete=models.SET_NULL, blank=True, null=True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)
    auteur                   =    models.ForeignKey(Model_Personne, related_name="auteur_moduleovermodel", null = True, blank = True, on_delete=models.SET_NULL)

    def __str__(self):
        return "%s" % (self.nom_modele)

class Model_Droit(models.Model):
    sous_module              =    models.ForeignKey(Model_SousModule, on_delete = models.SET_NULL, related_name="rel_droit", null = True, blank = True)
    droit                    =    models.CharField(max_length = 50, null = True, blank = True)
    roles                    =    models.CharField(max_length = 500, null = True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    auteur                   =    models.ForeignKey(Model_Personne, related_name="auteur_droit", null = True, blank = True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.droit

class Model_RoleUtilisateur(models.Model):
    utilisateur              =    models.ForeignKey(Model_Personne, on_delete=models.CASCADE)
    role                     =    models.ForeignKey(Model_Role, on_delete=models.CASCADE, related_name="utilisateurs_role")
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="roles_attribues", null = True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.utilisateur.nom_complet + ' --- ' + self.role.nom_role


class Model_Categorie(models.Model):
    designation              =    models.CharField(max_length = 30)
    url                      =    models.CharField(max_length = 30, default = "")
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    auteur                   =    models.ForeignKey(Model_Personne, related_name="categories", on_delete=models.SET_NULL ,null = True, blank = True)
    type                     =    models.CharField(max_length = 15)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation

class Model_Unite(models.Model):
    designation              =    models.CharField(max_length = 50)
    symbole_unite            =    models.CharField(max_length = 20)
    url                      =    models.CharField(max_length = 30, default = "")
    est_systeme              =    models.BooleanField(default = False)
    categorie_unite          =    models.ForeignKey(Model_Categorie, related_name="unites", on_delete=models.CASCADE)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    auteur                   =    models.ForeignKey(Model_Personne, related_name="unites", null = True, blank = True, on_delete=models.SET_NULL)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation


class Model_FournisseurArticle(models.Model):
    article                  =    models.ForeignKey("Model_Article", on_delete=models.CASCADE)
    fournisseur              =    models.ForeignKey(Model_Personne, on_delete=models.CASCADE)
    quantite_minimale        =    models.FloatField(default=0)
    prix_unitaire            =    models.FloatField(default=1)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    auteur                   =    models.ForeignKey(Model_Personne, related_name="fournisseurs_article", on_delete=models.SET_NULL, blank=True, null=True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        fournisseur = Model_Personne.objects.get(pk = self.fournisseur_id)
        article = Model_Article.objects.get(pk = self.article_id)
        return "%s fourni par %s" % (article.designation, fournisseur.nom_complet)


class Model_UniteAchatArticle(models.Model):
    article                  =    models.ForeignKey("Model_Article", on_delete=models.CASCADE, related_name="unites_achat")
    unite                    =    models.ForeignKey(Model_Unite, on_delete=models.CASCADE)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    auteur                   =    models.ForeignKey(Model_Personne, related_name="unites_achat", null = True, blank = True, on_delete=models.SET_NULL )
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        unite = Model_Unite.objects.get(pk = self.unite_id)
        article = Model_Article.objects.get(pk = self.article_id)

        return "%s à(au) %s" % (article.designation, unite.designation)


class Model_Article(models.Model):
    image                    =    models.CharField(max_length = 500, null = True, blank = True, default="")
    designation              =    models.CharField(max_length = 50, null = True, blank = True)
    designation_court        =    models.CharField(max_length = 10, null = True, blank = True, default="")
    code_article             =    models.CharField(max_length = 50, null = True, blank = True, default="")
    code_barre               =    models.CharField(max_length = 50, null = True, blank = True, default="")
    type_article             =    models.IntegerField(choices = TypeArticle, null = True, blank = True)
    categorie                =    models.ForeignKey(Model_Categorie, on_delete=models.SET_NULL, blank=True, null=True, related_name="categories_articles")
    prix_unitaire            =    models.FloatField()
    est_achetable            =    models.BooleanField(default = False)
    est_vendable             =    models.BooleanField(default = False)
    est_stockable            =    models.BooleanField(default = False)
    est_manufacturable       =    models.BooleanField(default = False)
    est_amortissable         =    models.BooleanField(default = False)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    unite_fonctionnelle      =    models.ForeignKey("Model_Unite_fonctionnelle", on_delete = models.SET_NULL, related_name="article_of_unite_fonctionnelle", null = True, blank = True)
    unite                    =    models.ForeignKey(Model_Unite, on_delete=models.SET_NULL, blank=True, null=True, related_name="unites_articles")
    compte                   =    models.ForeignKey("Model_Compte", on_delete=models.SET_NULL, blank = True, null = True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="articles", null = True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)


    def __str__(self):
        return self.designation

    def value_type_article(self):
        if self.type_article:
            return dict(TypeArticle)[int(self.type_article)]

    def checkAsset(self):
        Serie = Model_Asset.objects.filter(article_id = self.id)
        if Serie != None:
            return True
        else:
            return False

    @property
    def disponible(self):
        dispo = Model_StockArticle.objects.filter(article_id = self.id).aggregate(Sum('quantite_disponible'))
        dispo = dispo['quantite__sum']

        if dispo == None:
            return 0
        return dispo

    @property
    def valeur_inventaire(self):
        return self.disponible * self.prix_unitaire


    @property
    def separateur_prix_unitaire(self):
        return AfficheEntier(float(self.prix_unitaire))

    @property
    def est_service(self):
        if self.type_article == 2: return True
        return False

    @property
    def quantite_stock(self):
        try:

            if self.est_service: return "INFINIE"

            type_emplacement = Model_TypeEmplacement.objects.filter(est_systeme = True).get(designation = "STOCK")
            if type_emplacement == None : return 0

            quantite_stock = 0
            emplacements = Model_Emplacement.objects.filter(type_emplacement_id = type_emplacement.id)
            for emplacement in emplacements :
                stocks = Model_StockArticle.objects.filter(article_id = self.id).filter(emplacement_id = emplacement.id)
                for stock in stocks :
                    quantite_stock = quantite_stock + stock.quantite_disponible
            return quantite_stock
        except Exception as e:
            return 0

    @property
    def quantite_prevue(self):
        try:
            if self.est_service: return "INFINIE"
            quantite_prevue = 0
            type_emplacement = Model_TypeEmplacement.objects.filter(est_systeme = True).get(designation = "IN")
            if type_emplacement == None : return quantite_prevue

            emplacements = Model_Emplacement.objects.filter(type_emplacement_id = type_emplacement.id)
            for emplacement in emplacements :
                stocks = Model_StockArticle.objects.filter(article_id = self.id).filter(emplacement_id = emplacement.id)
                for stock in stocks :
                    quantite_prevue = quantite_prevue + stock.quantite_disponible

                    bons_achat = Model_Bon_reception.objects.filter(date_prevue__isnull = False).filter(est_realisee = False)
                    for bon in bons_achat :
                        lignes = Model_Ligne_reception.objects.filter(bon_reception_id = bon.id).filter(stock_article_id = stock.id)
                        for ligne in lignes :
                            quantite_prevue = quantite_prevue + ligne.quantite_demande
            #return quantite_prevue + self.quantite_stock
            return quantite_prevue
        except Exception as e:
            return 0

    @property
    def quantite_stock_of_emplacement(self, id_emplacement):
        try:
            if self.est_service: return "INFINIE"
            quantite_stock = 0
            if id_emplacement != 0:
                stocks = Model_StockArticle.objects.filter(article_id = self.id).filter(emplacement_id = id_emplacement)
                for stock in stocks :
                    quantite_stock = quantite_stock + stock.quantite_disponible
            return quantite_stock
        except Exception as e:
            return 0

    @property
    def nombre_achat(self):
        nombre_achat = 0
        try:
            fournitures = Model_Bon_reception.objects.all()#TODO les fournitures sont les bons validés (donc les achats en attente de livraison)
            for fourniture in fournitures :
                lignes = Model_Ligne_reception.objects.filter(bon_reception_id = fourniture.id)
                for ligne in lignes :
                    if ligne.stock_article.article_id == self.id :
                        nombre_achat = nombre_achat + 1
            return nombre_achat
        except Exception as e:
            return nombre_achat

    @property
    def nombre_vente(self):
        nombre_vente = 0
        try:
            commandes = Model_Bon_commande.objects.all()#TODO Ici aussi récupérer que le bon validé
            for commande in commandes :
                lignes = Model_Ligne_commande.objects.filter(bon_commande_id = commande.id)
                for ligne in lignes :
                    if ligne.stock_article.article_id == self.id :
                        nombre_vente = nombre_vente + 1
            return nombre_vente
        except Exception as e:
            return nombre_vente


class Model_TypeArticle(models.Model):
    nature                   =    models.CharField(max_length = 20, null = True, blank = True)
    est_stockable            =    models.BooleanField(default = False)
    est_amortissable         =    models.BooleanField(default = False)
    duree_amortissement      =    models.CharField(max_length = 20, null = True, blank = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    auteur                   =    models.ForeignKey(Model_Personne, default=None, null=True, blank=True, on_delete=models.SET_NULL)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

class Model_Devise(models.Model):
    symbole_devise           =    models.CharField(max_length = 5, null = True, blank = True)
    code_iso                 =    models.CharField(max_length = 3, null = True, blank = True)
    designation              =    models.CharField(max_length = 20, null = True, blank = True)
    est_reference            =    models.BooleanField(default = False)
    est_active               =    models.BooleanField(default = False)
    est_virtuelle            =    models.BooleanField(default = False)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    auteur                   =    models.ForeignKey(Model_Personne, default=None, null=True, blank=True, on_delete=models.SET_NULL)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation


class Model_Taux(models.Model):
    devise_depart            =    models.ForeignKey(Model_Devise, on_delete = models.SET_NULL, related_name="taux_lies", null = True, blank = True)
    devise_arrive            =    models.ForeignKey(Model_Devise,on_delete = models.SET_NULL,  related_name="taux_subits", null = True, blank = True)
    montant                  =    models.FloatField()
    est_courant              =    models.BooleanField(default = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="taux_crees", null = True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

# MODULE ARCHIVAGE

class Model_Dossier(models.Model):
    designation              =    models.CharField(max_length = 100, null = True, blank=True, default = '')
    description              =    models.CharField(max_length = 500, null = True, blank=True, default = '')
    url_dossier              =    models.CharField(max_length = 100, null = True, blank=True, default = 'default storage')
    dossier                  =    models.ForeignKey("Model_Dossier", on_delete = models.SET_NULL, related_name = 'dossier_fk_eja', null = True, blank = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    created_at               =    models.DateTimeField(auto_now_add = True)
    update_at                =    models.DateTimeField(auto_now = True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_dossier_osx', null = True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation
    @property
    def hisdossier(self):
        cont = Model_Dossier.objects.get(pk = self.dossier_id)
        return cont.designation


class Model_Document(models.Model):
    type_document            =     models.CharField(max_length = 600, null = True, blank=True, default = '')
    url_document             =     models.CharField(max_length = 600, null = True, blank=True, default = '')
    bon_reception            =     models.ForeignKey("Model_Bon_reception", on_delete = models.SET_NULL, blank=True, null=True, default=None, related_name="doc_bons_receptions")
    demande_achat            =     models.ForeignKey("Model_Demande_achat", on_delete = models.SET_NULL, blank=True, null=True, default=None, related_name="doc_demande")
    bon_transfert            =     models.ForeignKey("Model_Bon_transfert", on_delete = models.SET_NULL, blank=True, null=True, default=None, related_name="doc_bons_transfert")
    bon_entree               =     models.ForeignKey("Model_Bon", on_delete = models.SET_NULL, blank=True, null=True, default=None, related_name="doc_bons_entree")
    facture                  =     models.ForeignKey("Model_Facture", on_delete = models.SET_NULL, blank=True, null=True, default=None, related_name="doc_factures")
    paiement                 =     models.ForeignKey("Model_Paiement", on_delete = models.SET_NULL, blank=True, null=True, default=None, related_name="doc_paiements")
    numero_document          =     models.CharField(max_length = 600, null = True, blank=True, default = '')
    description              =     models.CharField(max_length = 600, null = True, blank=True, default = '')
    est_verifie              =     models.BooleanField(default = False)
    etat_facturation         =     models.ForeignKey("Model_Etat_Facturation", on_delete = models.SET_NULL, blank=True, null=True, default=None, related_name="doc_etat_facturation")
    index                    =     models.TextField(blank=True)
    content_type             =     models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    source_document_id       =     models.PositiveIntegerField(blank=True, null=True)
    content_object           =     GenericForeignKey('content_type', 'source_document_id')
    status                   =     models.CharField(max_length = 600, null = True, blank=True, default = '')
    metadonnees              =     models.TextField(null = True, blank=True)
    statut                   =     models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =     models.CharField(max_length=50, blank=True, null=True)
    created_at               =     models.DateTimeField(auto_now_add = True)
    dossier                  =     models.ForeignKey("Model_Dossier", on_delete = models.SET_NULL, related_name = 'dossier_fk_xjc', null = True, blank = True)
    update_at                =     models.DateTimeField(auto_now = True)
    auteur                   =     models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_document_oej', null = True, blank = True)
    url                      =     models.CharField(max_length = 600, blank=True, null=True)
    taille                   =     models.CharField(max_length = 100, blank=True, null=True)

    def __str__(self):
        return str(self.id)
    @property
    def hisdossier(self):
        cont = Model_Dossier.objects.get(pk = self.dossier_id)
        return cont.designation

# MODULE ACHAT

class Model_Fournisseur(Model_Personne):
    denomination             =    models.CharField(max_length = 100, blank=True, null=True)
    domaine                  =    models.CharField(max_length = 50, blank=True, null=True)
    categorie                =    models.CharField(max_length = 100, blank=True, null=True)
    date_fondation           =    models.DateTimeField(auto_now_add = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)


class Model_Expression(models.Model):
    numero_expression        =    models.CharField(max_length = 100, null = True, blank=True, default = '')
    demandeur                =    models.ForeignKey("Model_Employe", on_delete=models.SET_NULL, blank=True, null=True, related_name="expressions")
    date_expression          =    models.DateTimeField(blank=True, null=True)
    ligne_budgetaire         =    models.ForeignKey("Model_LigneBudgetaire", on_delete=models.SET_NULL, blank=True, null=True, related_name="budget_expression")
    justification            =    models.CharField(max_length = 300, null = True, blank=True, default = '')
    services_ref             =    models.ForeignKey("Model_Unite_fonctionnelle", blank=True, null=True, on_delete = models.SET_NULL, default=None, related_name="services_refer")
    centre_cout              =    models.ForeignKey("Model_Centre_cout", on_delete = models.SET_NULL, related_name = 'centre_cout_fk_expression', null = True, blank = True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    document                 =    models.CharField(max_length = 100, blank=True, null=True)
    #codes_budgetaires       =    models.ManyToManyField("Model_LigneBudgetaire", related_name="demandes_code")
    #requete                 =    models.ForeignKey("Model_Requete_demande", on_delete = models.SET_NULL, related_name="request_of_demande", null = True, blank = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_of_expression", null = True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    '''def __str__(self):
        return self.numero_expression'''



class Model_Ligne_Expression(models.Model):
    expression               =    models.ForeignKey(Model_Expression, on_delete = models.CASCADE, related_name="ligne_of_expression", null = True, blank = True)
    quantite_demande         =    models.IntegerField()
    quantite_restante        =    models.IntegerField(null=True)
    prix_unitaire            =    models.FloatField()
    description              =    models.CharField(max_length = 50, blank=True, null=True)
    unite_achat              =    models.ForeignKey(Model_UniteAchatArticle, null = True, blank = True, on_delete=models.SET_NULL)
    article                  =    models.ForeignKey(Model_Article, on_delete = models.SET_NULL, related_name="article_of_ligne_expression", null = True, blank = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)
    auteur                   =    models.ForeignKey(Model_Personne, related_name="auteur_ligne_expression", null = True, blank = True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.expression.numero_expression

    def montant_total(self):
        return self.prix_unitaire * self.quantite_demande

class Model_Demande_achat(models.Model):
    numero_demande           =    models.CharField(max_length = 100, null = True, blank=True, default = '')
    demandeur                =    models.ForeignKey("Model_Employe", on_delete=models.SET_NULL, blank=True, null=True, related_name="demandeurs")
    url                      =    models.CharField(max_length = 250, blank=True, null=True)
    expression               =    models.ForeignKey("Model_Expression", on_delete=models.SET_NULL, blank=True, null=True, related_name="expression")
    date_demande             =    models.DateTimeField(blank=True, null=True)
    expressions              =    models.ManyToManyField("Model_Expression")
    centre_cout              =    models.ForeignKey("Model_Centre_cout", on_delete = models.SET_NULL, related_name = 'centre_cout_fk_demande', null = True, blank = True)
    fournisseur              =    models.ForeignKey(Model_Fournisseur,on_delete = models.SET_NULL, related_name="fournisseur_preparation_for_bon_commande", null = True, blank = True)
    est_groupe               =    models.BooleanField(default = False)
    description              =    models.CharField(max_length = 300, null = True, blank=True, default = '')
    services_ref             =    models.ForeignKey("Model_Unite_fonctionnelle", blank=True, null=True, on_delete = models.SET_NULL, default=None, related_name="services_ref")
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    type_demande             =    models.CharField(max_length = 100, null = True, blank=True, default = '')
    document                 =    models.CharField(max_length = 100, blank=True, null=True)
    #codes_budgetaires       =    models.ManyToManyField("Model_LigneBudgetaire", related_name="demandes_code")
    #requete                 =    models.ForeignKey("Model_Requete_demande", on_delete = models.SET_NULL, related_name="request_of_demande", null = True, blank = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True, related_name="statut_demande")
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_of_demande_achat", null = True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)


    def __str__(self):
        return self.numero_demande

    @property
    def montant_total(self):
        try:
            somme = 0
            lignes = Model_Ligne_demande_achat.objects.filter(demande_achat = self)
            for ligne in lignes:
                somme += ligne.montant_total
            return somme
        except Exception as e:
            return 0


class Model_Ligne_demande_achat(models.Model):
    demande_achat            =    models.ForeignKey(Model_Demande_achat, on_delete = models.CASCADE, related_name="ligne_of_demande", null = True, blank = True)
    quantite_demande         =    models.IntegerField()
    prix_unitaire            =    models.FloatField()
    description              =    models.CharField(max_length = 50, blank=True, null=True)
    unite_achat              =    models.ForeignKey(Model_UniteAchatArticle, null = True, blank = True, on_delete=models.SET_NULL)
    article                  =    models.ForeignKey(Model_Article, on_delete = models.SET_NULL, related_name="article_of_ligne_demande", null = True, blank = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)
    auteur                   =    models.ForeignKey(Model_Personne, related_name="auteur_ligne_demande", null = True, blank = True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.demande_achat.numero_demande

    @property
    def montant_total(self):
        return float(self.prix_unitaire) * float(self.quantite_demande)

class Model_Bon_reception(models.Model):
    numero_reception         =    models.CharField(max_length = 100, null = True, blank=True, default = '')
    date_prevue              =    models.DateTimeField(default = timezone.now, blank=True, null=True)
    date_reception           =    models.DateTimeField(blank=True, null=True,default = timezone.now)
    montant_total            =    models.FloatField(blank=True, null=True)
    devise                   =    models.ForeignKey(Model_Devise,on_delete = models.SET_NULL,  related_name="bon_receptions", null = True, blank = True)
    ligne_budgetaire         =    models.ForeignKey("Model_LigneBudgetaire", on_delete=models.SET_NULL, blank=True, null=True, related_name="budget_achat")
    codes_budgetaires        =    models.ManyToManyField("Model_LigneBudgetaire", related_name="demandes")
    est_realisee             =    models.BooleanField(default = False)
    url                      =    models.CharField(max_length = 100, default = "")
    reference_document       =    models.CharField(max_length = 300, null = True, blank=True, default = '')
    description              =    models.CharField(max_length = 300, null = True, blank=True, default = '')
    est_groupe               =    models.BooleanField(default = False)
    document                 =    models.ForeignKey(Model_Document,on_delete = models.SET_NULL, related_name="document_bon_reception", null = True, blank = True)
    fournisseur              =    models.ForeignKey(Model_Fournisseur,on_delete = models.SET_NULL, related_name="fournisseur_bon_reception", null = True, blank = True)
    demande_achat            =    models.ForeignKey("Model_Demande_achat",on_delete = models.SET_NULL, related_name="from_demande_bon_reception", null = True, blank = True)
    demandes_achat           =    models.ManyToManyField("Model_Demande_achat")
    condition_reglement      =    models.ForeignKey("Model_ConditionReglement", on_delete=models.SET_NULL, related_name="conditions_reglement", blank=True, null=True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True, related_name="statut_bon_reception")
    etat                     =    models.CharField(max_length=300, blank=True, null=True)
    receveur                 =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="receveur_bon_reception", null = True, blank = True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_bon_reception", null = True, blank = True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    is_actif                 =    models.BooleanField(default = True)
    duree                    =   models.IntegerField(choices = TypeDuree, default=1,null = True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.numero_reception

    @property
    def prix_total(self):
        total = 0
        lignes = Model_Ligne_reception.objects.filter(bon_reception_id = self.id)
        for i in lignes :
            if i.prix_unitaire != None and i.prix_unitaire != 0 :
                quantite = i.quantite_demande
                if self.est_realisee == True :
                    quantite = i.quantite_fournie
                total = total + (i.prix_unitaire * quantite)
            elif i.prix_lot != None and i.prix_lot != 0 :
                total = total + i.prix_lot
        return "%.2f" % total
    @property
    def separateur_prix_total(self):
        return AfficheEntier(float(self.prix_total))

    @property
    def nbre_lignes(self):
        nb_lignes = 0
        nbres = Model_Ligne_reception.objects.filter(bon_reception_id = self.id).count()
        if nbres:
            nb_lignes = nbres
        return "%.2f" % nb_lignes

    @property
    def quantite_total(self):
        total = 0
        items = Model_Ligne_reception.objects.filter(bon_reception_id = self.id)
        for item in items :
            if item.quantite_demande != None and item.quantite_demande != 0 :
                quantite = item.quantite_demande
                if self.est_realisee == True :
                    quantite = item.quantite_fournie
                total = total + quantite
        return "%.2f" % total

    @property
    def statut_achat(self):
        art_demandes = 0.0
        art_fournie = 0.0

        art_demandes = Model_Ligne_reception.objects.filter(bon_reception_id = self.id).aggregate(demandes=Sum('quantite_demande'))
        art_fournie =  Model_Ligne_reception.objects.filter(bon_reception_id = self.id).aggregate(fournies=Sum('quantite_fournie'))

        #Les deux valeures doivent etre differentes de none pour que le calcul s effectue
        #print("BAAAAAAAAAAAAAAAAAAAAAAAA")
        #print(art_demandes["demandes"] != None)
        #print(art_fournie["fournies"] != None)

        if art_demandes["demandes"] != None and art_fournie["fournies"] != None :
            if float(art_fournie["fournies"]) == float(0.0) :

                if self.etat == 1:
                    return "Créé, en attente de validation"
                else:
                    return "Envoyé au fournisseur"
            elif float(art_demandes["demandes"]) > float(art_fournie["fournies"]):
                return "Reçu Partiellement"
            else : return "Reçu Totalement"

    @property
    def est_modifiable(self):
        items = Model_Ligne_reception.objects.filter(bon_reception_id = self.id)
        for item in items :
            if item.quantite_fournie != 0 :
                return False
        return True

    @property
    def etat_facturation(self):
        #if self.est_realisee == False : return "Rien à facturer"

        nombre_factures = Model_Facture.objects.filter(bon_reception_id = self.id).count()
        if nombre_factures == 0 :
            return "En attente de facture"
        elif nombre_factures == 1 :
            total_paie = 0.00
            factures = Model_Facture.objects.filter(bon_reception_id = self.id)
            for facture in factures :
                total_paie = total_paie + facture.montant
            prix_total = float(self.prix_total)

            if total_paie >= prix_total :
                return "Facture reçue soldée"
            else:
                return "Facture reçue non soldée"


    @property
    def status_paiement(self):

        total_paie = 0.00
        factures = Model_Facture.objects.filter(bon_reception_id = self.id)
        for facture in factures :
            total_paie = total_paie + facture.montant
        prix_total = float(self.prix_total)

        if total_paie >= prix_total :
            return "Bon Soldé"
        else:
            return "Bon non Soldé"

    @property
    def est_facturable(self):
        if self.est_modifiable == True : return False

        total_facture = 0.00
        factures = Model_Facture.objects.filter(bon_reception_id = self.id)
        for facture in factures :
            total_facture = total_facture + facture.montant
        prix_total = float(self.prix_total)
        if total_facture >= prix_total : return False
        else: return True

    @property
    def montant_rapproche(self):
        """Calcul du montant rapproché du BC par rapport aux transaction
        budgétaires. Un montant rapproché est un montant contenu dans une
        transaction de type 'réels' et ayant le BC recherché comme FK"""
        montant = .0
        try:
            transactions = Model_Transactionbudgetaire.objects.filter(
                bon_reception = self, typetransactionbudgetaire = 1, status = 2)
            for transaction in transactions:
                montant += transaction.montant

            # print('**Price Montant Rapproche', montant)
            return montant
        except Exception as e:
            # print(e)
            return 0

    @property
    def montant_non_rapproche(self):
        """Montant Non rapproché d'un bon de commande"""
        return float(self.prix_total)  - float(self.montant_rapproche)

    @property
    def statusRapprochement(self):
        if self.prix_total == self.montant_rapproche: return 1 #Rapproché
        elif float(self.montant_rapproche) < float(self.prix_total): return 2 #Partiellement rapproché
        return 0 #Non rapproché





class Model_Ligne_reception(models.Model):
    bon_reception            =    models.ForeignKey(Model_Bon_reception, on_delete = models.CASCADE, related_name="ligne_of_reception")
    quantite_demande         =    models.IntegerField()
    quantite_fournie         =    models.IntegerField(default=0)
    ligne_budgetaire         =    models.ForeignKey("Model_LigneBudgetaire", on_delete = models.SET_NULL, related_name = 'ligne_budget_of_ligne', null = True, blank = True)
    stock_article            =    models.ForeignKey("Model_StockArticle", null = True, blank = True, on_delete=models.SET_NULL, related_name="ligne_of_reception")
    prix_unitaire            =    models.FloatField()
    description              =    models.CharField(max_length = 100, blank=True, null=True)
    prix_lot                 =    models.FloatField(null = True, blank = True, default=0)
    unite_achat              =    models.ForeignKey(Model_UniteAchatArticle, null = True, blank = True, on_delete=models.SET_NULL)
    article                  =    models.ForeignKey(Model_Article, on_delete = models.SET_NULL, related_name="article_of_ligne_reception", null = True, blank = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)
    auteur                   =    models.ForeignKey(Model_Personne, related_name="auteur_ligne_reception", null = True, blank = True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.bon_reception.numero_reception

    def montant_total(self):
        return self.prix_unitaire * self.quantite_demande

    @property
    def unite_article(self):
        try:
            stock = Model_StockArticle.objects.get(pk = self.stock_article_id)
            return stock.article.unite.symbole_unite
        except:
            return ""

    @property
    def separateur_prix_unitaire(self):
        return AfficheEntier(float(self.prix_unitaire))

    @property
    def separateur_montant_total(self):
        return AfficheEntier(float(self.montant_total))

    @property
    def nom_article(self):
        stock = Model_StockArticle.objects.get(pk = self.stock_article_id)
        article = Model_Article.objects.get(pk = stock.article_id)
        return article.designation

    @property
    def separateur_nom_article(self):
        return AfficheEntier(float(self.nom_article))

    @property
    def unite(self):
        unite_achat = Model_UniteAchatArticle.objects.get(pk = self.unite_achat_id)
        unite = Model_Unite.objects.get(pk = unite_achat.unite_id)
        return unite

    @property
    def separateur_unite(self):
        return AfficheEntier(float(self.unite))

    @property
    def total(self):
        order = Model_Bon_reception.objects.get(pk = self.bon_reception_id)
        total = 0
        if self.prix_unitaire != None and self.prix_unitaire != 0 :
            quantite = self.quantite_demande
            if order.est_realisee == True :
                quantite = self.quantite_fournie
            total = (self.prix_unitaire * quantite)
        elif self.prix_lot != None and self.prix_lot != 0 :
            total = self.prix_lot
        return "%.2f" % total

    @property
    def separateur_total(self):
        return AfficheEntier(float(self.total))

    @property
    def emplacement(self):
        stock = Model_StockArticle.objects.get(pk = self.stock_article_id)
        emplacement = Model_Emplacement.objects.get(pk = stock.emplacement_id)
        return emplacement.designation

    @property
    def separateur_emplacement(self):
        return AfficheEntier(float(self.emplacement))



class Model_Image(models.Model):
    doc                      =    models.CharField(max_length = 100)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    auteur                   =    models.ForeignKey(Model_Personne, related_name="auteur_images", null = True, blank = True, on_delete=models.SET_NULL)


# MODULE COMPTABILITE
class Model_Annee_fiscale(models.Model):
    designation              =    models.CharField(max_length = 100, null = True, blank=True, default = '')
    observation              =    models.CharField(max_length = 250, null = True, blank=True, default = '')
    date_debut               =    models.DateTimeField()
    date_fin                 =    models.DateTimeField()
    est_active               =    models.BooleanField(default = False)
    created_at               =    models.DateTimeField(auto_now_add = True)
    update_at                =    models.DateTimeField(auto_now = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    seuil_immobilisation     =    models.FloatField(default = 0)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_annee_fiscale_zty', null = True, blank = True)

    def __str__(self):
        return self.designation


class Model_TypeCompte(models.Model):
    designation                     =    models.CharField(max_length = 100)
    type                            =    models.IntegerField(choices=TypeOfTypeCompte)
    description                     =    models.CharField(max_length = 500, null = True, blank = True, default="")
    est_inclu_dans_balance_initiale =    models.BooleanField(default = False)
    statut                          =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                            =    models.CharField(max_length=50, blank=True, null=True)
    update_date                     =    models.DateTimeField(auto_now=True)
    creation_date                   =    models.DateTimeField(auto_now_add=True)
    auteur                          =    models.ForeignKey(Model_Personne, default=None, null=True, blank=True, on_delete=models.SET_NULL)
    url                             =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation

class Model_Compte(models.Model):
    numero                   =    models.CharField(max_length = 64)
    designation              =    models.CharField(max_length = 500, null = True, blank = True, default="")
    permet_reconciliation    =    models.BooleanField(default=False)
    description              =    models.CharField(max_length = 500, null = True, blank = True, default="")
    balance                  =    models.FloatField(default=0.0)
    type_compte              =    models.ForeignKey(Model_TypeCompte, on_delete=models.CASCADE, related_name="comptes_associes")
    devise                   =    models.ForeignKey(Model_Devise, on_delete=models.SET_NULL, related_name="comptes_associes", null=True, blank=True, default=None)
    creation_date            =    models.DateTimeField(auto_now_add =True)
    est_obsolete             =    models.BooleanField(default = False)
    origine                  =    models.IntegerField(choices=OrigineCompte, default=1)
    vente_par_defaut         =    models.BooleanField(default = False)
    achat_par_defaut         =    models.BooleanField(default = False)
    fournisseur_par_defaut   =    models.BooleanField(default = False)
    client_par_defaut        =    models.BooleanField(default = False)
    taxe_par_defaut          =    models.BooleanField(default = False)
    caisse_par_defaut        =    models.BooleanField(default = False)
    banque_par_defaut        =    models.BooleanField(default = False)
    marchandise_par_defaut   =    models.BooleanField(default = False)
    personnel_par_defaut     =    models.BooleanField(default = False)
    salaire_par_defaut       =    models.BooleanField(default = False)
    liaison_par_defaut       =    models.BooleanField(default = False)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    auteur                   =    models.ForeignKey(Model_Personne, default=None, null=True, blank=True, on_delete=models.SET_NULL)
    url                      =     models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return "%s %s" % (self.numero, self.designation)

    @property
    def valeur_debit(self):
        montant = 0
        try:
            annee_encours = Model_Annee_fiscale.objects.filter(est_active = True).first()
            ecritures = Model_EcritureComptable.objects.filter(compte_id = self.id, annee_fiscale_id = annee_encours.id).aggregate(debit=Sum('montant_debit'))
            montant = float(ecritures["debit"])
            return montant
        except Exception as e:
            #print('Erreur valeur_debit(): {}'.format(e))
            return "%.2f" % montant

    @property
    def valeur_credit(self):
        montant = 0
        try:
            annee_encours = Model_Annee_fiscale.objects.filter(est_active = True).first()
            ecritures = Model_EcritureComptable.objects.filter(compte_id = self.id, annee_fiscale_id = annee_encours.id).aggregate(credit=Sum('montant_credit'))
            montant = float(ecritures["credit"])
            return montant
        except Exception as e:
            #print('Erreur valeur_credit(): {}'.format(e))
            return "%.2f" % montant


class Model_CaptureCompte(models.Model):
    compte                            =    models.ForeignKey(Model_Compte, on_delete=models.CASCADE, related_name="captures")
    montant_ouverture                =    models.FloatField(default=0)
    montant_solde                    =    models.FloatField(default=0)
    date_ouverture                    =    models.DateField(blank=True, null=True)
    date_fermeture                    =    models.DateField(blank=True, null=True)
    index                            =    models.IntegerField(default=0)
    est_credit                        =    models.BooleanField()
    date_capture                    =    models.DateField()
    url                    =     models.CharField(max_length = 250, blank=True, null=True)
    auteur                    =    models.ForeignKey(Model_Personne, related_name="auteur_capture_compte", null = True, blank = True, on_delete=models.SET_NULL)

class Model_Taxe(models.Model):
    designation              =    models.CharField(max_length = 100)
    categorie_taxe           =    models.CharField(max_length = 500, null = True, blank = True, default="")
    portee_taxe              =    models.IntegerField(choices=PorteeTaxe, default = 3)
    est_par_defaut           =    models.BooleanField(default=False)
    type_montant_taxe        =    models.IntegerField(choices=TypeMontant,default=1)
    montant                  =    models.FloatField(default=0)
    devise                   =    models.ForeignKey(Model_Devise, on_delete = models.SET_NULL, related_name="devise_of_taxe", null = True, blank = True)
    compte_taxe              =    models.ForeignKey(Model_Compte, default=None, null=True, blank=True, on_delete=models.SET_NULL)
    est_active               =    models.BooleanField(default=True)
    description              =    models.CharField(max_length = 500, null = True, blank = True, default="")
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    date_creation            =    models.DateTimeField(auto_now_add=True)
    auteur                   =    models.ForeignKey(Model_Personne, default=None, null=True, blank=True, on_delete=models.SET_NULL)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation

    def value_portee_taxe(self):
        return dict(PorteeTaxe)[int(self.portee_taxe)]

    def value_type_montant_taxe(self):
        return dict(TypeMontant)[int(self.type_montant_taxe)]

class Model_TaxeOrderItem(models.Model):
    taxe                            =    models.ForeignKey(Model_Taxe, on_delete=models.CASCADE)
    #oder_item                        =    models.ForeignKey(Model_ItemOrder, on_delete=models.CASCADE)

class Model_Journal(models.Model):
    designation                     =     models.CharField(max_length = 100, null = True, blank=True, default = '')
    code                            =     models.CharField(max_length = 15, null = True, blank=True, default = '')
    type_journal                    =     models.IntegerField(choices=TypeJournal, default = 1)
    est_affiche                     =     models.BooleanField(default = False)
    creation_date                   =     models.DateTimeField(auto_now_add = True)
    est_journal_par_defaut          =     models.BooleanField(default = False)
    sequence                        =     models.IntegerField(default = 100)
    compte_debit                    =     models.ForeignKey(Model_Compte, on_delete = models.SET_NULL, related_name="compte_debitE_by_journal", null = True, blank = True)
    compte_credit                   =     models.ForeignKey(Model_Compte, on_delete = models.SET_NULL, related_name="compte_creditE_by_journal", null = True, blank = True)
    devise                          =     models.ForeignKey(Model_Devise, on_delete = models.SET_NULL, related_name="devise_of_journal", null = True, blank = True)
    statut                          =     models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                            =     models.CharField(max_length=50, blank=True, null=True)
    update_date                     =     models.DateTimeField(auto_now=True)
    auteur                          =     models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_of_journal", null = True, blank = True)
    url                             =     models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation

    @property
    def nom_type_journal(self):
        for key, value in TypeJournal:
            if key == self.type_journal: return value
        return ""

    @property
    def value_type_journal(self):
        return dict(TypeJournal)[int(self.type_journal)]

    @property
    def valeur_debit(self):
        montant = 0
        try:
            annee_encours = Model_Annee_fiscale.objects.filter(est_active = True).first()
            ecritures = Model_EcritureComptable.objects.filter(piece_comptable__journal_comptable_id = self.id, annee_fiscale_id = annee_encours.id ).aggregate(debit=Sum('montant_debit'))
            return "%.2f" % ecritures["debit"]
        except Exception as e:
            #print('Erreur valeur_debit(): {}'.format(e))
            return "%.2f" % montant

    @property
    def valeur_credit(self):
        montant = 0
        try:
            annee_encours = Model_Annee_fiscale.objects.filter(est_active = True).first()
            ecritures = Model_EcritureComptable.objects.filter(piece_comptable__journal_comptable_id = self.id, annee_fiscale_id = annee_encours.id ).aggregate(credit=Sum('montant_credit'))
            return "%.2f" % ecritures["credit"]
        except Exception as e:
            #print('Erreur valeur_credit(): {}'.format(e))
            return "%.2f" % montant

    @property
    def kanban_dashboard_datas(self):
        return json.dumps(self.get_journal_dashboard_datas())

    @property
    def kanban_dashboard_graph_datas(self):
        #Pour les journaux factures Achats et Ventes
        if self.type_journal in [1, 2]:
            data = []
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            data.append({"label": 'Echue', "value":0.0, "time": 'past',"color": '#3e95cd'})
            day_of_week = int(today.strftime('%w'))
            first_day_of_week = today + timedelta(days=-day_of_week+1)
            for i in range(-1,4):
                if i==0: label = 'Cette semaine'
                elif i==3: label = 'Non echue'
                else:
                    start_week = first_day_of_week + timedelta(days=i*7)
                    end_week = start_week + timedelta(days=6)
                    if start_week.month == end_week.month:
                        label = str(start_week.day) + '-' + str(end_week.day) + ' ' + end_week.strftime('%b')
                    else:
                        label = start_week.strftime('%d %b') + '-' + end_week.strftime('%d %b')
                data.append({"label":label,"value":0.0, "time": 'past' if i<0 else 'future', "color": '#8e5ea2'})

            # On cherche le montant Hors taxe cumulé par semaine
            #On recupère le premier jour de la semaine passée (pcq la prémière itération sera de la plus vielle facture jusqu'à ce jour là)
            start_date = (first_day_of_week + timedelta(days=-7))
            for i in range(0,6):
                try:
                    if i == 0:
                        factures = Model_Facture.objects.filter(journal_comptable_id = self.id, est_soldee = False, date_echeance__lt = start_date).aggregate(ht=Sum('montant_ht'))#<
                        montant = float(factures["ht"])
                    elif i == 5:
                        factures = Model_Facture.objects.filter(journal_comptable_id = self.id, est_soldee = False, date_echeance__gte = start_date).aggregate(ht=Sum('montant_ht'))#>=
                        montant = float(factures["ht"])
                    else:
                        next_date = start_date + timedelta(days=7)
                        factures = Model_Facture.objects.filter(journal_comptable_id = self.id, est_soldee = False, date_echeance__range = [start_date, next_date]).aggregate(ht=Sum('montant_ht'))
                        montant = float(factures["ht"])
                        start_date = next_date
                    data[i]['value'] = montant
                except Exception as e:
                    #print('Erreur get montant HT: {}'.format(e))
                    data[i]['value'] = 0.0

            [graph_title, graph_key] = ['', "Montant Hors taxe"]
            #print("data: {}".format(data))
            typ = 'bar'
            bar_graph_datas = [{"values": data, "title": graph_title, "key": graph_key, "type": typ}]
            return json.dumps(bar_graph_datas)
        #Pour les journaux de trésorerie
        elif self.type_journal in [3, 4]:

            def build_graph_data(date, montant):
                name = date.strftime("%d %B %Y")
                short_name = date.strftime('%d %b')
                color = '#875A7B'
                return {"label":short_name,"value": montant, "name": name, "color": color}

            data = []
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            last_month = today + timedelta(days=-30)

            #Le dernier point du graphique est le dernier rélévé
            last_operation = Model_OperationTresorerie.objects.filter(journal_id = self.id, date_operation__lte = datetime.now()).order_by("-date_operation").first()

            last_balance = last_operation and last_operation.solde or 0
            data.append(build_graph_data(today, last_balance))

            #then we subtract the total amount of bank statement lines per day to get the previous points
            #(graph is drawn backward)
            date = today
            montant = float(last_balance)
            dates = Model_Ligne_OperationTresorerie.objects.filter(operation_tresorerie__journal_id = self.id, date_ligne_operation__gt = last_month, date_ligne_operation__lte = today ).dates('date_ligne_operation', 'day').order_by("-date_ligne_operation")

            for dt in dates:
                #print("dt: {}, today: {}".format(dt, today))
                date = dt
                amount = 0
                if dt.strftime("%Y-%m-%d") != today.strftime("%Y-%m-%d"):  # make sure the last point in the graph is today
                    operations = Model_Ligne_OperationTresorerie.objects.filter(operation_tresorerie__journal_id = self.id, date_ligne_operation = dt).aggregate(amount=Sum('montant'))
                    amount = float(operations["amount"])
                    data[:0] = [build_graph_data(date, amount)]
                montant -= amount

            # make sure the graph starts 1 month ago
            if date.strftime("%Y-%m-%d") != last_month.strftime("%Y-%m-%d"):
                data[:0] = [build_graph_data(last_month, montant)]

            if self.type_journal == 4:
                [graph_title, graph_key] = ['', 'Caisse: Solde']
            elif self.type_journal == 3:
                [graph_title, graph_key] = ['', 'Banque: Solde']
            #print("data: {}".format(data))
            color = '#875A7B'
            typ = 'line'
            line_graph_datas = [{"values": data, "title": graph_title, "key": graph_key, "area": True, "type": typ, "color": color}]
            return json.dumps(line_graph_datas)
        #Pour les autres journaux pas de graphique
        else:
            return None


class Model_PieceComptable(models.Model):
    designation                     =    models.CharField(max_length = 400, null = True, blank=True, default = '')
    reference                       =    models.CharField(max_length = 400, null = True, blank=True, default = '')
    montant                         =    models.FloatField()
    description                     =    models.CharField(max_length = 500, null = True, blank=True, default = '')
    partenaire                      =    models.ForeignKey(Model_Personne, on_delete=models.SET_NULL, null = True, blank = True)
    journal_comptable               =    models.ForeignKey(Model_Journal, on_delete = models.SET_NULL, related_name="journal_of_piece_comptable", null = True, blank = True)
    facture                         =    models.ForeignKey("Model_Facture", on_delete = models.SET_NULL, related_name="facture_on_piece_comptable", null = True, blank = True)
    devise                          =    models.ForeignKey(Model_Devise, on_delete = models.SET_NULL, related_name="devise_of_piece_comptable", null = True, blank = True)
    bon_commande                    =    models.ForeignKey("Model_Bon_commande", on_delete = models.SET_NULL, related_name="bon_commande_of_piece_commande", null = True, blank = True)
    lot_bulletin                    =    models.ForeignKey("Model_LotBulletins", on_delete = models.SET_NULL, related_name="lot_bulletin_of_piece_comptable", null = True, blank = True )
    bon_reception                   =    models.ForeignKey(Model_Bon_reception, on_delete = models.SET_NULL, related_name="bon_reception_of_piece_commande", null = True, blank = True)
    taux                            =    models.ForeignKey(Model_Taux, on_delete = models.SET_NULL, related_name="taux_of_piece_comptable", null = True, blank = True)
    date_piece                      =    models.DateTimeField(default=None, null=True, blank=True)
    externe_id                      =    models.IntegerField(null=True, blank=True)
    est_a_nouveau                   =    models.BooleanField(default=False)
    statut                          =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                            =    models.CharField(max_length=50, blank=True, null=True)
    update_date                     =    models.DateTimeField(auto_now=True)
    date_creation                   =    models.DateTimeField(auto_now_add=True)
    auteur                          =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_of_piece_comptable", null = True, blank = True)
    url                             =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
            return self.designation

    @property
    def separateur_montant(self):
        return AfficheEntier(float(self.montant))

    @property
    def valeur_piece(self):
        montant = 0
        if self.montant > 0: return "%.2f" % self.montant

        ecritures = Model_EcritureComptable.objects.filter(piece_comptable_id = self.id).order_by("-montant_credit")
        for item in ecritures:
            montant = montant + item.montant_credit

        return  "%.2f" % montant

    @property
    def valeur_debit(self):
        montant = 0
        try:
            ecritures = Model_EcritureComptable.objects.filter(piece_comptable_id = self.id ).aggregate(debit=Sum('montant_debit'))
            return "%.2f" % ecritures["debit"]
        except Exception as e:
            #print('Erreur valeur_debit(): {}'.format(e))
            return "%.2f" % montant

    @property
    def valeur_credit(self):
        montant = 0
        try:
            ecritures = Model_EcritureComptable.objects.filter(piece_comptable_id = self.id ).aggregate(credit=Sum('montant_credit'))
            return "%.2f" % ecritures["credit"]
        except Exception as e:
            #print('Erreur valeur_credit(): {}'.format(e))
            return "%.2f" % montant

    @property
    def separateur_valeur_piece(self):
        return AfficheEntier(float(self.valeur_piece))


class Model_EcritureComptable(models.Model):
    designation                 =    models.CharField(max_length = 400, null = True, blank=True, default = '')
    montant_credit              =    models.FloatField()
    montant_debit               =    models.FloatField()
    date_echeance               =    models.DateTimeField(null=True)
    est_lettre                  =    models.BooleanField(default=False)
    compte                      =    models.ForeignKey(Model_Compte, on_delete = models.SET_NULL, related_name="compte_of_ecriture", null = True, blank = True)
    lettrage                    =    models.ForeignKey("Model_Lettrage", on_delete = models.SET_NULL, related_name="lettrage_ecriture_comptable", null = True, blank = True)
    piece_comptable             =    models.ForeignKey(Model_PieceComptable, on_delete = models.CASCADE, related_name="piece_comptable_of_ecriture", null = True, blank = True)
    annee_fiscale               =    models.ForeignKey("Model_Annee_fiscale", on_delete = models.SET_NULL, related_name="annee_fiscale_ecriture", null = True, blank = True)
    statut                      =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    externe_id                      =    models.IntegerField(null=True, blank=True)
    etat                        =    models.CharField(max_length=50, blank=True, null=True)
    update_date                 =    models.DateTimeField(auto_now=True)
    date_creation               =    models.DateTimeField(auto_now_add = True)
    auteur                      =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_of_ecriture", null = True, blank = True)
    url                         =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation

    @property
    def separateur_montant_credit(self):
        return AfficheEntier(float(self.montant_credit))

    @property
    def separateur_montant_debit(self):
        return AfficheEntier(float(self.montant_debit))

    @property
    def debit(self):
        piece = self.piece_comptable
        if piece.taux == None: return "%.2f" % self.montant_debit
        else:
            montant = self.montant_debit / piece.taux.montant
            return "%.2f" % montant
    @property
    def separateur_debit(self):
        return AfficheEntier(float(self.debit))


    @property
    def credit(self):
        piece = self.piece_comptable
        if piece.taux == None: return "%.2f" % self.montant_credit
        else:
            montant = self.montant_credit / piece.taux.montant
            return "%.2f" % montant
    @property
    def separateur_credit(self):
        return AfficheEntier(float(self.credit))


class Model_Facture(models.Model):
    facture_mere            =    models.ForeignKey('Model_Facture', on_delete = models.CASCADE, related_name="factures_fille", null = True, blank = True)
    fournisseur             =    models.ForeignKey(Model_Fournisseur, on_delete = models.SET_NULL, related_name="factures_fournisseur", null = True, blank = True)
    client                  =    models.ForeignKey("Model_Client", on_delete = models.SET_NULL, related_name="factures_client", null = True, blank = True)
    bon_commande            =    models.ForeignKey("Model_Bon_commande", on_delete = models.SET_NULL, related_name="factures", null = True, blank = True)
    bon_reception           =    models.ForeignKey(Model_Bon_reception, on_delete = models.SET_NULL, related_name="factures", null = True, blank = True)
    devise                  =    models.ForeignKey(Model_Devise, on_delete = models.SET_NULL, related_name="factures", null = True, blank = True)
    periode                 =    models.CharField(max_length = 50, null = True, blank = True, default = "")
    numero_facture          =    models.CharField(max_length = 50, null = True, blank = True, default = "")
    montant                 =    models.FloatField(null = True, blank = True, default = 0)
    montant_en_lettre       =    models.TextField()
    montant_ht              =    models.FloatField(null = True, blank = True, default = 0)
    montant_taxe            =    models.FloatField(null = True, blank = True, default = 0)
    document                =    models.CharField(max_length = 500, null = True, blank = True, default = "")
    type_facture            =    models.ForeignKey("Model_Typefacture", related_name="type_facture", on_delete=models.SET_NULL, null = True, blank = True)
    est_soldee              =    models.BooleanField(default = False)
    condition_reglement     =    models.ForeignKey("Model_ConditionReglement", on_delete=models.SET_NULL, related_name="factures", blank=True, null=True)
    lettrage                =    models.ForeignKey("Model_Lettrage", on_delete = models.SET_NULL, related_name="lettrage_link", null = True, blank = True)
    est_facture_avoir       =    models.BooleanField(default = False)
    est_nullable            =    models.BooleanField(default=True)
    est_facture_avoir       =    models.BooleanField(default = False)
    est_facture_acompte     =    models.BooleanField(default = False)
    type_service            =    models.ForeignKey("Model_Type_service", related_name="factures", on_delete=models.SET_NULL, null = True, blank = True)
    objet_facture           =    models.CharField(max_length = 50, null = True, blank = True, default = "")
    type                    =    models.CharField(max_length = 20)
    type_facture_client     =    models.CharField(max_length = 20, blank=True, null=True)
    etat_facturation        =    models.ForeignKey("Model_Etat_Facturation", on_delete=models.SET_NULL, related_name="factures", blank=True, null=True)
    date_facturation        =    models.DateTimeField(null = True, blank = True)
    date_echeance           =    models.DateTimeField(null = True, blank = True)
    externe_id                      =    models.IntegerField(null=True, blank=True)
    statut                  =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True, related_name="statut_facture")
    etat                    =    models.CharField(max_length=300, blank=True, null=True)
    update_date             =    models.DateTimeField(auto_now=True)
    creation_date           =    models.DateTimeField(auto_now_add=True)
    journal_comptable       =    models.ForeignKey(Model_Journal, on_delete=models.SET_NULL, null = True, blank = True, related_name="factures")
    auteur                  =    models.ForeignKey(Model_Personne, related_name="factures_creees", on_delete=models.SET_NULL, null = True, blank = True)
    url                     =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.numero_facture


    @property
    def valeur_date_echeance(self):
        try:
            condition_reglement = Model_ConditionReglement.objects.get(pk = self.condition_reglement_id)
            date_echeance = self.date_facturation.date() + timedelta(days = condition_reglement.nombre_jours)
            return date_echeance
        except Exception as e:
            return None

    @property
    def etat_facture(self):
        etat = "Facture non soldée"
        if float(self.montant_restant) <= 0 : etat = "Facture soldée"
        return etat

    @property
    def etat_facture_fille(self):
        if self.est_soldee == True:
            return 'Facture solée'
        else:
            return 'Facture non soldée'

    @property
    def est_mere(self):
        if self.facture_mere == None or self.facture_mere == '':
            return True
        else:
            return False


    @property
    def montant_paye(self):
        try:
            montant = 0
            paiements = Model_Paiement.objects.filter(facture_id = self.id, est_valide = True)

            if paiements.count() != 0 :
                for paiement in paiements:
                    if int(paiement.transaction.moyen_paiement) == 1:
                        montant = montant + paiement.montant
                    elif int(paiement.transaction.moyen_paiement) == 2 :
                        transaction = Model_Transaction.objects.get(paiement_id = paiement.id)
                        payloads = json.loads(transaction.payloads.replace("'",'"'))

                        pay_montant = float(payloads["montant"])
                        pay_currency = int(payloads["devise"])
                        montant = montant + pay_montant
            return "%.2f" % montant
        except Exception as e:
            return 0.0

    @property
    def separateur_montant_paye(self):
        return AfficheEntier(float(self.montant_paye))

    @property
    def montant_restant(self):
        montant = self.montant - float(self.montant_paye)
        return "%.2f" % montant

    @property
    def separateur_montant(self):
        return AfficheEntier(float(self.montant))

    @property
    def separateur_montant_restant(self):
        return AfficheEntier(float(self.montant_restant))

class Model_Ligne_facture(models.Model):
    facture                  =    models.ForeignKey(Model_Facture, on_delete = models.CASCADE, related_name="ligne_of_facture")
    quantite_demande         =    models.IntegerField()
    prix_unitaire            =    models.FloatField()
    remise                   =    models.FloatField(default = 0)
    prix_lot                 =    models.FloatField(null = True, blank = True, default=0)
    ligne_montant_taxe       =    models.FloatField(null=True, blank = True, default=0)
    unite_achat              =    models.ForeignKey(Model_UniteAchatArticle, null = True, blank = True, on_delete=models.SET_NULL)
    designation              =    models.CharField(max_length = 300, null = True, blank=True, default = '')
    article                  =    models.ForeignKey(Model_Article, on_delete = models.SET_NULL, related_name="article_of_ligne_facture", null = True, blank = True)
    compte_comptable         =    models.ForeignKey(Model_Compte, on_delete=models.SET_NULL, blank=True, null=True)
    #ligne_bon_commande      =    models.ForeignKey("Model_Ligne_reception",on_delete = models.SET_NULL, related_name="ligne_bon_commande_of_facture", null = True, blank = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)
    auteur                   =    models.ForeignKey(Model_Personne, related_name="auteur_ligne_facture", null = True, blank = True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.facture.numero_facture

    def montant_total(self):
        return self.prix_unitaire * self.quantite_demande

    @property
    def separateur_prix_unitaire(self):
        return AfficheEntier(float(self.prix_unitaire))

    @property
    def separateur_prix_lot(self):
        return AfficheEntier(float(self.prix_lot))

    @property
    def separateur_quantite_demande(self):
        return AfficheEntier(float(self.quantite_demande))



    @property
    def nom_article(self):
        article = Model_Article.objects.get(pk = self.article_id)
        return article.designation

    @property
    def unite(self):
        unite_achat = Model_UniteAchatArticle.objects.get(pk = self.unite_achat_id)
        unite = Model_Unite.objects.get(pk = unite_achat.unite_id)
        return unite

    @property
    def total(self):
        total = 0
        if self.prix_unitaire != None and self.prix_unitaire != 0 :
            quantite = self.quantite_demande
            total = (self.prix_unitaire * quantite)
        elif self.prix_lot != None and self.prix_lot != 0 :
            total = self.prix_lot
        return "%.2f" % total
    @property
    def separateur_total(self):
        return AfficheEntier(float(self.total))

class Model_Transaction(models.Model):
    reference                =     models.CharField(max_length = 300, null = True, blank=True, default = '')
    facture                  =    models.ForeignKey(Model_Facture, on_delete = models.CASCADE, related_name = "transactions", null = True, blank = True)
    statut                   =    models.IntegerField(choices = StatutTransaction)
    creation_date            =    models.DateTimeField(auto_now_add = True)
    moyen_paiement           =    models.CharField(choices = MoyenPaiement, max_length = 20, blank = True, default="")
    auteur                   =    models.ForeignKey(Model_Personne, related_name = "transactions", on_delete=models.SET_NULL, null = True, blank = True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    url                      =     models.CharField(max_length = 250, blank=True, null=True)

class Model_Paiement(models.Model):
    designation                 =    models.CharField(max_length = 300, null = True, blank=True, default = '')
    description                 =    models.CharField(max_length = 300, null = True, blank=True, default = '')
    type_paiement               =    models.IntegerField(choices = TypePaiement, null = True, blank = True, default=1)
    transaction                 =    models.OneToOneField(Model_Transaction, on_delete = models.SET_NULL, related_name = "paiement", null = True, blank = True)
    facture                     =    models.ForeignKey(Model_Facture, on_delete = models.CASCADE, related_name = "paiements", null = True, blank = True)
    journal                     =    models.ForeignKey(Model_Journal, on_delete = models.SET_NULL, null = True, blank = True, related_name = "paiements")
    ligne_operation_tresorerie  =    models.ForeignKey("Model_Ligne_OperationTresorerie", on_delete = models.SET_NULL, null = True, blank = True, related_name = "ligne_operation_link_paiement")
    partenaire                  =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, null = True, blank = True, related_name = "paiements")
    montant                     =    models.FloatField(null = True, blank = True)
    devise                      =    models.ForeignKey(Model_Devise, on_delete=models.SET_NULL, null = True, blank = True)
    taux                        =    models.ForeignKey(Model_Taux, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    est_lettre                  =    models.BooleanField(default = False)
    est_valide                  =    models.BooleanField(default=False)
    type                        =    models.CharField(max_length = 20, blank=True, null=True)
    externe_id                      =    models.IntegerField(null=True, blank=True)
    statut                      =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True, related_name="statut_paiement")
    etat                        =    models.CharField(max_length=300, blank=True, null=True)
    date_paiement               =    models.DateTimeField()
    update_date                 =    models.DateTimeField(auto_now=True)
    date_creation               =    models.DateTimeField(auto_now_add=True)
    auteur                      =    models.ForeignKey(Model_Personne, related_name = "auteur_paiements", on_delete=models.SET_NULL, null = True, blank = True)
    url                         =    models.CharField(max_length = 250, blank=True, null=True)

    @property
    def montant_paye(self):
        transaction = Model_Transaction.objects.get(pk = self.transaction_id)
        devise = Model_Devise.objects.get(pk = self.devise_id)

        if int(transaction.moyen_paiement) == 1 : return "%.2f %s" % (self.montant, devise.symbole_devise)
        elif int(transaction.moyen_paiement) == 2 :
            payloads = Model_Payloads.objects.get(paiement_id = self.id)
            logs = json.loads(payloads.logs.replace("'",'"'))
            return "%.2f %s" % (float(logs["montant"]), logs["devise"])

    @property
    def information(self):
        transaction = Model_Transaction.objects.get(pk = self.transaction_id)
        moyen_paiement = ""
        for key, value in MoyenPaiement:
            #print(key)
            #print(transaction.moyen_paiement)
            if(int(key) == int(transaction.moyen_paiement)):
                #print(value)
                if value == "Cash" :
                    moyen_paiement = "en %s" % value
                else:
                    moyen_paiement = "via un %s" % value
                break
        return "Paiement %s le %s à %s" % (moyen_paiement, self.date_paiement.strftime("%d-%m-%Y"), self.date_paiement.strftime("%I:%M"))

    def __str__(self):
        return self.information


class Model_Payloads(models.Model):
    paiement                 =    models.OneToOneField(Model_Paiement, on_delete = models.CASCADE, related_name = "paiement_transaction")
    logs                     =    models.CharField(max_length = 500, null = True, blank = True, default="")
    url                      =    models.CharField(max_length = 250, blank=True, null=True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    auteur                   =    models.ForeignKey(Model_Personne, related_name="auteur_payload", null = True, blank = True, on_delete=models.SET_NULL)

    def __str__(self):
        return "Transaction du %s" % (Model_Paiement.objects.get(pk = self.paiement_id))

class Model_Immobilisation(models.Model):
    code                     =    models.CharField(max_length=15)
    immobilier               =    models.ForeignKey("Model_Asset", related_name="immobilisations", on_delete=models.CASCADE)
    taux_amortissement       =    models.FloatField()
    valeur_immobilier        =    models.FloatField()
    type_amortissement       =    models.IntegerField(choices=TypeAmortissement, default = 1)
    duree_amortissement      =    models.FloatField(null=True)
    unite_duree              =    models.IntegerField(choices = UniteDuree, default = 2)
    est_prorata_temportis    =    models.BooleanField(default=False)
    prorata_date             =    models.DateTimeField(null=True)
    compte_depreciation      =    models.ForeignKey("Model_Compte", on_delete = models.SET_NULL, related_name="compte_depreciation", null = True, blank = True)
    compte_dotation          =    models.ForeignKey("Model_Compte", on_delete = models.SET_NULL, related_name="compte_depense_dotation", null = True, blank = True)
    compte_immobilier        =    models.ForeignKey("Model_Compte",on_delete = models.SET_NULL, related_name="compte_immobilisation", null = True, blank = True)
    journal                  =    models.ForeignKey("Model_Journal", on_delete = models.SET_NULL, related_name="journal_immobilisation", null = True, blank = True)
    devise                   =    models.ForeignKey(Model_Devise, on_delete = models.SET_NULL, related_name="immobilisations_devise", null = True, blank = True)
    coefficient              =    models.FloatField(default = 0)
    is_available             =    models.BooleanField(default = True)
    est_comptabilise         =    models.BooleanField(default = False)
    local                    =    models.ForeignKey("Model_Local", on_delete = models.SET_NULL, related_name="local_keep_immobilisation", null = True, blank = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True, related_name="statut_immobilisation")
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    date_acquisition         =    models.DateTimeField()
    update_date              =    models.DateTimeField(auto_now=True)
    date_creation            =    models.DateTimeField(auto_now_add=True)
    auteur                   =    models.ForeignKey(Model_Personne, related_name="immobilisations", on_delete=models.SET_NULL, null = True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return "Immobilisation de(du, de l') %s [%s]" % (self.immobilier.article.designation, self.immobilier.numero_identification)

    @property
    def duree_vie(self):
        #return 100 / self.taux_amortissement
        return self.duree_amortissement

    @property
    def valeur_acquisition(self):
        return "%.2f" % self.valeur_immobilier

    @property
    def valeur_taux_amortissement(self):
        return "%.2f" % self.taux_amortissement

    @property
    def value_type_amortissement(self):
        return dict(TypeAmortissement)[int(self.type_amortissement)]

    @property
    def dotation(self):
        return self.valeur_immobilier * self.taux_amortissement / 100

    @property
    def valeur_dotation(self):
        return "%.2f" % self.dotation

    @property
    def cumul_amortissement(self):
        annee_courante = timezone.now().year
        annee_acquisition = self.date_acquisition.year
        return self.dotation * (annee_courante - annee_acquisition)

    @property
    def valeur_cumul_amortissement(self):
        return "%.2f" % self.cumul_amortissement

    @property
    def residuelle(self):
        return self.valeur_immobilier - self.cumul_amortissement

    @property
    def valeur_residuelle(self):
        return "%.2f" % self.residuelle

class Model_Config_Comptabilite(models.Model):
    annee_fiscale       =    models.OneToOneField(Model_Annee_fiscale, on_delete = models.SET_NULL, related_name="config", null = True, blank = True)
    societe_configure   =    models.BooleanField(default = False)
    tresorerie_configure=    models.BooleanField(default = False)
    periode_configure   =    models.BooleanField(default = False)
    est_active          =    models.BooleanField(default = True)
    est_ajour           =    models.BooleanField(default = False)
    digit_compte        =    models.IntegerField(default=6)
    created_at          =    models.DateTimeField(auto_now_add = True)
    update_at           =    models.DateTimeField(auto_now = True)
    auteur              =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_config_comptabilite', null = True, blank = True)

    def __str__(self):
        if self.annee_fiscale != None:
            return "Configuration {}".format(self.annee_fiscale.designation)
        else: return "Configuration de la comptabilité"

# MODULE INVENTAIRE

class Model_OperationStock(models.Model):
    designation              =    models.CharField(max_length=50)
    type                     =    models.CharField(max_length=20, null = True, blank = True)
    reference                =    models.CharField(max_length=10, default = "")
    sequence                 =    models.IntegerField(default=100, null= True, blank=True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    auteur                   =    models.ForeignKey(Model_Personne, related_name="auteur_operation_stock", null = True, blank = True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.designation

class Model_TypeEmplacement(models.Model):
    designation              =    models.CharField(max_length = 50)
    est_systeme              =    models.BooleanField(default = False)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    auteur                   =    models.ForeignKey(Model_Personne, related_name="types_emplacement", null = True, blank = True, on_delete=models.SET_NULL)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)


    def __str__(self):
        return self.designation

class Model_Emplacement(models.Model):
    designation              =    models.CharField(max_length = 100, null = True, blank=True, default = '')
    couloir                  =    models.IntegerField(default=0)
    rayon                    =    models.IntegerField(default=0)
    hauteur                  =    models.IntegerField(default=0)
    creation_date            =    models.DateTimeField(auto_now = True)
    is_racine                =    models.BooleanField(default = False)
    est_systeme              =    models.BooleanField(default = False)
    type_emplacement         =    models.ForeignKey(Model_TypeEmplacement, on_delete = models.SET_NULL, related_name="emplacement_type", null = True, blank = True)
    parent                   =    models.ForeignKey("Model_Emplacement", on_delete = models.SET_NULL, related_name="emplacement_parent", null = True, blank = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_emplacement", null = True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation
#RETOUR STOCK
class Model_Bon_retour(models.Model):
    numero_bon_retour        =    models.CharField(max_length = 100, null = True, blank=True, default = '')
    date_retour              =    models.DateTimeField(auto_now = True)
    date_realisation         =    models.DateTimeField(null = True, blank=True)
    montant_global           =    models.FloatField(default = 0.0)
    creation_date            =    models.DateTimeField(auto_now_add = True)
    est_realisee             =    models.BooleanField(default = False)
    quantite                 =    models.IntegerField(default = 0)
    services_ref             =    models.ForeignKey("Model_Unite_fonctionnelle", blank=True, null=True, on_delete = models.SET_NULL, default=None, related_name="services_referent_bon_retour")
    type                     =    models.CharField(max_length = 100, null = True, blank=True, default = '')
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True, related_name="statut_bon_retour")
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    description              =    models.CharField(max_length = 300, null = True, blank=True, default = '')
    reference_document       =    models.CharField(max_length = 300, null = True, blank=True, default = '')
    status                   =    models.CharField(max_length = 100, null = True, blank=True, default = '')
    employe                  =    models.ForeignKey("Model_Employe",on_delete = models.SET_NULL, related_name="employe_bon_retour", null = True, blank = True)
    agent                    =    models.ForeignKey("Model_Employe",on_delete = models.SET_NULL, related_name="agent_charge_du_bon_retour", null = True, blank = True)
    responsable              =    models.ForeignKey("Model_Employe",on_delete = models.SET_NULL, related_name="demandeur_doing_bon_retour", null = True, blank = True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_bon_retour", null = True, blank = True)
    operation_stock          =    models.ForeignKey(Model_OperationStock, related_name="bon_retour_tranferts", null = True, blank = True, on_delete=models.SET_NULL)
    emplacement_destination  =    models.ForeignKey(Model_Emplacement,on_delete = models.SET_NULL, related_name="emplacement_bon_retour", null = True, blank = True)
    emplacement_origine      =    models.ForeignKey(Model_Emplacement,on_delete= models.SET_NULL, related_name="origin_bon_retour", null = True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.numero_bon_retour


class Model_Ligne_bon_retour(models.Model):
    quantite_demandee        =    models.IntegerField()
    quantite_fournie         =    models.IntegerField()
    creation_date            =    models.DateTimeField(auto_now_add = True)
    numero_serie             =    models.CharField(max_length = 100, null = True, blank=True, default = '')
    description              =    models.CharField(max_length = 100, null = True, blank=True, default = '')
    type                     =    models.CharField(max_length = 100, null = True, blank=True, default = '')
    bon_retour            =    models.ForeignKey("Model_Bon_retour",on_delete = models.SET_NULL, related_name="ligne_of_bon_retour", null = True, blank = True)
    stock_article            =    models.ForeignKey("Model_StockArticle",on_delete = models.SET_NULL, related_name="ligne_bon_retour_take_on_stock_article", null = True, blank = True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="bon_retour_auteur_ligne", null = True, blank = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)


    @property
    def nom_article(self):
        try:
            stock = Model_StockArticle.objects.get(pk = self.stock_article_id)
            article = Model_Article.objects.get(pk = stock.article_id)
            return article.designation
        except:
            return ""
    @property
    def unite_article(self):
        try:
            stock = Model_StockArticle.objects.get(pk = self.stock_article_id)
            return stock.article.unite.symbole_unite
        except:
            return ""

    @property
    def article_identifiant(self):
        try:
            stock = Model_StockArticle.objects.get(pk = self.stock_article_id)
            article = Model_Article.objects.get(pk = stock.article_id)
            return article.id
        except:
            return ""

    @property
    def emplacement(self):
        try:
            stock = Model_StockArticle.objects.get(pk = self.stock_article_id)
            emplacement = Model_Emplacement.objects.get(pk = stock.emplacement_id)
            return emplacement.designation
        except:
            return ""




#BON TRANSFERT
class Model_Bon_transfert(models.Model):
    numero_transfert         =    models.CharField(max_length = 100, null = True, blank=True, default = '')
    date_transfert           =    models.DateTimeField(auto_now = True)
    date_realisation         =    models.DateTimeField(null = True, blank=True)
    montant_global           =    models.FloatField(default = 0.0)
    creation_date            =    models.DateTimeField(auto_now_add = True)
    est_realisee             =    models.BooleanField(default = False)
    quantite                 =    models.IntegerField(default = 0)
    services_ref             =    models.ForeignKey("Model_Unite_fonctionnelle", blank=True, null=True, on_delete = models.SET_NULL, default=None, related_name="services_referent_of_bt")
    type                     =    models.CharField(max_length = 100, null = True, blank=True, default = '')
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True, related_name="statut_bon_transfert")
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    description              =    models.CharField(max_length = 300, null = True, blank=True, default = '')
    reference_document       =    models.CharField(max_length = 300, null = True, blank=True, default = '')
    status                   =    models.CharField(max_length = 100, null = True, blank=True, default = '')
    employe                  =    models.ForeignKey("Model_Employe",on_delete = models.SET_NULL, related_name="employe_doing_transfert", null = True, blank = True)
    agent                    =    models.ForeignKey("Model_Employe",on_delete = models.SET_NULL, related_name="agent_charge_du_transfert", null = True, blank = True)
    responsable              =    models.ForeignKey("Model_Employe",on_delete = models.SET_NULL, related_name="demandeur_doing_transfert", null = True, blank = True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_transfert", null = True, blank = True)
    operation_stock          =    models.ForeignKey(Model_OperationStock, related_name="tranferts", null = True, blank = True, on_delete=models.SET_NULL)
    emplacement_destination  =    models.ForeignKey(Model_Emplacement,on_delete = models.SET_NULL, related_name="tranferts", null = True, blank = True)
    emplacement_origine      =    models.ForeignKey(Model_Emplacement,on_delete= models.SET_NULL, related_name="origin_transfert", null = True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)
    demande_achat            =    models.ForeignKey("Model_Demande_achat",on_delete = models.SET_NULL, related_name="demande_of_bon_transfert", null = True, blank = True)
    expression               =    models.ForeignKey(Model_Expression, on_delete = models.SET_NULL, related_name = "expression_of_bon_transfert", null = True, blank = True)
    update_date              =    models.DateTimeField(auto_now=True)
    is_return_materiel       =    models.BooleanField(default = False)
    creation_date            =    models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.numero_transfert

    '''@property
    def emplacement_origine_transfert(self):
        lignes = Model_Ligne_transfert.objects.filter(bon_transfert_id = self.id)
        item = lignes[0]
        stock = Model_StockArticle.objects.get(pk = item.stock_article_id)
        emplacement_origine = Model_Emplacement.objects.get(pk = stock.emplacement_id)
        return emplacement_origine'''

'''@receiver(post_save, sender=Model_Bon_transfert)
def bon_transfert_soumis(sender,instance,created, **kwargs):
if created:
        texte = "Votre demande de transfert a été enregistré au numéro {0} en date du {1} avec comme Réf. Document {2}".format(instance.numero_transfert, instance.date_transfert, instance.reference_document)
        Model_Notification.objects.create(user_id=instance.demandeur_id,est_lu=False,text=texte,created_at=timezone.now())'''


class Model_Ligne_transfert(models.Model):
    quantite_demandee        =    models.IntegerField()
    quantite_fournie         =    models.IntegerField()
    creation_date            =    models.DateTimeField(auto_now_add = True)
    numero_serie             =    models.CharField(max_length = 100, null = True, blank=True, default = '')
    description              =    models.CharField(max_length = 100, null = True, blank=True, default = '')
    type                     =    models.CharField(max_length = 100, null = True, blank=True, default = '')
    bon_transfert            =    models.ForeignKey("Model_Bon_transfert",on_delete = models.SET_NULL, related_name="ligne_of_bon_commande", null = True, blank = True)
    stock_article            =    models.ForeignKey("Model_StockArticle",on_delete = models.SET_NULL, related_name="ligne_transfere_take_on_stock_article", null = True, blank = True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_ligne_transfert", null = True, blank = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)


    @property
    def nom_article(self):
        try:
            stock = Model_StockArticle.objects.get(pk = self.stock_article_id)
            article = Model_Article.objects.get(pk = stock.article_id)
            return article.designation
        except:
            return ""
    @property
    def unite_article(self):
        try:
            stock = Model_StockArticle.objects.get(pk = self.stock_article_id)
            return stock.article.unite.symbole_unite
        except:
            return ""

    @property
    def article_identifiant(self):
        try:
            stock = Model_StockArticle.objects.get(pk = self.stock_article_id)
            article = Model_Article.objects.get(pk = stock.article_id)
            return article.id
        except:
            return ""

    @property
    def emplacement(self):
        try:
            stock = Model_StockArticle.objects.get(pk = self.stock_article_id)
            emplacement = Model_Emplacement.objects.get(pk = stock.emplacement_id)
            return emplacement.designation
        except:
            return ""

class Model_Bon_inventaire(models.Model):
    numero_inventaire        =    models.CharField(max_length = 100, null = True, blank=True, default = '')
    date_inventaire          =    models.DateTimeField(auto_now = True)
    montant_global           =    models.FloatField(null = True, blank=True)
    creation_date            =    models.DateTimeField(auto_now_add = True)
    est_realisee             =    models.BooleanField(default = False)
    quantite                 =    models.IntegerField(null = True, blank=True)
    description              =    models.CharField(max_length = 300, null = True, blank=True, default = '')
    status                   =    models.CharField(max_length = 100, null = True, blank=True, default = '')
    employe                  =    models.ForeignKey("Model_Employe",on_delete = models.SET_NULL, related_name="employe_doing_inventaire", null = True, blank = True)
    emplacement              =    models.ForeignKey(Model_Emplacement,on_delete = models.SET_NULL, related_name="emplacement_inventaire", null = True, blank = True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_inventaire", null = True, blank = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)


    def __str__(self):
        return self.numero_inventaire

class Model_Ligne_inventaire(models.Model):
    quantite_demandee        =    models.IntegerField()
    quantite_fournie         =    models.IntegerField()
    creation_date            =    models.DateTimeField(auto_now_add = True)
    type                     =    models.CharField(max_length = 100, null = True, blank=True, default = '')
    bon_inventaire           =    models.ForeignKey("Model_Bon_Inventaire",on_delete = models.SET_NULL, related_name="ligne_of_bon_inventaire", null = True, blank = True)
    stock_article            =    models.ForeignKey("Model_StockArticle",on_delete = models.SET_NULL, related_name="ligne_inventaire_take_on_stock_article", null = True, blank = True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_ligne_inventaire", null = True, blank = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.quantite_demandee

    @property
    def nom_article(self):
        stock = Model_StockArticle.objects.get(pk = self.stock_article_id)
        article = Model_Article.objects.get(pk = stock.article_id)
        return article.designation

    @property
    def emplacement(self):
        stock = Model_StockArticle.objects.get(pk = self.stock_article_id)
        emplacement = Model_Emplacement.objects.get(pk = stock.emplacement_id)
        return emplacement.designation

class Model_Mouvement_stock(models.Model):
    reference                =    models.CharField(max_length = 100, null = True, blank=True, default = '')
    quantite_mouvement       =    models.IntegerField()
    details                  =    models.CharField(max_length = 250, null = True, blank=True, default = '')
    creation_date            =    models.DateTimeField(auto_now_add = True)
    type                     =    models.CharField(max_length = 100, null = True, blank=True, default = '')
    stock_article_entrant    =    models.ForeignKey("Model_StockArticle",on_delete = models.SET_NULL, related_name="mouvement_stock_article_entrant", null = True, blank = True)
    stock_article_sortant    =    models.ForeignKey("Model_StockArticle",on_delete = models.SET_NULL, related_name="mouvement_stock_article_sortant", null = True, blank = True)
    bon_commande             =    models.ForeignKey("Model_Bon_commande",on_delete = models.SET_NULL, related_name="bon_commande_of_mouvement_stock", null = True, blank = True)
    bon_reception            =    models.ForeignKey(Model_Bon_reception,on_delete = models.SET_NULL, related_name="bon_commande_of_mouvement_stock", null = True, blank = True)
    bon_inventaire           =    models.ForeignKey(Model_Bon_inventaire,on_delete = models.SET_NULL, related_name="bon_commande_of_mouvement_stock", null = True, blank = True)
    bon_transfert            =    models.ForeignKey(Model_Bon_transfert,on_delete = models.SET_NULL, related_name="bon_commande_of_mouvement_stock", null = True, blank = True)
    bon_retour               =    models.ForeignKey("Model_Bon_retour",on_delete = models.SET_NULL, related_name="bon_commande_of_mouvement_stock", null = True, blank = True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_mouvement_stock", null = True, blank = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return "Mouvement stock de {} {} après {}".format(self.quantite_mouvement, self.article, self.type)

    @property
    def article(self):
        if self.stock_article_entrant_id != None and self.stock_article_entrant_id != 0:
            return self.stock_article_entrant.article
        else: return self.stock_article_sortant.article

class Model_Local(models.Model):
    designation =    models.CharField(max_length = 100, null = True, blank=True, default = '')
    description =    models.CharField(max_length = 250, null = True, blank=True, default = '')
    type_local  =    models.IntegerField(choices = TypeLocal, default = 1)
    parent      =    models.ForeignKey("Model_Local",on_delete= models.SET_NULL, related_name="locals_parent", null=True, blank = True)
    lieu        =    models.ForeignKey(Model_Place,on_delete= models.SET_NULL, related_name="locals", null=True, blank = True)
    created_at  =    models.DateTimeField(auto_now_add= True)
    update_at   =    models.DateTimeField(auto_now = True)
    statut      =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat        =    models.CharField(max_length=50, blank=True, null=True)
    auteur      =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_local_kxv', null = True, blank = True)

    def __str__(self):
        return self.designation

    def value_type_local(self):
        return dict(TypeLocal)[int(self.type_local)]

    @property
    def local_filles(self):
        return Model_Local.objects.filter(parent_id = self.id)


class Model_Asset(models.Model):
    numero_identification = models.CharField(max_length = 100, null = True, blank=True, default = '')
    type = models.CharField(max_length = 100, null = True, blank=True, default = '')
    local = models.ForeignKey(Model_Local,on_delete= models.SET_NULL, related_name="local_of_asset", null=True, blank = True)
    article = models.ForeignKey(Model_Article, on_delete = models.SET_NULL, related_name = 'article_fk_jrw', null = True, blank = True)
    description = models.CharField(max_length = 250, null = True, blank=True, default = '')
    employe = models.ForeignKey("Model_Employe", on_delete = models.SET_NULL, related_name = 'employe_fk_fag', null = True, blank = True)
    bon_entree = models.ForeignKey("Model_Bon", on_delete = models.SET_NULL, related_name = 'bon_of_asset', null = True, blank = True)
    bon_reception = models.ForeignKey("Model_Bon_reception", on_delete = models.SET_NULL, related_name = 'bon_reception_of_asset', null = True, blank = True)
    emplacement                =    models.ForeignKey(Model_Emplacement, null = True, blank = True, on_delete=models.SET_NULL, default = None,related_name = 'emplacement_asset')
    created_at = models.DateTimeField(auto_now_add = True)
    est_immobilise = models.BooleanField(default = False)
    update_at = models.DateTimeField(auto_now = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_asset_aid', null = True, blank = True)
    url                    =     models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.numero_identification



class Model_AssetHistorique(models.Model):
    reference                =    models.CharField(max_length = 100, null = True, blank=True, default = '')
    document                 =    models.CharField(max_length = 500, null = True, blank=True, default = '')
    est_initial              =    models.BooleanField(default = False)
    est_encours              =    models.BooleanField(default = False)
    asset                    =    models.ForeignKey(Model_Asset, on_delete = models.CASCADE, related_name = 'asset_historiques')
    employe                  =    models.ForeignKey("Model_Employe", on_delete = models.SET_NULL, related_name = 'employe_asset_historiques', null = True, blank = True)
    content_type             =    models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    bon_id                   =    models.PositiveIntegerField(blank=True, null=True)
    content_object           =    GenericForeignKey('content_type', 'bon_id')
    created_at               =    models.DateTimeField(auto_now_add = True)
    update_at                =    models.DateTimeField(auto_now = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_asset_historiques', null = True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.reference

# MODULE RH
class Model_TypeOrganisation(models.Model):
    designation              =    models.CharField(max_length = 50)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="types_organisations", null = True, blank = True)

    def __str__(self):
        return self.designation

class Model_Organisation(models.Model):
    nom                      =    models.CharField(max_length = 150)
    slogan                   =    models.CharField(max_length = 150, null = True, blank = True, default="")
    email                    =    models.CharField(max_length = 150, null = True, blank = True, default="")
    image                    =    models.CharField(max_length = 500, null = True, blank = True, default="")
    icon                     =    models.CharField(max_length = 500, null = True, blank = True, default="")
    image_cover              =    models.CharField(max_length = 500, null = True, blank = True, default="")
    phone                    =    models.CharField(max_length = 50, null = True, blank = True, default="")
    boite_postal             =    models.CharField(max_length = 50, null = True, blank = True, default="")
    fax                      =    models.CharField(max_length = 50, null = True, blank = True, default="")
    numero_fiscal            =    models.CharField(max_length = 50, null = True, blank = True, default="")
    site_web                 =    models.CharField(max_length = 100, null = True, blank = True, default="")
    type_organisation        =    models.ForeignKey(Model_TypeOrganisation, on_delete = models.SET_NULL, related_name = "organisations", null = True, blank = True)
    commune_quartier         =    models.ForeignKey(Model_Place, on_delete = models.SET_NULL, related_name = "organisations", null = True, blank = True)
    adresse                  =    models.CharField(max_length = 100, null = True, blank = True, default="")
    devise                   =    models.ForeignKey(Model_Devise, on_delete = models.SET_NULL, related_name="organisations", null = True, blank = True)
    nom_application          =    models.CharField(max_length = 50, null = True, blank = True, default="")
    est_active               =    models.BooleanField(default = False)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="organisations", null = True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.nom

class Model_Employe(Model_Personne):
    profilrh                 =    models.ForeignKey("Model_ProfilRH", on_delete = models.SET_NULL, related_name="profil_creees", null = True, blank = True)
    unite_fonctionnelle      =    models.ForeignKey("Model_Unite_fonctionnelle", blank=True, null=True, on_delete = models.SET_NULL, default=None, related_name="employes")
    lieu_travail             =    models.ForeignKey("Model_LieuTravail", on_delete = models.SET_NULL, blank = True, null = True )
    categorie_employe        =    models.ForeignKey("Model_Categorie_employe", blank=True, null=True, on_delete = models.SET_NULL, default=None, related_name="categorie_empl")
    poste                    =    models.ForeignKey("Model_Poste", on_delete = models.SET_NULL, related_name="poste_employe", null = True, blank = True)
    classification_pro       =    models.ForeignKey("Model_ClassificationProfessionelle", on_delete = models.SET_NULL, related_name="postes", null = True, blank = True)
    # type_structure           =    models.ForeignKey("Model_TypeStructure", on_delete = models.SET_NULL, related_name="employes", null = True, blank = True)
    diplome                  =    models.ForeignKey("Model_Diplome", on_delete = models.SET_NULL, related_name="diplome_employes", null = True, blank = True)
    modele_bulletin          =    models.ForeignKey("Model_BulletinModele", on_delete = models.SET_NULL, related_name="employes_modele_bulletin", null = True, blank = True)
    statutrh                 =    models.ForeignKey("Model_StatusRH", on_delete = models.SET_NULL, related_name="fk_statut_employes", null = True, blank = True)
    document                 =    models.ForeignKey(Model_Document, on_delete = models.SET_NULL, related_name="document_employe", null = True, blank = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    user                     =    models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE, related_name="users_employes")

    #sexe                     =    models.CharField(max_length = 10, blank=True, null=True)
    #date_entree              =    models.DateTimeField(auto_now = True)



    @property
    def hisunitefonctionnelle(self):
        cont = Model_Unite_fonctionnelle.objects.get(pk = self.unite_fonctionnelle_id)
        return cont.libelle

    @property
    def all_employes(self):
        return Model_Employe.objects.all()

    @property
    def superieur_hierarchique(self):
        superieur = None
        try:
            superieur = self.unite_fonctionnelle.responsable
            return superieur
        except Exception as e:
            return self
    @property
    def is_connected(self):
        try:
            employe = Model_UserSessions.objects.filter(user = self.user, is_active = True, logout_date = None)
            if employe:
                return True
            return False
        except Exception as e:
            return False

    @property
    def nombre_enfants(self):
        nombre = 0
        try:
            nombre = Model_Dependant.objects.filter(employe_id = self.id, type_dependance = 'enfant').count()
            return nombre
        except Exception as e:
            return nombre

    @property
    def nombre_parts(self):
        try:
            nombre_part = 0
            part_agent = 1
            part_conjoint = 1
            dependant = Model_Dependant.objects.filter(employe_id = self.id)
            if dependant.count() == 0:
                nombre_part = part_agent
                return nombre_part
            elif dependant.exclude(type_dependance = "enfant").count() == 0:
                #cas célibataire
                nombre_enfant = dependant.filter(type_dependance = "enfant").count()
                nombre_enfant = nombre_enfant - 1
                part_enfant_celibataire = nombre_enfant * 0.5
                part_premier_enfant = 1
                nombre_part = part_agent + part_premier_enfant + part_enfant_celibataire
            else :
                #Cas marié
                nombre_enfant = dependant.filter(type_dependance = "enfant").count()
                part_enfant_marie = nombre_enfant * 0.5
                nombre_part = part_agent + part_conjoint + part_enfant_marie
            return nombre_part
        except Exception as e:
            #print("ERREUR nombrePartEmploye")
            #print(e)
            return 1

    @property
    def GetprofilRH(self):
        try:
            profilEmploye = Model_ProfilRH.objects.get(pk = self.profilrh_id)
            print('**PROFIL', profilEmploye)
            return profilEmploye
        except Exception as e:
            return None

class Model_LieuTravail(models.Model):
    designation              =    models.CharField(max_length = 50)
    description              =    models.TextField(null = True, blank = True, default="")
    created_at               =    models.DateTimeField(auto_now_add= True)
    update_at                =    models.DateTimeField(auto_now = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_lieu_travail', null = True, blank = True)


class Model_Fonction(models.Model):
    designation              =    models.CharField(max_length = 50)
    description              =    models.TextField(null = True, blank = True, default="")
    departement              =    models.ForeignKey("Model_Unite_fonctionnelle", on_delete = models.SET_NULL, related_name="fonctions", null = True, blank = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_fonction", null = True, blank = True)

    def __str__(self):
        return self.designation


class Model_Poste(models.Model):
    designation              =    models.CharField(max_length = 500)
    description              =    models.TextField(null = True, blank = True, default="")
    creation_date            =    models.DateTimeField(auto_now_add=True)
    departement              =    models.ForeignKey("Model_Unite_fonctionnelle", on_delete = models.SET_NULL, related_name="postes", null = True, blank = True)
    categorie                =    models.ForeignKey("Model_Categorie", on_delete = models.SET_NULL, related_name="postes", null = True, blank = True)
    lieu_exercice            =    models.ForeignKey(Model_Local, on_delete = models.SET_NULL, related_name="postes", null = True, blank = True)
    localisation             =    models.ForeignKey(Model_Place, on_delete = models.SET_NULL, related_name="postes", null = True, blank = True)
    responsable              =    models.ForeignKey("Model_Poste", on_delete = models.SET_NULL, related_name="postes", null = True, blank = True)
    nombre_subordonnes       =    models.IntegerField(default=0)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_poste", null = True, blank = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation

    @property
    def nombre_employe(self):
        nbre_employe = Model_Personne.objects.filter(type = "EMPLOYE").filter(poste_id = self.id).count()
        if(nbre_employe == 0):
            return "Aucun employé"
        elif(nbre_employe == 1): return "%s employé" % str(nbre_employe)
        elif(nbre_employe > 1): return "%s employés" % str(nbre_employe)


class Model_ClassificationProfessionelle(models.Model):
    designation              =    models.CharField(max_length = 50)
    code                     =    models.CharField(max_length = 50, null = True, blank = True)
    numero_reference         =    models.IntegerField(null = True, blank = True)
    description              =    models.TextField(null = True, blank = True, default="")
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    creation_date            =    models.DateTimeField(auto_now_add=True)
    update_date              =    models.DateTimeField(auto_now=True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_classification", null = True, blank = True)

    def __str__(self):
        return self.designation

    class Meta:
        ordering = ['numero_reference']

class Model_TypeUnite_fonctionnelle(models.Model):
    designation                 =    models.CharField(max_length = 250)
    description                 =    models.TextField(null = True, blank = True, default="")
    code                        =    models.CharField(max_length = 20, null = True, blank = True, default="")
    creation_date               =    models.DateTimeField(auto_now = True)
    update_date                 =    models.DateTimeField(auto_now_add = True)
    statut                      =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                        =    models.CharField(max_length=50, blank=True, null=True)
    auteur                      =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="type_unite_fonctionnelles", null = True, blank = True)
    url                         =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation

class Model_Unite_fonctionnelle(models.Model):
    libelle                  =    models.CharField(max_length = 100, null = True, blank=True, default = '')
    code                     =    models.CharField(max_length = 10, null = True, blank=True, default = '')
    est_racine               =    models.BooleanField(default = False)
    description              =    models.CharField(max_length = 250, null = True, blank=True, default = '')
    niveau                   =    models.IntegerField()
    creation_date            =    models.DateTimeField(auto_now_add = True)
    type                     =    models.CharField(max_length = 100, null = True, blank=True, default = '')
    type_unite_fonctionnelle =    models.ForeignKey(Model_TypeUnite_fonctionnelle, on_delete = models.SET_NULL, related_name="unite_fonctionnelles", null = True, blank = True)
    emplacement              =    models.ForeignKey(Model_Emplacement, null = True, blank = True, on_delete=models.SET_NULL, default = None)
    unite_fonctionnelle      =    models.ForeignKey("Model_Unite_fonctionnelle", on_delete = models.SET_NULL, related_name="unite_fonctionnelle_parent", null = True, blank = True)
    responsable              =    models.ForeignKey(Model_Employe, on_delete = models.SET_NULL, related_name="responsable_unite_fonctionnelle", null = True, blank = True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_unite_fonctionnelle", null = True, blank = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    update_date              =    models.DateTimeField(auto_now=True)
    url                      =     models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        parent = None
        if self.unite_fonctionnelle: parent = self.unite_fonctionnelle.code
        return "{} ({}) / {}".format(self.libelle, self.code, parent)

    @property
    def get_label(self):
        try:
            unite_fonctionnelle = Model_Unite_fonctionnelle.objects.get(pk = self.unite_fonctionnelle_id)
            name_label = unite_fonctionnelle.get_label + "/" + self.code
            return name_label
        except Exception as e:
            name_label = self.code
            return name_label

"""
class Model_Grade(models.Model):
    denomination = models.CharField(max_length = 50, null = True, blank=True, default = '')
    salaire = models.FloatField()
    creation_date = models.DateTimeField(auto_now = True)
    unite_fonctionnelle    = models.ForeignKey(Model_Unite_fonctionnelle, on_delete = models.SET_NULL, related_name="grade_in_unite_fonctionnelle", null = True, blank = True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_grade", null = True, blank = True)

    def __str__(self):
        return self.denomination """


class Model_Dependant(models.Model):
    nom_complet              =    models.CharField(max_length = 200, null = True, blank=True, default = '')
    type_dependance          =    models.CharField(choices = TypeDependant, max_length = 100, null = True, blank=True, default = 'enfant')
    description              =    models.CharField(max_length = 200, null = True, blank=True, default = '')
    date_naissance           =    models.DateField(null = True,  blank = True)
    employe                  =    models.ForeignKey(Model_Employe, on_delete = models.SET_NULL, related_name="dependant_employe", null = True, blank = True)
    document                 =    models.ForeignKey(Model_Document, on_delete = models.SET_NULL, related_name="document_dependant", null = True, blank = True)
    created_at               =    models.DateTimeField(null=True, blank=True)
    update_at                =    models.DateTimeField(auto_now = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_dependant", null = True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.nom_complet

    @property
    def value_type_dependance(self):
        if self.type_dependance:
            return dict(TypeDependant)[str(self.type_dependance)]


class Model_Pret(models.Model):
    reference                =    models.CharField(max_length=50, blank=True, null=True)
    rubrique                 =    models.ForeignKey("Model_Rubrique", on_delete= models.SET_NULL, blank=True, null=True)
    montant                  =    models.FloatField()
    devise                   =    models.ForeignKey(Model_Devise, on_delete = models.SET_NULL, null = True, blank = True,  related_name="devise_of_pret")
    nbre_mensualite          =    models.IntegerField(default = 1)
    date_premiere_echeance   =    models.DateTimeField(null=True, blank=True)
    taux_interet             =    models.FloatField(default = 0)
    employe                  =    models.ForeignKey(Model_Employe, on_delete = models.SET_NULL, related_name="pret_of_employe", null = True, blank = True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_pret", null = True, blank = True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    description 		     = 	  models.CharField(max_length = 500, null = True, blank=True, default = '')
    created_at               =    models.DateTimeField(null=True, blank=True)
    updated_at               =    models.DateTimeField(auto_now = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.reference

    @property
    def date_cloture(self):
        return self.date_premiere_echeance + relativedelta(months = self.nbre_mensualite)

    @property
    def is_running(self):
        '''Cette fonction test si un pret est applicable à une periode donné
        Il faut pour cela que la periode definie dans le dossier de paie soit comprise entre la date de premiere echeance et la date de cloture
        Puis Que l'Etat de la demande soit Valider et enfin que la dette à terme soit > 0.'''
        try:
            #Recuperation du dossier de paie actif
            dossier_paie = Model_DossierPaie.objects.filter(est_actif = True).first()
            if dossier_paie:
                monthrange = calendar.monthlen(int(dossier_paie.annee), int(dossier_paie.mois))
                date_en_cours = datetime(int(dossier_paie.annee), int(dossier_paie.mois), monthrange)
                start = self.date_premiere_echeance
                end = self.date_cloture
                #Test1 Date Comprise dans la periode de paie
                if start <= date_en_cours <= end:
                    return True if (self.etat == "Valider" and self.dette_a_terme > 0) else False
            return False
        except Exception as e:
            #print("is_running", e)
            return False

    @property
    def dette_a_terme(self):
        return self.montant - self.prelevement_anterieur

    @property
    def mensualite(self):
        return (self.montant + (self.montant * self.taux_interet) )  / self.nbre_mensualite

    @property
    def amount_to_pay(self):
        return self.mensualite if self.dette_a_terme > self.mensualite else self.dette_a_terme

    @property
    def prelevement_anterieur(self):
        somme = 0
        lignes = Model_LignePaiementPret.objects.filter(pret = self, est_succes = True)
        for ligne in lignes:
            #Dans le strict cas où la devise est la même
            somme += ligne.montant
        return somme

    @property
    def reste_a_recouvrer(self):
        return self.dette_a_terme - self.mensualite

    @property
    def str_value_amount(self, montant):
        return "{} {}".format(montant, self.devise.code_iso)



class Model_LignePaiementPret(models.Model):
    designation 		     = 	  models.CharField(max_length = 250, null = True, blank=True, default = '')
    pret                     =    models.ForeignKey(Model_Pret, on_delete = models.SET_NULL, null = True, blank = True,  related_name="paiement_of_ligne_pret")
    montant                  =    models.FloatField()
    devise                   =    models.ForeignKey(Model_Devise, on_delete = models.SET_NULL, null = True, blank = True,  related_name="devise_of_paiement_pret")
    est_succes               =    models.BooleanField(default = False)
    description 		     = 	  models.CharField(max_length = 500, null = True, blank=True, default = '')
    rubrique     		     =	  models.ForeignKey("Model_Rubrique", on_delete = models.SET_NULL, null = True, blank = True,  related_name="RubriqueLignePaiement")
    dossier_paie             =    models.ForeignKey("Model_DossierPaie", on_delete = models.CASCADE, blank=True, null=True)
    #item_bulletin		     =	  models.ForeignKey("Model_ItemBulletin", on_delete = models.SET_NULL, null = True, blank = True,  related_name="ItemBulletinLignePaiement")
    created_at               =    models.DateTimeField(null=True, blank=True)
    updated_at               =    models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.designation



class Model_PaiementInterne(models.Model):
    designation 		= 	models.CharField(max_length = 250, null = True, blank=True, default = '')
    description 		= 	models.CharField(max_length = 500, null = True, blank=True, default = '')
    pret 				=	models.ForeignKey("Model_Pret", on_delete=models.SET_NULL, null=True, blank=True, default=None, related_name = "paiements_internes_pret")
    conge 				=	models.ForeignKey("Model_Conge", on_delete=models.SET_NULL, null=True, blank=True, default=None, related_name = "paiements_internes_conge")
    montant				=	models.FloatField()
    periode_paye 		= 	models.IntegerField(default = 0)
    date_periode 		= 	models.DateTimeField(null = True, blank=True)
    taux				=	models.ForeignKey(Model_Taux, on_delete = models.SET_NULL, null = True, blank = True, default = None, related_name="paiements_intern_taux")
    dossier_paie		=	models.ForeignKey("Model_LotBulletins", on_delete = models.SET_NULL, null=True, blank = True, related_name="paiements_internes_item")
    item_bulletin		=	models.ForeignKey("Model_ItemBulletin", on_delete = models.SET_NULL, null = True, blank = True,  related_name="paiements_internes_devise")
    devise              =   models.ForeignKey(Model_Devise, on_delete = models.SET_NULL, null = True, blank = True,  related_name="paiements_internes_etat")
    etat 				=	models.CharField(max_length=300, blank=True, null=True)
    est_valide          = 	models.BooleanField(default = False)
    creation_date 		= 	models.DateTimeField(auto_now_add = True)
    update_date 		= 	models.DateTimeField(auto_now = True, blank=True, null=True)
    statut              =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                =   models.CharField(max_length=50, blank=True, null=True)
    auteur 				=	models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_paiements_internes", null = True, blank = True)
    url					= 	models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.information

    def status(self):
        statut = "En attente de validation"
        if self.est_valide: statut = "Validé"
        return statut

    @property
    def information(self):
        info = "Paiement Interne de %s %s du %s à %s" %(self.montant, self.devise.symbole_devise, self.creation_date.strftime('%d-%m-%Y'), self.creation_date.strftime('%I:%M'))
        return info

class Model_Presence(models.Model):
    employe                =    models.ForeignKey(Model_Employe, on_delete = models.SET_NULL, related_name = 'employe_fk_zok', null = True, blank = True)
    unite_fonctionelle     =    models.ForeignKey(Model_Unite_fonctionnelle, on_delete = models.SET_NULL, related_name = 'unite_fonctionelle_fk_qvi', null = True, blank = True)
    date                   =    models.DateField(blank=True, null=True)
    arrive                 =    models.TimeField()
    depart                 =    models.TimeField()
    created_at             =    models.DateTimeField(auto_now_add= True)
    update_at              =    models.DateTimeField(auto_now = True)
    statut                 =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                   =    models.CharField(max_length=50, blank=True, null=True)
    auteur                 =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_presence_gzc', null = True, blank = True)
    url                    =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return "Journée du " + str(self.arrive.date())

    @property
    def hisemploye(self):
        cont = Model_Employe.objects.get(pk = self.employe_id)
        return cont.nom_complet

    @property
    def hisunitefonctionnelle(self):
        cont = Model_Unite_fonctionnelle.objects.get(pk = self.unite_fonctionelle_id)
        return cont.libelle

class Model_Type_conge(models.Model):
    designation             =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    nombre_limite           =   models.IntegerField()
    is_active               =   models.BooleanField(default = False)
    max_leaves              =   models.IntegerField()
    leaves_taken            =   models.IntegerField()
    remaining               =   models.IntegerField()
    double_validation       =   models.BooleanField(default = False)
    created_at              =   models.DateTimeField(auto_now_add=True)
    update_at               =   models.DateTimeField(auto_now = True)
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_type_conge_lsd', null = True, blank = True)
    url                     =   models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation

    @property
    def incrementLeavesTaken(self):
        self.leaves_taken += 1

    @property
    def DecrementRemaining(self):
        self.remaining -= 1

class Model_Conge(models.Model):
    numero_conge            =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    description             =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    employe                 =   models.ForeignKey(Model_Employe, on_delete = models.SET_NULL, related_name = 'employe_fk_mei', null = True, blank = True)
    user                    =   models.ForeignKey(User, on_delete = models.SET_NULL, related_name = 'user_fk_apy', null = True, blank = True)
    date_from               =   models.DateField(null = True, blank = True)
    date_to                 =   models.DateField(null = True, blank = True)
    type_conge              =   models.ForeignKey(Model_Type_conge, on_delete = models.SET_NULL, related_name = 'type_conge_fk_sln', null = True, blank = True)
    type                    =   models.CharField(max_length = 25, null = True, blank=True, default = '')
    nombre_jour             =   models.IntegerField(default = 0)
    nombre_jour_temp        =   models.IntegerField(default = 0)
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True, related_name="statut_conge")
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    observation             =   models.CharField(max_length = 300, null = True, blank=True, default = '')
    created_at              =   models.DateTimeField(auto_now_add = True)
    update_at               =   models.DateTimeField(auto_now = True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_conge_gts', null = True, blank = True)
    url                     =   models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.description

    @property
    def hisemploye(self):
        cont = Model_Employe.objects.get(pk = self.employe_id)
        return cont.nom_complet

    @property
    def hismanager(self):
        cont = Model_Employe.objects.get(pk = self.manager_id)
        return cont.nom_complet

    @property
    def hismanager2(self):
        cont = Model_Employe.objects.get(pk = self.manager2_id)
        return cont.nom_complet

    @property
    def histypeconge(self):
        cont = Model_Type_conge.objects.get(pk = self.type_conge_id)
        return cont.designation



# Dossier du Social
class Model_Dossier_Social(models.Model):
    numero_dossier_social   =   models.CharField(max_length = 250, blank=True, null=True, default="")
    creation_date           =   models.DateTimeField(auto_now_add=True)
    employe                 =   models.ForeignKey(Model_Employe, on_delete=models.CASCADE, blank=True, null=True, related_name="dossier_social_employe")
    description             =   models.CharField(max_length = 500, blank=True, null=True, default="")
    structure               =   models.CharField(max_length = 250, blank=True, null=True, default="")
    lieu                    =   models.CharField(max_length = 250, blank=True, null=True, default="")
    sujet_plainte           =   models.CharField(max_length = 250, blank=True, null=True, default="")
    observation             =   models.CharField(max_length = 250, blank=True, null=True, default="")
    url                     =   models.CharField(max_length = 500, blank=True, null=True, default="")
    responsable             =   models.ForeignKey(Model_Employe, on_delete=models.CASCADE, blank=True, null=True,related_name="responsable_employe", default="")
    mail_envoye             =   models.TextField(max_length = 500, blank=True, null=True, default="")
    date_fermeture          =   models.DateTimeField(auto_now=True)
    statute                 =   models.IntegerField(choices = TypeEvenementSocial, null = True, blank = True)
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True, related_name="statut_dossier_social")
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    update_date             =   models.DateTimeField(auto_now=True)
    alerte                  =   models.BooleanField(default=False)
    auteur                  =   models.ForeignKey(Model_Employe, on_delete=models.CASCADE, blank=True, null=True, related_name="dossier_social_auteur")

    def __str__(self):
        return self.numero_dossier_social


#PARC AUTOMOBILE
class Model_Vehicule_model(models.Model):
    nom                     =   models.CharField(max_length = 50, null = True, blank=True, default = '')
    type                    =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    logo                    =   models.CharField(max_length = 150, null = True, blank=True, default = '')
    description             =   models.CharField(max_length = 250, null = True, blank=True, default = '')
    created_at              =   models.DateTimeField(auto_now_add=True)
    update_at               =   models.DateTimeField(auto_now = True)
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_vehicule_model_hou', null = True, blank = True)
    url                     =   models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.nom


class Model_Vehicule(models.Model):
    designation             =   models.CharField(max_length = 50, null = True, blank=True, default = '')
    marque                  =   models.CharField(max_length = 50, null = True, blank=True, default = '')
    vehicule_model          =   models.ForeignKey(Model_Vehicule_model, on_delete = models.SET_NULL, related_name = 'vehicule_model_fk_qvt', null = True, blank = True)
    date_acquisition        =   models.DateTimeField()
    image                   =   models.CharField(max_length = 250, null = True, blank=True, default = '')
    reference_licence       =   models.CharField(max_length = 50, null = True, blank=True, default = '')
    document                =   models.ForeignKey(Model_Document, on_delete = models.SET_NULL, related_name = 'document_fk_mhf', null = True, blank = True)
    employe                 =   models.ForeignKey(Model_Employe, on_delete = models.SET_NULL, related_name = 'employe_fk_oej', null = True, blank = True)
    couleur                 =   models.CharField(max_length = 50, null = True, blank=True, default = '')
    transmission            =   models.CharField(max_length = 15, null = True, blank=True, default = '')
    type_carburant          =   models.CharField(max_length = 20, null = True, blank=True, default = '')
    description             =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    created_at              =   models.DateTimeField(auto_now_add=True)
    update_at               =   models.DateTimeField(auto_now = True)
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_vehicule_lvh', null = True, blank = True)
    url                     =   models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation

    @property
    def hisemploye(self):
        cont = Model_Employe.objects.get(pk = self.employe_id)
        return cont.nom_complet

    @property
    def hisdocument(self):
        cont = Model_Document.objects.get(pk = self.document_id)
        return cont.numero_document

    @property
    def hisvehiculemodel(self):
        cont = Model_Vehicule_model.objects.get(pk = self.vehicule_model_id)
        return cont.nom

# MODULE PAYROLL

class Model_LotBulletins(models.Model):
    designation              =    models.CharField(max_length = 250)
    reference                =    models.CharField(max_length = 500, null = True, blank = True, default="")
    type                     =    models.CharField(choices = TypeLotBulletin, max_length = 250, null = True, blank = True)
    dossier_paie             =    models.ForeignKey("Model_DossierPaie", on_delete = models.CASCADE, related_name="lot_bulletins", null = True, blank=True )
    type_modele              =    models.IntegerField(choices = TypeModeleBulletin, null = True, blank = True, default=1)
    modele_bulletin          =    models.ForeignKey("Model_BulletinModele", on_delete = models.SET_NULL, blank=True, null=True, related_name="lot_bulletins")
    est_regulier             =    models.BooleanField(default = False)
    departement              =    models.ForeignKey(Model_Unite_fonctionnelle, on_delete = models.SET_NULL, related_name="lot_bulletins", null = True, blank = True)
    date_dossier             =    models.DateTimeField(blank=True, null=True)
    date_debut               =    models.DateTimeField(blank=True, null=True)
    date_fin                 =    models.DateTimeField(blank=True, null=True)
    est_soumis               =    models.BooleanField(default = False)
    est_valide               =    models.BooleanField(default = False)
    lignes                   =    models.ManyToManyField("Model_LignesLot")
    etat                     =    models.CharField(max_length = 250, blank=True, null=True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True, related_name="lot_bulletins")
    creation_date            =    models.DateTimeField(auto_now_add = True)
    update_date              =    models.DateTimeField(auto_now = True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="lot_bulletins", null=True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation

    @property
    def value_type(self):
        try:
            return dict(TypeLotBulletin)[str(self.type)]
        except Exception as e:
            return ""

    @property
    def value_type_modele(self):
        try:
            return dict(TypeModeleBulletin)[int(self.type_modele)]
        except Exception as e:
            return ""

@receiver(pre_delete, sender=Model_LotBulletins)
def pre_delete_story(sender, instance, **kwargs):
    for ligne_lot in instance.lignes.all():
        if ligne_lot.model_lotbulletins_set.all().count() == 1 and instance in ligne_lot.model_lotbulletins_set.all():
            # On supprime le ligne_lot quand c'est la seule instance du lot qui veut être supprimé
            ligne_lot.delete()

class Model_LignesLot(models.Model):
    reference                =    models.CharField(max_length = 500, null = True, blank = True, default="")
    employe                  =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="lignes_lots", null=True, blank = True)
    departement              =    models.ForeignKey(Model_Unite_fonctionnelle, on_delete = models.SET_NULL, related_name="lignes_lots", null = True, blank = True)
    creation_date            =    models.DateTimeField(auto_now_add = True)
    updated_date              =    models.DateTimeField(auto_now = True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_lignes_lots", null=True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)


class Model_Bulletin(models.Model):
    designation             =   models.CharField(max_length = 250)
    employe                 =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="mes_bulletins", null=True, blank = True)
    lot                     =   models.ForeignKey(Model_LotBulletins, on_delete = models.CASCADE, related_name="lot_of_this_bulletins", null=True, blank = True)
    reference               =   models.CharField(max_length = 500, null = True, blank = True, default="")
    periode                 =   models.CharField(max_length = 500, null = True, blank = True, default="")
    image                   =   models.CharField(max_length = 500, null = True, blank = True, default="")
    type                    =   models.CharField(max_length = 50, null = True, blank = True)
    total_a_retenir         =   models.FloatField(null = True, blank = True)
    brut_total              =   models.FloatField(null = True, blank = True)
    net_a_payer             =   models.FloatField(null = True, blank = True)
    brut_imposable          =   models.FloatField(null = True, blank = True)
    net_imposable           =   models.FloatField(null = True, blank = True)
    est_recalcule           =   models.BooleanField(default = False, null = True, blank = True)
    creation_date           =   models.DateTimeField(auto_now_add = True)
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    update_date             =   models.DateTimeField(auto_now=True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_bulletins", null=True, blank = True)
    url                     =   models.CharField(max_length = 250, blank=True, null=True)
    # Champs Add
    fonction                =   models.CharField(max_length = 500, null = True, blank = True, default="")
    grade                   =   models.CharField(max_length = 500, null = True, blank = True, default="")
    departemant             =   models.CharField(max_length = 500, null = True, blank = True, default="")
    diplome                 =   models.CharField(max_length = 500, null = True, blank = True, default="")
    nombrepart              =   models.FloatField(null = True, blank = True, default = 1)
    cycle_diplome           =   models.CharField(max_length = 100, null = True, blank = True, default="")


    def __str__(self):
        return self.designation

class Model_ItemBulletin(models.Model):
    designation             =    models.CharField(max_length = 50)
    sequence                =    models.IntegerField(null = True, blank = True)
    bulletin                =    models.ForeignKey(Model_Bulletin, related_name="item_bulletins", on_delete=models.CASCADE, null = True, blank = True)
    taux                    =    models.FloatField(null = True, blank = True, default=0.0)
    base                    =    models.FloatField(null = True, blank = True, default=0.0)
    montant                 =    models.FloatField(null = True, blank = True, default=0.0)
    nombre                  =    models.FloatField(null = True, blank = True, default=0.0)
    taux_parpat             =    models.FloatField(null = True, blank = True, default=0.0)
    montant_parpat          =    models.FloatField(null = True, blank = True, default=0.0)
    type                    =    models.IntegerField(null = True, blank = True)
    rubrique                =    models.ForeignKey("Model_Rubrique", on_delete=models.SET_NULL, null = True, blank = True)
    update_date             =    models.DateTimeField(auto_now = True)
    creation_date           =    models.DateTimeField(auto_now_add = True)
    statut                  =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =    models.CharField(max_length=50, blank=True, null=True)
    update_date             =    models.DateTimeField(auto_now=True)
    reference               =    models.CharField(max_length = 500, null = True, blank = True, default="")
    periode                 =    models.CharField(max_length = 500, null = True, blank = True, default="")
    auteur                  =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="item_bulletins", null=True, blank = True)
    url                     =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation

    class Meta:
        ordering = ['sequence']

class Model_temp_Nbre_Part(models.Model):
    periode_end_date        =    models.DateTimeField(blank=True, null=True)
    payroll_id              =   models.CharField(max_length = 100, null = True, blank = True, default="")
    element_name            =   models.CharField(max_length = 100, null = True, blank = True, default="")
    reporting_name          =   models.CharField(max_length = 100, null = True, blank = True, default="")
    class_name              =   models.CharField(max_length = 100, null = True, blank = True, default="")
    entry_start_date        =    models.DateTimeField(blank=True, null=True)
    entry_end_date          =    models.DateTimeField(blank=True, null=True)
    input_value_name        =   models.CharField(max_length = 100, null = True, blank = True, default="")
    resultat_value          =   models.CharField(max_length = 100, null = True, blank = True, default="")
    employe_number          =   models.CharField(max_length = 50, null = True, blank = True, default="")
    cl_ret                  =   models.CharField(max_length = 50, null = True, blank = True, default="")



class Model_ElementBulletin(models.Model):
    designation             =    models.CharField(max_length = 50)
    sequence                =    models.IntegerField(null = True, blank = True)
    type_element            =    models.IntegerField(choices = TypeElementBulletin, null = True, blank = True)
    categorie_element       =    models.IntegerField(choices = CategorieElementBulletin, null = True, blank = True)
    type_calcul             =    models.IntegerField(choices = TypeCalcul, null = True, blank = True)
    type_resultat           =    models.IntegerField(choices = TypeResultat, null = True, blank = True)
    reference               =    models.CharField(max_length = 500, null = True, blank = True, default="")
    montant                 =    models.FloatField(null = True, blank = True)
    pourcentage             =    models.FloatField(null = True, blank = True)
    calcul                  =    models.CharField(max_length = 250, null = True, blank = True)
    bareme                  =    models.ForeignKey("Model_Bareme", related_name="element_bulletins", on_delete=models.SET_NULL, null = True, blank = True, default=None)
    devise                  =    models.ForeignKey(Model_Devise, on_delete=models.SET_NULL, related_name="element_bulletins", null=True, blank=True, default=None)
    est_actif               =    models.BooleanField(default = True)
    creation_date           =    models.DateTimeField(auto_now_add = True)
    statut                  =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =    models.CharField(max_length=50, blank=True, null=True)
    update_date             =    models.DateTimeField(auto_now=True)
    compte                  =    models.ForeignKey("Model_Compte", on_delete=models.SET_NULL, blank = True, null = True)
    auteur                  =    models.ForeignKey(Model_Personne, on_delete=models.SET_NULL, related_name="element_bulletins", null = True, blank = True)
    url                     =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation

class Model_Bareme(models.Model):
    designation             =    models.CharField(max_length = 250)
    devise                  =    models.ForeignKey(Model_Devise, on_delete=models.SET_NULL, related_name="baremes", null=True, blank=True, default=None)
    reference               =    models.CharField(max_length = 500, null = True, blank = True, default="")
    type                    =    models.CharField(max_length = 250, null = True, blank = True)
    creation_date           =    models.DateTimeField(auto_now_add = True)
    statut                  =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =    models.CharField(max_length=50, blank=True, null=True)
    update_date             =    models.DateTimeField(auto_now=True)
    auteur                  =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="baremes", null=True, blank = True)
    url                     =    models.CharField(max_length = 500, blank=True, null=True)

    def __str__(self):
        return self.designation

class Model_TrancheBareme(models.Model):
    designation                =    models.CharField(max_length = 250)
    sequence                =    models.IntegerField(null = True, blank = True)
    bareme                    =    models.ForeignKey(Model_Bareme, related_name="tranche_baremes", on_delete=models.SET_NULL, null = True, blank = True)
    pourcentage_net_impot    =    models.FloatField(null = True, blank = True)
    tranche_debut            =    models.FloatField(null = True, blank = True)
    tranche_fin                =    models.FloatField(null = True, blank = True)
    montant_net_impot        =    models.FloatField(null = True, blank = True)
    devise                    =    models.ForeignKey(Model_Devise, on_delete=models.SET_NULL, related_name="tranche_baremes", null=True, blank=True, default=None)
    creation_date            =    models.DateTimeField(auto_now_add = True)
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    update_date             =   models.DateTimeField(auto_now=True)
    auteur                    =    models.ForeignKey(Model_Personne, on_delete=models.SET_NULL, related_name="tranche_baremes", null = True, blank = True)
    url                    =     models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation


class Model_ProfilPaye(models.Model):
    designation             =    models.CharField(max_length = 300, null = True, blank = True)
    reference               =    models.CharField(max_length = 500, null = True, blank = True, default="")
    poste                   =    models.ForeignKey(Model_Poste, on_delete = models.SET_NULL, related_name="poste_on_profil_paie", null = True, blank = True)
    employe                 =    models.ForeignKey(Model_Employe, on_delete = models.SET_NULL, related_name="profil_paie_of_employe", null = True, blank = True)
    date_profil             =    models.DateTimeField(auto_now = True)
    montant                 =    models.FloatField(default = 0)
    has_debt                =    models.BooleanField(default = False)
    structure_salariale     =    models.ForeignKey("Model_StructureSalariale", on_delete = models.SET_NULL, related_name="profils_paies", null = True, blank = True)
    creation_date           =    models.DateTimeField(auto_now_add = True)
    statut                  =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =    models.CharField(max_length=50, blank=True, null=True)
    update_date             =    models.DateTimeField(auto_now=True)
    auteur                  =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_profil_paie", null = True, blank = True)
    url                     =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation


class Model_ItemProfilPaye(models.Model):
    designation             =    models.CharField(max_length = 50)
    sequence                =    models.IntegerField(null = True, blank = True)
    profil_paie             =    models.ForeignKey(Model_ProfilPaye, related_name="item_profil_payes", on_delete=models.SET_NULL, null = True, blank = True)
    element                 =    models.ForeignKey(Model_ElementBulletin, related_name="item_profil_payes", on_delete=models.SET_NULL, null = True, blank = True)
    valeur_pourcentage      =    models.FloatField(null = True, blank = True)
    montant                 =    models.FloatField(null = True, blank = True)
    devise                  =    models.ForeignKey(Model_Devise, on_delete=models.SET_NULL, related_name="item_profil_payes", null=True, blank=True, default=None)
    creation_date           =    models.DateTimeField(auto_now_add = True)
    statut                  =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =    models.CharField(max_length=50, blank=True, null=True)
    update_date             =    models.DateTimeField(auto_now=True)
    auteur                  =    models.ForeignKey(Model_Personne, on_delete=models.SET_NULL, related_name="item_profil_payes", null = True, blank = True)
    url                     =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation

# Restructuration PayRoll
class Model_TypeStructure(models.Model):
    designation            =    models.CharField(max_length = 300, null = True, blank = True)
    description            =    models.CharField(max_length = 500, null = True, blank = True, default="")
    type_salaire           =    models.IntegerField(choices = TypeSalaire, default=1)
    horaire_paye           =    models.IntegerField(choices = HorairePaye, default=1)
    creation_date          =    models.DateTimeField(auto_now_add = True)
    auteur                 =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_types_structures", null = True, blank = True)
    url                    =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation

    @property
    def value_type_salaire(self):
        return dict(TypeSalaire)[int(self.type_salaire)]

    @property
    def value_horaire_paye(self):
        return dict(HorairePaye)[int(self.horaire_paye)]

    @property
    def structure_par_defaut(self):
        try:
            structure = Model_StructureSalariale.objects.get(par_defaut = True)
            return structure
        except Exception as e:
            return None

    @property
    def nombre_structure(self):
        try:
            nbre = Model_StructureSalariale.objects.filter(type_id = self.id).count()
            return nbre
        except Exception as e:
            return 0


class Model_StructureSalariale(models.Model):
    designation            =    models.CharField(max_length = 250, null = True, blank = True)
    description            =    models.CharField(max_length = 500, null = True, blank = True, default="")
    type                   =    models.ForeignKey(Model_TypeStructure, on_delete = models.SET_NULL, related_name="structures_salariales", null = True, blank = True)
    journal                =    models.ForeignKey(Model_Journal, on_delete = models.SET_NULL, related_name="structures_salariales", null = True, blank = True)
    devise                 =    models.ForeignKey(Model_Devise, on_delete = models.SET_NULL, related_name="structures_salariales", null = True, blank = True)
    horaire_paye           =    models.IntegerField(choices = HorairePaye, default=1)
    est_actif              =    models.BooleanField(default = True)
    regles                 =    models.ManyToManyField("Model_RegleSalariale", related_name="structures_salariales")
    par_defaut             =    models.BooleanField(default = False)
    libelle_bulletin       =    models.CharField(max_length = 250, null = True, blank = True)
    creation_date          =    models.DateTimeField(auto_now_add = True)
    statut                 =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                   =    models.CharField(max_length=50, blank=True, null=True)
    update_date            =    models.DateTimeField(auto_now=True)
    auteur                 =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_structures_salariales", null = True, blank = True)
    url                    =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation

    @property
    def value_horaire_paye(self):
        return dict(HorairePaye)[int(self.horaire_paye)]

class Model_ItemStructureSalariale(models.Model):
    designation            =    models.CharField(max_length = 50)
    sequence               =    models.IntegerField(null = True, blank = True)
    structure              =    models.ForeignKey(Model_StructureSalariale, related_name="item_structures_salaires", on_delete=models.SET_NULL, null = True, blank = True)
    regle                  =    models.ForeignKey("Model_RegleSalariale", related_name="item_structures_salaires", on_delete=models.SET_NULL, null = True, blank = True)
    element                =    models.ForeignKey(Model_ElementBulletin, related_name="item_structures_salaires", on_delete=models.SET_NULL, null = True, blank = True)
    valeur_pourcentage     =    models.FloatField(null = True, blank = True)
    montant                =    models.FloatField(null = True, blank = True)
    devise                 =    models.ForeignKey(Model_Devise, on_delete=models.SET_NULL, related_name="item_structures_salaires", null=True, blank=True, default=None)
    creation_date          =    models.DateTimeField(auto_now_add = True)
    statut                 =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                   =    models.CharField(max_length=50, blank=True, null=True)
    update_date            =    models.DateTimeField(auto_now=True)
    auteur                 =    models.ForeignKey(Model_Personne, on_delete=models.SET_NULL, related_name="item_structures_salaires", null = True, blank = True)
    url                    =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation

class Model_CategorieRegle(models.Model):
    designation         =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    description         =   models.CharField(max_length = 250, null = True, blank=True, default = '')
    code                =   models.CharField(max_length = 10, null = True, blank=True, default = '')
    created_at          =   models.DateTimeField(auto_now_add = True)
    update_at           =   models.DateTimeField(auto_now = True)
    statut              =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                =   models.CharField(max_length=50, blank=True, null=True)
    auteur              =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_categories_regles', null = True, blank = True)

    def __str__(self):
        return self.designation

class Model_RegleSalariale(models.Model):
    designation             =    models.CharField(max_length = 250)
    reference             =    models.CharField(max_length = 250)
    description             =    models.CharField(max_length = 250, null = True, blank=True, default = '')
    code                    =    models.CharField(max_length = 10)
    sequence                =    models.IntegerField(default = 99)
    type_element            =    models.IntegerField(choices = TypeElementBulletin, default= 1)
    quantite                =    models.IntegerField(default = 1)
    categorie               =    models.ForeignKey(Model_CategorieRegle, on_delete=models.SET_NULL, related_name="regle_salariales", null=True, blank=True, default=None)
    type_condition          =    models.CharField(choices = TypeCondition, max_length = 100, default="aucun")
    plage_condition         =    models.CharField(null = True, blank = True, max_length = 250)
    code_condition          =    models.CharField(null = True, blank = True, max_length = 250)
    plage_min_condition     =    models.FloatField(null = True, blank = True)
    plage_max_condition     =    models.FloatField(null = True, blank = True)
    type_calcul             =    models.IntegerField(choices = TypeCalcul, default= 1)
    type_resultat           =    models.IntegerField(choices = TypeResultat, null = True, blank = True)
    montant_fixe            =    models.FloatField(null = True, blank = True)
    pourcentage             =    models.FloatField(null = True, blank = True)
    pourcentage_sur         =    models.CharField(max_length = 250, null = True, blank = True)
    code_python             =    models.CharField(max_length = 250, null = True, blank = True)
    bareme                  =    models.ForeignKey(Model_Bareme, related_name="regle_salariales", on_delete=models.SET_NULL, null = True, blank = True, default=None)
    devise                  =    models.ForeignKey(Model_Devise, on_delete=models.SET_NULL, related_name="regle_salariales", null=True, blank=True, default=None)
    est_actif               =    models.BooleanField(default = True)
    apparait_dans_bulletin  =    models.BooleanField(default = True)
    compte_debit            =    models.ForeignKey(Model_Compte, on_delete=models.SET_NULL, blank = True, null = True, related_name="debit_regle_salariales",)
    compte_credit           =    models.ForeignKey(Model_Compte, on_delete=models.SET_NULL, blank = True, null = True, related_name="credit_regle_salariales",)
    creation_date           =    models.DateTimeField(auto_now_add = True)
    statut                  =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =    models.CharField(max_length=50, blank=True, null=True)
    update_date             =    models.DateTimeField(auto_now=True)
    auteur                  =    models.ForeignKey(Model_Personne, on_delete=models.SET_NULL, related_name="regle_salariales", null = True, blank = True)
    url                     =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation

    @property
    def value_type_condition(self):
        try:
            return dict(TypeCondition)[str(self.type_condition)]
        except Exception as e:
            return ""

    @property
    def value_type_calcul(self):
        try:
            return dict(TypeCalcul)[int(self.type_calcul)]
        except Exception as e:
            return ""

    @property
    def value_type_resultat(self):
        try:
            return dict(TypeResultat)[int(self.type_resultat)]
        except Exception as e:
            return ""

    @property
    def value_type_element(self):
        try:
            return dict(TypeElementBulletin)[int(self.type_element)]
        except Exception as e:
            return ""

class Model_Rubrique(models.Model):
    designation             =    models.CharField(max_length = 250)
    reference               =    models.CharField(max_length = 50, null = True, blank=True, default = '')
    description             =    models.CharField(max_length = 4000, null = True, blank=True, default = '')
    code                    =    models.CharField(max_length = 10)
    sequence                =    models.IntegerField(default = 99)
    type_element            =    models.IntegerField(choices = TypeElementBulletin, null = True, blank = True)
    type_rubrique           =    models.IntegerField(choices = TypeRubrique, default= 1)
    type_formule            =    models.IntegerField(choices = TypeFormule, default= 1)
    nombre_parsal           =    models.FloatField(null = True, blank = True)
    nombre_parsal_is_const  =    models.BooleanField(default = False)
    nombre_parsal_const     =    models.ForeignKey("Model_Constante", on_delete=models.SET_NULL, null=True, blank=True, related_name="nombre_pp_rubriques")
    nombre_est_modifiable   =    models.BooleanField(default = False)
    base_parsal             =    models.FloatField(null = True, blank = True)
    base_parsal_is_const    =    models.BooleanField(default = False)
    base_parsal_const       =    models.ForeignKey("Model_Constante", on_delete=models.SET_NULL, null=True, blank=True, related_name="base_pp_rubriques")
    base_est_modifiable     =    models.BooleanField(default = False)
    taux_parsal             =    models.FloatField(null = True, blank = True)
    taux_parsal_is_const    =    models.BooleanField(default = False)
    taux_parsal_const       =    models.ForeignKey("Model_Constante", on_delete=models.SET_NULL, null=True, blank=True, related_name="taux_ps_rubriques")
    taux_est_modifiable     =    models.BooleanField(default = False)
    montant_parsal          =    models.FloatField(null = True, blank = True)
    montant_parsal_is_const =    models.BooleanField(default = False)
    montant_parsal_const    =    models.ForeignKey("Model_Constante", on_delete=models.SET_NULL, null=True, blank=True, related_name="montant_ps_rubriques")
    montant_est_modifiable  =    models.BooleanField(default = False)
    taux_parpat             =    models.FloatField(null = True, blank = True)
    taux_parpat_is_const    =    models.BooleanField(default = False)
    taux_parpat_const       =    models.ForeignKey("Model_Constante", on_delete=models.SET_NULL, null=True, blank=True, related_name="taux_pp_rubriques")
    taux_pp_est_modifiable  =    models.BooleanField(default = False)
    montant_parpat          =    models.FloatField(null = True, blank = True)
    montant_parpat_is_const =    models.BooleanField(default = False)
    montant_parpat_const    =    models.ForeignKey("Model_Constante", on_delete=models.SET_NULL, null=True, blank=True, related_name="montant_pp_rubriques")
    montant_pp_est_modifiable=   models.BooleanField(default = False)
    devise                  =    models.ForeignKey(Model_Devise, on_delete=models.SET_NULL, related_name="rubriques", null=True, blank=True)
    est_actif               =    models.BooleanField(default = True)
    apparait_dans_bulletin  =    models.BooleanField(default = True)
    est_cumul               =    models.BooleanField(default = False)
    compte_debit            =    models.ForeignKey(Model_Compte, on_delete=models.SET_NULL, related_name="debit_rubriques", null = True, blank = True)
    compte_credit           =    models.ForeignKey(Model_Compte, on_delete=models.SET_NULL, related_name="credit_rubriques", null = True, blank = True)
    creation_date           =    models.DateTimeField(auto_now_add = True)
    update_date             =    models.DateTimeField(auto_now = True)
    statut                  =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =    models.CharField(max_length=50, blank=True, null=True)
    auteur                  =    models.ForeignKey(Model_Personne, on_delete=models.SET_NULL, related_name="rubriques", null = True, blank = True)
    est_patronal            =    models.BooleanField(default = False)

    def __str__(self):
        return self.designation

    @property
    def value_type_element(self):
        try:
            return dict(TypeElementBulletin)[int(self.type_element)]
        except Exception as e:
            return ""

    @property
    def value_type_rubrique(self):
        try:
            return dict(TypeRubrique)[int(self.type_rubrique)]
        except Exception as e:
            return ""

    @property
    def value_type_formule(self):
        try:
            return dict(TypeFormule)[int(self.type_formule)]
        except Exception as e:
            return ""

class Model_Constante(models.Model):
    designation             =    models.CharField(max_length = 250)
    reference               =    models.CharField(max_length = 250, null = True, blank=True, default = '')
    description             =    models.CharField(max_length = 4000, null = True, blank=True, default = '')
    code                    =    models.CharField(max_length = 50)
    type_constant           =    models.IntegerField(choices = TypeConstante, default= 1)
    periode_cumul           =    models.IntegerField(choices = PeriodeCumul, null = True, blank=True, default= 1)
    date_debut_cumul        =    models.BigIntegerField(null = True, blank=True)
    date_fin_cumul          =    models.BigIntegerField(null = True, blank=True)
    date_constante          =    models.BigIntegerField(null = True, blank=True)
    base_test               =    models.FloatField(null = True, blank = True)
    base_test_is_const      =    models.BooleanField(default = False)
    base_test_const         =    models.ForeignKey("Model_Constante", on_delete=models.SET_NULL, null=True, blank=True, related_name="base_constantes")
    rubrique                =    models.ForeignKey(Model_Rubrique, on_delete=models.CASCADE, blank=True, null=True, related_name="constantes")
    valeur                  =    models.FloatField(null = True, blank = True)
    valeur_is_const         =    models.BooleanField(default = False)
    valeur_const            =    models.ForeignKey("Model_Constante", on_delete=models.SET_NULL, null=True, blank=True, related_name="valeur_constantes")
    alors                   =    models.FloatField(null = True, blank = True)
    alors_is_const          =    models.BooleanField(default = False)
    alors_const             =    models.ForeignKey("Model_Constante", on_delete=models.SET_NULL, null=True, blank=True, related_name="alors_constantes")
    sinon                   =    models.FloatField(null = True, blank = True)
    sinon_is_const          =    models.BooleanField(default = False)
    sinon_const             =    models.ForeignKey("Model_Constante", on_delete=models.SET_NULL, null=True, blank=True, related_name="sinon_constantes")
    fonction                =    models.CharField(max_length = 100, blank=True, null=True)
    devise                  =    models.ForeignKey(Model_Devise, on_delete=models.SET_NULL, related_name="constantes", null=True, blank=True)
    creation_date           =    models.DateTimeField(auto_now_add = True)
    update_date             =    models.DateTimeField(auto_now = True)
    statut                  =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =    models.CharField(max_length=50, blank=True, null=True)
    auteur                  =    models.ForeignKey(Model_Personne, on_delete=models.SET_NULL, related_name="constantes", null = True, blank = True)

    def __str__(self):
        return self.designation

    @property
    def value_type_constant(self):
        try:
            return dict(TypeConstante)[int(self.type_constant)]
        except Exception as e:
            return ""

    @property
    def value_periode_cumul(self):
        try:
            return dict(PeriodeCumul)[int(self.periode_cumul)]
        except Exception as e:
            return ""

    @property
    def value_date_constante(self):
        try:
            ts = float(self.date_constante)
            date = datetime.fromtimestamp(ts)
            return date
        except Exception as e:
            return None

    @property
    def last_sequence_calcul(self):
        try:
            last_sequence = Model_ConstanteCalcul.objects.filter(constante_parent_id = self.id).aggregate(Max('sequence'))['sequence__max']
            #print("last_sequence: {}".format(last_sequence))
            return int(last_sequence)
        except Exception as e:
            return 0

    @property
    def last_sequence_test(self):
        try:
            last_sequence = Model_ConstanteTest.objects.filter(constante_parent_id = self.id).aggregate(Max('sequence'))['sequence__max']
            return int(last_sequence)
        except Exception as e:
            return 0

    @property
    def last_sequence_tranche(self):
        try:
            last_sequence = Model_ConstanteTranche.objects.filter(constante_parent_id = self.id).aggregate(Max('sequence'))['sequence__max']
            return int(last_sequence)
        except Exception as e:
            return 0

class Model_ConstanteCalcul(models.Model):
    sequence                =    models.IntegerField(default = 99)
    constante_parent        =    models.ForeignKey(Model_Constante, on_delete=models.CASCADE, related_name="parametres_calculs")
    type_operation          =    models.IntegerField(choices = TypeOperationCalcul, default= 1)
    rubrique                =    models.ForeignKey(Model_Rubrique, on_delete=models.SET_NULL, blank=True, null=True, related_name="parametres_calculs")
    code                    =    models.FloatField(null = True, blank = True)
    code_is_const           =    models.BooleanField(default = False)
    code_const              =    models.ForeignKey(Model_Constante, on_delete=models.SET_NULL, null=True, blank=True)
    creation_date           =    models.DateTimeField(auto_now_add = True)
    update_date             =    models.DateTimeField(auto_now = True)
    auteur                  =    models.ForeignKey(Model_Personne, on_delete=models.SET_NULL, related_name="auteur_parametres_calculs", null = True, blank = True)

    class Meta:
        ordering = ['sequence']

    def __str__(self):
        return "Ligne Calcul No {} - {}".format(self.sequence, self.constante_parent.code)

    @property
    def value_type_operation(self):
        try:
            return dict(TypeOperationCalcul)[int(self.type_operation)]
        except Exception as e:
            return ""


class Model_ConstanteTest(models.Model):
    sequence                =    models.IntegerField(default = 99)
    constante_parent        =    models.ForeignKey(Model_Constante, on_delete=models.CASCADE, related_name="parametres_tests")
    type_operation          =    models.IntegerField(choices = TypeOperationTest, default= 1)
    type_condition          =    models.IntegerField(choices = TypeConditionTest, default= 1)
    valeur                  =    models.FloatField(null = True, blank = True)
    valeur_is_const         =    models.BooleanField(default = False)
    valeur_const            =    models.ForeignKey(Model_Constante, on_delete=models.SET_NULL, null=True, blank=True, related_name="valeur_constantes_tests")
    code                    =    models.FloatField(null = True, blank = True)
    code_is_const           =    models.BooleanField(default = False)
    code_const              =    models.ForeignKey(Model_Constante, on_delete=models.SET_NULL, null=True, blank=True, related_name="code_constantes_tests")
    creation_date           =    models.DateTimeField(auto_now_add = True)
    update_date             =    models.DateTimeField(auto_now = True)
    auteur                  =    models.ForeignKey(Model_Personne, on_delete=models.SET_NULL, related_name="auteur_parametres_tests", null = True, blank = True)

    class Meta:
        ordering = ['sequence']

    def __str__(self):
        return "Ligne Test No {} - {}".format(self.sequence, self.constante_parent.code)

    @property
    def value_type_operation(self):
        try:
            return dict(TypeOperationTest)[int(self.type_operation)]
        except Exception as e:
            return ""

    @property
    def value_type_condition(self):
        try:
            return dict(TypeConditionTest)[int(self.type_condition)]
        except Exception as e:
            return ""

class Model_ConstanteTranche(models.Model):
    sequence                =    models.IntegerField(default = 99)
    constante_parent        =    models.ForeignKey(Model_Constante, on_delete=models.CASCADE, related_name="parametres_tranches")
    tranche_debut           =    models.FloatField(null = True, blank = True)
    tranche_debut_is_const  =    models.BooleanField(default = False)
    tranche_debut_const     =    models.ForeignKey(Model_Constante, on_delete=models.SET_NULL, null=True, blank=True, related_name="debut_constantes_tranches")
    tranche_fin             =    models.FloatField(null = True, blank = True)
    tranche_fin_is_const    =    models.BooleanField(default = False)
    tranche_fin_const       =    models.ForeignKey(Model_Constante, on_delete=models.SET_NULL, null=True, blank=True, related_name="fin_constantes_tranches")
    type_operation_debut    =    models.IntegerField(choices = TypeOperationTest, null = True, blank = True)
    type_operation_fin      =    models.IntegerField(choices = TypeOperationTest, null = True, blank = True)
    valeur                  =    models.FloatField(null = True, blank = True)
    valeur_is_const         =    models.BooleanField(default = False)
    valeur_const            =    models.ForeignKey(Model_Constante, on_delete=models.SET_NULL, null=True, blank=True, related_name="valeur_constantes_tranches")
    creation_date           =    models.DateTimeField(auto_now_add = True)
    update_date             =    models.DateTimeField(auto_now = True)
    auteur                  =    models.ForeignKey(Model_Personne, on_delete=models.SET_NULL, related_name="parametres_tranches", null = True, blank = True)

    class Meta:
        ordering = ['sequence']

    def __str__(self):
        return "Ligne Tranche No {} - {}".format(self.sequence, self.constante_parent.code)

    @property
    def value_type_operation_debut(self):
        try:
            return dict(TypeOperationTest)[int(self.type_operation_debut)]
        except Exception as e:
            return ""

    @property
    def value_type_operation_fin(self):
        try:
            return dict(TypeOperationTest)[int(self.type_operation_fin)]
        except Exception as e:
            return ""

class Model_BulletinModele(models.Model):
    designation            =    models.CharField(max_length = 250, null = True, blank = True)
    description            =    models.CharField(max_length = 500, null = True, blank = True, default="")
    type                   =    models.ForeignKey(Model_TypeStructure, on_delete = models.SET_NULL, related_name="Bulletins_modeles", null = True, blank = True)
    journal                =    models.ForeignKey(Model_Journal, on_delete = models.SET_NULL, related_name="Bulletins_modeles", null = True, blank = True)
    devise                 =    models.ForeignKey(Model_Devise, on_delete = models.SET_NULL, related_name="Bulletins_modeles", null = True, blank = True)
    horaire_paye           =    models.IntegerField(choices = HorairePaye, default=1)
    est_actif              =    models.BooleanField(default = True)
    rubriques              =    models.ManyToManyField(Model_Rubrique, related_name="Bulletins_modeles")
    par_defaut             =    models.BooleanField(default = False)
    libelle_bulletin       =    models.CharField(max_length = 250, null = True, blank = True)
    creation_date          =    models.DateTimeField(auto_now_add = True)
    statut                 =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                   =    models.CharField(max_length=50, blank=True, null=True)
    update_date            =    models.DateTimeField(auto_now=True)
    auteur                 =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_Bulletins_modeles", null = True, blank = True)

    def __str__(self):
        return self.designation

    @property
    def value_horaire_paye(self):
        try:
            return dict(HorairePaye)[int(self.horaire_paye)]
        except Exception as e:
            return ""

class Model_Config_Payroll(models.Model):
    taux_cnss                   =    models.FloatField(default = 3.5)
    nbre_max_jours_travailles   =    models.FloatField(default = 22.0)
    nbre_mensualite             =    models.IntegerField(default = 10)
    taux_interet                =    models.FloatField(default = 0)
    est_active                  =    models.BooleanField(default = False)
    creation_date               =    models.DateTimeField(auto_now_add = True)
    update_date                 =    models.DateTimeField(auto_now = True)
    organisation                =    models.ForeignKey(Model_Organisation, on_delete= models.CASCADE, blank=True, null=True)
    auteur                      =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_config_payroll', null = True, blank = True)

    def __str__(self):
        return "Configuration du PayRoll ID - {}".format(self.pk)

#PROFIL AGENT
class Model_ProfilRH(models.Model):
    date_engagement           =    models.DateField(null = True, blank = True)
    debut_service             =    models.DateField(null = True, blank = True)
    date_naissance            =    models.DateField(null = True,  blank = True)
    lieu_naissance            =    models.CharField(max_length = 100,null = True,  blank = True)
    nationalite               =    models.CharField(max_length = 100, null = True, blank = True)
    numero_passeport          =    models.CharField(max_length = 100, null = True , blank = True)
    numero_identification     =    models.CharField(max_length = 100 , null = True , blank = True)
    etat_civil                =    models.CharField(max_length = 100, null = True, blank = True)
    fonctions                 =    models.ManyToManyField("Model_Fonction")#models.CharField(max_length = 300, null = True, blank = True)
    numero_ss                 =    models.CharField (max_length = 100 ,null = True , blank = True)
    genre                     =    models.CharField(max_length = 100 ,null = True , blank = True)
    matricule                 =    models.CharField(max_length = 100, null = True, blank = True)
    email_professionnel       =    models.CharField(max_length = 100 ,null = True , blank = True)
    phone_professionnel       =    models.CharField(max_length = 100 ,null = True , blank = True)
    phone_personnel           =    models.CharField(max_length = 100 ,null = True , blank = True)
    phone_professionnel2      =    models.CharField(max_length = 100 ,null = True , blank = True)
    contrat                   =    models.CharField(max_length = 100, blank = True, null = True, default = '')
    est_permanent            =    models.BooleanField(default = True)
    statut                    =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                      =    models.CharField(max_length=50, blank=True, null=True)
    auteur                    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="profil_auteur", null = True, blank = True)
    update_date               =    models.DateTimeField(auto_now=True)
    creation_date             =    models.DateTimeField(auto_now_add=True)
    url                       =    models.CharField(max_length = 250, blank=True, null=True)
    education                 =    models.CharField(max_length = 100, null = True, blank = True)


    #date_creation             =    models.DateField(null = True,  blank = True, auto_now=True)
    #date_modification         =    models.DateField(null = True, blank = True)
    #seconde_nationalite       =    models.CharField(max_length = 100, null = True, blank = True)
    #compte_bancaire           =    models.CharField(max_length = 100 , null = True , blank = True)
    #agent                     =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="agent", null = True, blank = True)
    #est_enconge               =    models.BooleanField(default = False)
    #designation_banque        =    models.CharField(max_length = 100, null = True , blank = True )
    #adresse_banque            =    models.CharField(max_length = 100, null = True , blank = True )
    #code_swift                =    models.CharField(max_length = 100, null = True , blank = True )
    #categorie                 =    models.CharField(choices=CategoriePros,max_length = 100, null = True, blank=True, default = '')
    #classificaion             =    models.CharField(max_length = 250, blank = True, null = True, default = '')
    #lieu_exercice             =    models.CharField(max_length = 100, blank = True, null = True, default = '')
    #responsable_id            =  models.ForeignKey("Model_Employe", on_delete = models.SET_NULL, related_name="responsable", null = True, blank = True)
    #dependant                 =    models.IntegerField(null = True,blank=True)
    #grade                     =    models.CharField(max_length = 100 ,null = True , blank = True)
    #situation_famille         =    models.CharField(max_length = 10 ,null = True , blank = True)
    #lieu_travail              =    models.CharField(max_length = 100, null = True, blank = True)
    #permis           =    models.CharField(max_length = 100, null = True, blank = True)







    def __str__(self):
        try:
            employe = Model_Employe.objects.get(profilrh_id = self.id)
            return "Profil de {}".format(employe.nom_complet)
        except Exception as e:
            return "Profil inconnu"



class Model_Ordre_paie(models.Model):
    numero_ordre_paie       =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    date_paie               =   models.DateTimeField(auto_now = True)
    is_validate             =   models.BooleanField(default = False)
    is_accepted             =   models.BooleanField(default = False)
    montant_global          =   models.FloatField()
    creation_date           =   models.DateTimeField(auto_now_add = True)
    preuve                  =   models.CharField(max_length = 300, null = True, blank=True, default = '')
    compte                  =   models.ForeignKey(Model_Compte, on_delete = models.SET_NULL, related_name="compte_about_ordre_paie", null = True, blank = True)
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    update_date             =   models.DateTimeField(auto_now=True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_ordre_paie", null = True, blank = True)
    url                     =   models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.numero_ordre_paie

# MODULE VENTE

class Model_Client(Model_Personne):
    sexe                    =   models.CharField(max_length = 10, blank=True, null=True)
    numero_compte_b         =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    nui                     =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    personne_contact        =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    bp                      =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    raison_sociale          =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    fax                     =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    fiscale                 =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    autre_info                 =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    mode_reglement          =   models.ForeignKey("Model_ConditionReglement", on_delete = models.SET_NULL, related_name="client_condition_reglement", blank=True, null=True)
    #postnom                    =    models.CharField(max_length = 50, null = True, blank = True)
    #civilite                =    models.ForeignKey("Model_Civilite", on_delete=models.SET_NULL, null = True, blank = True)
    langue                    =    models.CharField(max_length = 50, null = True, blank = True, default="")
    #type                    =    models.CharField(max_length = 30, null = True, blank = True)
    lieu_de_naissance         =    models.CharField(max_length = 50, blank=True, null=True)
    date_de_naissance        =    models.DateField(max_length = 50, null = True, blank = True)
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    update_date             =   models.DateTimeField(auto_now=True)
    #date_entree = models.DateTimeField(auto_now = True)


class Model_Condition_reglement(models.Model):
    designation             =   models.CharField(max_length = 250, null = True, blank=True, default = '')
    nombre_jour             =   models.IntegerField()
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    update_date             =   models.DateTimeField(auto_now=True)
    creation_date           =   models.DateTimeField(auto_now_add = True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_condition_reglement", null = True, blank = True)
    url                     =   models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation


class Model_Bon_commande(models.Model):
    numero_commande         =    models.CharField(max_length = 100, null = True, blank=True, default = '')
    date_prevue             =    models.DateTimeField(default = timezone.now, blank=True, null=True)
    date_commande           =    models.DateTimeField(blank=True, null=True)
    montant_total           =    models.FloatField(blank=True, null=True)
    devise                  =    models.ForeignKey(Model_Devise,on_delete = models.SET_NULL,  related_name="bon_commandes_devises", null = True, blank = True)
    est_realisee            =    models.BooleanField(default = False)
    reference_document      =    models.CharField(max_length = 300, null = True, blank=True, default = '')
    document                =    models.ForeignKey(Model_Document,on_delete = models.SET_NULL, related_name="document_bon_commande", null = True, blank = True)
    client                  =    models.ForeignKey(Model_Client,on_delete = models.SET_NULL, related_name="client_bon_reception", null = True, blank = True)
    condition_reglement     =    models.ForeignKey("Model_ConditionReglement", on_delete=models.SET_NULL, related_name="conditions_reglement_commande", blank=True, null=True)
    externe_id              =    models.IntegerField(null=True, blank=True)
    statut                  =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True, related_name="statut_bon_commnde")
    etat                    =    models.CharField(max_length=300, blank=True, null=True)
    auteur                  =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_bon_commande", null = True, blank = True)
    url                     =    models.CharField(max_length = 250, blank=True, null=True)
    update_date             =    models.DateTimeField(auto_now=True)
    creation_date           =    models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.numero_commande

    @property
    def prix_total(self):
        total = 0

        items = Model_Ligne_commande.objects.filter(order_id = self.id)
        for item in items :
            if item.prix_unitaire != None and item.prix_unitaire != 0 :
                quantite = item.quantite_demandee
                if self.est_realisee == True :
                    quantite = item.quantite_fournie
                total = total + (item.prix_unitaire * quantite)
            elif item.prix_lot != None and item.prix_lot != 0 :
                total = total + item.prix_lot
        return "%.2f" % total

    @property
    def nbre_lignes(self):
        nb_lignes = 0
        nbres = Model_Ligne_commande.objects.filter(order_id = self.id).count()
        if nbres:
            nb_lignes = nbres
        return "%.2f" % nb_lignes

    @property
    def quantite_total(self):
        total = 0

        items = Model_Ligne_commande.objects.filter(order_id = self.id)
        for item in items :
            if item.quantite_demandee != None and item.quantite_demandee != 0 :
                quantite = item.quantite_demandee
                if self.est_realisee == True :
                    quantite = item.quantite_fournie
                total = total + quantite
        return "%.2f" % total

    @property
    def statut_vente(self):
        art_demandes = 0.0
        art_fournie = 0.0

        art_demandes = Model_Ligne_commande.objects.filter(bon_commande_id = self.id).aggregate(demandes=Sum('quantite_demandee'))
        art_fournie =  Model_Ligne_commande.objects.filter(bon_commande_id = self.id).aggregate(fournies=Sum('quantite_fournie'))

        #Les deux valeures doivent etre differentes de none pour que le calcul s effectue
        #print(art_demandes["demandes"] != None)
        #print(art_fournie["fournies"] != None)

        if art_demandes["demandes"] != None and art_fournie["fournies"] != None :
            if float(art_fournie["fournies"]) == float(0.0) :

                if self.status == 1:
                    return "Créé, en attente de validation"
                else:
                    return "Envoyé au client"
            elif float(art_demandes["demandes"]) > float(art_fournie["fournies"]):
                return "Livré Partiellement"
            else : return "Livré Totalement"



    @property
    def est_modifiable(self):
        items = Model_Ligne_commande.objects.filter(bon_commande_id = self.id)
        for item in items :
            if item.quantite_fournie != 0 :
                return False
        return True

    @property
    def etat_facturation(self):
        #if self.est_realisee == False : return "Rien à facturer"

        nombre_factures = Model_Facture.objects.filter(bon_commande_id = self.id).count()
        if nombre_factures == 0 :
            return "En attente de facture"
        elif nombre_factures == 1 :

            #items =

            total_paie = 0.00
            factures = Model_Facture.objects.filter(bon_commande_id = self.id)
            for facture in factures :
                total_paie = total_paie + facture.montant
            prix_total = float(self.prix_total)

            if total_paie >= prix_total :
                return "Facture reçue soldée"
            else:
                return "Facture reçue non soldée"


    @property
    def status_paiement(self):

        total_paie = 0.00
        factures = Model_Facture.objects.filter(bon_commande_id = self.id)
        for facture in factures :
            total_paie = total_paie + facture.montant
        prix_total = float(self.prix_total)

        if total_paie >= prix_total :
            return "Bon Soldé"
        else:
            return "Bon non Soldé"

    @property
    def est_facturable(self):
        if self.est_modifiable == True : return False

        total_facture = 0.00
        factures = Model_Facture.objects.filter(bon_commande_id = self.id)
        for facture in factures :
            total_facture = total_facture + facture.montant
        prix_total = float(self.prix_total)
        if total_facture >= prix_total : return False
        else: return True

class Model_Ligne_commande(models.Model):
    quantite_demandee       =   models.IntegerField()
    quantite_fournie        =   models.IntegerField()
    prix_unitaire           =   models.FloatField()
    prix_lot                =   models.FloatField()
    creation_date           =   models.DateTimeField(auto_now_add = True)
    type                    =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    bon_commande            =   models.ForeignKey(Model_Bon_commande,on_delete = models.SET_NULL, related_name="ligne_of_bon_commande", null = True, blank = True)
    stock_article           =   models.ForeignKey("Model_StockArticle", on_delete = models.SET_NULL, related_name="ligne_commande_take_on_stock_article", null = True, blank = True)
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    update_date             =   models.DateTimeField(auto_now=True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_ligne_commande", null = True, blank = True)
    url                     =   models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.quantite_demandee

class Model_Bon_livraison(models.Model):
    numero_livraison        =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    date_livraison          =   models.DateTimeField(auto_now = True)
    creation_date           =   models.DateTimeField(auto_now_add = True)
    quantite_demandee       =   models.IntegerField()
    quantite_recue          =   models.IntegerField()
    bon_commande            =   models.ForeignKey(Model_Bon_commande,on_delete = models.SET_NULL, related_name="bon_livraison_of_bon_commande", null = True, blank = True)
    document                =   models.ForeignKey(Model_Document,on_delete = models.SET_NULL, related_name="document_of_bon_livraison", null = True, blank = True)
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    update_date             =   models.DateTimeField(auto_now=True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_bon_livraison", null = True, blank = True)
    url                     =   models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.numero_livraison



class Model_ConditionReglement(models.Model):
    designation             =   models.CharField(max_length = 20)
    nombre_jours            =   models.IntegerField()
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    update_date             =   models.DateTimeField(auto_now=True)
    creation_date           =   models.DateTimeField(auto_now_add=True)
    auteur                  =   models.ForeignKey(Model_Personne, related_name="confitions_reglement",on_delete=models.SET_NULL ,null = True, blank = True)
    url                     =   models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation


class Model_StockArticle(models.Model):
    article                    =    models.ForeignKey(Model_Article, on_delete=models.CASCADE, related_name="stocks")
    quantite_disponible        =    models.FloatField()
    emplacement                =    models.ForeignKey(Model_Emplacement, null = True, blank = True,related_name="emplacement_of_lks", on_delete=models.SET_NULL)
    auteur                     =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_stock_article", null = True, blank = True)
    statut                     =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                       =    models.CharField(max_length=50, blank=True, null=True)
    update_date                =    models.DateTimeField(auto_now=True)
    creation_date              =    models.DateTimeField(auto_now_add = True)
    url                        =    models.CharField(max_length = 250, blank=True, null=True)
    #transformation_source     =    models.ForeignKey(Model_Order, null = True, blank = True, on_delete=models.SET_NULL, related_name="stocks_resultants")

    def __str__(self):
        return self.emplacement.designation + " / " + self.article.designation


    def series_emplacement(self):
        return Model_Asset.objects.filter(article_id = self.article.id, emplacement_id=self.emplacement.id)


class Model_Etat_Facturation(models.Model):
    numero_etat_facturation =   models.CharField(max_length = 50, blank=True, null=True)
    description             =   models.CharField(max_length = 250, blank=True, null=True)
    date_etat               =   models.DateTimeField(blank=True, null=True)
    document                =   models.ForeignKey(Model_Document,on_delete = models.SET_NULL, related_name="document_etat_facturation", null = True, blank = True)
    etat                    =   models.CharField(max_length = 50)
    est_facture             =   models.BooleanField(default = False)
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True, related_name="statut_etat_facturation")
    update_date             =   models.DateTimeField(auto_now=True)
    creation_date           =   models.DateTimeField(auto_now_add = True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_etat_facturation", null = True, blank = True)

    def __str__(self):
        return self.numero_etat_facturation


#MODULE RH DEMANDE ET LIGNE DEMANDE

class Model_Requete_demande(models.Model):
    designation             =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    type_requete            =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    description             =   models.CharField(max_length = 250, null = True, blank=True, default = '')
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    update_date             =   models.DateTimeField(auto_now=True)
    creation_date           =   models.DateTimeField(auto_now_add = True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_of_requete_demande", null = True, blank = True)
    url                     =   models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation

# Bon Speciale --- Demande Mr Thomas -----
class Model_Bon(models.Model):
    numero                  =    models.CharField(max_length = 20)
    date_prevue             =    models.DateTimeField(null = True, blank = True)
    date_realisation        =    models.DateTimeField(null = True, blank = True)
    est_realisee            =    models.BooleanField(default = True)
    devise                  =    models.ForeignKey(Model_Devise, null= True, blank=True, on_delete=models.SET_NULL)
    inventoriste            =    models.ForeignKey(Model_Employe, related_name="bons_inventoristes", null= True, blank=True, on_delete=models.SET_NULL)
    #fournisseur            =    models.ForeignKey(Model_Personne, related_name="bons_inventoristes", null= True, blank=True, on_delete=models.SET_NULL)
    quantite_voulue         =    models.FloatField(default=0)
    quantite_obtenue        =    models.FloatField(default=0)
    est_reserve             =    models.BooleanField(default = False)
    reference_document      =    models.CharField(max_length = 200)
    description             =    models.TextField(null= True, blank=True)
    type                    =    models.CharField(max_length = 50)
    creation_date           =    models.DateTimeField(auto_now_add=True)
    bon_commande            =    models.ForeignKey(Model_Bon_commande, on_delete=models.SET_NULL, null = True, blank = True, related_name="bons_commande_of_bon")
    bon_reception           =    models.ForeignKey(Model_Bon_reception, on_delete=models.SET_NULL, null = True, blank = True, related_name="bons_reception_of_bon")
    bon_transfert           =    models.ForeignKey(Model_Bon_transfert, on_delete=models.SET_NULL, null = True, blank = True, related_name="bons_transfert_of_bon")
    statut                  =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True, related_name="statut_bon")
    etat                    =    models.CharField(max_length=300, blank=True, null=True)
    update_date             =    models.DateTimeField(auto_now=True)
    taux                    =    models.ForeignKey(Model_Taux, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    auteur                  =    models.ForeignKey(Model_Personne, related_name="bons_auteurs", on_delete=models.SET_NULL, null = True, blank = True)
    url                     =    models.CharField(max_length = 250, blank=True, null=True)



class Model_ItemBon(models.Model):
    bon                     =    models.ForeignKey(Model_Bon, related_name="itembons", on_delete=models.SET_NULL, null = True, blank = True)
    article                 =    models.ForeignKey(Model_Article, on_delete = models.SET_NULL, related_name="article_of_item_bon", null = True, blank = True)
    quantite_demandee       =    models.FloatField(default=0)
    quantite_fournie        =    models.FloatField(default=0)
    unite                   =    models.CharField(max_length = 50,null = True, blank = True)
    prix_unitaire           =    models.FloatField(null = True, blank = True)
    prix_lot                =    models.FloatField(null = True, blank = True)
    type                    =    models.CharField(max_length = 50)
    statut                  =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =    models.CharField(max_length=50, blank=True, null=True)
    update_date             =    models.DateTimeField(auto_now=True)
    creation_date           =    models.DateTimeField(auto_now_add=True)
    auteur                  =    models.ForeignKey(Model_Personne, related_name="auteur_itembons", on_delete=models.SET_NULL, null = True, blank = True)
    url                     =    models.CharField(max_length = 250, blank=True, null=True)


    @property
    def nom_article(self):
        try:
            return self.article.designation
        except:
            return ""
    @property
    def unite_article(self):
        try:
            return self.article.unite.symbole_unite
        except:
            return ""

# MODEL WORKFLOW

class Model_Wkf_Workflow(models.Model):
    type_document           =    models.CharField(max_length=30, unique=True)
    content_type            =    models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    update_date             =   models.DateTimeField(auto_now=True)
    creation_date           =   models.DateTimeField(auto_now_add = True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_wkfs', null = True, blank = True)

    def __str__(self):
        return self.type_document

class Model_Wkf_Etape(models.Model):
    designation             =    models.CharField(max_length=50)
    label                   =    models.CharField(max_length=50, blank=True, null=True)
    workflow                =    models.ForeignKey(Model_Wkf_Workflow, on_delete=models.CASCADE, related_name="etapes_workflows")
    est_initiale            =    models.BooleanField(default=False)
    est_succes              =    models.BooleanField(default=False)
    est_echec               =    models.BooleanField(default = False)
    num_ordre               =    models.IntegerField(blank=True, null=True)
    update_date             =    models.DateTimeField(auto_now=True)
    creation_date           =    models.DateTimeField(auto_now_add = True)
    auteur                  =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_wkf_etapes', null = True, blank = True)


    def __str__(self):
        return self.workflow.type_document +' / '+ self.designation

    def etat_initial(self):
        if self.est_initiale == True : return "Initiale"
        else : return "Non initiale"

class Model_Wkf_Condition(models.Model):
    designation             =    models.CharField(max_length=50)
    update_date             =   models.DateTimeField(auto_now=True)
    creation_date           =   models.DateTimeField(auto_now_add = True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_wkf_conditions', null = True, blank = True)

    def __str__(self):
        return self.designation

class Model_Wkf_Transition(models.Model):
    etape_source            =    models.ForeignKey(Model_Wkf_Etape, on_delete=models.CASCADE, related_name="transitions_etapes_source")
    etape_destination       =    models.ForeignKey(Model_Wkf_Etape, on_delete=models.CASCADE, related_name="transitions_etapes_destination")
    role_utilisateur        =    models.ForeignKey(Model_Role, on_delete=models.SET_NULL, blank=True, null=True ,related_name="roles_transitions")
    groupe_permission       =    models.ForeignKey(Model_GroupePermission, on_delete=models.SET_NULL, blank=True, null=True ,related_name="transition_groupe_permission")
    unite_fonctionnelle     =    models.ForeignKey("Model_Unite_fonctionnelle", blank=True, null=True, on_delete = models.SET_NULL, default=None, related_name="unite_fonctionnelle_of_transition")
    condition               =    models.ForeignKey(Model_Wkf_Condition, on_delete=models.SET_NULL, blank=True, null=True , related_name="conditions_transitions")
    url                     =    models.CharField(max_length = 250, blank=True, null=True)
    operateur               =    models.IntegerField(choices = TypeOperateur, default=1) #Dans le cas de plusieurs transitions, ca peut avoir son importance
    traitement              =    models.CharField(max_length=250, blank=True, null=True)
    est_decisive            =    models.BooleanField(default = False)
    est_configurable        =    models.BooleanField(default = False)
    est_delegable           =    models.BooleanField(default=False)
    est_filtrable           =    models.BooleanField(default = False)
    est_generate_doc        =    models.BooleanField(default = False) #Action generer document
    filtre                  =    models.CharField(max_length=50, blank=True, null=True)#Champ Utilisable dans le cas ou la condition est GenerateDoc
    update_date             =    models.DateTimeField(auto_now=True)
    creation_date           =    models.DateTimeField(auto_now_add = True)
    auteur                  =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_wkf_transitions', null = True, blank = True)


    def __str__(self):
        return self.etape_source.workflow.type_document + ': ' + self.etape_source.designation + ' > ' + self.etape_destination.designation

    def value_operateur(self):
        return dict(TypeOperateur)[int(self.operateur)]

    @property
    def transitions_suivantes(self):
        return Model_Wkf_Transition.objects.filter(etape_source = self.etape_destination)






class Model_Wkf_Stakeholder(models.Model):
    '''Modèle utilisé si et seulement si la transition est configurable ou delegable, Ca permet à l'utilisateur de fixer la suite du traitement'''
    transition              =    models.ForeignKey(Model_Wkf_Transition, on_delete=models.CASCADE, related_name="transitions_stakeholder")
    content_type            =    models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    document_id             =    models.PositiveIntegerField(blank=True, null=True)
    #condition              =    models.ForeignKey(Model_Wkf_Condition, on_delete=models.SET_NULL, blank=True, null=True) #A utiliser si l'utilisaeur peut mm rédéfinir l'action
    employes                =    models.ManyToManyField("Model_Employe", related_name="destinataires")
    carbon_copies           =    models.ManyToManyField("Model_Employe", related_name="copie_information")
    est_delegation          =    models.BooleanField(default= False)
    comments                =    models.CharField(max_length=500, blank=True, null=True)
    url_detail              =    models.CharField(max_length=100, blank=True, null=True) # Usefull for Notification
    module_source           =    models.CharField(max_length= 100, blank=True, null=True) # Usefull for Notification
    created_at              =   models.DateTimeField(auto_now_add = True)
    updated_at               =   models.DateTimeField(auto_now = True)
    auteur                  =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_wkf_stakeholder', null = True, blank = True)

class Model_Wkf_Historique(models.Model):
    employe                 =    models.ForeignKey(Model_Employe,on_delete=models.SET_NULL, related_name="workflow_utilisateurs", blank=True, null=True)
    etape                   =    models.ForeignKey(Model_Wkf_Etape,on_delete=models.SET_NULL, related_name="workflow_etapes",null = True, blank = True)
    timestamp               =    models.DateTimeField(auto_now_add=True)
    content_type            =    models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    document_id             =    models.PositiveIntegerField(blank=True, null=True)
    content_object          =    GenericForeignKey('content_type', 'document_id')
    notes                   =    models.CharField(max_length=500, blank=True, null=True)
    update_date             =    models.DateTimeField(auto_now=True)
    creation_date           =    models.DateTimeField(auto_now_add = True)
    auteur                  =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_wkf_historiques', null = True, blank = True)

    def __str__(self):
        return self.etape.designation

class Model_Wkf_Approbation(models.Model):
    designation             =   models.CharField(max_length = 500)
    transition              =   models.ForeignKey(Model_Wkf_Transition, on_delete=models.SET_NULL, blank=True, null=True ,related_name="approbations")
    update_date             =   models.DateTimeField(auto_now=True)
    creation_date           =   models.DateTimeField(auto_now_add = True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_wkf_appros', null = True, blank = True)

    def __str__(self):
        return self.designation

# MODULE BUDGET
class Model_Categoriebudget(models.Model):
    designation             =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    description             =   models.CharField(max_length = 250, null = True, blank=True, default = '')
    type                    =   models.IntegerField(choices = TypeBudget, default=2)
    created_at              =   models.DateTimeField(auto_now_add = True)
    update_at               =   models.DateTimeField(auto_now = True)
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_categoriebudget_zyd', null = True, blank = True)

    def __str__(self):
        return self.designation

    @property
    def solde(self):
        "Somme des valeurs soldes des budget de cette catégorie"
        try:
            montant = 0
            budgets = Model_Budget.objects.filter(categoriebudget = self)
            for item in budgets:
                montant += item.solde
            return montant
        except Exception as e:
            return 0
    @property
    def montant_alloue(self):
        "Somme des montant alloué de tous les budgets de cette catégorie"
        try:
            budgets = Model_Budget.objects.filter(categoriebudget = self)
            montant = 0
            for ligne in budgets:
                montant += ligne.montant_alloue
            return montant
        except Exception as e:
            return 0

    @property
    def devise_montant(self):
        "La Devise de somme des montant alloué de tous les budgets de cette catégorie"
        try:
            budgets = Model_Budget.objects.filter(categoriebudget = self).first()
            devise = budgets.devise.symbole_devise
            return devise
        except Exception as e:
            return 'CFA'

class Model_Exercicebudgetaire(models.Model):
    designation             =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    montant                 =   models.FloatField()
    devise                  =   models.ForeignKey(Model_Devise, on_delete = models.SET_NULL, related_name = 'devise_of_exercice_budgetaire', blank=True, null=True)
    annee                   =   models.IntegerField()
    is_active               =   models.BooleanField(default = False)
    is_cloture              =   models.BooleanField(default = False)
    date_debut              =   models.DateTimeField(blank=True, null=True)
    date_fin                =   models.DateTimeField(blank=True, null=True)
    created_at              =   models.DateTimeField()
    update_at               =   models.DateTimeField(auto_now = True)
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_exercicebudgetaire_jts', null = True, blank = True)

    def __str__(self):
        return self.designation
    @property
    def separateur_montant(self):
        return AfficheEntier(float(self.montant))

    @property
    def montant_alloue_exercice(self):
        "Montant alloué à un exercice budgétaire"
        try:
            montant_alloue_exercice = 0
            transactions = Model_Transactionbudgetaire.objects.filter(exercice_budgetaire = self).filter(typetransactionbudgetaire=4)
            for transaction in transactions:
                montant_alloue_exercice += transaction.montant
            return montant_alloue_exercice
        except Exception as e:
            return 0



class Model_Budget(models.Model):
    designation             =    models.CharField(max_length=50)
    categoriebudget         =    models.ForeignKey("Model_Categoriebudget", on_delete = models.SET_NULL, related_name = 'categoriebudget_fk_jkw', null = True, blank = True)
    #annee                  =    models.IntegerField()
    #solde                  =    models.FloatField(default=0)
    devise                  =    models.ForeignKey(Model_Devise, on_delete = models.SET_NULL, related_name = 'devise_fk_jut', null = True, blank = True)
    url                     =    models.CharField(max_length = 250, blank=True, null=True)
    #exericebudgetaires     =    models.ManyToManyField("Model_Exercicebudgetaire")
    statut                  =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =    models.CharField(max_length=50, blank=True, null=True)
    update_date             =    models.DateTimeField(auto_now=True)
    creation_date           =    models.DateTimeField(auto_now_add = True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_budgets', null = True, blank = True)

    def __str__(self):
        return self.designation

    @property
    def montant_alloue(self):
        "Somme des montant alloué de toutes les lignes de ce budget"
        try:
            lignes = Model_LigneBudgetaire.objects.filter(budget = self)
            montant_alloue = 0
            for ligne in lignes:
                montant_alloue += ligne.montant_alloue
            return montant_alloue
        except Exception as e:
            return 0

    @property
    def separateur_montant_alloue(self):
        return AfficheEntier(float(self.montant_alloue))

    @property
    def solde(self):
        "Solde Ou Montant disponible: Somme de tous les soldes des lignes"
        try:
            lignes = Model_LigneBudgetaire.objects.filter(budget = self)
            # print('***Lignes BUDGET****', lignes)
            solde = 0
            for ligne in lignes:
                solde += float(ligne.valeur_solde)
            # print('***SOLDE BUDGET', solde)
            return solde
        except Exception as e:
            # print('***ERREUR SOLDE', e)
            return 0

    @property
    def separateur_solde(self):
        return AfficheEntier(float(self.solde))

    @property
    def montant_consomme(self):
        "Valeur consommée: Sommede toutes les valeurs consommées des lignes"
        montant = 0
        try:
            lignes = Model_LigneBudgetaire.objects.filter(budget = self)
            for ligne in lignes:
                montant = montant + ligne.valeur_total_consommee
            return montant
        except Exception as e:
            #print('Erreur valeur montant: {}'.format(e))
            return montant
    @property
    def separateur_montant_consomme(self):
        return AfficheEntier(float(self.montant_consomme))



    @property
    def montant_engage(self):
        montant = 0
        try:
            lignes = Model_LigneBudgetaire.objects.filter(budget = self)
            for ligne in lignes:
                montant = montant + float(ligne.valeur_engagement)
            return montant
        except Exception as e:
            return montant

    @property
    def montant_reel(self):
        montant = 0
        try:
            lignes = Model_LigneBudgetaire.objects.filter(budget = self)
            for ligne in lignes:
                montant = montant + ligne.valeur_reel
            return montant
        except Exception as e:
            return montant

    @property
    def montant_rallonge(self):
        montant = 0
        try:
            lignes = Model_LigneBudgetaire.objects.filter(budget = self)
            for ligne in lignes:
                montant = montant + ligne.valeur_rallonge
            return montant
        except Exception as e:
            return montant

    @property
    def montant_diminution(self):
        montant = 0
        try:
            lignes = Model_LigneBudgetaire.objects.filter(budget = self)
            for ligne in lignes:
                montant = montant + ligne.valeur_diminution
            return montant
        except Exception as e:
            return montant

    @property
    def montant_ajuste(self):
        montant = 0
        try:
            self.montant_rallonge - self.montant_diminution
        except Exception as e:
            return montant



class Model_LigneBudgetaire(models.Model):
    code                    =   models.CharField(max_length = 50)
    entite                  =   models.CharField(max_length=1, default="1", blank=True, null=True)
    unite_fonctionnelle     =   models.ForeignKey("Model_Unite_fonctionnelle", blank=True, null=True, on_delete = models.SET_NULL, default=None, related_name="budgets")
    compte                  =   models.OneToOneField("Model_Compte", blank= True, null = True, on_delete=models.SET_NULL)
    #poste_budgetaire        =   models.ForeignKey("Model_Poste_budgetaire", on_delete=models.SET_NULL, related_name="compte_fk",null = True, blank = True)
    nature_activite         =   models.IntegerField(choices = natureActivite, default=0,null = True, blank = True)
    centre_cout             =   models.ForeignKey("Model_Centre_cout", on_delete=models.SET_NULL, related_name="centre_cout_of_ligne",null = True, blank = True)
    activite                =   models.ForeignKey("Model_Activite", on_delete=models.SET_NULL, related_name="activite_fk",null = True, blank = True)
    nature_charge           =   models.IntegerField(choices = natureCharge, default=0, blank=True, null=True)
    localite                =   models.IntegerField(choices = localite, default=0,null = True, blank = True)
    responsable             =   models.ForeignKey(Model_Employe, on_delete=models.CASCADE, related_name="budgets_lignes", blank=True, null=True)
    designation             =   models.CharField(max_length = 50)
    type                    =   models.IntegerField(choices = TypeCombinaison, default=1,null = True, blank = True)
    budget                  =   models.ForeignKey(Model_Budget, on_delete=models.CASCADE, related_name="budgets_lignes_kg", blank=True, null=True)
    url                     =   models.CharField(max_length = 250, blank=True, null=True)
    status                  =   models.IntegerField(choices = natureLigneBgt, default=0)
    pourcentage_alert       =   models.FloatField(default=0)
    message_alert           =   models.CharField(max_length = 500, blank=True, null=True)
    is_alerted              =   models.BooleanField(default = False)
    is_reportable           =   models.BooleanField(default = True)
    is_bloqued              =   models.BooleanField(default = False)
    is_waiting_confirmation =   models.BooleanField(default = False) #Booleen double confirmation of is bloqued
    user_confirmation       =   models.ForeignKey("Model_Employe", on_delete=models.SET_NULL, blank=True, null=True) #User of confirmation
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    update_date             =   models.DateTimeField(auto_now=True)
    creation_date           =   models.DateTimeField(auto_now_add = True)
    correspondant           =   models.ManyToManyField(Model_Personne,related_name="correspondants_lignes_bgt")
    auteur                  =   models.ForeignKey(Model_Personne, related_name="auteu_ligne_budgetaire", null = True, blank = True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.designation


    @property
    def montant_alloue(self):
        '''Budget reajusté ou Montant alloue = Dotation + Rallonge - Diminution
        Note: Les rallonges et diminutions prises en compte sont celles où le statut via le workflow est success (complete)
        On parle de prévision dans le cas de budget de type recette'''
        try:
            montant_alloue = 0
            transactions = Model_Transactionbudgetaire.objects.filter(ligne_budgetaire = self).filter(Q(typetransactionbudgetaire=2, statut__est_succes = True) | Q(typetransactionbudgetaire=4)).filter(exercice_budgetaire__is_active = True)
            for transaction in transactions:
                montant_alloue += transaction.montant
            transactions = Model_Transactionbudgetaire.objects.filter(ligne_budgetaire = self).filter(typetransactionbudgetaire=3, statut__est_succes = True).filter(exercice_budgetaire__is_active = True)
            for transaction in transactions:
                montant_alloue -= transaction.montant
            return montant_alloue
        except Exception as e:
            return 0
    @property
    def montant_disponible_reporter(self):
        "Ici On trouve le dernier montant disponible de l\'exerciece passe"
        try:
            montant_dispo = 0
            montant_alloue = 0
            exercice = Model_Exercicebudgetaire.objects.order_by('-id')[:2]
            exerciceid = exercice[1].id
            #MONTANT ALLOUE
            transactions = Model_Transactionbudgetaire.objects.filter(ligne_budgetaire = self).filter(Q(typetransactionbudgetaire=2, statut__est_succes = True) | Q(typetransactionbudgetaire=4)).filter(exercice_budgetaire__id = exerciceid)
            for transaction in transactions:
                montant_alloue += transaction.montant
            transactions = Model_Transactionbudgetaire.objects.filter(ligne_budgetaire = self).filter(typetransactionbudgetaire=3, statut__est_succes = True).filter(exercice_budgetaire__id = exerciceid)
            for transaction in transactions:
                montant_alloue -= transaction.montant
            #MONTANT ENGAGEMENT
            montant_eng = 0
            transactions = Model_Transactionbudgetaire.objects.filter(ligne_budgetaire = self.id , exercice_budgetaire__id = exerciceid, typetransactionbudgetaire = 1).filter(Q(status=0) | Q(status=1)).aggregate(engagement=Sum('montant'))
            if transactions["engagement"]:
                montant_eng = transactions["engagement"]

            #MONTANT REEL
            montant_reel = 0
            transactions = Model_Transactionbudgetaire.objects.filter(ligne_budgetaire = self.id ,status=2, exercice_budgetaire__id = exerciceid, typetransactionbudgetaire = 1).aggregate(reel=Sum('montant'))
            if transactions["reel"]:
                montant_reel = transactions["reel"]

            #CALCUL TOTAL CONSOMME
            total_comm = 0
            if montant_eng > montant_reel:
                total_comm = montant_eng
            else:
                total_comm = montant_reel

            #CALCUL SOLDE FINAL
            montant_dispo = float(montant_alloue) - float(total_comm)
            return montant_dispo
        except Exception as e:
            # print('ERREUR DISPO', e)
            return 0.0

    @property
    def montant_dotation(self):
        "Montant de la dotation à l'ouverture de l'exercice budgétaire"
        try:
            montant_dotation = 0
            transactions = Model_Transactionbudgetaire.objects.filter(ligne_budgetaire = self).filter(typetransactionbudgetaire=4).filter(exercice_budgetaire__is_active = True)
            for transaction in transactions:
                montant_dotation += transaction.montant
            return montant_dotation
        except Exception as e:
            return 0

    @property
    def separateur_montant_alloue(self):
        return AfficheEntier(float(self.montant_alloue))


    @property
    def valeur_engagement(self):
        '''Montant engagé via les bons de commandes . Il s'agit des transactions de type 1 (normal) ayant comme status 0 ou 1(Généré ou En cours).'''
        montant = 0
        try:
            transactions = Model_Transactionbudgetaire.objects.filter(ligne_budgetaire = self.id , exercice_budgetaire__is_active = True, typetransactionbudgetaire = 1).filter(Q(status=0) | Q(status=1)).aggregate(engagement=Sum('montant'))
            if transactions["engagement"]:
                montant = transactions["engagement"]
            return "%.2f" % montant
        except Exception as e:
            #print('Erreur valeur_engagement(): {}'.format(e))
            return "%.2f" % montant
    @property
    def separateur_valeur_engagement(self):
        return AfficheEntier(float(self.valeur_engagement))


    @property
    def valeur_reel(self):
        "Montant réalisé via les factures. Il s'agit des transactions ayant comme statut 2 (Traité) et comme type de transaction 1(normal)"
        montant = 0
        try:
            transactions = Model_Transactionbudgetaire.objects.filter(ligne_budgetaire = self.id ,status=2, exercice_budgetaire__is_active = True, typetransactionbudgetaire = 1).aggregate(reel=Sum('montant'))
            if transactions["reel"]:
                montant = transactions["reel"]
            return "%.2f" % montant
        except Exception as e:
            #print('Erreur valeur_reel(): {}'.format(e))
            return "%.2f" % montant

    @property
    def valeur_ecriture_reel(self):
        "Suivi Analytique de la consommation de la ligne budgétaire"
        montant = 0
        try:
            ecritures = Model_Ecriture_analytique.objects.filter(ligne_budgetaire_id = self.id).aggregate(reel=Sum('montant'))
            if ecritures["reel"]:
                montant = ecritures["reel"]
            return "%.2f" % montant
        except Exception as e:
            #print('Erreur valeur_ecriture_reel(): {}'.format(e))
            return "%.2f" % montant
    @property
    def valeur_ecriture_pourcentage(self):
        "Valeur écriture réel en pourcentage par rapport au montant alloué"
        valeur = 0
        try:
            valeur = 100 * float (self.valeur_ecriture_reel) / float (self.montant_alloue)
            return  "%.2f" % valeur
        except Exception as e:
            ##print('Erreur valeur_pourcentage(): {}'.format(e))
            return "%.2f" % valeur


    @property
    def separateur_valeur_reel(self):
        return AfficheEntier(float(self.valeur_reel))


    @property
    def valeur_total_consommee(self):
        "Valeur consommée de la ligne budgétaire = valeur engagement si Engagement > réel sinon, il vaut le réel"
        montant = 0
        try:
            if self.valeur_engagement > self.valeur_reel:
                return self.valeur_engagement
            else:
                return self.valeur_reel
        except Exception as e:
            # print("Buuuuuuuuuug", e)
            return 0

    @property
    def separateur_valeur_total_consommee(self):
        return AfficheEntier(float(self.valeur_total_consommee))



    @property
    def valeur_solde(self):
        '''Solde Ou Montant disponible  = Montant Alloué (Budget reajusté càd Dotation + Rallonge - Diminution) - Valeur Consommé (valeur engagement si engagement > reel sinon valeur reelle
        On parle de Ecart dans le budget de type recette'''
        montant = 0
        try:
            montant = float(self.montant_alloue) - float(self.valeur_total_consommee)
            # print('******VALEUR SOLDE CHAQUE LIGNE', "%.2f" % montant)
            return "%.2f" % montant
        except Exception as e:
            # print('Erreur valeur_solde(): {}'.format(e))
            return "%.2f" % montant
    @property
    def separateur_valeur_solde(self):
        return float(self.valeur_solde)

    @property
    def valeur_pourcentage(self):
        """Pourcentage de consommation d'une ligne budgétaire"""
        valeur = 0
        try:
            if self.montant_alloue > 0:
                valeur = 100 * float (self.valeur_total_consommee) / float (self.montant_alloue)
            return  "%.2f" % valeur
        except Exception as e:
            #print('Erreur valeur_pourcentage(): {}'.format(e))
            return "%.2f" % valeur
    @property
    def separateur_valeur_pourcentage(self):
        return AfficheEntier(float(self.valeur_pourcentage))


    @property
    def valeur_rallonge(self):
        "Reajustement budgétaire positif. Il s'agit des transactions ayant comme statut 2 (Traité) et comme type de transaction 2(Rallonge)"
        montant = 0
        try:
            transactions = Model_Transactionbudgetaire.objects.filter(ligne_budgetaire = self.id , status=2, exercice_budgetaire__is_active = True, typetransactionbudgetaire=2, statut__est_succes = True).aggregate(montant_rallonge=Sum('montant'))
            if transactions["montant_rallonge"]:
                montant = transactions["montant_rallonge"]
            return "%.2f" % montant
        except Exception as e:
            #print('Erreur valeur_rallonge(): {}'.format(e))
            return "%.2f" % montant
    @property
    def separateur_valeur_rallonge(self):
        return AfficheEntier(float(self.valeur_rallonge))

    @property
    def valeur_diminution(self):
        "Reajustement budgétaire négatif. Il s'agit des transactions ayant comme statut 2 (Traité) et comme type de transaction 3(Rallonge)"
        montant = 0
        try:
            transactions = Model_Transactionbudgetaire.objects.filter(ligne_budgetaire = self.id , status=2, exercice_budgetaire__is_active = True, typetransactionbudgetaire=3, statut__est_succes = True).aggregate(montant_diminution=Sum('montant'))
            if transactions["montant_diminution"]:
                montant = transactions["montant_diminution"]
            return "%.2f" % montant
        except Exception as e:
            #print('Erreur valeur_diminution(): {}'.format(e))
            return "%.2f" % montant
    @property
    def separateur_valeur_diminution(self):
        return AfficheEntier(float(self.valeur_diminution))

    def value_localite(self):
        return dict(localite)[int(self.localite)]

    def value_nature_activite(self):
        return dict(natureActivite)[int(self.nature_activite)]

    def value_nature_charge(self):
        return dict(natureCharge)[int(self.nature_charge)]

    def bon_reception(self):
        trans =Model_Transactionbudgetaire.objects.filter(ligne_budgetaire=self.id)
        listBon = []
        for item in trans:
            bon = item.bon_reception_id
            if bon != None:
                BC = Model_Bon_reception.objects.get(pk=bon)
                # print(BC.numero_reception)
                listBon.append(BC.numero_reception)
        # print('Tableau bon', listBon)
        return listBon


class Model_Projet(models.Model):
    codeprojet              =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    designation             =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    description             =   models.CharField(max_length = 250, null = True, blank=True, default = '')
    categoriebudget         =   models.ForeignKey("Model_Categoriebudget", on_delete = models.SET_NULL, related_name = 'categoriebudget_fk_nch', null = True, blank = True)
    date_debut              =   models.DateTimeField()
    montant                 =   models.FloatField(default = 0.0)
    devise                  =   models.ForeignKey(Model_Devise, on_delete = models.SET_NULL, related_name = 'devise_fk_mxb', null = True, blank = True)
    solde                   =   models.FloatField(default = 0.0)
    pourcentage_alert       =   models.FloatField(default=0)
    message_alert           =   models.CharField(max_length = 500, blank=True, null=True)
    is_alerted              =   models.BooleanField(default = False)
    date_fin                =   models.DateTimeField()
    created_at              =   models.DateTimeField(auto_now_add=True)
    update_at               =   models.DateTimeField(auto_now = True)
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_projet_loc', null = True, blank = True)

    def __str__(self):
        return self.codeprojet

    @property
    def separateur_montant(self):
        return AfficheEntier(float(self.montant))


    @property
    def montant_non_utilise(self):
        montant = 0
        montant_non_utilise = 0
        try:
            lignes = Model_LigneBudgetaire.objects.filter(code_projet = self.id)
            for ligne in lignes:
                montant = montant + ligne.montant_alloue
            montant_non_utilise = self.montant - montant
            return montant_non_utilise
        except Exception as e:
            #print('Erreur valeur montant: {}'.format(e))
            return montant_non_utilise
    @property
    def separateur_montant_non_utilise(self):
        return AfficheEntier(float(self.montant_non_utilise))



    @property
    def montant_utilise(self):
        montant = 0
        try:
            lignes = Model_LigneBudgetaire.objects.filter(code_projet = self.id)
            for ligne in lignes:
                montant = montant + ligne.montant_alloue
            return montant
        except Exception as e:
            #print('Erreur valeur montant: {}'.format(e))
            return montant
    @property
    def separateur_montant_utilise(self):
        return AfficheEntier(float(self.montant_utilise))

#GREG
class Model_Transactionbudgetaire(models.Model):
    designation = models.CharField(max_length = 100, null = True, blank=True, default = '')
    montant = models.FloatField()
    description = models.CharField(max_length = 500, null = True, blank=True, default = '')
    devise = models.ForeignKey(Model_Devise, on_delete = models.SET_NULL, related_name = 'devise_fk_xaw', null = True, blank = True)
    ligne_budgetaire = models.ForeignKey("Model_LigneBudgetaire", on_delete = models.SET_NULL, related_name = 'ligne_on_transaction', null = True, blank = True)
    compte_comptable = models.ForeignKey(Model_Compte, on_delete=models.SET_NULL, related_name="compte_of_transaction", blank=True, null=True)
    typetransactionbudgetaire = models.IntegerField(choices=TypeTransactionBudgetaire, default = 1)
    status =    models.IntegerField(choices = statutOp, default=0)
    statut =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat   =   models.CharField(max_length=50, blank=True, null=True)
    bon_reception = models.ForeignKey(Model_Bon_reception, on_delete = models.SET_NULL, related_name = 'bon_reception_trans_bgt', null = True, blank = True)
    ordre_mission = models.ForeignKey("Model_Ordre_de_mission", on_delete = models.SET_NULL, related_name = 'ordre_mission_of_transaction', null = True, blank = True)
    facture =    models.ForeignKey(Model_Facture, on_delete = models.SET_NULL, related_name="facture_of_transaction_budgetaire", null = True, blank = True)
    exercice_budgetaire = models.ForeignKey(Model_Exercicebudgetaire, on_delete = models.CASCADE, related_name = "exerice_bdgt_of_transaction", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    update_at = models.DateTimeField(auto_now = True)
    employe = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'employe_de_model_transactionbudgetaire_gpj', null = True, blank = True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_transactionbudgetaire_gpj', null = True, blank = True)

    def __str__(self):
        return self.designation
    @property
    def separateur_montant(self):
        return AfficheEntier(float(self.montant))

    @property
    def valuEcart(self):
        try:
            if self.reel <= self.engagement:
                Ecart = self.ligne_budgetaire.montant_dotation - self.engagement
            elif self.reel > self.engagement:
                Ecart = int(self.ligne_budgetaire.montant_dotation - self.reel)
            return Ecart
        except Exception as e:
            print(e)
            return 0

    def value_type_transaction_budgetaire(self):
        return dict(TypeTransactionBudgetaire)[int(self.typetransactionbudgetaire)]



class Model_Typetransactionbudgetaire(models.Model):
    designation = models.CharField(max_length = 100, null = True, blank=True, default = '')
    created_at = models.DateTimeField(auto_now_add = True)
    update_at = models.DateTimeField(auto_now = True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_typetransactionbudgetaire_gaw', null = True, blank = True)

    def __str__(self):
        return self.designation

#CONVERSATION
class Model_Message(models.Model):
    objet                   =   models.CharField(max_length = 50, null = True, blank=True, default = '')
    corps                   =   models.CharField(max_length = 500, null = True, blank=True, default = '')
    type                    =   models.CharField(max_length = 50, null = True, blank=True, default = '')
    destinataire            =   models.ManyToManyField(Model_Employe)
    expediteur              =   models.ForeignKey(Model_Employe, on_delete = models.SET_NULL, related_name = 'expediteur_fk_ezk', null = True, blank = True)
    status                  =   models.CharField(max_length = 200, null = True, blank=True, default = '')
    document                =   models.ForeignKey(Model_Document, on_delete = models.SET_NULL, related_name = 'document_fk_odz', null = True, blank = True)
    created_at              =   models.DateTimeField(auto_now_add=True)
    update_at               =   models.DateTimeField(auto_now = True)
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_message_zam', null = True, blank = True)
    url                     =   models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.objet

    @property
    def hisexpediteur(self):
        cont = Model_Employe.objects.get(pk = self.expediteur_id)
        return cont.nom_complet

    @property
    def hisdocument(self):
        cont = Model_Document.objects.get(pk = self.document_id)
        return 'N° ' + cont.numero_document + '      -      ' + cont.url_document

class Model_Notification(models.Model):
    text                    =   models.CharField(max_length = 500, null = True, blank=True, default = '')
    url_piece_concernee     =   models.CharField(max_length = 300, null = True, blank=True, default = '')
    module_source           =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    created_at              =   models.DateTimeField(auto_now_add=True)
    update_at               =   models.DateTimeField(auto_now = True)
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_notification_dmj', null = True, blank = True)
    url                     =   models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.text

    @property
    def hismessageexpediteur(self):
        #print("allo")
        cont = Model_Message.objects.get(pk = self.auteur_id)
        return cont.hisexpediteur

class Model_Temp_Notification(models.Model):
    user                    =  models.ForeignKey(Model_Employe, on_delete = models.SET_NULL, related_name = 'user_fk_koy', null = True, blank = True)
    notification            =   models.ForeignKey(Model_Notification, on_delete = models.CASCADE, related_name='notif_fk_sk', null = True, blank = True)
    type_action             =   models.CharField(max_length = 50, null = True, blank=True, default = '')
    lien_action             =   models.CharField(max_length = 300, null = True, blank=True, default = '')
    source_identifiant      =   models.IntegerField(null=True,blank=True)
    est_lu                  =   models.BooleanField(default = False)
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    created_at              =   models.DateTimeField(auto_now_add=True)
    update_at               =   models.DateTimeField(auto_now = True)
    url                     =   models.CharField(max_length = 250, blank=True, null=True)
    auteur                  =   models.ForeignKey(Model_Personne, related_name="auteur_temp_notification", null = True, blank = True, on_delete=models.SET_NULL)


############ GESTION DE CONTRATS #############
class Model_Avis_appel_offre(models.Model):
    numero_reference        =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    numero_dossier          =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    designation_commission  =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    intitule                =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    nombre_lots             = models.IntegerField(default = 0)
    financement             =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    type_appel_offre        =   models.IntegerField(choices = TypeAppelOffre, default = 1)
    type_marche             = models.ForeignKey("Model_TypeMarche", on_delete = models.SET_NULL, related_name = 'type_marche_avis', null = True, blank = True)
    lieu_consultation       =   models.CharField(max_length = 500, null = True, blank=True, default = '')
    qualification           =   models.CharField(max_length = 1000, null = True, blank=True, default = '')
    conditions              =   models.CharField(max_length = 1000, null = True, blank=True, default = '')
    date_signature          =   models.DateTimeField(blank = True, null=True)
    lieu_depot              =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    date_depot              =   models.DateTimeField(blank = True, null=True)
    delai_engagement        =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    montant_commission      =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    montant                 =   models.FloatField(default = 0)
    fournisseur             = models.ForeignKey(Model_Fournisseur, on_delete = models.SET_NULL, related_name = 'fournisseur_fk_ao', null = True, blank = True)
    devise                  =   models.ForeignKey(Model_Devise, on_delete=models.SET_NULL, blank=True, null=True)
    desc                    =   models.CharField(max_length = 1000, null = True, blank=True, default = '')
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True, related_name="statut_expression_avis_appel_offre")
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    demande_achat           =   models.ForeignKey("Model_Demande_achat",on_delete = models.SET_NULL, related_name="avis_demande_bon_reception", null = True, blank = True)
    created_at              =   models.DateTimeField(auto_now_add=True)
    update_at               =   models.DateTimeField(auto_now = True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_avis_appel_offre_cqe', null = True, blank = True)

    def __str__(self):
        return self.numero_reference

#Complement RH
class Model_Categorie_employe(models.Model):
    categorie = models.ForeignKey("Model_CategorieRH", on_delete = models.SET_NULL, related_name = 'categorie_rh_fk', null = True, blank = True)
    echelon = models.ForeignKey("Model_EchelonRH", on_delete = models.SET_NULL, related_name = 'echellon_rh_fk', null = True, blank = True)
    salaire_base = models.FloatField()
    devise = models.ForeignKey(Model_Devise, on_delete = models.SET_NULL, related_name = 'devise_id_fk_mtj', null = True, blank = True)
    description = models.CharField(max_length = 250, null = True, blank=True, default = '')
    created_at = models.DateTimeField()
    update_at = models.DateTimeField(auto_now = True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_categorie_employe_gbm', null = True, blank = True)
    def __str__(self):
        return self.label
    @property
    def separateur_salaire_base(self):
        return AfficheEntier(float(self.salaire_base))

    @property
    def label(self):
        try:
            echelon_label = ""
            categorie_label = self.categorie.designation.replace("'", "P")
            if len(self.echelon.designation) == 1:
                echelon_label = '0{}'.format(self.echelon.designation)
            else:
                echelon_label = self.echelon.designation

            return "{}:{}".format(categorie_label,echelon_label)
        except Exception as e:
            return self

class Model_Syndicat(models.Model):
    designation             =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    role                    =   models.CharField(max_length = 50, null = True, blank=True, default = '')
    objectifs               =   models.CharField(max_length = 500, null = True, blank=True, default = '')
    delegue_principal       =   models.ForeignKey(Model_Employe, on_delete = models.SET_NULL, related_name = 'delegue_principal_fk_tkq', null = True, blank = True)
    delegue_secondaire      =   models.ForeignKey(Model_Employe, on_delete = models.SET_NULL, related_name = 'delegue_secondaire_fk_emk', null = True, blank = True)
    description             =   models.CharField(max_length = 250, null = True, blank=True, default = '')
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    created_at              =   models.DateTimeField(auto_now_add=True)
    update_at               =   models.DateTimeField(auto_now = True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_syndicat_soo', null = True, blank = True)

    def __str__(self):
        return self.designation

    @property
    def number_of_ligne_syndicat(self):
        lignes = Model_Ligne_Syndicat.objects.filter(syndicat_id = self.id)
        return len(lignes)

class Model_Ligne_Syndicat(models.Model):
    syndicat                =   models.ForeignKey(Model_Syndicat, on_delete = models.CASCADE, related_name="ligne_of_syndicat", null = True, blank = True)
    employe                 =   models.ForeignKey(Model_Employe, on_delete = models.SET_NULL, related_name = 'employe_affilie_syndicat', null = True, blank = True)
    description             =   models.CharField(max_length = 50, blank=True, null=True)
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    created_at              =   models.DateTimeField(auto_now_add=True)
    update_at               =   models.DateTimeField(auto_now = True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_ligne_syndicat_soo', null = True, blank = True)

    def __str__(self):
        return self.syndicat.designation + " / "+ self.employe.nom_complet

class Model_Ligne_Competence(models.Model):
    employe = models.ForeignKey(Model_Employe, on_delete = models.SET_NULL, related_name = 'employe_competence', null = True, blank = True)
    competence = models.CharField(max_length = 100, blank=True, null=True)
    observation = models.CharField(max_length = 150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now = True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_ligne_scompetence_soo', null = True, blank = True)

    def __str__(self):
        return self.competence

class Model_Evaluation(models.Model):
    description = models.CharField(max_length = 250, null = True, blank=True, default = '')
    instructions = models.CharField(max_length = 350, null = True, blank=True, default = '')
    echelle_notation = models.CharField(max_length = 200, null = True, blank=True, default = '')
    echelle_performance = models.CharField(max_length = 200, null = True, blank=True, default = '')
    echelle_coefficient = models.CharField(max_length = 200, null = True, blank=True, default = '')
    appreciation = models.CharField(max_length = 100, null = True, blank=True, default = '')
    date_appreciation = models.DateTimeField()
    employe = models.ForeignKey(Model_Employe, on_delete = models.CASCADE, related_name = 'employe_fk_evalg', null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now = True)
    statut  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat =   models.CharField(max_length=50, blank=True, null=True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_evaluation_umf', null = True, blank = True)

    def __str__(self):
        return self.employe.nom_complet + " / " + self.description

class Model_Emploi(models.Model):
    etablissement = models.CharField(max_length = 100, null = True, blank=True, default = '')
    lieu = models.CharField(max_length = 100, null = True, blank=True, default = '')
    fonctions = models.CharField(max_length = 250, null = True, blank=True, default = '')
    categorie_socio_professionnelle = models.CharField(choices=CategoriePros, max_length = 100, null = True, blank=True, default = '')
    date_entree = models.DateTimeField()
    date_sortie = models.DateTimeField()
    employe = models.ForeignKey(Model_Employe, on_delete = models.CASCADE, related_name = 'employe_fk_whh', null = True, blank = True)
    statut =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat =   models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now = True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_emploi_nnv', null = True, blank = True)

    def __str__(self):
        return self.employe.nom_complet + " / " + self.etablissement

#old
class Model_Mobilite(models.Model):
    direction = models.CharField(max_length = 100, null = True, blank=True, default = '')
    service = models.CharField(max_length = 100, null = True, blank=True, default = '')
    type_mobilite = models.CharField(choices=Type_Mobilite,max_length = 100, null = True, blank=True, default ='Promotion')
    fonctions_occupees = models.CharField(max_length = 250, null = True, blank=True, default = '')
    categorie_socio_professionnelle = models.CharField(choices=CategoriePros,max_length = 100, null = True, blank=True, default = '')
    categorie_socia_pro_precedent=models.CharField(max_length = 100, null = True, blank =True, default='')
    modalites = models.CharField(max_length = 250, null = True, blank=True, default = '')
    ponderation = models.IntegerField(default=0)
    date_entree = models.DateTimeField(null = True, blank=True)
    date_sortie = models.DateTimeField(null = True, blank=True)
    employe = models.ForeignKey(Model_Employe, on_delete = models.CASCADE, related_name = 'employe_fk_nhg', null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now = True)
    statut =  models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat =  models.CharField(max_length=50, blank=True, null=True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_mobilite_gny', null = True, blank = True)
    def __str__(self):
        return self.employe.nom_complet + " / " + self.service + " / " + str(self.categorie_socio_professionnelle)


class Model_MobiliteEmploye(models.Model):
    reference = models.CharField(max_length = 100, null = True, blank=True, default = '')
    employe = models.ForeignKey(Model_Employe, on_delete = models.CASCADE, related_name = 'employe_of_mobilite_nhg', null = True, blank = True)
    type_mobilite = models.IntegerField(choices=Type_Mobilite, default =1)
    date_mobilite = models.DateTimeField(null = True, blank=True)
    poste = models.ForeignKey(Model_Poste, on_delete=models.SET_NULL, blank=True, null=True)
    categorie = models.ForeignKey("Model_CategorieRH", on_delete = models.SET_NULL, related_name = 'categorie_rh_mob_fk', null = True, blank = True)
    classification_pro = models.ForeignKey("Model_ClassificationProfessionelle", on_delete = models.SET_NULL, related_name="classification_pro_mobilite", null = True, blank = True)
    observation = models.CharField(max_length = 500, null = True, blank=True, default = '')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    est_actif = models.BooleanField(default=True)
    statut =  models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat =  models.CharField(max_length=50, blank=True, null=True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_mobilite_employe_gny', null = True, blank = True)

    def __str__(self):
        return self.reference

    def value_typeMobilite(self):
        return dict(Type_Mobilite)[int(self.type_mobilite)]




class Model_Formation(models.Model):
    departement = models.CharField(max_length = 100, null = True, blank=True, default = '')
    theme = models.CharField(max_length = 100, null = True, blank=True, default = '')
    objectif = models.CharField(max_length = 500, null = True, blank=True, default = '')
    public_cible = models.CharField(max_length = 250, null = True, blank=True, default = '')
    annee = models.IntegerField()
    nombre_jour_formation = models.IntegerField()
    type = models.CharField(max_length = 50, null = True, blank=True, default = '')
    organisme_formation = models.CharField(max_length = 100, null = True, blank=True, default = '')
    localite_organisme = models.CharField(max_length = 50, null = True, blank=True, default = '')
    nombre_heure_par_jour = models.CharField(max_length = 10, null = True, blank=True, default = '')
    cout_formation = models.FloatField()
    nombre_participant_par_jour = models.IntegerField()
    frais_mission_hebergement = models.FloatField()
    frais_deplacement_ht = models.FloatField()
    priorite = models.CharField(max_length = 100, null = True, blank=True, default = '')
    date_debut = models.DateTimeField(auto_now = True)
    date_fin = models.DateTimeField(auto_now = True)
    etat =    models.CharField(max_length=50, blank=True, null=True)
    cout_formation_effective = models.FloatField(default=0)
    frais_mission_hebergement_effective = models.FloatField(default=0)
    frais_deplacement_ht_effective = models.FloatField(default=0)
    nombre_participant_par_jour_effective = models.IntegerField(default=0)
    statut = models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now = True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_formation_ydl', null = True, blank = True)

    def __str__(self):
        return self.departement

    @property
    def separateur_nombre_participant_par_jour(self):
        return AfficheEntier(float(self.nombre_participant_par_jour))

    @property
    def separateur_frais_mission_hebergement(self):
        return AfficheEntier(float(self.frais_mission_hebergement))

    @property
    def separateur_frais_deplacement_ht(self):
        return AfficheEntier(float(self.frais_deplacement_ht))

    @property
    def separateur_frais_mission_hebergement_effective(self):
        return AfficheEntier(float(self.frais_mission_hebergement_effective))

    @property
    def separateur_frais_deplacement_ht_effective(self):
        return AfficheEntier(float(self.frais_deplacement_ht_effective))

    @property
    def separateur_cout_formation(self):
        return AfficheEntier(float(self.cout_formation))


class Model_Ligne_Formation(models.Model):
    formation =    models.ForeignKey(Model_Formation, on_delete = models.CASCADE, related_name="ligne_of_formation", null = True, blank = True)
    employe = models.ForeignKey(Model_Employe, on_delete = models.SET_NULL, related_name = 'employe_affilie_formation', null = True, blank = True)
    competence = models.CharField(max_length = 100, blank=True, null=True)
    description = models.CharField(max_length = 50, blank=True, null=True)
    statut =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat =   models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now = True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_ligne_formation_soo', null = True, blank = True)

    def __str__(self):
        return self.formation.theme + " / "+ self.employe.nom_complet


class Model_Ligne_releve(models.Model):
    employe = models.ForeignKey(Model_Employe, on_delete = models.SET_NULL, related_name = 'employe_fk_qqc', null = True, blank = True)
    superieur = models.ForeignKey(Model_Employe, on_delete = models.SET_NULL, related_name = 'employe_fk_qqcsuper', null = True, blank = True)
    degre = models.CharField(max_length = 250, null = True, blank=True, default = ' ')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now = True)
    statut =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat =   models.CharField(max_length=50, blank=True, null=True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_ligne_releve_qis', null = True, blank = True)

    def __str__(self):
        return self.superieur.nom_complet

class Model_Projet_professionnel(models.Model):
    projet = models.CharField(max_length = 1000, null = True, blank=True, default = ' ')
    employe = models.ForeignKey(Model_Employe, on_delete = models.SET_NULL, related_name = 'employe_fk_dzv', null = True, blank = True)
    numero_projet = models.CharField(max_length = 50, null = True, blank=True, default = ' ')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now = True)
    statut =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat =   models.CharField(max_length=50, blank=True, null=True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_projet_professionnel_yhf', null = True, blank = True)

    def __str__(self):
        return self.projet

class Model_Recrutement_interne(models.Model):
    designation = models.CharField(max_length = 100, null = True, blank=True, default = '')
    description = models.CharField(max_length = 250, null = True, blank=True, default = '')
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    est_fini = models.BooleanField(default = False)
    service = models.ForeignKey(Model_Unite_fonctionnelle, on_delete = models.SET_NULL, related_name = 'service_fk_dbo', null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now = True)
    statut =  models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat =  models.CharField(max_length=50, blank=True, null=True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_recrutement_interne_txm', null = True, blank = True)

    def __str__(self):
        return self.designation + " / " + self.date_debut
        # + " / " + self.date_debut

class Model_Ligne_postulation(models.Model):
    recrutement             =   models.ForeignKey(Model_Recrutement_interne, on_delete=models.CASCADE, null=True, blank=True, related_name="postulation_recrutementç_fk")
    employe                 =   models.ForeignKey(Model_Employe, on_delete = models.SET_NULL, related_name = 'employe_fk_postulation', null = True, blank = True)
    date_postulation        =   models.DateTimeField(auto_now = True)
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    update_date             =   models.DateTimeField(auto_now=True)
    creation_date           =   models.DateTimeField(auto_now_add = True)
    auteur                  =   models.ForeignKey(Model_Personne, related_name="auteur_ligne_postulation", null = True, blank = True, on_delete=models.SET_NULL)

    def __str__(self):
        return "Postulation de {} au recrutement {}".format(self.employe.nom_complet, self.recrutement.description)


class Model_Centre_cout(models.Model):
    code = models.CharField(max_length = 20, null = True, blank=True, default = '')
    designation = models.CharField(max_length = 100, null = True, blank=True, default = '')
    abbreviation = models.CharField(max_length = 10, null = True, blank=True, default = '')
    centre_cout = models.ForeignKey("Model_Centre_cout", on_delete = models.SET_NULL, related_name = 'centre_cout_fk_ffa', null = True, blank = True)
    typeCentre =  models.IntegerField(choices=TypeCentre, default = 2)
    groupe_analytique = models.ForeignKey("Model_GroupeAnalytique", on_delete = models.SET_NULL, related_name = "groupe_analytique_of_centre_cout", null = True, blank = True)
    date_debut = models.DateTimeField(blank=True, null=True)
    date_fin = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now = True)
    statut =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat =   models.CharField(max_length=50, blank=True, null=True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_centre_cout_kkt', null = True, blank = True)
    def __str__(self):
        return self.designation

    def value_typeCentre(self):
        return dict(TypeCentre)[int(self.typeCentre)]

    @property
    def get_label(self):
        try:
            centre = Model_Centre_cout.objects.get(pk = self.centre_cout_id)
            name_label = centre.get_label + "/" + self.abbreviation
            return name_label
        except Exception as e:
            name_label = self.abbreviation
            return name_label

class Model_Lettrage(models.Model):
    designation = models.CharField(max_length = 100, null = True, blank=True, default = '')
    description = models.CharField(max_length = 250, null = True, blank=True, default = '')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now = True)
    statut =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat =   models.CharField(max_length=50, blank=True, null=True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_lettrage_qef', null = True, blank = True)

    def __str__(self):
        return self.designation

class Model_CompteBanque(models.Model):
    designation = models.CharField(max_length = 100, null = True, blank=True, default = '')
    description = models.CharField(max_length = 250, null = True, blank=True, default = '')
    numero_compte = models.CharField(max_length=50, null = True, blank = True, default ='')
    compte_comptable = models.ForeignKey(Model_Compte, on_delete = models.SET_NULL, related_name = 'compte_of_this_banque', null =True, blank = True)
    type_compte = models.CharField(max_length=50, null=True, blank = True, default="")
    banque = models.ForeignKey("Model_Banque", on_delete = models.SET_NULL, related_name = 'banque_of_compte', null = True, blank = True)
    journal = models.ForeignKey(Model_Journal, on_delete = models.SET_NULL, related_name = 'journal_of_this_banque', null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now = True)
    statut =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat =   models.CharField(max_length=50, blank=True, null=True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_banque_gkv', null = True, blank = True)

    def __str__(self):
        return self.designation

    @property
    def solde(self):
        solde = 0
        try:
            operations = Model_OperationTresorerie.objects.filter(compte_banque = self)
            for operation in operations:
                solde += operation.compute_solde
            return solde
        except Exception as e:
            return solde

class Model_Caisse(models.Model):
    designation = models.CharField(max_length = 100, null = True, blank=True, default = '')
    description = models.CharField(max_length = 250, null = True, blank=True, default = '')
    journal = models.ForeignKey(Model_Journal, on_delete = models.SET_NULL, related_name = 'journal_of_this_caisse', null = True, blank = True)
    compte_comptable = models.ForeignKey(Model_Compte, on_delete = models.SET_NULL, related_name = 'compte_of_this_caisse', null =True, blank = True)
    responsable = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'responsable_fk_vji', null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now = True)
    statut =  models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat =  models.CharField(max_length=50, blank=True, null=True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_caisse_ayc', null = True, blank = True)

    def __str__(self):
        return self.designation

    @property
    def solde(self):
        solde = 0
        try:
            operations = Model_OperationTresorerie.objects.filter(caisse = self)
            for operation in operations:
                solde += operation.compute_solde
            return solde
        except Exception as e:
            return solde

class Model_OperationTresorerie(models.Model):
    reference = models.CharField(max_length = 100, null = True, blank=True, default = '')
    journal = models.ForeignKey(Model_Journal, on_delete = models.SET_NULL, related_name = 'journal_fk_ukq', null = True, blank = True)
    caisse = models.ForeignKey(Model_Caisse, on_delete = models.SET_NULL, related_name = 'caisse_fk_zix', null = True, blank = True)
    compte_banque = models.ForeignKey(Model_CompteBanque, on_delete = models.SET_NULL, related_name = 'banque_fk_ygi', null = True, blank = True)
    type_operation = models.CharField(choices=TypeOperation, max_length=100, null = True, blank=True, default = '')
    balance_initiale = models.FloatField()
    solde = models.CharField(max_length = 100, null = True, blank=True, default = '')
    date_operation = models.DateTimeField()
    etat = models.CharField(max_length = 50,choices=EtatOperationTresorerie, default="created")
    date_comptable = models.DateTimeField()
    devise = models.ForeignKey(Model_Devise, on_delete = models.SET_NULL, related_name = 'devise_fk_kzb', null = True, blank = True)
    taux = models.ForeignKey(Model_Taux, on_delete = models.SET_NULL, related_name = 'taux_fk_pyi', null = True, blank = True)
    description = models.CharField(max_length = 250, null = True, blank=True, default = '')
    billeterie = models.ForeignKey('Model_Billeterie', on_delete = models.SET_NULL, related_name = "billeterie_of_operation_tresorerie", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now = True)
    statut =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_operationtresorerie_zbm', null = True, blank = True)

    def __str__(self):
        return self.reference

    @property
    def compute_solde(self):
        solde = 0
        try:
            lignes = Model_Ligne_OperationTresorerie.objects.filter(operation_tresorerie = self)
            for ligne in lignes:
                if ligne.type_operation == 1:
                    solde += ligne.montant
                elif ligne.type_operation == 2:
                    solde -= ligne.montant
            return solde
        except Exception as e:
            return solde

class Model_Ligne_OperationTresorerie(models.Model):
    reference = models.CharField(max_length = 100, null = True, blank=True, default = '')
    libelle = models.CharField(max_length = 100, null = True, blank=True, default = '')
    partenaire = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'partenaire_fk_gaq', null = True, blank = True)
    montant = models.FloatField()
    date_ligne_operation = models.DateTimeField(null=True)
    est_lettre = models.BooleanField(default=False)
    lettrage =    models.ForeignKey("Model_Lettrage", on_delete = models.SET_NULL, related_name="lettrage_ligne_operation_tresorerie", null = True, blank = True)
    facture = models.ForeignKey("Model_Facture", on_delete=models.SET_NULL, related_name="ligne_operation_by_facture", null=True, blank=True)
    paiement = models.ForeignKey(Model_Paiement, on_delete=models.SET_NULL, related_name = "paiement_link_in_ligne", blank=True, null=True)
    devise = models.ForeignKey(Model_Devise, on_delete = models.SET_NULL, related_name = 'devise_fk_wuk', null = True, blank = True)
    taux = models.ForeignKey(Model_Taux, on_delete = models.SET_NULL, related_name = 'taux_fk_dca', null = True, blank = True)
    type_operation = models.IntegerField(choices=LigneTypeOperation, default=1)
    operation_tresorerie = models.ForeignKey(Model_OperationTresorerie, on_delete= models.CASCADE,related_name="operation_of_ligne")
    description = models.CharField(max_length = 200, null = True, blank=True, default = '')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now = True)
    statut =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat =   models.CharField(max_length=50, blank=True, null=True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_ligne_operation_transaction_wup', null = True, blank = True)

    def __str__(self):
        return self.reference


    def value_type_operation(self):
        return dict(LigneTypeOperation)[int(self.type_operation)]

class Model_Banque(models.Model):
    designation = models.CharField(max_length = 100, null = True, blank=True, default = '')
    adresse = models.CharField(max_length = 100, null = True, blank=True, default = '')
    observation = models.CharField(max_length = 200, null = True, blank=True, default = '')
    code = models.CharField(max_length = 50, null = True, blank=True, default = '')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now = True)
    statut =  models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat =  models.CharField(max_length=50, blank=True, null=True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_bank_rfk', null = True, blank = True)

    def __str__(self):
        return self.designation

    @property
    def solde(self):
        solde = 0
        try:
            compte_banques = Model_CompteBanque.objects.filter(banque = self)
            for compte in compte_banques:
                solde += compte.solde
            return solde
        except Exception as e:
            return solde

class Model_Requete(models.Model):
    numero_reference = models.CharField(max_length = 150, null = True, blank=True, default = ' ')
    demandeur = models.ForeignKey(Model_Employe, on_delete = models.SET_NULL, related_name = 'demandeur_fk_imq', null = True, blank = True)
    date_depart = models.DateTimeField()
    date_retour = models.DateTimeField()
    description = models.CharField(max_length = 300, null = True, blank=True, default = ' ')
    service_ref = models.ForeignKey(Model_Unite_fonctionnelle, on_delete = models.SET_NULL, related_name = 'service_ref_fk_nxn', null = True, blank = True)
    centre_cout = models.ForeignKey("Model_Centre_cout", on_delete = models.SET_NULL, related_name = 'centre_cout_fk_eko', null = True, blank = True)
    document = models.CharField(max_length = 150, null = True, blank=True, default = ' ')
    statut = models.ForeignKey(Model_Wkf_Etape, on_delete = models.SET_NULL, related_name = 'statut_fk_hgk', null = True, blank = True)
    etat = models.CharField(max_length = 100, null = True, blank=True, default = ' ')
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_fk_cje', null = True, blank = True)
    url = models.CharField(max_length = 250, null = True, blank=True, default = ' ')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.numero_reference


class Model_Ligne_requete(models.Model):
    requete = models.ForeignKey(Model_Requete, on_delete = models.SET_NULL, related_name = 'requete_fk_tzj', null = True, blank = True)
    employe = models.ForeignKey(Model_Employe, on_delete = models.SET_NULL, related_name = 'employe_fk_pev', null = True, blank = True)
    frais_de_mission = models.IntegerField()
    frais_hebergement = models.FloatField()
    description = models.CharField(max_length = 150, null = True, blank=True, default = ' ')
    url = models.CharField(max_length = 300, null = True, blank=True, default = ' ')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length = 150, null = True, blank=True, default = ' ')
    update_at = models.DateTimeField(auto_now = True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_ligne_requete_aae', null = True, blank = True)

    def __str__(self):
        return "Ligne{}".format(self.requete_id)

    @staticmethod
    def montant_total(self):
        return self.frais_de_mission + self.frais_hebergement


class Model_Ordre_de_mission(models.Model):
    numero_ordre = models.CharField(max_length = 150, null = True, blank=True, default = ' ')
    objet_mission = models.CharField(max_length = 150, null = True, blank=True, default = ' ')
    destination = models.CharField(max_length = 250, null = True, blank=True, default = ' ')
    moyen_transport = models.CharField(max_length = 150, null = True, blank=True, default = ' ')
    date_retour = models.DateTimeField()
    demandeur = models.ForeignKey(Model_Employe, on_delete = models.SET_NULL, related_name = 'demandeur_fk_imq_mission', null = True, blank = True)
    requete = models.ForeignKey(Model_Requete, on_delete = models.SET_NULL, related_name = 'requete_fk_1_tzj', null = True, blank = True)
    date_depart = models.DateTimeField()
    ligne_budgetaire = models.ForeignKey(Model_LigneBudgetaire, on_delete = models.SET_NULL, related_name = 'ligne_budgetaire_fk_iwx', null = True, blank = True)
    type = models.CharField(max_length = 150, null = True, blank=True, default = ' ')
    frais_mission = models.FloatField(default=0)
    description = models.CharField(max_length = 150, null = True, blank=True, default = ' ')
    observation = models.CharField(max_length = 50, null = True, blank=True, default = '')
    statut = models.ForeignKey(Model_Wkf_Etape, on_delete = models.SET_NULL, related_name = 'statut_fk_hgk_mission', null = True, blank = True)
    etat = models.CharField(max_length = 100, null = True, blank=True, default = ' ')
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_fk_bxn', null = True, blank = True)
    url = models.CharField(max_length = 250, null = True, blank=True, default = ' ')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.numero_ordre

class Model_Ligne_ordre_de_mission(models.Model):
    ordre_mission = models.ForeignKey(Model_Ordre_de_mission, on_delete = models.SET_NULL, related_name = 'ordre_mission_fk_chg', null = True, blank = True)
    employe = models.ForeignKey(Model_Employe, on_delete = models.SET_NULL, related_name = 'employe_fk_kku', null = True, blank = True)
    frais_de_mission = models.IntegerField()
    frais_hebergement = models.FloatField()
    status = models.CharField(max_length = 150, null = True, blank=True, default = ' ')
    description = models.CharField(max_length = 150, null = True, blank=True, default = ' ')
    url = models.CharField(max_length = 250, null = True, blank=True, default = ' ')
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_fk_pbg', null = True, blank = True)
    created_at = models.DateTimeField()
    update_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return "Ligne {} de l'ordre {}".format(self.id,self.ordre_mission.numero_ordre)

    @staticmethod
    def montant_total(self):
        return self.frais_de_mission + self.frais_hebergement

class Model_Activite(models.Model):
    code = models.CharField(max_length = 2, null = True, blank=True, default = '')
    designation = models.CharField(max_length = 150, null = True, blank=True, default = '')
    statut = models.ForeignKey(Model_Wkf_Etape, on_delete = models.SET_NULL, related_name = 'statut_fgtk_hgk_mission', null = True, blank = True)
    etat = models.CharField(max_length = 100, null = True, blank=True, default = ' ')
    created_at = models.DateTimeField(null=True, blank=True)
    update_at = models.DateTimeField(auto_now = True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_activite_hgp', null = True, blank = True)

    def __str__(self):
        return self.code

class Model_GroupeAnalytique(models.Model):
    designation = models.CharField(max_length = 100, null = True, blank=True, default = '')
    description = models.CharField(max_length = 200, null = True, blank=True, default = '')
    statut = models.ForeignKey(Model_Wkf_Etape, on_delete = models.SET_NULL, related_name = 'statut_pok_hgk_mission', null = True, blank = True)
    etat = models.CharField(max_length = 100, null = True, blank=True, default = ' ')
    est_projet = models.BooleanField(default = False)
    groupe_analytique = models.ForeignKey("Model_GroupeAnalytique", on_delete = models.SET_NULL, related_name = 'groupe_analytique_fk_aes', null = True, blank = True)
    created_at = models.DateTimeField()
    update_at = models.DateTimeField(auto_now = True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_groupeanalytique_ydk', null = True, blank = True)

    def __str__(self):
        return self.designation

class Model_Poste_budgetaire(models.Model):
    code                    =   models.CharField(max_length = 6, null = True, blank=True, default = '')
    designation             =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    created_at              =   models.DateTimeField(auto_now_add=True)
    update_at               =   models.DateTimeField(auto_now = True)
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_poste_budgetaire_dxg', null = True, blank = True)

    def __str__(self):
        return self.code

    @property
    def comptes(self):
        comptes = []
        lignes = Model_LignePosteBudgetaire.objects.filter(poste_budgetaire = self).order_by("-id")
        for ligne in lignes:
            comptes.append(ligne.compte)
        return comptes
    @property
    def compte_principal(self):
        try:
            return Model_Compte.objects.filter(numero = self.code).first()
        except Exception:
            self.comptes[0]


class Model_LignePosteBudgetaire(models.Model):
    compte                  =   models.ForeignKey("Model_Compte", on_delete = models.SET_NULL, related_name="compte_of_postbudgetaire", null = True, blank = True)
    poste_budgetaire        =   models.ForeignKey("Model_Poste_budgetaire", on_delete = models.SET_NULL, related_name="ref_of_postbudgetaire", null = True, blank = True)
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    update_date             =   models.DateTimeField(auto_now=True)
    creation_date           =   models.DateTimeField(auto_now_add = True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_lignes_postes', null = True, blank = True)

    def __str__(self):
        return self.compte.designation

class Model_Ecriture_analytique(models.Model):
    libelle = models.CharField(max_length = 200, null = True, blank=True, default = '')
    compte = models.ForeignKey(Model_Compte, on_delete = models.SET_NULL, related_name = 'compte_fk_pbd', null = True, blank = True)
    centre_cout = models.ForeignKey(Model_Centre_cout, on_delete = models.SET_NULL, related_name = 'centre_cout_fk_mij', null = True, blank = True)
    montant = models.FloatField(default = 0)
    type = models.IntegerField(choices=TypeEcritureAnalytique, default=2)
    devise = models.ForeignKey(Model_Devise, on_delete = models.SET_NULL, related_name= "devise_of_ecritures_analytiques", null = True, blank = True)
    facture = models.ForeignKey(Model_Facture, on_delete = models.SET_NULL, related_name = 'facture_fk_uzy', null = True, blank = True)
    ligne_budgetaire = models.ForeignKey("Model_LigneBudgetaire", on_delete=models.SET_NULL, blank=True, null=True, related_name="ligne_of_ecriture_analytique")
    ecriture_comptable = models.ForeignKey("Model_EcritureComptable", on_delete = models.SET_NULL, related_name = "ecriture_comptable_link", null=True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now = True)
    statut =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat =   models.CharField(max_length=50, blank=True, null=True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_ecriture_analytique_mxc', null = True, blank = True)

    def __str__(self):
        return self.libelle

    def montant_valeur_absolue(self):
        return abs(self.montant)

    def value_type(self):
        return dict(TypeEcritureAnalytique)[int(self.type)]


class Model_Ligne_Immobilisation(models.Model):
    annee = models.IntegerField(null = True, blank = True)
    base_amortissement = models.FloatField(blank=True, null=True)
    dotation = models.FloatField(blank=True, null=True)
    cumul = models.FloatField(blank=True, null=True)
    valeur_residuelle = models.FloatField(blank=True, null=True)
    immobilisation = models.ForeignKey(Model_Immobilisation, on_delete = models.CASCADE, related_name="immo_of_ammortissement", blank=True, null=True)
    observation = models.CharField(max_length=250, blank=True, null=True)
    date_amortissement = models.DateTimeField(auto_now = True)
    statut =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat =   models.CharField(max_length=50, blank=True, null=True)
    update_date =   models.DateTimeField(auto_now=True)
    creation_date =   models.DateTimeField(auto_now_add = True)
    auteur                      =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_lignes_immo', null = True, blank = True)

    def __str__(self):
        return self.immobilisation.libelle


class Model_TraitementImmobilisation(models.Model):
    numero_traitement       =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    rapport_inventaire      =   models.ForeignKey(Model_Document, on_delete = models.SET_NULL, related_name = 'rapport_inventaire_fk_dyb', null = True, blank = True)
    description             =   models.CharField(max_length = 250, null = True, blank=True, default = '')
    type_traitement         =   models.IntegerField(choices = TypeTraitement, default=1)
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True, related_name="etat_of_traitement_immo")
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    created_at              =   models.DateTimeField(auto_now_add=True)
    update_at               =   models.DateTimeField(auto_now = True)
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_traitement_immobilisation_pgu', null = True, blank = True)

    def __str__(self):
        return self.numero_traitement

    def value_type_traitement(self):
        return dict(TypeTraitement)[int(self.type_traitement)]


class Model_LigneTraitementImmobilisation(models.Model):
    immobilisation = models.ForeignKey(Model_Immobilisation, on_delete = models.SET_NULL, related_name = 'immobilisation_fk_dhr', null = True, blank = True)
    description = models.CharField(max_length = 200, null = True, blank=True, default = '')
    prix_vente = models.FloatField(blank=True, null=True)
    est_traite = models.BooleanField(default = False)
    traitement_immobilisation = models.ForeignKey(Model_TraitementImmobilisation, on_delete = models.CASCADE, related_name = "ligne_of_traitement", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now = True)
    statut =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat =   models.CharField(max_length=50, blank=True, null=True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_ligne_traitementimmobilisation_apv', null = True, blank = True)

    def __str__(self):
        return self.traitement_immobilisation.numero_traitement


class Model_Billeterie(models.Model):
    reference = models.CharField(max_length = 100, blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now = True)
    statut  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat =   models.CharField(max_length=50, blank=True, null=True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_billeterie', null = True, blank = True)

    def __str__(self):
        return self.reference

class Model_LigneBilleterie(models.Model):
    billet = models.CharField(max_length = 100, blank=True, null=True)
    valeur = models.FloatField(blank=True, null=True)
    sous_total = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now = True)
    billeterie = models.ForeignKey('Model_Billeterie', on_delete = models.CASCADE, related_name = "ligne_billeterie_of_operation_tresorerie", blank=True, null=True)
    statut  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat  =   models.CharField(max_length=50, blank=True, null=True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_ligne_billeterie', null = True, blank = True)

    def __str__(self):
        return self.billeterie.reference

class Model_Analyse_Personnel_Mouve(models.Model):
    masse_salariale = models.IntegerField(null = True, blank = True, default=0)
    prorogation_stage = models.IntegerField(null = True, blank = True, default=0)
    total_mise_stage = models.IntegerField(null= True, blank = True, default=0)
    depart_definitif = models.IntegerField(null= False, blank= True, default=0)
    depart_provision = models.IntegerField(null= True, blank = True, default=0)
    nombre_emploi_paye = models.IntegerField(null= False, blank = True, default=0)
    depart_volontaire = models.IntegerField(null = True, blank =True, default=0)
    demission = models.IntegerField(null = True, blank = True, default=0)
    arrivee = models.IntegerField(null = False, blank = True, default=0)
    poste_vacant_by_mob = models.IntegerField(null= True, blank = True, default=0)
    poste_vacant_pouvu = models.IntegerField(null = True, blank = True, default=0)
    recru_emploi_permanent = models.IntegerField(null = False, blank = True, default=0)
    concours = models.IntegerField(null = True, blank = True, default=0)
    mutation = models.IntegerField(null = True, blank = True, default=0)
    detachement = models.IntegerField(null = True, blank = True, default=0)
    recru_direct = models.IntegerField(null = True, blank = True, default=0)
    interimaire = models.IntegerField(null = True, blank= True, default=0)
    total_recru = models.IntegerField(null = True, blank= True, default=0)
    annee = models.IntegerField(null = True, blank = True)
    statut =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat =   models.CharField(max_length=50, blank=True, null=True)
    update_date  =   models.DateTimeField(auto_now=True)
    creation_date  =   models.DateTimeField(auto_now_add = True)
    auteur =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_analyses_personnels', null = True, blank = True)


    @property
    def Tx_depart(self):
        try:
            value = self.depart_definitif / self.nombre_emploi_paye
            return value

        except Exception as e:
            return 0.0

    @property
    def Tx_depart_volontaire(self):
        try:
            value = self.depart_volontaire / self.nombre_emploi_paye
            return value
        except Exception as e:
            return 0.0

    @property
    def Tx_remplacement(self):
        try:
            value = (self.depart_definitif / self.arrivee ) * 100
            return value
        except Exception as e:
            return 0.0

    @property
    def Total_poste(self):
        try:
            valeur = self.poste_vacant_by_mob + self.poste_vacant_pouvu
            return valeur
        except Exception as e:
            return 0.0

    @property
    def Tx_poste_vacant(self):
        try:
            value = (self.poste_vacant_pouvu / (self.poste_vacant_by_mob + self.poste_vacant_pouvu) )
            return value
        except Exception as e:
            return 0.0

    @property
    def Taux_prop_stage(self):
        try:
            value = (self.prorogation_stage /  self.total_mise_stage)
            return value
        except Exception as e:
            return 0.0

class Model_Analyse_indice_princsuivi(models.Model):
    nombre_entree = models.IntegerField(null = True, blank = True, default=0)
    nombre_sortie = models.IntegerField(null = True, blank = True, default=0)
    massa_salariale_eff = models.IntegerField(null = True, blank = True, default=0)
    masse_salariale_bud = models.IntegerField(null = True, blank = True, default=0)
    salairesentre_diff_catehorie = models.IntegerField(null = True, blank = True, default=0)
    prime_remuneration = models.IntegerField(null = True, blank = True, default=0)
    heure_supplementaire = models.IntegerField(null = True, blank = True, default=0)
    salaire_median_collectivite = models.IntegerField(null = True, blank = True, default=0)
    accident_travail_arret = models.IntegerField(null = True, blank = True, default=0)
    nombre_heure_travail = models.IntegerField(null = True, blank = True, default=0)
    nombre_jour_arret = models.IntegerField(null = True, blank = True, default=0)
    nbre_jr_absence = models.IntegerField(null = True, blank = True, default=0)
    arret_maladie_moins_jour = models.IntegerField(null = True, blank = True, default=0)
    arret_maladie = models.IntegerField(null = True, blank = True, default=0)
    montant_formation = models.IntegerField(null = True, blank = True, default=0)
    masse_sal = models.IntegerField(null = True, blank = True, default=0)
    nbr_jour_formation_D = models.IntegerField(null = True, blank = True, default=0)
    nbr_agent_occupe_D = models.IntegerField(null = True, blank = True, default=0)
    frais_personnel = models.IntegerField(null = True, blank = True, default=0)
    Budget_fonct = models.IntegerField(null = True, blank = True, default=0)
    txformationMetier = models.IntegerField(null = True, blank = True, default=0)
    txabsentiemal = models.IntegerField(null = True, blank = True, default=0)
    annee = models.IntegerField(null = True, blank = True)
    statut =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat =   models.CharField(max_length=50, blank=True, null=True)
    update_date  =   models.DateTimeField(auto_now=True)
    creation_date  =   models.DateTimeField(auto_now_add = True)
    auteur  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_analyses', null = True, blank = True)

    @property
    def Taux_absenteisme_maladie_court(self):
        try:
            value = self.arret_maladie_moins_jour / self.arret_maladie
            return value
        except Exception as e:
            return 0.0

    @property
    def Tx_frequence_Acc_travail(self):
        try:
            value = (self.nombre_jour_arret * 10) / self.nombre_heure_travail
            return value
        except Exception as e:
            return 0.0


    @property
    def Taux_gravite_acc_travail(self):
        try:
            value = (self.accident_travail_arret * 10) / self.nombre_heure_travail
            return value
        except Exception as e:
            return 0.0

    @property
    def Taux_participant_formation(self):
        try:
            value = self.montant_formation / self.masse_sal
            return value
        except Exception as e:
            return 0.0

    @property
    def Taux_formation_DG(self):
        try:
            value = self.nbr_jour_formation_D / self.nbr_agent_occupe_D
            return value
        except Exception as e:
            return 0.0

    @property
    def Taux_formation_DG(self):
        try:
            value = self.nbr_jour_formation_D / self.nbr_agent_occupe_D
            return value
        except Exception as e:
            return 0.0

    @property
    def Taux_formation_DAFC(self):
        try:
            value = self.nbr_agent_occupe_D / self.nbr_agent_occupe_D
            return value
        except Exception as e:
            return 0.0

    @property
    def Taux_formation_DRSCE(self):
        try:
            value = self.frais_personnel / self.nbr_agent_occupe_D
            return value
        except Exception as e:
            return 0.0

    @property
    def Taux_formation_DEM(self):
        try:
            value = self.Budget_fonct / self.nbr_agent_occupe_D
            return value
        except Exception as e:
            return 0.0


class Model_Ordre_paiement(models.Model):
    reference = models.CharField(max_length = 20, null = True, blank=True, default = '')
    type_paiement = models.IntegerField()
    date_echeance = models.DateTimeField()
    compte_banque = models.ForeignKey(Model_CompteBanque, on_delete = models.SET_NULL, related_name = 'banque_fk_wiw', null = True, blank = True)
    caisse = models.ForeignKey(Model_Caisse, on_delete = models.SET_NULL, related_name = 'caisse_fk_upy', null = True, blank = True)
    statut = models.ForeignKey(Model_Wkf_Etape, on_delete = models.SET_NULL, related_name = 'statut_fkordre_depaiement', null = True, blank = True)
    etat = models.CharField(max_length = 100, null = True, blank=True, default = ' ')
    description = models.CharField(max_length = 250, null = True, blank=True, default = '')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now = True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_ordre_paiement_mat', null = True, blank = True)

    def __str__(self):
        return self.reference

    def value_type_paiement(self):
        if self.type_paiement:
            return dict(TypePaiement)[int(self.type_paiement)]

    def Totalsomme(self):
        somme = 0
        ligne = Model_Ligne_ordre_paiement.objects.filter(ordre_paiement__id = self.id)
        for item in ligne:
            somme =somme + item.montant
        return somme

    def Totalsomme_paye(self):
        try:
            SommeP = 0
            ligne = Model_Ligne_ordre_paiement.objects.filter(ordre_paiement__id = self.id)
            for item in ligne:
                SommeP =SommeP + item.facture.montant_paye
            return SommeP
        except Exception as e:
            return 0.0

    def Totalmontant_restant(self):
        try:
            SommeR = 0
            ligne = Model_Ligne_ordre_paiement.objects.filter(ordre_paiement__id = self.id)
            for item in ligne:
                SommeR =SommeR + item.montant_restant
            return SommeR
        except Exception as e:
            return 0.0


    def getfss(self):
        try:
            ligne = Model_Ligne_ordre_paiement.objects.filter(ordre_paiement__id = self.id).first()
            fournisseur = ligne.partenaire
            return fournisseur
        except Exception as e:
            return ""


class Model_Ligne_ordre_paiement(models.Model):
    libelle = models.CharField(max_length = 100, null = True, blank=True, default = '')
    partenaire = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'partenaire_dk_fk_pjh', null = True, blank = True)
    facture = models.ForeignKey(Model_Facture, on_delete = models.SET_NULL, related_name = 'facture_fk_pjh', null = True, blank = True)
    montant = models.FloatField()
    ordre_paiement = models.ForeignKey(Model_Ordre_paiement, on_delete = models.CASCADE, related_name = 'ordre_paieemnt_id', null = True, blank = True)
    devise = models.ForeignKey(Model_Devise, on_delete = models.SET_NULL, related_name = 'devise_fk_exs', null = True, blank = True)
    observation = models.CharField(max_length = 100, null = True, blank=True, default = '')
    statut =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat =   models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now = True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_ligne_ordre_paiement_dvq', null = True, blank = True)

    def __str__(self):
        return self.libelle

    def montant_restant(self):
        try:
            Mafacture = Model_Facture.objects.get(pk = self.facture.id)
            Montant = float(Mafacture.montant)
            Montant_paye = float(Mafacture.montant_paye)
            Reste = float(Montant - Montant_paye) - float(self.montant)
            return Reste
        except Exception as e:
            return 0.0


class Model_Requete_competence(models.Model):
    numero_requete = models.CharField(max_length = 100, null = True, blank=True, default = '')
    competence = models.CharField(max_length = 150, null = True, blank=True, default = '')
    observation = models.CharField(max_length = 100, null = True, blank=True, default = '')
    statut = models.ForeignKey(Model_Wkf_Etape, on_delete = models.SET_NULL, related_name = 'statut_requete_competence', null = True, blank = True)
    etat = models.CharField(max_length = 100, null = True, blank=True, default = ' ')
    employe    =    models.ForeignKey(Model_Employe, on_delete = models.SET_NULL, related_name="employe_asking_requete", null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now = True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_requete_competence_myp', null = True, blank = True)

    def __str__(self):
        return self.numero_requete


#Model utilisé pour assurer une seule connexion à un instant T sur un seul compte
class Model_UserSessions(models.Model):
    user = models.ForeignKey(User, related_name='user_of_usersession', on_delete = models.CASCADE)
    session = models.ForeignKey(Session, related_name='session_of_usersession',on_delete=models.SET_NULL, null = True, blank=True)
    session_key = models.CharField(max_length = 100, null = True, blank=True, default = '')
    login_date = models.DateTimeField(blank=True, null=True)
    logout_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default = False)

    def __str__(self):
        return '%s - %s' % (self.user, self.session.session_key)

@receiver(user_logged_in)
def concurrent_logins(sender, **kwargs):
    user = kwargs.get('user')
    request = kwargs.get('request')
    if user is not None and request is not None:
        session = Session.objects.get(session_key=request.session.session_key)
        user_session = Model_UserSessions.objects.filter(session = session, is_active = True)
        if not user_session:
            #print("abbah")
            Model_UserSessions.objects.create(user=user, session=session, session_key=request.session.session_key, is_active = True, login_date = timezone.now())
    if user is not None:
        request.session['LOGIN_COUNT'] = user.user_of_usersession.count()

@receiver(user_logged_out)
def performing_logout(sender, **kwargs):
    user = kwargs.get('user')
    request = kwargs.get('request')
    if user is not None and request is not None:
        session = Session.objects.get(session_key=request.session.session_key)
        user_sessions = Model_UserSessions.objects.filter(session = session, is_active = True)
        if user_sessions:
            for session in user_sessions:
                user_session = Model_UserSessions.objects.get(pk = session.id)
                user_session.is_active = False
                user_session.logout_date = timezone.now()
                user_session.save()

# CALENDRIER MODEL
class Model_TypeEvenement(models.Model):
    designation            =   models.CharField(max_length = 300, null = True, blank = True)
    description            =   models.CharField(max_length = 500, null = True, blank = True, default="")
    statut                 =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                   =   models.CharField(max_length=50, blank=True, null=True)
    update_date            =   models.DateTimeField(auto_now=True)
    creation_date          =   models.DateTimeField(auto_now_add = True)
    auteur                 =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_type_evenements", null = True, blank = True)
    url                    =   models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation

class Model_Evenement(models.Model):
    designation            =    models.CharField(max_length = 250, null = True, blank = True)
    description            =    models.CharField(max_length = 500, null = True, blank = True, default="")
    duree                  =    models.CharField(max_length = 500, null = True, blank = True, default="00:00")
    date_debut             =    models.DateTimeField(null = True, blank = True)
    date_fin               =    models.DateTimeField(null = True, blank = True)
    type_evenement         =    models.ForeignKey(Model_TypeEvenement, on_delete = models.SET_NULL, related_name="evenements", null = True, blank = True)
    local                  =    models.ForeignKey(Model_Local, on_delete = models.SET_NULL, related_name="evenements", null = True, blank = True)
    confidentialite        =    models.IntegerField(choices = Confidentialite, default=1)
    est_actif              =    models.BooleanField(default = True)
    journee                =    models.BooleanField(default = False)
    est_recurrent          =    models.BooleanField(default = False)
    interval_recurrent     =    models.IntegerField(default=1)
    type_recurrent         =    models.IntegerField(choices = TypeRecurrent, default=1)
    compte_recurrent       =    models.IntegerField(default=1)
    type_fin_recurrent     =    models.IntegerField(choices = TypeFinRecurrent, default=1)
    date_fin_recurrent     =    models.DateTimeField(null = True, blank = True)
    recurrent_id           =    models.IntegerField(default=0)
    lundi                  =    models.BooleanField(default = False)
    mardi                  =    models.BooleanField(default = False)
    mercredi               =    models.BooleanField(default = False)
    jeudi                  =    models.BooleanField(default = False)
    vendredi               =    models.BooleanField(default = False)
    samedi                 =    models.BooleanField(default = False)
    dimanche               =    models.BooleanField(default = False)
    par_mois               =    models.IntegerField(choices = ParMois, default=1)
    date_du_mois           =    models.IntegerField(default=1)
    jour_de_semaine        =    models.CharField(choices = JoursDelaSemaine, max_length = 10, default='1')
    par_jour               =    models.IntegerField(choices = ParJour, default=1)
    proprietaires          =    models.ManyToManyField(Model_Employe)
    rappels                =    models.ManyToManyField("Model_Alarme")
    statut                 =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                   =   models.CharField(max_length=50, blank=True, null=True)
    update_date            =    models.DateTimeField(auto_now = True)
    creation_date          =    models.DateTimeField(auto_now_add = True)
    auteur                 =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_evenements", null = True, blank = True)
    url                    =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation

    @property
    def value_confidentialite(self):
        return dict(Confidentialite)[int(self.confidentialite)]

    @property
    def value_type_recurrent(self):
        return dict(TypeRecurrent)[int(self.type_recurrent)]

    @property
    def value_type_fin_recurrent(self):
        return dict(TypeFinRecurrent)[int(self.type_fin_recurrent)]

    @property
    def value_par_mois(self):
        return dict(ParMois)[int(self.par_mois)]

    @property
    def value_jour_de_semaine(self):
        return dict(JoursDelaSemaine)[str(self.jour_de_semaine)]

    @property
    def value_par_jour(self):
        return dict(ParJour)[int(self.par_jour)]

class Model_Participant(models.Model):
    nom_complet            =    models.CharField(max_length = 300, null = True, blank = True)
    email                  =    models.CharField(max_length = 300, null = True, blank = True)
    employe                =    models.ForeignKey(Model_Employe, on_delete = models.SET_NULL, related_name="participants", null = True, blank = True)
    description            =    models.CharField(max_length = 500, null = True, blank = True, default="")
    evenement              =    models.ForeignKey(Model_Evenement, on_delete = models.SET_NULL, related_name="participants", null = True, blank = True)
    disponibilite          =    models.IntegerField(choices = Disponibilite, default=1)
    statut_participation   =    models.IntegerField(choices = StatutParticipation, default=1)
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    update_date             =   models.DateTimeField(auto_now=True)
    creation_date          =    models.DateTimeField(auto_now_add = True)
    auteur                 =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_participants", null = True, blank = True)
    url                    =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.nom_participant

    @property
    def value_disponibilite(self):
        return dict(Disponibilite)[int(self.disponibilite)]

    @property
    def value_statut_participation(self):
        return dict(StatutParticipation)[int(self.statut_participation)]

    @property
    def nom_participant(self):
        try:
            nom = ""
            if self.employe == None: nom = self.nom_complet
            else: nom = "%s %s" % (self.employe.prenom, self.employe.nom)
            return nom
        except Exception as e:
            return ""

    @property
    def email_participant(self):
        try:
            email = ""
            if self.employe == None: email = self.email
            else: email = self.employe.email
            return email
        except Exception as e:
            return ""

class Model_Alarme(models.Model):
    designation            =    models.CharField(max_length = 250, null = True, blank = True)
    description            =    models.CharField(max_length = 500, null = True, blank = True, default="")
    temps                  =    models.IntegerField(default=1)
    type_alarme            =    models.IntegerField(choices = TypeAlarme, default=1)
    type_intervalle        =    models.IntegerField(choices = TypeIntervalle, default=1)
    statut                 =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                   =    models.CharField(max_length=50, blank=True, null=True)
    update_date            =    models.DateTimeField(auto_now=True)
    creation_date          =    models.DateTimeField(auto_now_add = True)
    auteur                 =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_alarmes", null = True, blank = True)
    url                    =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation

    @property
    def value_type_alarme(self):
        return dict(TypeAlarme)[int(self.type_alarme)]

    @property
    def value_type_intervalle(self):
        return dict(TypeIntervalle)[int(self.type_intervalle)]

    @property
    def temps_en_minutes(self):
        try:
            if self.type_intervalle == 1:
                return int(self.temps)
            elif self.type_intervalle == 2:
                return int(self.temps) * 60
            elif self.type_intervalle == 3:
                return int(self.temps) * 60 * 24
            else:
                return 0
        except Exception as e:
            return 0

# RECOUVREMENT MODEL
class Model_Recouvrement(models.Model):
    designation            =    models.CharField(max_length = 300, null = True, blank = True)
    description            =    models.CharField(max_length = 500, null = True, blank = True, default="")
    client                 =    models.OneToOneField(Model_Client, on_delete = models.CASCADE, related_name="recouvrements")
    statut_recouvrement    =    models.IntegerField(choices = StatutRecouvrement, default=1)
    relances               =    models.ManyToManyField("Model_RelanceRecouvrement")
    statut                 =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                   =    models.CharField(max_length=50, blank=True, null=True)
    update_date            =    models.DateTimeField(auto_now = True)
    creation_date          =    models.DateTimeField(auto_now_add = True)
    auteur                 =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_recouvrements", null = True, blank = True)
    url                    =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation

    @property
    def value_statut_recouvrement(self):
        return dict(StatutRecouvrement)[int(self.statut_recouvrement)]

class Model_RecouvrementLigne(models.Model):
    designation            =    models.CharField(max_length = 300, null = True, blank = True)
    description            =    models.CharField(max_length = 500, null = True, blank = True, default="")
    recouvrement           =    models.ForeignKey(Model_Recouvrement, on_delete = models.SET_NULL, related_name="lignes", null = True, blank = True)
    facture                =    models.ForeignKey(Model_Facture, on_delete = models.SET_NULL, related_name="lignes_recouvrements", null = True, blank = True)
    statut_recouvrement    =    models.IntegerField(choices = StatutRecouvrement, default=1)
    statut                 =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                   =    models.CharField(max_length=50, blank=True, null=True)
    update_date            =    models.DateTimeField(auto_now=True)
    creation_date          =    models.DateTimeField(auto_now_add = True)
    creation_date          =    models.DateTimeField(auto_now_add = True)
    update_date            =    models.DateTimeField(auto_now = True)
    auteur                 =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_lignes_recouvrements", null = True, blank = True)
    url                    =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation

class Model_RelanceRecouvrement(models.Model):
    designation            =    models.CharField(max_length = 300, null = True, blank = True)
    description            =    models.CharField(max_length = 250)
    type_relance           =    models.IntegerField(choices = TypeRelance, default=1)
    client                 =    models.ForeignKey(Model_Client, on_delete = models.SET_NULL, related_name="relances", null = True, blank = True)
    date_relance           =    models.DateTimeField(blank=True, null=True)
    statut                 =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                   =    models.CharField(max_length=50, blank=True, null=True)
    creation_date          =    models.DateTimeField(auto_now_add = True)
    update_date            =    models.DateTimeField(auto_now = True)
    auteur                 =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_relances_recouvrements", null = True, blank = True)
    url                    =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation

    @property
    def value_type_relance(self):
        return dict(TypeRelance)[int(self.type_relance)]

class Model_Relance(models.Model):
    numero_relance              =   models.CharField(max_length = 50)
    description                 =   models.CharField(max_length = 250)
    client                      =   models.ForeignKey(Model_Client, on_delete = models.SET_NULL, related_name="clients_relance", null = True, blank = True)
    date_relance                =   models.DateTimeField(blank=True, null=True)
    statut                      =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                        =   models.CharField(max_length=50, blank=True, null=True)
    update_date                 =   models.DateTimeField(auto_now=True)
    creation_date               =   models.DateTimeField(auto_now_add = True)
    auteur                      =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_relances', null = True, blank = True)

    def __str__(self):
        return self.description


class Model_Operationnalisation_module(models.Model):
    designation = models.CharField(max_length = 100, null = True, blank=True, default = '')
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    est_active = models.BooleanField(default = False)
    est_cloture = models.BooleanField(default = False)
    observation = models.CharField(max_length = 100, null = True, blank=True, default = '')
    module      = models.ForeignKey(Model_Module, on_delete = models.SET_NULL, related_name = 'module_fk_xdu', null = True, blank = True)
    statut      =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    update_at   = models.DateTimeField(auto_now = True)
    auteur      = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_operationnalisation_module_pyz', null = True, blank = True)

    def __str__(self):
        return self.designation


class Model_Typefacture(models.Model):
    designation = models.CharField(max_length = 100, null = True, blank=True, default = '')
    observation = models.CharField(max_length = 100, null = True, blank=True, default = '')
    type = models.IntegerField(choices = TypeFacture, default = 2)
    statut =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat =   models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now = True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_typefactureclient_rri', null = True, blank = True)

    def __str__(self):
        return self.designation

class Model_CategorieRH(models.Model):
    designation             =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    description             =   models.TextField(max_length = 100, null = True, blank=True, default = '')
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    update_date             =   models.DateTimeField(auto_now=True)
    creation_date           =   models.DateTimeField(auto_now_add = True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_categories_rh', null = True, blank = True)

    def __str__(self):
        return self.designation

class Model_EchelonRH(models.Model):
    designation             =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    description             =   models.TextField(max_length = 100, null = True, blank=True, default = '')
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                    =   models.CharField(max_length=50, blank=True, null=True)
    update_date             =   models.DateTimeField(auto_now=True)
    creation_date           =   models.DateTimeField(auto_now_add = True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_echelons_rh', null = True, blank = True)

    def __str__(self):
        return self.designation

class Model_StatusRH(models.Model):
    designation             =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    etat                    =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    description             =   models.TextField(max_length = 100, null = True, blank=True, default = '')
    statut                  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    update_date             =   models.DateTimeField(auto_now=True)
    creation_date           =   models.DateTimeField(auto_now_add = True)
    auteur                  =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_statuts_rh', null = True, blank = True)

    def __str__(self):
        return self.designation

class Model_CompteBanque_Employe(models.Model):
    designation = models.CharField(max_length = 100, null = True, blank=True, default = '')
    banque = models.ForeignKey("Model_Banque", on_delete = models.SET_NULL, related_name = 'banque_compte_banque_employe', null = True, blank = True)
    description = models.CharField(max_length = 250, null = True, blank=True, default = '')
    numero_compte = models.CharField(max_length=50, null = True, blank = True, default ='')
    type_compte = models.CharField(max_length=50, null=True, blank = True, default="")
    repartition = models.IntegerField(null = True, blank = True)
    mode_paiement = models.CharField(max_length=100, null=True, blank = True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now = True)
    statut =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat =   models.CharField(max_length=50, blank=True, null=True)
    profilrh =    models.ForeignKey("Model_ProfilRH", on_delete = models.SET_NULL, related_name="profil_employe_compte_banciare", null = True, blank = True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_compte_banque_employe', null = True, blank = True)

    def __str__(self):
        return self.numero_compte

    @property
    def rib_banque_designation(self):
        try:
            rib = Model_Rib.objects.filter(comptebanque = self.id).first()
            return rib.banque
        except Exception as e:
            return None

    @property
    def rib_info(self):
        try:
            rib = Model_Rib.objects.filter(comptebanque = self.id).first()
            return rib
        except Exception as e:
            return None

class Model_Rib(models.Model):
    comptebanque = models.ForeignKey("Model_CompteBanque_Employe", on_delete = models.CASCADE, related_name="compte_bancaire_employe", null = True, blank = True)
    banque = models.ForeignKey("Model_Banque", on_delete = models.SET_NULL, related_name = 'banque_rib', null = True, blank = True)
    cle_rib =   models.IntegerField(null = True, blank = True)
    statut =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat =   models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now = True)
    pays = models.ForeignKey("Model_Place", on_delete = models.SET_NULL, related_name = 'pays', null = True, blank = True)
    code_guichet =   models.CharField(max_length=50, blank=True, null=True)
    nom_guichet =   models.CharField(max_length=100, blank=True, null=True)
    titulaire_compte = models.CharField(max_length = 100, null = True, blank=True, default = '')
    iban = models.CharField(max_length=100, blank=True, null=True)
    bic = models.CharField(max_length=100, blank=True, null=True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_rib_compte_bancaire', null = True, blank = True)

    def __str__(self):
        return '{} / {} / {}'.format(self.titulaire_compte, self.cle_rib, self.numero_compte)

    @property
    def numero_compte(self):
        return self.comptebanque.numero_compte if self.comptebanque else "Aucun"

class Model_DossierPaie(models.Model):
    mois = models.IntegerField(choices = MoisAnnee, default = 1)
    annee = models.CharField(max_length = 100, null = True, blank=True, default = '')
    date_dossier = models.DateTimeField(null = True, blank=True)
    date_fin = models.DateTimeField(null = True, blank=True)
    est_actif = models.BooleanField(default = False)
    est_cloture =   models.BooleanField(default = False)
    est_calcul = models.BooleanField(default = False)
    etat    =   models.CharField(max_length = 100, null = True, blank=True, default = '')
    statut  =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    update_at = models.DateTimeField(auto_now = True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_periodepaie_vxu', null = True, blank = True)
    def __str__(self):
        return '{} {}'.format(self.value_mois, self.annee)

    @property
    def value_mois(self):
        return dict(MoisAnnee)[int(self.mois)]


class Temp_EcritureComptable(models.Model):
    designation                 =    models.CharField(max_length = 100, null = True, blank=True, default = '')
    montant_credit              =    models.FloatField()
    montant_debit               =    models.FloatField()
    date_echeance               =    models.DateTimeField(null=True)
    est_lettre                  =    models.BooleanField(default=False)
    compte                      =    models.ForeignKey(Model_Compte, on_delete = models.SET_NULL, related_name="temp_compte_of_ecriture", null = True, blank = True)
    lettrage                    =    models.ForeignKey("Model_Lettrage", on_delete = models.SET_NULL, related_name="temp_lettrage_ecriture_comptable", null = True, blank = True)
    piece_comptable             =    models.ForeignKey(Model_PieceComptable, on_delete = models.CASCADE, related_name="temp_piece_comptable_of_ecriture", null = True, blank = True)
    lot_bulletin                =    models.ForeignKey("Model_LotBulletins", on_delete = models.CASCADE, related_name="lot_bulletin_of_temp", null = True, blank = True)
    dossier_paie                =    models.ForeignKey("Model_DossierPaie", on_delete = models.CASCADE, related_name="dossier_paie_of_ecriture", blank=True, null=True)
    annee_fiscale               =    models.ForeignKey("Model_Annee_fiscale", on_delete = models.SET_NULL, related_name="temp_annee_fiscale_ecriture", null = True, blank = True)
    statut                      =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                        =    models.CharField(max_length=50, blank=True, null=True)
    update_date                 =    models.DateTimeField(auto_now=True)
    date_creation               =    models.DateTimeField(auto_now_add = True)
    auteur                      =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="temp_auteur_of_ecriture", null = True, blank = True)
    url                         =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation

    @property
    def separateur_montant_credit(self):
        return AfficheEntier(float(self.montant_credit))

    @property
    def separateur_montant_debit(self):
        return AfficheEntier(float(self.montant_debit))

    @property
    def debit(self):
        piece = self.piece_comptable
        if piece.taux == None: return "%.2f" % self.montant_debit
        else:
            montant = self.montant_debit / piece.taux.montant
            return "%.2f" % montant
    @property
    def separateur_debit(self):
        return AfficheEntier(float(self.debit))


    @property
    def credit(self):
        piece = self.piece_comptable
        if piece.taux == None: return "%.2f" % self.montant_credit
        else:
            montant = self.montant_credit / piece.taux.montant
            return "%.2f" % montant
    @property
    def separateur_credit(self):
        return AfficheEntier(float(self.credit))


class Model_Type_Diplome(models.Model):
    designation     =   models.CharField(max_length = 250, null = True, blank=True, default = '')
    description     =   models.CharField(max_length = 250, null = True, blank=True, default = '')
    numero_reference =    models.IntegerField(null = True, blank=True)
    statut          =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat            =   models.CharField(max_length=50, blank=True, null=True)
    auteur          =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_type_diplome", null = True, blank = True)
    created_at      =   models.DateTimeField(auto_now = True)
    update       =   models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.designation

class Model_Diplome(models.Model):
    designation     =   models.CharField(max_length = 250, null = True, blank=True, default = '')
    description     =   models.CharField(max_length = 500, null = True, blank=True, default = '')
    type            =   models.ForeignKey("Model_Type_Diplome", on_delete=models.SET_NULL, blank=True, null=True)
    institution     =   models.CharField(max_length = 250, null = True, blank=True, default = '')
    statut          =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat            =   models.CharField(max_length=50, blank=True, null=True)
    auteur          =   models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_diplome", null = True, blank = True)
    created_at      =   models.DateTimeField(auto_now = True)
    update_at       =   models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.designation



class Model_TypeMarche(models.Model):
	designation = models.CharField(max_length = 100, null = True, blank=True, default = '')
	code = models.CharField(max_length = 10, null = True, blank=True, default = '')
	statut =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
	etat            =   models.CharField(max_length=50, blank=True, null=True)
	description = models.CharField(max_length = 500, null = True, blank=True, default = '')
	url_interne = models.CharField(max_length=200, blank=True, null=True)
	created_at = models.DateTimeField()
	update_at = models.DateTimeField(auto_now = True)
	auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_typemarche_avo', null = True, blank = True)
	def __str__(self):
		return self.designation

	@property
	def nbcontrat(self):
		lettre = Model_Contrat.objects.filter(type_marche_id = self.id).count()
		return lettre

	@property
	def nbLettreC(self):
		lettre = Model_Lettre_commande.objects.filter(type_marche_id = self.id).count()
		return lettre

	@property
	def nbdemandeCot(self):
		Demande = Model_Demande_cotation.objects.filter(type_marche_id = self.id).count()
		return Demande


class Model_Lettre_commande(models.Model):
	numero_reference = models.CharField(max_length = 100, null = True, blank=True, default = '')
	intitule = models.CharField(max_length = 100, null = True, blank=True, default = '')
	financement = models.CharField(max_length = 100, null = True, blank=True, default = '')
	nombre_lots = models.IntegerField(default = 0)
	demande_achat = models.ForeignKey(Model_Demande_achat, on_delete = models.SET_NULL, related_name = 'demande_achat_fk_fcl', null = True, blank = True)
	fournisseur = models.ForeignKey(Model_Fournisseur, on_delete = models.SET_NULL, related_name = 'fournisseur_fk_lc', null = True, blank = True)
	montant = models.FloatField()
	devise = models.ForeignKey(Model_Devise, on_delete = models.SET_NULL, related_name = 'devise_fk_nrp', null = True, blank = True)
	type_marche = models.ForeignKey(Model_TypeMarche, on_delete = models.SET_NULL, related_name = 'type_marche_fk_bnl', null = True, blank = True)
	statut =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
	etat   =   models.CharField(max_length=50, blank=True, null=True)
	description = models.CharField(max_length = 500, null = True, blank=True, default = '')
	created_at = models.DateTimeField()
	update_at = models.DateTimeField(auto_now = True)
	auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_lettre_commande_kdn', null = True, blank = True)
	def __str__(self):
		return self.numero_reference

class Model_Demande_cotation(models.Model):
	numero_reference = models.CharField(max_length = 100, null = True, blank=True, default = '')
	intitule = models.CharField(max_length = 100, null = True, blank=True, default = '')
	financement = models.CharField(max_length = 100, null = True, blank=True, default = '')
	nombre_lots = models.IntegerField(default = 0)
	demande_achat = models.ForeignKey(Model_Demande_achat, on_delete = models.SET_NULL, related_name = 'demande_achat_fk_plg', null = True, blank = True)
	montant = models.FloatField()
	devise = models.ForeignKey(Model_Devise, on_delete = models.SET_NULL, related_name = 'devise_fk_dvi', null = True, blank = True)
	fournisseur = models.ForeignKey(Model_Fournisseur, on_delete = models.SET_NULL, related_name = 'fournisseur_fk_gtn', null = True, blank = True)
	type_marche = models.ForeignKey(Model_TypeMarche, on_delete = models.SET_NULL, related_name = 'type_marche_fk_wag', null = True, blank = True)
	statut =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
	etat   =   models.CharField(max_length=50, blank=True, null=True)
	description = models.CharField(max_length = 500, null = True, blank=True, default = '')
	created_at = models.DateTimeField()
	update_at = models.DateTimeField(auto_now = True)
	auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_demande_cotation_gvb', null = True, blank = True)
	def __str__(self):
		return self.numero_reference
class Model_Contrat(models.Model):
	numero_reference = models.CharField(max_length = 100, blank=True, null=True)
	objet = models.CharField(max_length = 100, null = True, blank=True, default = '')
	montant = models.FloatField()
	modalite = models.CharField(max_length = 500, null = True, blank=True, default = '')
	appel_offre = models.ForeignKey(Model_Avis_appel_offre, on_delete = models.SET_NULL, related_name = 'appel_offre_dk', null = True, blank = True)
	demande_cotation = models.ForeignKey(Model_Demande_cotation, on_delete = models.SET_NULL, related_name = 'demande_cotation_fk', null = True, blank = True)
	devise = models.ForeignKey(Model_Devise, on_delete = models.SET_NULL, related_name = 'devise_fk_ooi', null = True, blank = True)
	type_marche = models.ForeignKey(Model_TypeMarche, on_delete = models.SET_NULL, related_name = 'type_marche_of_contrat', null = True, blank = True)
	date_debut = models.DateTimeField(blank=True, null=True)
	date_fin = models.DateTimeField(blank=True, null=True)
	fournisseur = models.ForeignKey(Model_Fournisseur, on_delete = models.SET_NULL, related_name = 'fournisseur_contrat_gtn', null = True, blank = True)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
	document_id = models.IntegerField(default = 0)
	statut =   models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
	etat   =   models.CharField(max_length=50, blank=True, null=True)
	created_at = models.DateTimeField()
	update_at = models.DateTimeField(auto_now = True)
	auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_contrat_soh', null = True, blank = True)
	def __str__(self):
		return self.numero_reference

	@property
	def operations(self):
		return Model_OperationContrat.objects.filter(contrat = self)


	@property
	def solde(self):
		"Les opérations de contrat se font sur la valeur du montant du contrat, tjrs!"
		value = 0
		for operation in self.operations:
			if operation.categorie == 2:#Avenant positif
				if operation.type == 2: value += self.montant*operation.valeur /100
				else: value += operation.valeur
			else:#Une facture et un avenant négatif viennent diminuer les sous
				if operation.type == 2: value -= self.montant*operation.valeur /100
				else:value -= operation.valeur
		return self.montant + value

	@property
	def totalconsome(self):
		"Pour Trouver le Total à Consomer dans le Contrat"
		return self.montant - float(self.solde)



class Model_OperationContrat(models.Model):
    designation = models.CharField(max_length = 100, null = True, blank=True, default = '')
    contrat    = models.ForeignKey(Model_Contrat, on_delete=models.CASCADE, related_name="contrat_of_op", blank=True, null=True)
    categorie  = models.IntegerField(choices= CategorieOperation, default=1)
    type       = models.IntegerField(choices= TypeOperation,default = 1)
    valeur    = models.FloatField(default = 0)
    devise = models.ForeignKey(Model_Devise, on_delete = models.SET_NULL, related_name = 'devise_ddfk_ooi', null = True, blank = True)
    reference_document = models.CharField(max_length = 100, null = True, blank=True, default = '')
    description = models.CharField(max_length = 500, null = True, blank=True, default = '')
    created_at = models.DateTimeField()
    update_at = models.DateTimeField(auto_now = True)
    auteur = models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_dde_model_contrat_soh', null = True, blank = True)

    def __str__(self):
        return f"{self.contrat.numero_reference} {self.designation}"

    def value_categorie(self):
        return dict(CategorieOperation)[int(self.categorie)]

    def value_type(self):
        return dict(TypeOperation)[int(self.type)]

class Model_Type_service(models.Model):
	designation    =    models.CharField(default = 100, max_length = 100, verbose_name = "Designation" )
	designation_courte    =    models.CharField(default = 100, max_length = 100, null = True, blank = True, verbose_name = "Designation courte")
	description    =    models.CharField(default = 510, max_length = 510, null = True, blank = True, verbose_name = "Description")
	statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True)
	etat    =    models.CharField(max_length=50, blank=True, null=True)
	creation_date    =    models.DateTimeField(auto_now_add = True)
	update_date    =    models.DateTimeField(auto_now = True)
	auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_type_service', null = True, blank = True)

	def __str__(self):
		return self.designation

	class Meta:
		verbose_name = 'Type de service'
		verbose_name_plural = 'Types de service'



#QUERY
class Model_Query(models.Model):
    title    =    models.CharField(max_length = 100, verbose_name = "Titre", blank=True, null = True )
    is_chart    =    models.BooleanField(default = True)
    is_card    =    models.BooleanField(default = False)
    model_chart  =  models.IntegerField(choices = choixGraphique, default = 0, null = True, blank = True)
    query_string    =    models.CharField(default = "", max_length = 1000, verbose_name = "Requête SQL DataTable" )
    query_graphic = models.CharField(default = "", max_length = 1000, verbose_name = "Requête SQL Graphic" )
    query_card = models.CharField(default = "", max_length = 1000, verbose_name = "Requête SQL Card" )
    select    =    models.CharField(default = "*", max_length = 1000, null = True, blank = True, verbose_name = "Selection")
    filter    =    models.CharField(default = "", max_length = 1000, null = True, blank = True, verbose_name = "Filtrage")
    main_model    =    models.ForeignKey(ContentType, on_delete=models.SET_NULL, blank=True, null=True)
    measure_function     =    models.CharField(default = "", max_length = 1000, null = True, blank = True, verbose_name = "Graphic: Fonction de mesure ")
    measure_attribute    =    models.CharField(default = "", max_length = 1000, null = True, blank = True, verbose_name = "Graphic:Attribut de mesure")
    dimension     =    models.CharField(default = "", max_length = 1000, null = True, blank = True, verbose_name = "Dimensions")
    card_function     =    models.CharField(default = "", max_length = 1000, null = True, blank = True, verbose_name = "Card: Fonction de mesure")
    card_attribute    =    models.CharField(default = "", max_length = 1000, null = True, blank = True, verbose_name = "Card:  Attribut de mesure")
    is_success    =    models.BooleanField(default = True)
    created_at    =    models.DateTimeField(auto_now_add = True)
    updated_at    =    models.DateTimeField(auto_now = True)
    auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_query', null = True, blank = True)

    def __str__(self):
        return self.title
class Model_Rebut(models.Model):
    numero                   =   models.CharField(max_length=25)
    date                     =   models.DateTimeField(auto_now_add=True)
    article                  =   models.ForeignKey(Model_Article, on_delete=models.CASCADE, related_name="_rebut_article")
    serie_article            =   models.ForeignKey(Model_Asset, on_delete=models.SET_NULL, blank=True, null=True, related_name="_serie_rebut")
    quantite                 =   models.FloatField()
    unite                    =   models.ForeignKey(Model_Unite, on_delete=models.SET_NULL, blank=True, null=True, related_name="_unite_rebut")
    emplacement              =   models.ForeignKey(Model_Emplacement, on_delete=models.CASCADE, related_name="_emplacement_rebut")
    emplacement_rebut        =   models.ForeignKey(Model_Emplacement, on_delete=models.CASCADE, related_name="_emplacement_rebut_destination")
    type_operation           =   models.ForeignKey(Model_OperationStock, on_delete=models.CASCADE, related_name="rebut_operation", blank=True, null=True)
    document                 =   models.CharField(max_length=25, blank=True, null=True)
    statut                   =    models.ForeignKey("Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True, related_name="inventaire_statut_rebut")
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    creation_date            =    models.DateTimeField(auto_now = True)
    update_date              =    models.DateTimeField(auto_now=True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="_auteur_rebut_stock", null = True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.numero

class Model_Combinaison(models.Model):
    externe_id        =    models.IntegerField(null=True, blank=True)
    compte            =    models.CharField(max_length = 300, null = True, blank = True)
    segment_3         =    models.CharField(max_length = 300, null = True, blank = True)
    segment_4         =    models.CharField(max_length = 300, null = True, blank = True)
    segment_5         =    models.CharField(max_length = 300, null = True, blank = True)
    segment_6         =    models.CharField(max_length = 300, null = True, blank = True)
    segment_7         =    models.CharField(max_length = 300, null = True, blank = True)
    segment_8         =    models.CharField(max_length = 300, null = True, blank = True)
