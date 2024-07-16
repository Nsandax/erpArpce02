from __future__ import unicode_literals
from ErpBackOffice.models import StatutTransaction

class dao_statut_transaction(object):
    @staticmethod
    def toListStatutTransaction():
        list = []
        for key, value in StatutTransaction:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list

    @staticmethod
    def toGetStatutTransaction(id):
        list = dao_statut_transaction.toListStatutTransaction()
        for item in list:
            if item["id"] == id: return item
        return None

    @staticmethod
    def toGetStatutCreated():
        return dao_statut_transaction.toGetStatutTransaction(1)

    @staticmethod
    def toGetStatutSubmitted():
        return dao_statut_transaction.toGetStatutTransaction(2)

    @staticmethod
    def toGetStatutCanceled():
        return dao_statut_transaction.toGetStatutTransaction(3)

    @staticmethod
    def toGetStatutSuccess():
        return dao_statut_transaction.toGetStatutTransaction(4)

    @staticmethod
    def toGetStatutError():
        return dao_statut_transaction.toGetStatutTransaction(5)