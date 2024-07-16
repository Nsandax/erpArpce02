from __future__ import unicode_literals
from ErpBackOffice.models import TypeCombinaison

class dao_type_ligne_budgetaite(object):
    @staticmethod
    def toListTypesLignesBudgetaire():
        list = []
        for key, value in TypeCombinaison:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list

    @staticmethod
    def toGetTypeLignesBudgetaire(id):
        list = dao_type_ligne_budgetaite.toListLocalites()
        for item in list:
            if item["id"] == id: return item
        return None