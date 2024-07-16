# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import *
from django.utils import timezone

class dao_rubrique(object):
    id = 0
    designation             =    ""
    reference               =    ""
    description             =    ""
    code                    =    ""
    auteur_id               =    0
    sequence                =    99
    type_rubrique           =    1
    type_formule            =    1
    type_element            =    1
    nombre_parsal           =    0.0
    nombre_parsal_is_const  =    False
    nombre_parsal_const_id  =    None
    base_parsal             =    0.0
    base_parsal_is_const    =    False
    base_parsal_const_id    =    None
    taux_parsal             =    0.0
    taux_parsal_is_const    =    False
    taux_parsal_const_id    =    None
    montant_parsal          =    0.0
    montant_parsal_is_const =    False
    montant_parsal_const_id =    None
    taux_parpat             =    0.0
    taux_parpat_is_const    =    False
    taux_parpat_const_id    =    None
    montant_parpat          =    0.0
    montant_parpat_is_const =    False
    montant_parpat_const_id =    None
    devise_id               =    None
    est_actif               =    True
    apparait_dans_bulletin  =    True
    compte_debit_id         =    None
    compte_credit_id        =    None


    @staticmethod
    def toList():
        return  Model_Rubrique.objects.all().order_by("sequence")

    @staticmethod
    def toListRubriques():
        return Model_Rubrique.objects.all().order_by('-id')

    @staticmethod
    def toCreate(auteur_id, designation,  reference = "", code = "", description = "", sequence  =  99, type_rubrique = 1, type_formule = 1, type_element = 1, nombre_parsal  = 0.0, nombre_parsal_is_const  = False, nombre_parsal_const_id  =  None, base_parsal  = 0.0, base_parsal_is_const  = False, base_parsal_const_id  =  None, taux_parsal  = 0.0, taux_parsal_is_const  = False, taux_parsal_const_id  =  None, montant_parsal  = 0.0, montant_parsal_is_const  = False, montant_parsal_const_id  =  None, taux_parpat  = 0.0, taux_parpat_is_const  = False, taux_parpat_const_id  =  None, montant_parpat  = 0.0, montant_parpat_is_const  = False, montant_parpat_const_id  =  None,  est_actif = True, apparait_dans_bulletin = True, compte_debit_id = None, compte_credit_id = None, devise_id = None):
        try:
            rubrique = dao_rubrique()
            if auteur_id == 0: auteur_id = None
            rubrique.auteur_id               =    auteur_id
            rubrique.designation             =    designation
            rubrique.reference               =    reference
            rubrique.description             =    description
            rubrique.code                    =    code
            rubrique.sequence                =    sequence
            rubrique.type_rubrique           =    type_rubrique
            rubrique.type_formule            =    type_formule
            rubrique.type_element            =    type_element
            rubrique.nombre_parsal           =    nombre_parsal
            rubrique.nombre_parsal_is_const  =    nombre_parsal_is_const
            rubrique.nombre_parsal_const_id  =    nombre_parsal_const_id
            rubrique.base_parsal             =    base_parsal
            rubrique.base_parsal_is_const    =    base_parsal_is_const
            rubrique.base_parsal_const_id    =    base_parsal_const_id
            rubrique.taux_parsal             =    taux_parsal
            rubrique.taux_parsal_is_const    =    taux_parsal_is_const
            rubrique.taux_parsal_const_id    =    taux_parsal_const_id
            rubrique.montant_parsal          =    montant_parsal
            rubrique.montant_parsal_is_const =    montant_parsal_is_const
            rubrique.montant_parsal_const_id =    montant_parsal_const_id
            rubrique.taux_parpat             =    taux_parpat
            rubrique.taux_parpat_is_const    =    taux_parpat_is_const
            rubrique.taux_parpat_const_id    =    taux_parpat_const_id
            rubrique.montant_parpat          =    montant_parpat
            rubrique.montant_parpat_is_const =    montant_parpat_is_const
            rubrique.montant_parpat_const_id =    montant_parpat_const_id
            rubrique.devise_id               =    devise_id
            rubrique.est_actif               =    est_actif
            rubrique.apparait_dans_bulletin  =    apparait_dans_bulletin
            rubrique.compte_debit_id         =    compte_debit_id
            rubrique.compte_credit_id         =    compte_credit_id
            return rubrique
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION (dao_rubrique)")
            #print(e)
            return None

    @staticmethod
    def toSave(dao_rubrique_object):
        try:
            rubrique =  Model_Rubrique()
            rubrique.auteur_id               =    dao_rubrique_object.auteur_id
            rubrique.designation             =    dao_rubrique_object.designation
            rubrique.reference               =    dao_rubrique_object.reference
            rubrique.description             =    dao_rubrique_object.description
            rubrique.code                    =    dao_rubrique_object.code
            rubrique.sequence                =    dao_rubrique_object.sequence
            rubrique.type_rubrique           =    dao_rubrique_object.type_rubrique
            rubrique.type_element            =    dao_rubrique_object.type_element
            rubrique.type_formule            =    dao_rubrique_object.type_formule
            rubrique.nombre_parsal           =    dao_rubrique_object.nombre_parsal
            rubrique.nombre_parsal_is_const  =    dao_rubrique_object.nombre_parsal_is_const
            rubrique.nombre_parsal_const_id  =    dao_rubrique_object.nombre_parsal_const_id
            rubrique.base_parsal             =    dao_rubrique_object.base_parsal
            rubrique.base_parsal_is_const    =    dao_rubrique_object.base_parsal_is_const
            rubrique.base_parsal_const_id    =    dao_rubrique_object.base_parsal_const_id
            rubrique.taux_parsal             =    dao_rubrique_object.taux_parsal
            rubrique.taux_parsal_is_const    =    dao_rubrique_object.taux_parsal_is_const
            rubrique.taux_parsal_const_id    =    dao_rubrique_object.taux_parsal_const_id
            rubrique.montant_parsal          =    dao_rubrique_object.montant_parsal
            rubrique.montant_parsal_is_const =    dao_rubrique_object.montant_parsal_is_const
            rubrique.montant_parsal_const_id =    dao_rubrique_object.montant_parsal_const_id
            rubrique.taux_parpat             =    dao_rubrique_object.taux_parpat
            rubrique.taux_parpat_is_const    =    dao_rubrique_object.taux_parpat_is_const
            rubrique.taux_parpat_const_id    =    dao_rubrique_object.taux_parpat_const_id
            rubrique.montant_parpat          =    dao_rubrique_object.montant_parpat
            rubrique.montant_parpat_is_const =    dao_rubrique_object.montant_parpat_is_const
            rubrique.montant_parpat_const_id =    dao_rubrique_object.montant_parpat_const_id
            rubrique.devise_id               =    dao_rubrique_object.devise_id
            rubrique.est_actif               =    dao_rubrique_object.est_actif
            rubrique.apparait_dans_bulletin  =    dao_rubrique_object.apparait_dans_bulletin
            rubrique.compte_debit_id         =    dao_rubrique_object.compte_debit_id
            rubrique.compte_credit_id        =    dao_rubrique_object.compte_credit_id
            rubrique.save()
            return rubrique
        except Exception as e:
            #print("ERREUR LORS DU SAVE (dao_rubrique)")
            #print(e)
            return None


    @staticmethod
    def toUpdate(id, dao_rubrique_object):
        try:
            rubrique =  Model_Rubrique.objects.get(pk = id)
            rubrique.designation             =    dao_rubrique_object.designation
            rubrique.reference               =    dao_rubrique_object.reference
            rubrique.description             =    dao_rubrique_object.description
            rubrique.code                    =    dao_rubrique_object.code
            rubrique.sequence                =    dao_rubrique_object.sequence
            rubrique.type_rubrique           =    dao_rubrique_object.type_rubrique
            rubrique.type_formule            =    dao_rubrique_object.type_formule
            rubrique.type_element            =    dao_rubrique_object.type_element
            rubrique.nombre_parsal           =    dao_rubrique_object.nombre_parsal
            rubrique.nombre_parsal_is_const  =    dao_rubrique_object.nombre_parsal_is_const
            rubrique.nombre_parsal_const_id  =    dao_rubrique_object.nombre_parsal_const_id
            rubrique.base_parsal             =    dao_rubrique_object.base_parsal
            rubrique.base_parsal_is_const    =    dao_rubrique_object.base_parsal_is_const
            rubrique.base_parsal_const_id    =    dao_rubrique_object.base_parsal_const_id
            rubrique.taux_parsal             =    dao_rubrique_object.taux_parsal
            rubrique.taux_parsal_is_const    =    dao_rubrique_object.taux_parsal_is_const
            rubrique.taux_parsal_const_id    =    dao_rubrique_object.taux_parsal_const_id
            rubrique.montant_parsal          =    dao_rubrique_object.montant_parsal
            rubrique.montant_parsal_is_const =    dao_rubrique_object.montant_parsal_is_const
            rubrique.montant_parsal_const_id =    dao_rubrique_object.montant_parsal_const_id
            rubrique.taux_parpat             =    dao_rubrique_object.taux_parpat
            rubrique.taux_parpat_is_const    =    dao_rubrique_object.taux_parpat_is_const
            rubrique.taux_parpat_const_id    =    dao_rubrique_object.taux_parpat_const_id
            rubrique.montant_parpat          =    dao_rubrique_object.montant_parpat
            rubrique.montant_parpat_is_const =    dao_rubrique_object.montant_parpat_is_const
            rubrique.montant_parpat_const_id =    dao_rubrique_object.montant_parpat_const_id
            rubrique.devise_id               =    dao_rubrique_object.devise_id
            rubrique.est_actif               =    dao_rubrique_object.est_actif
            rubrique.apparait_dans_bulletin  =    dao_rubrique_object.apparait_dans_bulletin
            rubrique.compte_debit_id         =    dao_rubrique_object.compte_debit_id
            rubrique.compte_credit_id        =    dao_rubrique_object.compte_credit_id
            rubrique.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR (dao_rubrique)")
            #print(e)
            return False


    @staticmethod
    def toUpdatePartial(id, dao_rubrique_object):
        try:
            rubrique =  Model_Rubrique.objects.get(pk = id)
            rubrique.designation             =    dao_rubrique_object.designation
            rubrique.reference               =    dao_rubrique_object.reference
            rubrique.description             =    dao_rubrique_object.description
            rubrique.code                    =    dao_rubrique_object.code
            rubrique.sequence                =    dao_rubrique_object.sequence

            rubrique.devise_id               =    dao_rubrique_object.devise_id
            rubrique.est_actif               =    dao_rubrique_object.est_actif
            rubrique.apparait_dans_bulletin  =    dao_rubrique_object.apparait_dans_bulletin
            rubrique.compte_debit_id         =    dao_rubrique_object.compte_debit_id
            rubrique.compte_credit_id        =    dao_rubrique_object.compte_credit_id
            rubrique.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR (dao_rubrique)")
            #print(e)
            return False


    @staticmethod
    def toDelete(dao_rubrique_object):
        try:
            rubrique =  Model_Rubrique.objects.get(pk = dao_rubrique_object.id)
            rubrique.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION (dao_rubrique)")
            #print(e)
            return False



    @staticmethod
    def toGet(id):
        try:
            rubrique =  Model_Rubrique.objects.get(pk = id)
            return rubrique
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE (dao_rubrique)")
            #print(e)
            return None

    @staticmethod
    def toListTypeElementBulletin():
        list = []
        for key, value in TypeElementBulletin:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list

    @staticmethod
    def toListTypeRubrique():
        list = []
        for key, value in TypeRubrique:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list

    @staticmethod
    def toListTypeFormule():
        list = []
        for key, value in TypeFormule:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list


    @staticmethod
    def toUpdateCompteComptable(id, compte_debit_id, compte_credit_id):
        try:
            rubrique =  Model_Rubrique.objects.get(pk = id)
            rubrique.compte_debit_id         =    compte_debit_id
            rubrique.compte_credit_id        =    compte_credit_id
            rubrique.save()
            return rubrique
        except Exception as e:
            #print("ERREUR LORS DU toUpdateCompteComptable")
            #print(e)
            return None


    @staticmethod
    def toGetRubriqueRemboursementPret():
        try:
            return Model_Rubrique.objects.filter(code = "620").first()
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE (dao_regle_salariale)")
            #print(e)
            return None


    @staticmethod
    def toGetRubriqueByReference(ref):
        try:
            # print('***REF SEND', ref)
            ref = str(ref)
            return Model_Rubrique.objects.get(reference = ref)
        except Exception as e:
            print("ERREUR LORS DU L'AFFICHAGE (dao_reubrique_ReferenceS)")
            print(e)
            return None



