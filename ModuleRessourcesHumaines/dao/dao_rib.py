from __future__ import unicode_literals
from ErpBackOffice.models import Model_Rib, Model_Employe, Model_CompteBanque_Employe
from django.utils import timezone
from django.db.models.functions import TruncMonth
from django.db.models import Count
from random import *


class dao_rib(object):
    id = 0
    cle_rib = 0
    comptebanque_id = None
    banque_id = None
    pays_id = None
    code_guichet = ""
    nom_guichet = ""
    titulaire_compte = ""
    iban = ""
    bic = ""

    @staticmethod
    def toListRibEmployes():
        return Model_Rib.objects.all().order_by('-id')


    @staticmethod
    def toCreateRibEmploye(banque_id,pays_id, cle_rib, code_guichet, nom_guichet, titulaire_compte, iban, bic, comptebanque_id):
        try:
            rib = dao_rib()
            rib.banque_id = banque_id
            rib.pays_id = pays_id
            rib.cle_rib = cle_rib
            rib.code_guichet = code_guichet
            rib.nom_guichet = nom_guichet
            rib.titulaire_compte = titulaire_compte
            rib.iban = iban
            rib.bic = bic
            rib.comptebanque_id = comptebanque_id
            return rib
        except Exception as e:
            #print("ERREUR TO CREATE RIB", e)
            return None

    @staticmethod
    def toSaveRibEmploye(auteur, objet_dao_rib):
        try:
            rib = Model_Rib()
            rib.banque_id = objet_dao_rib.banque_id
            rib.cle_rib = objet_dao_rib.cle_rib
            rib.code_guichet = objet_dao_rib.code_guichet
            rib.nom_guichet = objet_dao_rib.nom_guichet
            rib.titulaire_compte = objet_dao_rib.titulaire_compte
            rib.iban = objet_dao_rib.iban
            rib.bic = objet_dao_rib.bic
            rib.comptebanque_id = objet_dao_rib.comptebanque_id
            rib.created_at = timezone.now()
            rib.updated_at = timezone.now()
            rib.auteur_id = auteur.id
            rib.save()
            return rib
        except Exception as e:
            #print("ERREUR TO SAVE RIB", e)
            return None

    @staticmethod
    def toUpdateRibEmploye(id, objet_dao_rib):
        try:
            rib = Model_Rib.objects.get(pk = id)
            rib.banque_id = objet_dao_rib.banque_id
            rib.cle_rib = objet_dao_rib.cle_rib
            rib.comptebanque_id = objet_dao_rib.comptebanque_id
            rib.code_guichet = objet_dao_rib.code_guichet
            rib.nom_guichet = objet_dao_rib.nom_guichet
            rib.titulaire_compte = objet_dao_rib.titulaire_compte
            rib.iban = objet_dao_rib.iban
            rib.bic = objet_dao_rib.bic
            rib.updated_at = timezone.now()
            rib.auteur_id = auteur.id
            rib.save()
            return rib
        except Exception as e:
            return None

    @staticmethod
    def toGetRibEmploye(id):
        try:
            return Model_Rib.objects.get(pk = id)
        except Exception as e:
            return None
        
    @staticmethod
    def toListRibsOfEmploye(employe_id):
        try:
            employe = Model_Employe.objects.get(pk = employe_id)
            profil_id = employe.profilrh.id
            ribs = Model_Rib.objects.filter(comptebanque__profilrh_id = profil_id).order_by("-created_at")
            return ribs
        except Exception as e:
            return []

    @staticmethod
    def toDeleteRib(id):
        try:
            Rib = Model_Rib.objects.get(pk = id)
            Rib.delete()
            return True
        except Exception as e:
            return False


    @staticmethod
    def toGenerated_Cle():
        try:
            cle = randint(0, 2000)
            rib = Model_Rib.objects.all()
            tableau_key = []
            for item in rib:
                tableau_key.append(item.cle_rib)
            if cle in tableau_key:
                cle = randint(0, 2000)
                return cle
            else:
                return cle

        except Exception as e:
            return 0


    @staticmethod
    def toGetOrCreateRIB(auteur, code_guichet, cle_rib, compte_banque_employe_id, banque_id, nom_complet):
        try:
            rib = Model_Rib.objects.filter(comptebanque_id = compte_banque_employe_id).first()
            if not rib:
                unrib = dao_rib()
                rib = unrib.toCreateRibEmploye(banque_id, None, cle_rib, code_guichet, "", nom_complet, "", "", compte_banque_employe_id)
                rib = unrib.toSaveRibEmploye(auteur, rib)
            return rib
        except Exception as e:
            #print("erreur on toGetOrCreateRIB", e)
            return None

    @staticmethod
    def toGetRibCompteBancaire(comptebanque):
        try:
            rib = Model_Rib.objects.filter(comptebanque = comptebanque)
            return rib
        except Exception as e:
            #print("erreur on toGetRibCompteBancaire", e)
            return None


