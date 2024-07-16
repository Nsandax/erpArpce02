# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_StructureSalariale, HorairePaye
from django.utils import timezone

class dao_structure_salariale(object):
    id = 0
    designation = ""
    description = ""
    type_id = None
    horaire_paye  =  1
    journal_id = None
    devise_id = None
    auteur_id = 0
    est_actif  =  True
    par_defaut  =  False
    libelle_bulletin  = ""
    

    @staticmethod
    def toList():
        return  Model_StructureSalariale.objects.all().order_by("creation_date")
    
    @staticmethod
    def toCreate(auteur_id, designation, type_id = 1, horaire_paye  =  1, libelle_bulletin  = "", journal_id = None, devise_id = None, par_defaut  =  False, description = "", est_actif  =  True):
        try:
            structure_salariale = dao_structure_salariale()
            if auteur_id == 0: auteur_id = None
            structure_salariale.auteur_id = auteur_id
            structure_salariale.designation = designation
            structure_salariale.description = description
            if type_id == 0: type_id = None
            structure_salariale.type_id = type_id
            structure_salariale.horaire_paye = horaire_paye
            if journal_id == 0: journal_id = None
            structure_salariale.journal_id = journal_id
            if devise_id == 0: devise_id = None
            structure_salariale.devise_id = devise_id
            structure_salariale.est_actif = est_actif
            structure_salariale.par_defaut = par_defaut
            structure_salariale.libelle_bulletin = libelle_bulletin
            return structure_salariale
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION (dao_structure_salariale)")
            #print(e)
            return None

    @staticmethod
    def toSave(dao_structure_salariale_object):
        try:
            structure_salariale =  Model_StructureSalariale()
            structure_salariale.designation = dao_structure_salariale_object.designation
            structure_salariale.auteur_id = dao_structure_salariale_object.auteur_id
            structure_salariale.description = dao_structure_salariale_object.description
            structure_salariale.type_id = dao_structure_salariale_object.type_id
            structure_salariale.horaire_paye = dao_structure_salariale_object.horaire_paye
            structure_salariale.journal_id = dao_structure_salariale_object.journal_id
            structure_salariale.devise_id = dao_structure_salariale_object.devise_id
            structure_salariale.est_actif = dao_structure_salariale_object.est_actif
            structure_salariale.par_defaut = dao_structure_salariale_object.par_defaut
            structure_salariale.libelle_bulletin = dao_structure_salariale_object.libelle_bulletin
            structure_salariale.save()
            return structure_salariale
        except Exception as e:
            #print("ERREUR LORS DU SAVE (dao_structure_salariale)")
            #print(e)
            return None

    
    @staticmethod
    def toUpdate(id, dao_structure_salariale_object):
        try:
            structure_salariale =  Model_StructureSalariale.objects.get(pk = id)
            structure_salariale.designation = dao_structure_salariale_object.designation
            structure_salariale.description = dao_structure_salariale_object.description
            structure_salariale.type_id = dao_structure_salariale_object.type_id
            structure_salariale.horaire_paye = dao_structure_salariale_object.horaire_paye
            structure_salariale.journal_id = dao_structure_salariale_object.journal_id
            structure_salariale.devise_id = dao_structure_salariale_object.devise_id
            structure_salariale.est_actif = dao_structure_salariale_object.est_actif
            structure_salariale.par_defaut = dao_structure_salariale_object.par_defaut
            structure_salariale.libelle_bulletin = dao_structure_salariale_object.libelle_bulletin
            structure_salariale.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR (dao_structure_salariale)")
            #print(e)
            return False

    
    @staticmethod
    def toDelete(dao_structure_salariale_object):
        try:
            structure_salariale =  Model_StructureSalariale.objects.get(pk = dao_structure_salariale_object.id)
            structure_salariale.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION (dao_structure_salariale)")
            #print(e)
            return False

    
    @staticmethod
    def toGet(id):
        try:
            structure_salariale =  Model_StructureSalariale.objects.get(pk = id)
            return structure_salariale
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE (dao_structure_salariale)")
            #print(e)
            return None
        
    @staticmethod
    def toListHorairePaye():
        list = []
        for key, value in HorairePaye:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list
