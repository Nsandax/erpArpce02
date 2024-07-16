# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_RegleSalariale, TypeCondition, TypeCalcul, TypeResultat
from django.utils import timezone

class dao_regle_salariale(object):
    id = 0
    designation             =    ""
    description             =    ""
    code                    =    ""
    auteur_id               =    0
    sequence                =    99
    quantite                =    1
    categorie_id            =    None
    type_condition          =    "aucun"
    plage_condition         =    ""
    code_condition          =    ""
    plage_min_condition     =    0.0
    plage_max_condition     =    0.0
    type_calcul             =    1
    type_resultat           =    1
    montant_fixe            =    0.0
    pourcentage             =    0.0
    pourcentage_sur         =    ""
    code_python             =    ""
    bareme_id               =    None
    devise_id               =    None
    est_actif               =    True
    apparait_dans_bulletin  =    True
    compte_debit_id         =    None
    compte_credit_id         =    None

    
    @staticmethod
    def toList():
        return  Model_RegleSalariale.objects.all().order_by("sequence")
    
    @staticmethod
    def toCreate(auteur_id, designation, code = "", description = "",sequence  =  99,quantite = 1,categorie_id  = None,type_condition  = "aucun",plage_condition  =  "",code_condition  =  "",plage_min_condition =  0.0,plage_max_condition = 0.0,type_calcul = 1, type_resultat = 1, montant_fixe =  0.0,pourcentage  = 0.0,pourcentage_sur = "",code_python =  "",bareme_id  = None,devise_id = None,compte_debit_id = None,compte_credit_id = None, apparait_dans_bulletin  = True,est_actif = True ):
        try:
            regle_salariale = dao_regle_salariale()
            if auteur_id == 0: auteur_id = None 
            regle_salariale.auteur_id = auteur_id
            regle_salariale.designation = designation
            regle_salariale.description = description
            regle_salariale.code = code
            regle_salariale.sequence                =    sequence
            regle_salariale.quantite                =    quantite
            if categorie_id == "": categorie_id = 0.0 
            regle_salariale.categorie_id            =    categorie_id
            regle_salariale.type_condition          =    type_condition
            regle_salariale.plage_condition         =    plage_condition
            regle_salariale.code_condition          =    code_condition
            if plage_min_condition == "": plage_min_condition = 0.0 
            regle_salariale.plage_min_condition     =    plage_min_condition
            if plage_max_condition == "": plage_max_condition = 0.0 
            regle_salariale.plage_max_condition     =    plage_max_condition
            regle_salariale.type_calcul             =    type_calcul
            regle_salariale.type_resultat           =    type_resultat
            if montant_fixe == "": montant_fixe = 0.0 
            regle_salariale.montant_fixe            =    montant_fixe
            if pourcentage == "": pourcentage = 0.0 
            regle_salariale.pourcentage             =    pourcentage
            regle_salariale.pourcentage_sur         =    pourcentage_sur
            regle_salariale.code_python             =    code_python
            #print("bareme_id: {}".format(bareme_id)) 
            if bareme_id == 0: 
                bareme_id = None
                #print("Bareme is None") 
            regle_salariale.bareme_id               =    bareme_id
            if devise_id == 0: devise_id = None 
            regle_salariale.devise_id               =    devise_id
            regle_salariale.est_actif               =    est_actif
            regle_salariale.apparait_dans_bulletin  =    apparait_dans_bulletin
            if compte_debit_id == 0: compte_debit_id = None 
            regle_salariale.compte_debit_id         =    compte_debit_id
            if compte_credit_id == 0: compte_credit_id = None 
            regle_salariale.compte_credit_id         =    compte_credit_id
            return regle_salariale
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION (dao_regle_salariale)")
            #print(e)
            return None

    @staticmethod
    def toSave(dao_regle_salariale_object):
        try:
            regle_salariale =  Model_RegleSalariale()
            regle_salariale.designation = dao_regle_salariale_object.designation
            regle_salariale.auteur_id = dao_regle_salariale_object.auteur_id
            regle_salariale.description = dao_regle_salariale_object.description
            regle_salariale.code = dao_regle_salariale_object.code
            regle_salariale.sequence  = dao_regle_salariale_object.sequence
            regle_salariale.quantite  = dao_regle_salariale_object.quantite
            regle_salariale.categorie_id  = dao_regle_salariale_object.categorie_id
            regle_salariale.type_condition  = dao_regle_salariale_object.type_condition
            regle_salariale.plage_condition  = dao_regle_salariale_object.plage_condition
            regle_salariale.code_condition  = dao_regle_salariale_object.code_condition
            regle_salariale.plage_min_condition = dao_regle_salariale_object.plage_min_condition
            regle_salariale.plage_max_condition  = dao_regle_salariale_object.plage_max_condition
            regle_salariale.type_calcul = dao_regle_salariale_object.type_calcul
            regle_salariale.type_resultat = dao_regle_salariale_object.type_resultat
            regle_salariale.montant_fixe = dao_regle_salariale_object.montant_fixe
            regle_salariale.pourcentage   = dao_regle_salariale_object.pourcentage
            regle_salariale.pourcentage_sur = dao_regle_salariale_object.pourcentage_sur
            regle_salariale.code_python  = dao_regle_salariale_object.code_python
            regle_salariale.bareme_id  = dao_regle_salariale_object.bareme_id
            regle_salariale.devise_id  = dao_regle_salariale_object.devise_id
            regle_salariale.est_actif  = dao_regle_salariale_object.est_actif
            regle_salariale.apparait_dans_bulletin  = dao_regle_salariale_object.apparait_dans_bulletin
            regle_salariale.compte_debit_id  = dao_regle_salariale_object.compte_debit_id
            regle_salariale.compte_credit_id  = dao_regle_salariale_object.compte_credit_id
            regle_salariale.save()
            return regle_salariale
        except Exception as e:
            #print("ERREUR LORS DU SAVE (dao_regle_salariale)")
            #print(e)
            return None

    
    @staticmethod
    def toUpdate(id, dao_regle_salariale_object):
        try:
            regle_salariale =  Model_RegleSalariale.objects.get(pk = id)
            regle_salariale.designation = dao_regle_salariale_object.designation
            regle_salariale.description = dao_regle_salariale_object.description
            regle_salariale.code = dao_regle_salariale_object.code
            regle_salariale.sequence  = dao_regle_salariale_object.sequence
            regle_salariale.quantite  = dao_regle_salariale_object.quantite
            regle_salariale.categorie_id  = dao_regle_salariale_object.categorie_id
            regle_salariale.type_condition  = dao_regle_salariale_object.type_condition
            regle_salariale.plage_condition  = dao_regle_salariale_object.plage_condition
            regle_salariale.code_condition  = dao_regle_salariale_object.code_condition
            regle_salariale.plage_min_condition = dao_regle_salariale_object.plage_min_condition
            regle_salariale.plage_max_condition  = dao_regle_salariale_object.plage_max_condition
            regle_salariale.type_calcul = dao_regle_salariale_object.type_calcul
            regle_salariale.type_resultat = dao_regle_salariale_object.type_resultat
            regle_salariale.montant_fixe = dao_regle_salariale_object.montant_fixe
            regle_salariale.pourcentage   = dao_regle_salariale_object.pourcentage
            regle_salariale.pourcentage_sur = dao_regle_salariale_object.pourcentage_sur
            regle_salariale.code_python  = dao_regle_salariale_object.code_python
            regle_salariale.bareme_id  = dao_regle_salariale_object.bareme_id
            regle_salariale.devise_id  = dao_regle_salariale_object.devise_id
            regle_salariale.est_actif  = dao_regle_salariale_object.est_actif
            regle_salariale.apparait_dans_bulletin  = dao_regle_salariale_object.apparait_dans_bulletin
            regle_salariale.compte_debit_id  = dao_regle_salariale_object.compte_debit_id
            regle_salariale.compte_credit_id  = dao_regle_salariale_object.compte_credit_id
            regle_salariale.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR (dao_regle_salariale)")
            #print(e)
            return False

    
    @staticmethod
    def toDelete(dao_regle_salariale_object):
        try:
            regle_salariale =  Model_RegleSalariale.objects.get(pk = dao_regle_salariale_object.id)
            regle_salariale.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION (dao_regle_salariale)")
            #print(e)
            return False

    
    @staticmethod
    def toGet(id):
        try:
            regle_salariale =  Model_RegleSalariale.objects.get(pk = id)
            return regle_salariale
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE (dao_regle_salariale)")
            #print(e)
            return None
        
    @staticmethod
    def toListTypeCondition():
        list = []
        for key, value in TypeCondition:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list
    
    @staticmethod
    def toListTypeCalcul():
        list = []
        for key, value in TypeCalcul:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list
    
    @staticmethod
    def toListTypeResultat():
        list = []
        for key, value in TypeResultat:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list
