from __future__ import unicode_literals
from ErpBackOffice.models import Model_LigneBudgetaire
from django.db.models import Max
from django.utils import timezone


class dao_ligne_budgetaire(object):
    id = 0
    code = ""
    responsable 	= None
    designation = ""
    budget = None
    solde = 0
    date_debut = timezone.now()
    date_fin = timezone.now()

    @staticmethod
    def toCreateLigneBudgetaire(code, designation, date_debut, date_fin, budget, responsable, solde = 0):
        try:
            ligne = dao_ligne_budgetaire()
            ligne.code = code
            ligne.designation = designation
            ligne.budget = budget
            ligne.responsable = responsable
            ligne.solde = solde
            ligne.date_debut = date_debut
            ligne.date_fin = date_fin

            return ligne
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE LA LIGNE BUDGETAIRE")
            #print(e)
            return None

    @staticmethod
    def toSaveLigneBudgetaire(auteur, objet_dao_ligne_budgetaire):
        try :
            ligne = Model_LigneBudgetaire()
            ligne.code = objet_dao_ligne_budgetaire.code
            ligne.designation = objet_dao_ligne_budgetaire.designation
            ligne.budget = objet_dao_ligne_budgetaire.budget
            ligne.responsable = objet_dao_ligne_budgetaire.responsable
            ligne.solde = objet_dao_ligne_budgetaire.solde
            ligne.date_debut = objet_dao_ligne_budgetaire.date_debut
            ligne.date_fin = objet_dao_ligne_budgetaire.date_fin

            ligne.auteur = auteur

            ligne.save()
            return ligne
        except Exception as e:
            #print("ERREUR SAVE LIGNE BUDGETAIRE")
            #print(e)
            return None

    @staticmethod
    def toUpdateLigneBudgetaire(id, objet_dao_ligne_budgetaire):
        try:
            ligne = Model_LigneBudgetaire.objects.get(pk = id)
            ligne.code = objet_dao_ligne_budgetaire.code
            ligne.designation = objet_dao_ligne_budgetaire.designation
            ligne.budget = objet_dao_ligne_budgetaire.budget
            ligne.responsable = objet_dao_ligne_budgetaire.responsable
            ligne.solde = objet_dao_ligne_budgetaire.solde
            ligne.date_debut = objet_dao_ligne_budgetaire.date_debut
            ligne.date_fin = objet_dao_ligne_budgetaire.date_fin
            ligne.auteur = objet_dao_ligne_budgetaire.auteur

            ligne.save()
            return True
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return False

    @staticmethod
    def toGetLigneBudgetaire(id):
        try:
            return Model_LigneBudgetaire.objects.get(pk = id)
        except Exception as e:
            return None


    @staticmethod
    def toDeleteLigneBudgetaire(id):
        try:
            ligne = Model_LigneBudgetaire.objects.get(pk = id)
            ligne.delete()
            return True
        except Exception as e:
            return False

    @staticmethod
    def toListLigneBudgetaires():
        try:
            lignes = Model_LigneBudgetaire.objects.all().order_by('-id')
            return lignes
        except Exception as e:
            return None

    @staticmethod
    def toListLigneOfBudgets(id):
        try:
            lignes = Model_LigneBudgetaire.objects.filter(budget = id)
            return lignes
        except Exception as e:
            return None

    @staticmethod
    def toGetLigneOfCode(code):
        try:
            ligne = Model_LigneBudgetaire.objects.get(code = code)
            return ligne
        except Exception as e:
            return None
