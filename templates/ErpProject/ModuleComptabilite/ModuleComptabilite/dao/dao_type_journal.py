from __future__ import unicode_literals
from ErpBackOffice.models import TypeJournal

class dao_type_journal(object):
    @staticmethod
    def toListTypesJournal():
        list = []
        for key, value in TypeJournal:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list

    @staticmethod
    def toGetTypeJournal(id):
        list = dao_type_journal.toListTypesJournal()
        for item in list:
            if item["id"] == id: return item
        return None

    @staticmethod
    def toGetTypeVente():
        return dao_type_journal.toGetTypeJournal(1)

    @staticmethod
    def toGetTypeAchat():
        return dao_type_journal.toGetTypeJournal(2)

    @staticmethod
    def toGetTypeBanque():
        return dao_type_journal.toGetTypeJournal(3)

    @staticmethod
    def toGetTypeCaisse():
        return dao_type_journal.toGetTypeJournal(4)

    @staticmethod
    def toGetTypeDivers():
        return dao_type_journal.toGetTypeJournal(5)