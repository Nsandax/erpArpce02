from __future__ import unicode_literals
from ErpBackOffice.models import TypeTransactionBudgetaire

class dao_type_transaction_budgetaire(object):
    @staticmethod
    def toListTypesTransactionBudgetaire():
        list = []
        for key, value in TypeTransactionBudgetaire:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list

    @staticmethod
    def toGetTypeTransactionBudgetaire(id):
        list = dao_type_transaction_budgetaire.toListTypesTransactionBudgetaire()
        for item in list:
            if item["id"] == id: return item
        return None
    
    @staticmethod
    def toGetTypeRallonge():
        return dao_type_transaction_budgetaire.toGetTypeTransactionBudgetaire(2)
    
    @staticmethod
    def toGetTypeDiminution():
        return dao_type_transaction_budgetaire.toGetTypeTransactionBudgetaire(3)
    
    @staticmethod
    def toGetTypeNormal():
        return dao_type_transaction_budgetaire.toGetTypeTransactionBudgetaire(1)