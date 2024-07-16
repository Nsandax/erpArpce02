from __future__ import unicode_literals
from ErpBackOffice.models import MoisAnnee

class dao_mois_annee(object):
    @staticmethod
    def toListMoisAnnee():
        list = []
        for key, value in MoisAnnee:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list

    @staticmethod
    def toGetMoisAnnee(id):
        list = dao_mois_annee.toListMoisAnnee()
        for item in list:
            if item["id"] == id: return item
        return None