from __future__ import unicode_literals

from ErpBackOffice.models import Model_TypeCompte

class dao_type_compte(object):
    id = 0
    designation = ""
    description = ""
    type = ""
    est_inclu_dans_balance_initiale = False
    auteur_id = None

    @staticmethod
    def toCreateTypeCompte(designation, description, type, est_inclu_dans_balance_initiale, auteur_id = None):
        try:
            type_compte = dao_type_compte()
            type_compte.designation = designation
            type_compte.description = description
            type_compte.type = type
            type_compte.est_inclu_dans_balance_initiale = est_inclu_dans_balance_initiale
            type_compte.auteur_id = auteur_id
            return type_compte
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION")
            #print(e)
            return None
        
    @staticmethod
    def toSaveTypeCompte(dao_type_compte_object):
        try:
            type_compte = Model_TypeCompte()
            type_compte.designation = dao_type_compte_object.designation
            type_compte.description = dao_type_compte_object.description
            type_compte.type = dao_type_compte_object.type
            type_compte.auteur_id = dao_type_compte_object.auteur_id
            type_compte.est_inclu_dans_balance_initiale = dao_type_compte_object.est_inclu_dans_balance_initiale
            type_compte.save()
            return type_compte
        except Exception as e:
            #print("ERREUR LORS DU SAVE")
            #print(e)
            return None

    @staticmethod
    def toUpdateTypeCompte(id, dao_type_compte_object):
        try:
            type_compte = Model_TypeCompte.objects.get(pk = id)
            type_compte.designation = dao_type_compte_object.designation
            type_compte.description = dao_type_compte_object.description
            type_compte.type = dao_type_compte_object.type
            type_compte.auteur_id = dao_type_compte_object.auteur_id
            type_compte.est_inclu_dans_balance_initiale = dao_type_compte_object.est_inclu_dans_balance_initiale
            type_compte.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA MISE A JOUR")
            #print(e)
            return False

    @staticmethod
    def toDeleteTypeCompte(id, dao_type_compte_object):
        try:
            type_compte = Model_TypeCompte.objects.get(pk=id)
            type_compte.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DU DELETE")
            #print(e)
            return None

    @staticmethod
    def toListTypesCompte():
        try:
            return Model_TypeCompte.objects.all().order_by("designation")
        except Exception as e:
            #print("ERREUR LORS DE L'AFFICHAGE")
            #print(e)
            return None

    @staticmethod
    def toListTypesCompteOf(type_of_type_compte):
        try:
            return Model_TypeCompte.objects.filter(type = type_of_type_compte).order_by("designation")
        except Exception as e:
            #print("ERREUR LORS DE L'AFFICHAGE")
            #print(e)
            return None

    @staticmethod
    def toGetTypeCompte(id):
        try:
            return Model_TypeCompte.objects.get(pk = id)
        except Exception as e:
            #print("ERR")
            #print(e)
            return None
        
    @staticmethod
    def toGetTypeCompteRecevable():
        try:
            type_compte = Model_TypeCompte.objects.filter(type = 1).order_by("id").first()
            #print("type compte ID {} recupere ".format(type_compte.id))
            return type_compte
        except Exception as e:
            return None
        
    @staticmethod
    def toGetTypeComptePayable():
        try:
            type_compte = Model_TypeCompte.objects.filter(type = 2).order_by("id").first()
            #print("type compte ID {} recupere ".format(type_compte.id))
            return type_compte
        except Exception as e:
            return None
        
    @staticmethod
    def toGetTypeCompteBanqueCaisse():
        try:
            type_compte = Model_TypeCompte.objects.filter(type = 3).order_by("id").first()
            #print("type compte ID {} recupere ".format(type_compte.id))
            return type_compte
        except Exception as e:
            return None
        
    @staticmethod
    def toGetTypeCompteAutre():
        try:
            type_compte = Model_TypeCompte.objects.filter(type = 4).order_by("id").first()
            #print("type compte ID {} recupere ".format(type_compte.id))
            return type_compte
        except Exception as e:
            return None
       
        
        


    