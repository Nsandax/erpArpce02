# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_RecouvrementLigne, StatutRecouvrement
from django.utils import timezone

class dao_recouvrement_ligne(object):
    id = 0
    designation = ""
    description = ""
    statut_recouvrement = 1
    facture_id  =  None
    recouvrement_id  =  None
    auteur_id = 0

    @staticmethod
    def toList():
        return  Model_RecouvrementLigne.objects.all().order_by("designation")
    
    @staticmethod
    def toCreate(auteur_id, recouvrement_id  ,facture_id  =  None, designation = "", statut_recouvrement = 1, description = ""):
        try:
            recouvrement_ligne = dao_recouvrement_ligne()
            if auteur_id == 0: auteur_id = None
            recouvrement_ligne.auteur_id = auteur_id
            recouvrement_ligne.designation = designation
            recouvrement_ligne.description = description
            recouvrement_ligne.statut_recouvrement = statut_recouvrement
            if facture_id == 0: facture_id = None
            recouvrement_ligne.facture_id = facture_id
            if recouvrement_id == 0: recouvrement_id = None
            recouvrement_ligne.recouvrement_id = recouvrement_id
            return recouvrement_ligne
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION (dao_recouvrement_ligne)")
            #print(e)
            return None

    @staticmethod
    def toSave(dao_recouvrement_ligne_object):
        try:
            recouvrement_ligne =  Model_RecouvrementLigne()
            recouvrement_ligne.designation = dao_recouvrement_ligne_object.designation
            recouvrement_ligne.auteur_id = dao_recouvrement_ligne_object.auteur_id
            recouvrement_ligne.description = dao_recouvrement_ligne_object.description
            recouvrement_ligne.statut_recouvrement = dao_recouvrement_ligne_object.statut_recouvrement
            recouvrement_ligne.facture_id = dao_recouvrement_ligne_object.facture_id
            recouvrement_ligne.recouvrement_id = dao_recouvrement_ligne_object.recouvrement_id
            recouvrement_ligne.save()
            return recouvrement_ligne
        except Exception as e:
            #print("ERREUR LORS DU SAVE (dao_recouvrement_ligne)")
            #print(e)
            return None

    
    @staticmethod
    def toUpdate(id, dao_recouvrement_ligne_object):
        try:
            recouvrement_ligne =  Model_RecouvrementLigne.objects.get(pk = id)
            recouvrement_ligne.designation = dao_recouvrement_ligne_object.designation
            recouvrement_ligne.description = dao_recouvrement_ligne_object.description
            recouvrement_ligne.statut_recouvrement = dao_recouvrement_ligne_object.statut_recouvrement
            recouvrement_ligne.facture_id = dao_recouvrement_ligne_object.facture_id
            recouvrement_ligne.recouvrement_id = dao_recouvrement_ligne_object.recouvrement_id
            recouvrement_ligne.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR (dao_recouvrement_ligne)")
            #print(e)
            return False

    
    @staticmethod
    def toDelete(dao_recouvrement_ligne_object):
        try:
            recouvrement_ligne =  Model_RecouvrementLigne.objects.get(pk = dao_recouvrement_ligne_object.id)
            recouvrement_ligne.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION (dao_recouvrement_ligne)")
            #print(e)
            return False

    
    @staticmethod
    def toGet(id):
        try:
            recouvrement_ligne =  Model_RecouvrementLigne.objects.get(pk = id)
            return recouvrement_ligne
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE (dao_recouvrement_ligne)")
            #print(e)
            return None
        
    @staticmethod
    def toListLigneDuRecouvrement(id):
        try:
            lignes = Model_RecouvrementLigne.objects.filter(recouvrement_id = id).order_by("-creation_date")
            return lignes
        except Exception as e:
            return []
        
    @staticmethod
    def toListLigneDuRecouvrementActif(id):
        try:
            lignes = Model_RecouvrementLigne.objects.filter(recouvrement_id = id, statut_recouvrement = 1).order_by("-creation_date")
            return lignes
        except Exception as e:
            return []
        
    @staticmethod
    def toListLigneDuRecouvrementInatif(id):
        try:
            lignes = Model_RecouvrementLigne.objects.filter(recouvrement_id = id, statut_recouvrement = 2).order_by("-creation_date")
            return lignes
        except Exception as e:
            return []
        
    @staticmethod
    def toListStatutRecouvrement():
        list = []
        for key, value in StatutRecouvrement:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list
