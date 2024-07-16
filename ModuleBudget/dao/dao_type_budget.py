from __future__ import unicode_literals
from os import stat
from ErpBackOffice.models import Model_Budget, TypeBudget, Model_LigneBudgetaire, Model_Categoriebudget
from ModuleBudget.dao.dao_exercicebudgetaire import dao_exercicebudgetaire

class dao_type_budget(object):
    @staticmethod
    def toListTypeBudgets():
        list = []
        for key, value in TypeBudget:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list

    @staticmethod
    def toGetTypeBudget(id):
        list = dao_type_budget.toListTypeBudgets()
        for item in list:
            if item["id"] == id: return item
        return None

    @staticmethod
    def toGetVariable():
        return dao_type_budget.toGetTypeBudget(0)

    @staticmethod
    def toGetFixe():
        return dao_type_budget.toGetTypeBudget(1)

    @staticmethod
    def toGetTypeBudgetRecette():
        try:
            #Indicateurs
            somme_total, somme_engage, somme_realise, somme_consomme, somme_dispo, ladevise = 0, 0, 0, 0, 0, "CFA"
            lignes = Model_LigneBudgetaire.objects.filter(budget__categoriebudget__type = 1)
            # print("SHOW ME LIGNE", lignes)
            nature = []
            tempo = []
            others =[]
            for item in lignes:
                somme_total = somme_total + item.montant_alloue
                # print("SHOW ME somme_total", somme_total)
                somme_engage = somme_engage + float(item.valeur_engagement)
                somme_realise = somme_realise + float(item.valeur_reel)
                somme_consomme = somme_consomme + float(item.valeur_total_consommee)
                somme_dispo = somme_dispo + float(item.valeur_solde)
                ladevise = item.budget.devise.symbole_devise
                NaturebudgetDepenseR = Model_Budget.objects.filter(id = item.budget.id)
                for item in NaturebudgetDepenseR:
                    if not item.id in tempo:
                        tempo.append(item.id)
                        others.append(item)

            for ligne in others:
                item = {
                    "id": ligne.id,
                    "designation": ligne.designation,
                    "montant_alloue" : ligne.montant_alloue,
                    "devise": ligne.devise.symbole_devise
                }
                nature.append(item)                
            #Catégiories
            categories = Model_Categoriebudget.objects.filter(type = 1)
            # print("nature", nature)
            

            budget_recette = {
                'prevision' : somme_total,
                'engagement': somme_engage,
                'reel': somme_realise,
                'consommation': somme_consomme,
                'ecart': somme_dispo,
                'devise': ladevise,
                'categories': categories,
                'nature': nature
            }
            return budget_recette
        except Exception as e:
            # print("toGetTypeBudgetRecette", e)
            return None

    @staticmethod
    def toGetTypeBudgetDepense():
        try:
            somme_total, somme_engage, somme_realise, somme_consomme, somme_dispo, ladevise = 0, 0, 0, 0, 0, "CFA"
            exercice = dao_exercicebudgetaire.toGetActiveExercicebudgetaire()
            if exercice:
                lignes = Model_LigneBudgetaire.objects.filter(budget__categoriebudget__type = 2, exericebudgetaires__id=exercice.id)
            else: 
                lignes = Model_LigneBudgetaire.objects.filter(budget__categoriebudget__type = 2)
                
            somme_reaj = 0
            
            nature = []
            tempo = []
            others =[]
            for item in lignes:
                somme_total = somme_total + item.montant_dotation
                somme_engage = somme_engage + float(item.valeur_engagement)
                somme_realise = somme_realise + float(item.valeur_reel)
                somme_consomme = somme_consomme + float(item.valeur_total_consommee)
                somme_dispo = somme_dispo + float(item.valeur_solde)
                somme_reajute = somme_reaj + float(item.montant_alloue)
                ladevise = item.budget.devise.symbole_devise
                NaturebudgetDepenseR = Model_Budget.objects.filter(id = item.budget.id)
                # print('SHOW ME NATURE', NaturebudgetDepenseR)
                for item in NaturebudgetDepenseR:
                    if not item.id in tempo:
                        tempo.append(item.id)
                        others.append(item)

            
            # print('SHOW ME TEMPO NATURE', others)
            for ligne in others:
                item = {
                    "id": ligne.id,
                    "designation": ligne.designation,
                    "montant_alloue" : ligne.montant_alloue,
                    "devise": ligne.devise.symbole_devise
                }
                nature.append(item)
            #Catégiories
            categories = Model_Categoriebudget.objects.filter(type = 2)

            budget_depense = {
                'initial' : somme_total,
                'engagement': somme_engage,
                'reel': somme_realise,
                'consommation': somme_consomme,
                'disponible': somme_dispo,
                'devise': ladevise,
                'categories':categories,
                'nature': nature,
                'reajute': somme_reajute
            }
            return budget_depense
        except Exception as e:
            # print("toGetTypeBudgetDepense", e)
            return None