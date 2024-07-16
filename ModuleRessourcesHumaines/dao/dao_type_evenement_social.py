from __future__ import unicode_literals
from ErpBackOffice.models import TypeEvenementSocial

class dao_type_evenement_social(object):
    @staticmethod
    def toListTypeEvenementSocial():
        list = []
        for key, value in TypeEvenementSocial:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list

    @staticmethod
    def toGetTypeEvenementSocial(id):
        list = dao_type_evenement_social.toListTypeEvenementSocial()
        for item in list:
            if item["id"] == id: return item
        return None

    @staticmethod
    def toGetTypeMaternite():
        return dao_type_evenement_social.toGetTypeEvenementSocial(1)

    @staticmethod
    def toGetTypeCouvertureMaladie():
        return dao_type_evenement_social.toGetTypeEvenementSocial(2)

    @staticmethod
    def toGetTypeFraisMedicaux():
        return dao_type_evenement_social.toGetTypeEvenementSocial(3)

    @staticmethod
    def toGetTypeEvenementFamiliaux():
        return dao_type_evenement_social.toGetTypeEvenementSocial(4)
		
    @staticmethod
    def toGetTypeAccidentDeTravail():
        return dao_type_evenement_social.toGetTypeEvenementSocial(5)

    @staticmethod
    def toGetTypeEnqueteEtSuivi():
        return dao_type_evenement_social.toGetTypeEvenementSocial(6)

    @staticmethod
    def toGetTypeAudition():
        return dao_type_evenement_social.toGetTypeEvenementSocial(7)

    @staticmethod
    def toGetTypeAutres():
        return dao_type_evenement_social.toGetTypeEvenementSocial(8)