# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_BulletinModele, HorairePaye
from django.utils import timezone

class dao_bulletin_modele(object):
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
        return  Model_BulletinModele.objects.all().order_by("creation_date")
    
    @staticmethod
    def toCreate(auteur_id, designation, type_id = None, horaire_paye  =  1, libelle_bulletin  = "", journal_id = None, devise_id = None, par_defaut  =  False, description = "", est_actif  =  True):
        try:
            modele_bulletin = dao_bulletin_modele()
            if auteur_id == 0: auteur_id = None
            modele_bulletin.auteur_id = auteur_id
            modele_bulletin.designation = designation
            modele_bulletin.description = description
            if type_id == 0: type_id = None
            modele_bulletin.type_id = type_id
            modele_bulletin.horaire_paye = horaire_paye
            if journal_id == 0: journal_id = None
            modele_bulletin.journal_id = journal_id
            if devise_id == 0: devise_id = None
            modele_bulletin.devise_id = devise_id
            modele_bulletin.est_actif = est_actif
            modele_bulletin.par_defaut = par_defaut
            modele_bulletin.libelle_bulletin = libelle_bulletin
            return modele_bulletin
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION (dao_bulletin_modele)")
            #print(e)
            return None

    @staticmethod
    def toSave(dao_bulletin_modele_object):
        try:
            modele_bulletin =  Model_BulletinModele()
            modele_bulletin.designation = dao_bulletin_modele_object.designation
            modele_bulletin.auteur_id = dao_bulletin_modele_object.auteur_id
            modele_bulletin.description = dao_bulletin_modele_object.description
            modele_bulletin.type_id = dao_bulletin_modele_object.type_id
            modele_bulletin.horaire_paye = dao_bulletin_modele_object.horaire_paye
            modele_bulletin.journal_id = dao_bulletin_modele_object.journal_id
            modele_bulletin.devise_id = dao_bulletin_modele_object.devise_id
            modele_bulletin.est_actif = dao_bulletin_modele_object.est_actif
            modele_bulletin.par_defaut = dao_bulletin_modele_object.par_defaut
            modele_bulletin.libelle_bulletin = dao_bulletin_modele_object.libelle_bulletin
            modele_bulletin.save()
            return modele_bulletin
        except Exception as e:
            print("ERREUR LORS DU SAVE (dao_bulletin_modele)")
            print(e)
            return None

    
    @staticmethod
    def toUpdate(id, dao_bulletin_modele_object):
        try:
            modele_bulletin =  Model_BulletinModele.objects.get(pk = id)
            modele_bulletin.designation = dao_bulletin_modele_object.designation
            modele_bulletin.description = dao_bulletin_modele_object.description
            modele_bulletin.type_id = dao_bulletin_modele_object.type_id
            modele_bulletin.horaire_paye = dao_bulletin_modele_object.horaire_paye
            modele_bulletin.journal_id = dao_bulletin_modele_object.journal_id
            modele_bulletin.devise_id = dao_bulletin_modele_object.devise_id
            modele_bulletin.est_actif = dao_bulletin_modele_object.est_actif
            modele_bulletin.par_defaut = dao_bulletin_modele_object.par_defaut
            modele_bulletin.libelle_bulletin = dao_bulletin_modele_object.libelle_bulletin
            modele_bulletin.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR (dao_bulletin_modele)")
            #print(e)
            return False

    
    @staticmethod
    def toDelete(dao_bulletin_modele_object):
        try:
            modele_bulletin =  Model_BulletinModele.objects.get(pk = dao_bulletin_modele_object.id)
            modele_bulletin.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION (dao_bulletin_modele)")
            #print(e)
            return False

    
    @staticmethod
    def toGet(id):
        try:
            modele_bulletin =  Model_BulletinModele.objects.get(pk = id)
            return modele_bulletin
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE (dao_bulletin_modele)")
            #print(e)
            return None
    
    @staticmethod
    def toGetBulletinModeleParDefaut():
        try:
            return Model_BulletinModele.objects.filter(est_actif = True, par_defaut = True).first()            
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE (dao_bulletin_modele)")
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
