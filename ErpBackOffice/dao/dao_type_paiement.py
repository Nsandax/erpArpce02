from __future__ import unicode_literals
from ErpBackOffice.models import TypePaiement

class dao_type_paiement(object):
    @staticmethod
    def toListTypePaiement():
        list = []
        for key, value in TypePaiement:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list

    @staticmethod
    def toGetTypePaiement(id):
        list = dao_type_paiement.toListTypePaiement()
        for item in list:
            if item["id"] == id: return item
        return None

    @staticmethod
    def toGetTypeClient():
        return dao_type_paiement.toGetTypePaiement(1)

    @staticmethod
    def toGetTypeFournisseur():
        return dao_type_paiement.toGetTypePaiement(2)

    @staticmethod
    def toGetTypeTransfert():
        return dao_type_paiement.toGetTypePaiement(3)