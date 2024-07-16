from __future__ import unicode_literals
from ErpBackOffice.models import Model_Compte, Model_TypeCompte
from django.utils import timezone


class dao_type_compte(object):
    id = 0
    designation = ""
    type = ""
    description = ""
    est_inclu_dans_balance_initiale = False
    auteur_id = None

    @staticmethod
    def toListTypeCompte():
        return Model_TypeCompte.objects.all()

    @staticmethod
    def toCreateTypeCompte(designation, type, description, est_inclu_dans_balance_initiale = False):
        try:
            typecompte = dao_type_compteompte()
            typecompte.designation = designation
            typecompte.type = type
            typecompte.description = description
            typecompte.est_inclu_dans_balance_initiale = est_inclu_dans_balance_initiale

            return typecompte
        except Exception as e:
	        #print("ERREUR LORS DE LA CREATION DU COMPTE")
	        #print(e)
	        return None

    @staticmethod
    def toSaveTypeCompte(auteur, object_dao_type_compte):
        try:
            typecompte = Model_TypeCompte()
            typecompte.designation = object_dao_type_compte.designation	
            typecompte.type = object_dao_type_compte.type
            typecompte.est_inclu_dans_balance_initiale = object_dao_type_compte.est_inclu_dans_balance_initiale
            typecompte.description = object_dao_type_compte.description
            typecompte.auteur_id = auteur.id
            typecompte.creation_date = timezone.now()
            typecompte.save()
            return compte
        except Exception as e:
            #print("ERREUR LORS DU SAVE DU COMPTE")
            #print(e)
            return None

    @staticmethod
    def toUpdateCompte(id, object_dao_type_compte):
        try:
            typecompte = Model_TypeCompte.objects.get(pk = id)
            typecompte.designation = object_dao_type_compte.designation 
            typecompte.type = object_dao_type_compte.type
            typecompte.est_inclu_dans_balance_initiale = object_dao_type_compte.est_inclu_dans_balance_initiale
            typecompte.description = object_dao_type_compte.description
            typecompte.save()
            return compte
        except Exception as e:
            #print("ERREUR LORS DU UPDATE DU TYPE COMPTE")
            #print(e)
            return None
        
    @staticmethod
    def toGetTypeCompte(id):
        try:
            return Model_TypeCompte.objects.get(pk = id)
        except Exception as e:
            return None

    @staticmethod
    def toGetTypeCompteByDesignation(designation):
        try:
            return Model_TypeCompte.objects.get(designation = designation)
        except Exception as e:
            #print(e)
            return None

    @staticmethod
    def toDeleteTypeCompte(id):
        try:
            compte = Model_TypeCompte.objects.get(pk = id)
            compte.delete()
            return True
        except Exception as e:
            return False
        
    @staticmethod
    def toListTypesCompteOf(type_of_type_compte):
        try:
            return Model_TypeCompte.objects.filter(type = type_of_type_compte).order_by("designation")
        except Exception as e:
            #print("ERREUR LORS DE L'AFFICHAGE")
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