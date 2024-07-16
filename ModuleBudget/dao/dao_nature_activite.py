from __future__ import unicode_literals
from ErpBackOffice.models import natureActivite

class dao_nature_activite(object):
    @staticmethod
    def toListNatureActivites():
        list = []
        for key, value in natureActivite:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list

    @staticmethod
    def toGetnatureActivite(id):
        list = dao_nature_activite.toListNatureActivites()
        for item in list:
            if item["id"] == id: return item
        return None

    @staticmethod
    def toGetElectronique():
        return dao_nature_activite.toGetnatureActivite(0)

    @staticmethod
    def toGetPoste():
        return dao_nature_activite.toGetnatureActivite(1)