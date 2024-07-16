
from __future__ import unicode_literals

from ErpBackOffice.models import Model_Taux
from django.utils import timezone

class dao_taux_change(object):
    id = 0
    devise_depart_id = None
    devise_arrive_id = None		
    montant = 0
    est_courant = True	
    auteur_id = None

    @staticmethod
    def toListTaux():
        return Model_Taux.objects.all().order_by("-creation_date")

    @staticmethod
    def toListTauxDuJour(date_jour):
        try:
            return Model_Taux.objects.filter(creation_date__date = date_jour.date()).order_by("-creation_date")
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return []

    @staticmethod
    def toListTauxCourant():
        try:
            return Model_Taux.objects.filter(est_courant = True).order_by("-creation_date")
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return []

    @staticmethod
    def toGetTauxCourantDeLaDeviseArrive(devise_arrive_id):
        try:
            return Model_Taux.objects.filter(est_courant = True).get(devise_arrive_id = devise_arrive_id)
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return None

    @staticmethod
    def toCreateTaux(devise_depart_id, devise_arrive_id, montant, est_courant):        
        try:
            taux = dao_taux_change()
            taux.devise_depart_id = devise_depart_id
            taux.devise_arrive_id = devise_arrive_id
            taux.montant = montant
            taux.est_courant = est_courant
            return taux
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DU TAUX")
            #print(e)
            return None

    @staticmethod
    def toSaveTaux(auteur, object_dao_taux):
        try:
            taux = Model_Taux()
            taux.devise_depart_id = object_dao_taux.devise_depart_id
            taux.devise_arrive_id = object_dao_taux.devise_arrive_id
            taux.montant = object_dao_taux.montant
            taux.est_courant = object_dao_taux.est_courant
            taux.auteur_id = auteur.id
            taux.save()
            return taux
        except Exception as e:
            #print("ERREUR LORS DU SAVE DU TAUX")
            #print(e)
            return None

    @staticmethod
    def toUpdateTaux(id, object_dao_taux):
        try:
            taux = Model_Taux.objects.get(pk = id)
            taux.devise_depart_id = object_dao_taux.devise_depart_id
            taux.devise_arrive_id = object_dao_taux.devise_arrive_id
            taux.montant = object_dao_taux.montant
            taux.auteur_id = object_dao_taux.auteur_id
            taux.est_courant = object_dao_taux.est_courant
            taux.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU UPDATE DU TAUX")
            #print(e)
            return False

    @staticmethod
    def toDeleteTaux(id):
        try:
            taux = Model_Taux.objects.get(pk = id)
            taux.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION DU TAUX")
            #print(e)
            return False

    @staticmethod
    def toGetTaux(id):
        try:
            return Model_Taux.objects.get(pk = id)
        except Exception as e:
            #print("ERREUR LORS DE LA RECUPERATION DU TAUX")
            #print(e)
            return None