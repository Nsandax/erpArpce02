from __future__ import unicode_literals
from ErpBackOffice.models import TypeOfTypeCompte

class dao_type_of_typecompte(object):
    @staticmethod
    def toListTypesOfTypeCompte():
        list = []
        for key, value in TypeOfTypeCompte:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list

    @staticmethod
    def toGetTypeOfTypeCompte(id):
        list = dao_type_of_typecompte.toListTypesOfTypeCompte()
        for item in list:
            if item["id"] == id: return item
        return None

    @staticmethod
    def toGetTypeRecevable():
        return dao_type_of_typecompte.toGetTypeOfTypeCompte(1)

    @staticmethod
    def toGetTypePayable():
        return dao_type_of_typecompte.toGetTypeOfTypeCompte(2)

    @staticmethod
    def toGetTypeBanqueEtCaisse():
        return dao_type_of_typecompte.toGetTypeOfTypeCompte(3)

    @staticmethod
    def toGetTypeAutre():
        return dao_type_of_typecompte.toGetTypeOfTypeCompte(4)