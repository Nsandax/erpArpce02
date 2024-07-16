from __future__ import unicode_literals
from ErpBackOffice.models import MoyenPaiement

class dao_moyen_paiement(object):
    @staticmethod
    def toListMoyenPaiement():
        list = []
        for key, value in MoyenPaiement:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list

    @staticmethod
    def toGetMoyenPaiement(id):
        list = dao_moyen_paiement.toListMoyenPaiement()
        for item in list:
            if item["id"] == id: return item
        return None

    @staticmethod
    def toGetMoyenCash():
        return dao_moyen_paiement.toGetMoyenPaiement(1)

    @staticmethod
    def toGetMoyenVoucher():
        return dao_moyen_paiement.toGetMoyenPaiement(2)