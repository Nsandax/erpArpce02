from __future__ import unicode_literals
from ErpBackOffice.models import Model_Budget, Model_Unite_fonctionnelle
from django.db.models import Max
from django.utils import timezone

class dao_budget(object):
    id = 0
    designation = ""
    unite_fonctionnelle = None
    annee = 0
    solde = 0
    date_debut = timezone.now()
    date_fin = timezone.now()

    @staticmethod
    def toListBudget():
        return Model_Budget.objects.all().order_by('-id')

    @staticmethod
    def toCreateBudget(designation, annee, date_debut, date_fin, solde = 0, unite_fonctionnelle = None):
        try:
            budget = dao_budget()
            budget.designation = designation
            budget.annee = annee
            budget.date_debut = date_debut
            budget.date_fin = date_fin
            budget.solde = solde
            budget.unite_fonctionnelle = unite_fonctionnelle

            return budget
        except Exception as e :
            #print("Erreur lors de la création d'un budget : ")
            #print(e)
            return None

    @staticmethod
    def toSaveBudget(auteur, objet_dao_budget):
        try:
            budget = Model_Budget()
            budget.designation = objet_dao_budget.designation
            budget.annee = objet_dao_budget.annee
            budget.date_debut = objet_dao_budget.date_debut
            budget.date_fin = objet_dao_budget.date_fin
            budget.solde = objet_dao_budget.solde
            budget.unite_fonctionnelle = objet_dao_budget.unite_fonctionnelle
            budget.auteur = auteur.id

            budget.save()
            return True

        except Exception as e:
            #print("Erreur lors de l'enregistrement d'un budget")
            #print(e)
            return False

    @staticmethod
    def toUpdateBudget(id, objet_budget):
        try:
            budget = Model_Budget.objects.get(pk = id)
            budget.designation = objet_budget.designation
            budget.annee = objet_budget.annee
            budget.date_debut = objet_budget.date_debut
            budget.date_fin = objet_budget.date_fin
            budget.solde = objet_budget.solde
            budget.unite_fonctionnelle = objet_budget.unite_fonctionnelle

            budget.save()
            return True

        except Exception as e:
            #print("Erreur lors de la modification d'un budget")
            #print(e)
            return False

    @staticmethod
    def toGetBudget(id):
        try:
            return Model_Budget.objects.get(pk = id)
        except Exception as e:
            #print("Erreur lors de l'obtention d'un budget")
            #print(e)
            return None

    @staticmethod
    def toDeleteBudget(id):
        try:
            budget = Model_Budget.objects.get(pk = id)
            budget.delete()
            return True
        except Exception as e:
            #print("Erreur lors de la suppression d'un budget")
            #print(e)
            return False

    @staticmethod
    def toGetBudgetOfUnite_Fonctionnelle(unite_fonctionnelle_id):
        try:
            return Model_Budget.objects.filter(unite_fonctionnelle = unite_fonctionnelle_id).order_by('date_debut')
        except Exception as e:
            #print("Erreur lors de l'obtention du(des) budget(s) correspondant au département")
            #print(e)
            return None

