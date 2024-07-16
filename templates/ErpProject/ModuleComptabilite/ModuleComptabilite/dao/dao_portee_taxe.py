from __future__ import unicode_literals
from ErpBackOffice.models import PorteeTaxe

class dao_portee_taxe(object):
    @staticmethod
    def toListPorteesTaxe():
        list = []
        for key, value in PorteeTaxe:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list

    @staticmethod
    def toGetPorteeTaxe(id):
        list = dao_portee_taxe.toListPorteesTaxe()
        for item in list:
            if item['id'] == id: return item
        return None

    @staticmethod
    def toGetPorteeVente():
        return dao_portee_taxe.toGetPorteeTaxe(1)

    @staticmethod
    def toGetPorteeAchat():
        return dao_portee_taxe.toGetPorteeTaxe(2)

    @staticmethod
    def toGetPorteeAucune():
        return dao_portee_taxe.toGetPorteeTaxe(3)