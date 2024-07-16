from __future__ import unicode_literals
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from ErpBackOffice.utils.utils import utils
from ErpBackOffice.models import Model_Dependant, Model_Employe, Model_DossierPaie
from django.utils import timezone
from datetime import datetime, date
from calendar import monthrange
from ModulePayroll.dao.dao_rubrique import dao_rubrique
from ModuleRessourcesHumaines.dao.dao_pret import dao_pret
from ModuleRessourcesHumaines.dao.dao_ligne_paiement_pret import dao_ligne_paiement_pret

class function_constante(object):

    @staticmethod
    def salaireCategorieEchelon(employe_id):
        try:
            valeur = 0.0
            employe = Model_Employe.objects.get(pk = employe_id)
            valeur = employe.categorie_employe.salaire_base
            return valeur
        except Exception as e:
            #print("ERREUR salaireCategorieEchelon")
            #print(e)
            return 0.0

    @staticmethod
    def ancienneteEmploye(employe_id):
        try:
            valeur = 0
            employe = Model_Employe.objects.get(pk = employe_id)
            year = timezone.now().year
            valeur = int(year) - int(employe.profilrh.date_engagement.year)
            return valeur
        except Exception as e:
            #print("ERREUR ancienneteEmploye")
            #print(e)
            return 0

    @staticmethod
    def anciennetePoste(employe_id):
        try:
            valeur = 0
            employe = Model_Employe.objects.get(pk = employe_id)
            year = timezone.now().year
            #A définir
            valeur = int(year) - int(employe.profilrh.date_engagement.year)
            return valeur
        except Exception as e:
            #print("ERREUR anciennetePoste")
            #print(e)
            return 0

    @staticmethod
    def ageEmploye(employe_id):
        try:
            valeur = 0
            employe = Model_Employe.objects.get(pk = employe_id)
            today = date.today()
            born = employe.date_naissance
            rest = 1 if (today.month, today.day) < (born.month, born.day) else 0
            valeur = today.year - born.year - rest
            return valeur
        except Exception as e:
            #print("ERREUR ageEmploye")
            #print(e)
            return 0

    @staticmethod
    def numeroClassification(employe_id):
        try:
            valeur = 0
            employe = Model_Employe.objects.get(pk = employe_id)
            valeur = int(employe.poste.classification_pro.numero_reference)
            return valeur
        except Exception as e:
            #print("ERREUR numeroClassification")
            #print(e)
            return 0

    @staticmethod
    def nombreEnfantMineurEmploye(employe_id):
        try:
            dependant = Model_Dependant.objects.filter(employe_id = employe_id, type_dependance = 'enfant')
            nombre = 0
            year = timezone.now().year
            for item in dependant:
                age = int(year) - int(item.date_naissance.year)
                if age < 18:
                    nombre += 1
                else: nombre += 0
            return nombre
        except Exception as e:
            #print("ERREUR nombreEnfantMineurEmploye")
            #print(e)
            return 0

    @staticmethod
    def nombreEnfantPetitEmploye(employe_id):
        try:
            dependant = Model_Dependant.objects.filter(employe_id = employe_id, type_dependance = 'enfant')
            nombre = 0
            year = timezone.now().year
            for item in dependant:
                age = int(year) - int(item.date_naissance.year)
                if age < 15:
                    nombre += 1
                else: nombre += 0
            return nombre
        except Exception as e:
            #print("ERREUR nombreEnfantPetitEmploye")
            #print(e)
            return 0

    @staticmethod
    def nombreEnfantScolarisable(employe_id):
        try:
            dependant = Model_Dependant.objects.filter(employe_id = employe_id, type_dependance = 'enfant')
            nombre = 0
            year = timezone.now().year
            for item in dependant:
                age = int(year) - int(item.date_naissance.year)
                if age > 5 and age < 22:
                    nombre += 1
                else: nombre += 0
            return nombre
        except Exception as e:
            #print("ERREUR nombreEnfantScolarisable")
            #print(e)
            return 0

    @staticmethod
    def nombrePartEmploye(employe_id):
        try:
            nombre_part = 0
            part_agent = 1
            part_conjoint = 1
            dependant = Model_Dependant.objects.filter(employe_id = employe_id)
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

    @staticmethod
    def typeDiplomeEmploye(employe_id):
        try:
            valeur = 0
            employe = Model_Employe.objects.get(pk = employe_id)
            valeur = int(employe.diplome.type.numero_reference)
            return valeur
        except Exception as e:
            #print("ERREUR typeDiplomeEmploye")
            #print(e)
            return 0

    @staticmethod
    def localisationPosteEmploye(employe_id):
        try:
            valeur = 0
            employe = Model_Employe.objects.get(pk = employe_id)
            valeur = int(employe.poste.localisation.id)
            #valeur = int(employe.poste.lieu_exercice.lieu.id)
            return valeur
        except Exception as e:
            #print("ERREUR localisationPosteEmploye")
            #print(e)
            return 0

    @staticmethod
    def anneeEncours():
        try:
            year = timezone.now().year
            valeur = int(year)
            return valeur
        except Exception as e:
            #print("ERREUR anneeEncours")
            #print(e)
            return 0

    @staticmethod
    def dateDuJour():
        try:
            date_now = timezone.now()
            date_now = datetime.fromtimestamp(date_now)
            return date_now
        except Exception as e:
            #print("ERREUR dateDuJour")
            #print(e)
            return 0

    @staticmethod
    def anneeEngagementEmploye(employe_id):
        try:
            valeur = 0
            employe = Model_Employe.objects.get(pk = employe_id)
            valeur = int(employe.profilrh.date_engagement.year)
            return valeur
        except Exception as e:
            #print("ERREUR anneeEngagementEmploye")
            #print(e)
            return 0

    @staticmethod
    def dateEngagementEmploye(employe_id):
        try:
            employe = Model_Employe.objects.get(pk = employe_id)
            date_engagement = employe.profilrh.date_engagement
            date_engagement = datetime.fromtimestamp(date_engagement)
            return date_engagement
        except Exception as e:
            #print("ERREUR dateEngagementEmploye")
            #print(e)
            return 0

    @staticmethod
    def dateNaissanceEmploye(employe_id):
        try:
            employe = Model_Employe.objects.get(pk = employe_id)
            date_de_naissance = employe.date_de_naissance
            date_de_naissance = datetime.fromtimestamp(date_de_naissance)
            return date_de_naissance
        except Exception as e:
            #print("ERREUR dateNaissanceEmploye")
            #print(e)
            return 0

    @staticmethod
    def genreEmploye(employe_id):
        try:
            employe = Model_Employe.objects.get(pk = employe_id)
            genre = employe.profilrh.genre
            sexe = 1
            if genre == "M" or genre == "Masculin" : sexe = 1
            elif genre == "F" or genre == "Feminin" : sexe = 2
            else: raise Exception()
            return sexe
        except Exception as e:
            #print("ERREUR genreEmploye")
            #print(e)
            return 1

    @staticmethod
    def etatCivilEmploye(employe_id):
        try:
            employe = Model_Employe.objects.get(pk = employe_id)
            etat_civil = employe.profilrh.etat_civil
            if etat_civil == "M" or etat_civil == "Marié(e)" or etat_civil == "Marié" : etat_civil = 1
            elif etat_civil == "Célibataire" or etat_civil == "Celibataire" or etat_civil == "C": etat_civil = 2
            else: raise Exception()
            return etat_civil
        except Exception as e:
            #print("ERREUR etatCivilEmploye")
            #print(e)
            return 1

    @staticmethod
    def firstDayExerciceEncours():
        try:
            exerciceEncours = Model_DossierPaie.objects.filter(est_actif = True).first()
            date_debut = exerciceEncours.date_dossier
            date_debut = datetime.fromtimestamp(date_debut)
            return date_debut
        except Exception as e:
            #print("ERREUR firstDayExerciceEncours")
            #print(e)
            return 0

    @staticmethod
    def lastDayExerciceEncours():
        try:
            exerciceEncours = Model_DossierPaie.objects.filter(est_actif = True).first()
            date_fin = exerciceEncours.date_fin
            date_fin = datetime.fromtimestamp(date_fin)
            return date_fin
        except Exception as e:
            #print("ERREUR lastDayExerciceEncours")
            #print(e)
            return 0

    @staticmethod
    def nbreJoursMoisEncours():
        try:
            exerciceEncours = Model_DossierPaie.objects.filter(est_actif = True).first()
            month = int(exerciceEncours.mois)
            year = int(exerciceEncours.annee)
            return monthrange(year, month)[1]
        except Exception as e:
            #print("ERREUR nbreJoursMoisEncours")
            #print(e)
            return 0


    @staticmethod
    def montantARembourser(employe_id):
        try:
            valeur = 0
            prets = dao_pret.toListPretOfEmploye(employe_id)
            for pret in prets:
                montant = pret.amount_to_pay if pret.is_running else 0
                valeur += montant

            return valeur
        except Exception as e:
            #print("ERREUR montantARembourser")
            #print(e)
            return 0


    @staticmethod
    def rubriquefonction(employe_id):
        Primefonc = 0
        try:
            employe = Model_Employe.objects.get(pk = employe_id)
            if employe.fonction == 'chef de bureau': Primefonc=100000
            elif employe.fonction == "chef de service" or employe.fonction == "chef d'antenne" : Primefonc=200000
            elif employe.fonction == "directeur" : Primefonc=300000
            return Primefonc
        except Exception as e:
            print("ERREUR rubriquefonction")
            print(e)
            return Primefonc


    @staticmethod
    def ancienneteAgent(employe_id, date_paye):
        try:
            valeur = 0
            employe = Model_Employe.objects.get(pk = employe_id)
            date_paye = date_paye
            date_engagement = employe.profilrh.date_engagement
            rest = 1 if (date_paye.month, date_paye.day) < (date_engagement.month, date_engagement.day) else 0
            valeur = date_paye.year - date_engagement.year - rest
            return valeur
        except Exception as e:
            print("ERREUR ageEmploye")
            print(e)
            return 0

    @staticmethod
    def rubriqueLogement(employe_id):
        Primelog = 0
        try:
            employe = Model_Employe.objects.get(pk = employe_id)
            if employe.grade.lower() == 'execution': Primelog = 75000
            elif employe.grade.lower() == "maitrise": Primelog = 100000
            elif employe.grade.lower() == "cadre" : Primelog = 150000
            return Primelog
        except Exception as e:
            print("ERREUR rubriqueLogement")
            print(e)
            return Primelog

    @staticmethod
    def rubriqueDiplome(employe_id):
        Primediplome = 0
        try:
            employe = Model_Employe.objects.get(pk = employe_id)
            if employe.cycle_diplome.lower() == 'sec1': Primediplome = 25000
            elif employe.cycle_diplome.lower()== "sec2": Primediplome = 50000
            elif employe.cycle_diplome.lower() == "sup" : Primediplome = 100000
            return Primediplome
        except Exception as e:
            print("ERREUR rubriqueDiplome")
            print(e)
            return Primediplome

    @staticmethod
    def rubriqueELoignement(employe_id):
        Primelog = 0
        try:
            employe = Model_Employe.objects.get(pk = employe_id)
            if employe.grade.lower() == 'cadre' : Primelog = 75000
            elif employe.grade.lower() == "maitrise": Primelog = 100000
            elif employe.grade.lower() == "execution" : Primelog = 150000
            return Primelog
        except Exception as e:
            print("ERREUR rubriqueELoignement")
            print(e)
            return Primelog

    @staticmethod
    def rubriqueCaisse(employe_id):
        Primelog = 0
        try:
            employe = Model_Employe.objects.get(pk = employe_id)
            if employe.fonction.lower() == "caissier secondaire": Primelog=50000
            elif employe.fonction.lower() == "caissier primaire": Primelog=100000
            return Primelog
        except Exception as e:
            print("ERREUR rubriqueCaisse")
            print(e)
            return Primelog


    @staticmethod
    def rubriqueINDTRANSP(employe_id):
        Primelog = 0
        try:
            employe = Model_Employe.objects.get(pk = employe_id)
            if employe.grade.lower() == 'cadre' : Primelog = 150000
            elif employe.grade.lower() == 'maitrise' : Primelog = 100000
            elif employe.grade.lower() == 'execution' : Primelog = 75000
            return Primelog
        except Exception as e:
            print("ERREUR rubriqueINDTRANSP")
            print(e)
            return Primelog


    @staticmethod
    def rubriquePRIREPRP(employe_id):
        Primelog = 0
        try:
            employe = Model_Employe.objects.get(pk = employe_id)
            if employe.grade.lower() == "chef d'antenne": Primelog=200000
            return Primelog
        except Exception as e:
            print("ERREUR rubriquePRIREPRP")
            print(e)
            return Primelog