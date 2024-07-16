from __future__ import unicode_literals
from ErpBackOffice.models import Model_Budget, Model_Unite_fonctionnelle, Model_Exercicebudgetaire, Model_LigneBudgetaire
from django.db.models import Max
from django.utils import timezone

class dao_budget(object):
    id = 0
    designation = ""
    devise_id =""
    categoriebudget_id = 0
    #unite_fonctionnelle_id = 0

    @staticmethod
    def toListBudget():
        return Model_Budget.objects.all().order_by('-id')


    @staticmethod
    def toListBudgetByAuteur(user_id):
        return Model_Budget.objects.filter(auteur_id=user_id)

    @staticmethod
    def toCreateBudget(designation, categoriebudget_id = 0, devise_id=0):
        try:
            budget = dao_budget()
            budget.designation = designation
            budget.devise_id = devise_id
            #budget.unite_fonctionnelle_id = unite_fonctionnelle_id
            budget.categoriebudget_id = categoriebudget_id

            return budget
        except Exception as e :
            # print("Erreur lors de la création d'un budget : ")
            # print(e)
            return None

    @staticmethod
    def toSaveBudget(auteur, objet_dao_budget):
        try:
            budget = Model_Budget()
            budget.designation = objet_dao_budget.designation
            budget.devise_id = objet_dao_budget.devise_id
            budget.categoriebudget_id = objet_dao_budget.categoriebudget_id
            budget.auteur_id = auteur.id
            budget.save()
            return budget
        except Exception as e:
            # print("Erreur lors de l'enregistrement d'un budget")
            # print(e)
            return False

    @staticmethod
    def toUpdateBudget(id, objet_budget):
        try:
            budget = Model_Budget.objects.get(pk = id)
            budget.designation = objet_budget.designation
            budget.devise_id = objet_budget.devise_id
            #budget.unite_fonctionnelle_id = objet_budget.unite_fonctionnelle
            #budget.auteur = auteur

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
    def toListBudgetRecettes():
        try:
            return  Model_Budget.objects.filter(categoriebudget__type = 1)

        except Exception as e:
            #print("Erreur lors de la suppression d'un budget")
            #print(e)
            return None

    @staticmethod
    def toListBudgetDepenses():
        try:
            return  Model_Budget.objects.filter(categoriebudget__type = 2)
        except Exception as e:
            #print("Erreur lors de la suppression d'un budget")
            #print(e)
            return None

    @staticmethod
    def toListBudgetProjets():
        try:
            return  Model_Budget.objects.get()
        except Exception as e:
            #print("Erreur lors de la suppression d'un budget")
            #print(e)
            return None

    """@staticmethod
    def toGetBudgetOfUnite_Fonctionnelle(unite_fonctionnelle_id):
        try:
            return Model_Budget.objects.filter(unite_fonctionnelle_id = unite_fonctionnelle_id).order_by('date_debut')
        except Exception as e:
            #print("Erreur lors de l'obtention du(des) budget(s) correspondant au département")
            #print(e)
            return None"""

    @staticmethod
    def toComputeBudget(type):
        resultat = {
                'prevision':0,
                'realisation':0,
                'ecart':0
                }
        try:
            prevision = 0
            realisation = 0

            budgets = Model_Budget.objects.filter(categoriebudget__type = type)
            for budget in budgets:
                #print("on budget", budget)
                prevision += float(budget.solde)
                lignes = Model_LigneBudgetaire.objects.filter(budget = budget)
                for ligne in lignes:
                    realisation += float(ligne.valeur_total_consommee)

            resultat['prevision'] = prevision
            resultat['realisation'] = realisation
            resultat['ecart'] = prevision - realisation

            return  resultat
        except Exception as e:
            #print("Erreur lors du calcul")
            #print(e)
            return resultat

