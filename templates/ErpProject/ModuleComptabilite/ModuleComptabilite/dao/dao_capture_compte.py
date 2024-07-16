
from __future__ import unicode_literals

from ErpBackOffice.models import Model_CaptureCompte, Model_Compte
from django.utils import timezone

class dao_capture_compte(object):
    id = 0
    montant_ouverture = 0
    montant_solde = 0
    date_ouverture = None
    date_fermeture = None
    index = 0
    est_credit = True
    compte_id = 0
    date_capture = None

    @staticmethod
    def toListCapturesCompte():
        return Model_CaptureCompte.objects.all().order_by('-id')

    @staticmethod
    def toGetCaptureDuCompte(compte_id, index):
        try:
            return Model_CaptureCompte.objects.get(compte_id = compte_id, index= index)
        except Exception as e:
            #print("ERREUR toGetCaptureDuCompte")
            #print(e)
            return None

    @staticmethod
    def toGetCapturePrecedenteDuCompte(compte_id):
        try:
            return dao_capture_compte.toGetCaptureDuCompte(compte_id, -1)
        except Exception as e:
            #print("ERREUR toGetCapturePrecedenteDuCompte")
            #print(e)
            return None

    @staticmethod
    def toGetCaptureRecenteDuCompte(compte_id):
        try:
            return dao_capture_compte.toGetCaptureDuCompte(compte_id, 1)
        except Exception as e:
            #print("ERREUR toGetCaptureRecenteDuCompte")
            #print(e)
            return None

    @staticmethod
    def toCreateCaptureCompte(compte_id, montant_ouverture, montant_solde, date_ouverture, date_fermeture, index, est_credit):
        try:
            capture_compte = dao_capture_compte()
            capture_compte.compte_id = compte_id
            capture_compte.montant_ouverture = montant_ouverture
            capture_compte.montant_solde = montant_solde
            capture_compte.date_ouverture = date_ouverture
            capture_compte.date_fermeture = date_fermeture
            capture_compte.index = index
            capture_compte.est_credit = est_credit
            return capture_compte
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE LA CAPTURE")
            #print(e)
            return None

    @staticmethod
    def toSaveCaptureCompte(object_dao_capture_compte):
        try:
            capture_compte = dao_capture_compte.toGetCaptureDuCompte(object_dao_capture_compte.compte_id, object_dao_capture_compte.index)
            if capture_compte == None:
                capture_compte = Model_CaptureCompte()
                capture_compte.compte_id = object_dao_capture_compte.compte_id
                capture_compte.index = object_dao_capture_compte.index

            capture_compte.montant_ouverture = object_dao_capture_compte.montant_ouverture
            capture_compte.montant_solde = object_dao_capture_compte.montant_solde
            capture_compte.date_ouverture = object_dao_capture_compte.date_ouverture
            capture_compte.date_fermeture = object_dao_capture_compte.date_fermeture
            capture_compte.est_credit = object_dao_capture_compte.est_credit
            capture_compte.date_capture = timezone.now()
            capture_compte.save()
            return capture_compte
        except Exception as e:
            #print("ERREUR LORS DE L'ENREGISTREMENT DE LA CAPTURE")
            #print(e)
            return None

    @staticmethod
    def toInstallComptabilite():
        comptes = Model_Compte.objects.all()
        for item in comptes:
            # timezone.datetime(Y, m, d)
            _date = timezone.datetime(2019, 1, 1)
            capture = dao_capture_compte.toCreateCaptureCompte(item.id, 0, 0, _date, _date, -1, False)
            dao_capture_compte.toSaveCaptureCompte(capture)