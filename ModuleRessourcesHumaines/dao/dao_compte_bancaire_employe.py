from __future__ import unicode_literals
from ErpBackOffice.models import Model_CompteBanque_Employe
from ErpBackOffice.models import Model_Employe
from ErpBackOffice.models import Model_ProfilRH
from django.utils import timezone
from django.db.models.functions import TruncMonth
from django.db.models import Count


class dao_compte_banque_employe(object):
    id = 0
    designation = ''
    description = ''
    numero_compte = ""
    type_compte = ""
    profilrh_id = None
    banque_id = None

    @staticmethod
    def toListCompteBanqueEmployes():
        return Model_CompteBanque_Employe.objects.all().order_by('-id')

    @staticmethod
    def toCreateCompteBanqueEmploye(designation,description, numero_compte, type_compte,profilrh_id = None, banque_id = None):
        try:
            banque = dao_compte_banque_employe()
            banque.designation = designation
            banque.description = description
            banque.numero_compte = numero_compte
            banque.type_compte = type_compte
            banque.profilrh_id = profilrh_id
            banque.banque_id = banque_id
            return banque
        except Exception as e:
            #print("ERREUR CREATION OBJET COMPTE", e)
            return None


    @staticmethod
    def toSaveCompteBanqueEmploye(auteur, objet_dao_Banque):
        try:
            banque  = Model_CompteBanque_Employe()
            banque.designation = objet_dao_Banque.designation
            banque.description = objet_dao_Banque.description
            banque.profilrh_id = objet_dao_Banque.profilrh_id
            banque.numero_compte = objet_dao_Banque.numero_compte
            banque.type_compte = objet_dao_Banque.type_compte
            banque.banque_id = objet_dao_Banque.banque_id
            banque.created_at = timezone.now()
            banque.updated_at = timezone.now()
            banque.auteur_id = auteur.id
            banque.save()
            # #print("CREATION TO SAVE COMPTE", banque)
            return banque
        except Exception as e:
            #print("ERREUR TO SAVE COMPTE", e)
            return None

    @staticmethod
    def toUpdateCompteBanqueEmploye(id, objet_dao_Banque):
        try:
            banque = Model_CompteBanque_Employe.objects.get(pk = id)
            banque.designation = objet_dao_Banque.designation
            banque.description = objet_dao_Banque.description
            banque.profilrh_id = objet_dao_Banque.profilrh_id
            banque.numero_compte = objet_dao_Banque.numero_compte
            banque.type_compte = objet_dao_Banque.type_compte
            banque.banque_id = objet_dao_Banque.banque_id
            banque.updated_at = timezone.now()
            banque.auteur_id = auteur.id
            banque.save()
            return banque
        except Exception as e:
            return None


    @staticmethod
    def toGetCompteBanqueEmploye(id):
        try:
            return Model_CompteBanque_Employe.objects.get(pk = id)
        except Exception as e:
            return None

    @staticmethod
    def toDeleteCompteBanque(id):
        try:
            banque = Model_CompteBanque_Employe.objects.get(pk = id)
            banque.delete()
            return True
        except Exception as e:
            return False

    @staticmethod
    def toGet_compteBancaire_employe(employe):
        try:
            Employe = Model_Employe.objects.get(pk = employe)
            profilRH = Employe.profilrh.id
            CompteB = Model_CompteBanque_Employe.objects.filter(profilrh=profilRH)
            return CompteB
        except Exception as e:
            return None
    
    @staticmethod
    def toGetOrCreateCompteBanqueEmploye(auteur, libelle, numero_compte, profilrh_id, banque_id):
        try:
            compte_banque_employe = Model_CompteBanque_Employe.objects.filter(numero_compte = numero_compte).first()
            if not compte_banque_employe:
                compte = dao_compte_banque_employe()
                compte_banque_employe = compte.toCreateCompteBanqueEmploye(libelle, "", numero_compte, "", profilrh_id, banque_id)
                compte_banque_employe = compte.toSaveCompteBanqueEmploye(auteur, compte_banque_employe)
            return compte_banque_employe
        except Exception as e:
            #print("erreur on toGetOrCreateCompteBanqueEmploye", e)
            return None

