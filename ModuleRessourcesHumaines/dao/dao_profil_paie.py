# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_ProfilPaye
from django.utils import timezone

class dao_profil_paie(object):
    id = 0
    designation = ""
    reference = ""
    employe_id = 0
    auteur_id = 0

    @staticmethod
    def toListProfil():
        return Model_ProfilPaye.objects.all().order_by("designation")
    
    @staticmethod
    def toCreateProfil(auteur_id, designation, employe_id, reference = ""):
        try:
            profil_paie = dao_profil_paie()
            profil_paie.auteur_id = auteur_id
            profil_paie.designation = designation
            profil_paie.reference = reference
            profil_paie.employe_id = employe_id
            return profil_paie
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION")
            #print(e)
            return None

    @staticmethod
    def toSaveProfil(dao_profil_paie_object):
        try:
            profil_paie = Model_ProfilPaye()
            profil_paie.designation = dao_profil_paie_object.designation
            profil_paie.auteur_id = dao_profil_paie_object.auteur_id
            profil_paie.reference = dao_profil_paie_object.reference
            profil_paie.employe_id = dao_profil_paie_object.employe_id
            profil_paie.creation_date = timezone.now()
            profil_paie.save()
            return profil_paie
        except Exception as e:
            #print("ERREUR LORS DU SAVE")
            #print(e)
            return None

    
    @staticmethod
    def toUpdateProfil(id, dao_profil_paie_object):
        try:
            profil_paie = Model_ProfilPaye.objects.get(pk = id)
            profil_paie.designation = dao_profil_paie_object.designation
            profil_paie.reference = dao_profil_paie_object.reference
            profil_paie.employe_id = dao_profil_paie_object.employe_id
            profil_paie.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR")
            #print(e)
            return False

    
    @staticmethod
    def toDeleteProfil(dao_profil_paie_object):
        try:
            profil_paie = Model_ProfilPaye.objects.get(pk = dao_profil_paie_object.id)
            profil_paie.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION")
            #print(e)
            return False

    
    @staticmethod
    def toGetProfil(id):
        try:
            profil_paie = Model_ProfilPaye.objects.get(pk = id)
            return profil_paie
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE")
            #print(e)
            return None

    @staticmethod
    def toGetProfilOfEmployee(id):
        try:
            profil_paie = Model_ProfilPaye.objects.get(employe_id = id)
            return profil_paie
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE")
            #print(e)
            return None