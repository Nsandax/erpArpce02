from __future__ import unicode_literals
from ErpBackOffice.models import Model_Bon
from django.db.models import Max
from django.utils import timezone
from django.db.models import Q


class dao_bon_special(object):
    id = 0
    numero = ""
    date_prevue = None
    date_realisation = None
    est_realisee = False
    devise_id  = 0
    inventoriste_id = 0
    quantite_voulue = 0
    quantite_obtenue = 0
    est_reserve = False
    reference_document = ""
    description = ""
    type = ""
    bon_commande_id = 0
    bon_reception_id = 0
    bon_transfert_id = 0
    taux_id = None
    auteur_id = 0

    @staticmethod
    def toCreateBonSpecial(numero, bon_commande_id = None, bon_reception_id = None, bon_transfert_id = None, reference_document= "", devise_id = None, inventoriste_id = None,  description = "", date_realisation = None, est_realisee = True, date_prevue = None, quantite_voulue = 0, quantite_obtenue = 0, est_reserve = True, taux_id = None):
        try:
            bon_special = dao_bon_special()
            if numero == None or numero == "": 
                numero = bon_special.toGenerateNumeroBon()
            bon_special.numero = numero
            if date_prevue != None : 
                bon_special.date_prevue = date_prevue
            if date_realisation != None : 
                bon_special.date_realisation = date_realisation
            bon_special.devise_id = devise_id
            bon_special.inventoriste_id = inventoriste_id
            bon_special.bon_commande_id = bon_commande_id
            bon_special.bon_reception_id = bon_reception_id
            bon_special.bon_transfert_id = bon_transfert_id
            bon_special.quantite_voulue = quantite_voulue
            bon_special.quantite_obtenue = quantite_obtenue
            bon_special.est_reserve = est_reserve
            bon_special.reference_document = reference_document
            bon_special.description = description
            bon_special.est_realisee = est_realisee
            bon_special.taux_id = taux_id
            return bon_special
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DU BON")
            #print(e)
            return None

    @staticmethod
    def toSaveBonSpecial(auteur, objet_dao_bon_special):
        try :
            bon_special = Model_Bon()
            bon_special.numero = objet_dao_bon_special.numero		
            bon_special.date_prevue =	objet_dao_bon_special.date_prevue
            bon_special.date_realisation = objet_dao_bon_special.date_realisation
            bon_special.est_realisee = objet_dao_bon_special.est_realisee
            bon_special.devise_id	= objet_dao_bon_special.devise_id
            bon_special.inventoriste_id =	objet_dao_bon_special.inventoriste_id
            bon_special.quantite_voulue = objet_dao_bon_special.quantite_voulue
            bon_special.quantite_obtenue = objet_dao_bon_special.quantite_obtenue
            bon_special.est_reserve = objet_dao_bon_special.est_reserve
            bon_special.reference_document =	objet_dao_bon_special.reference_document
            bon_special.description =	objet_dao_bon_special.description
            bon_special.type = objet_dao_bon_special.type
            bon_special.taux_id = objet_dao_bon_special.taux_id
            bon_special.auteur_id = auteur.id
            bon_special.creation_date = timezone.now()
            bon_special.bon_commande_id = objet_dao_bon_special.bon_commande_id
            bon_special.bon_reception_id = objet_dao_bon_special.bon_reception_id
            bon_special.bon_transfert_id = objet_dao_bon_special.bon_transfert_id
            bon_special.save()
            return bon_special
        except Exception as e:
            #print("ERREUR LORS DE LA SAUVEGARDE DU BON")
            #print(e)
            return None

    @staticmethod
    def toUpdateBonSpecial(id, objet_dao_bon_special):
        try:
            bon_special = Model_Bon.objects.get(pk = id)
            bon_special.numero = objet_dao_bon_special.numero		
            bon_special.date_prevue =	objet_dao_bon_special.date_prevue
            bon_special.date_realisation = objet_dao_bon_special.date_realisation
            bon_special.est_realisee = objet_dao_bon_special.est_realisee
            bon_special.devise_id	= objet_dao_bon_special.devise_id
            bon_special.inventoriste_id =	objet_dao_bon_special.inventoriste_id
            bon_special.quantite_voulue = objet_dao_bon_special.quantite_voulue
            bon_special.quantite_obtenue = objet_dao_bon_special.quantite_obtenue
            bon_special.est_reserve = objet_dao_bon_special.est_reserve
            bon_special.reference_document =	objet_dao_bon_special.reference_document
            bon_special.description =	objet_dao_bon_special.description
            bon_special.type = objet_dao_bon_special.type
            bon_special.taux_id = objet_dao_bon_special.taux_id
            bon_special.auteur_id = auteur.id
            bon_special.creation_date = timezone.now()
            bon_special.bon_commande_id = objet_dao_bon_special.bon_commande_id
            bon_special.bon_reception_id = objet_dao_bon_special.bon_reception_id
            bon_special.bon_transfert_id = objet_dao_bon_special.bon_transfert_id
            bon_special.save()
            return True
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return False

    @staticmethod
    def toGetBonSpecial(id):
        try:
            return Model_Bon.objects.get(pk = id)
        except Exception as e:
            return None
    
    @staticmethod
    def toGetBonEntreeOfDemande(demande_achat_id):
        try:
            return Model_Bon.objects.get(Q(bon_reception__demande_achat__id =demande_achat_id)|Q(bon_reception__demandes_achat__id=demande_achat_id))
        except Exception as e:
            return None

    @staticmethod
    def toGetBonEntreeOfDemandeByAuteur(demande_achat_id, user_id):
        try:
            return Model_Bon.objects.get(Q(bon_reception__demande_achat__id =demande_achat_id)|Q(bon_reception__demandes_achat__id=demande_achat_id)).filter(auteur_id=user_id)
        except Exception as e:
            return None

    @staticmethod
    def toGetBonSpecialMax():
        try:
            #return Model_Bon.objects.all().aggregate(Max('rating'))
            max = Model_Bon.objects.all().count()
            max = max + 1
            return max
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return None

    @staticmethod
    def toGetBonSpecialMaxByAuteur(user_id):
        try:
            #return Model_Bon.objects.all().aggregate(Max('rating'))
            max = Model_Bon.objects.filter(auteur_id=user_id).count()
            max = max + 1
            return max
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return None


    @staticmethod
    def toDeleteBonSpecial(id):
        try:
            bon_special = Model_Bon.objects.get(pk = id)
            bon_special.delete()
            return True
        except Exception as e:
            return False

    @staticmethod
    def toGenerateNumeroBon():
        total_bons = Model_Bon.objects.all().count()
        total_bons = total_bons + 1
        temp_numero = str(total_bons)

        for i in range(len(str(total_bons)), 4):
            temp_numero = "0" + temp_numero

        mois = timezone.now().month
        if mois < 10: mois = "0%s" % mois
        
        temp_numero = "BE%s%s%s" % (timezone.now().year, mois, temp_numero)
        return temp_numero


    @staticmethod
    def toListBonsEntrees():
        Liste = Model_Bon.objects.all().order_by('-creation_date')
        return Liste

    @staticmethod
    def toListBonsEntreesByAuteur(user_id):
        Liste = Model_Bon.objects.filter(auteur_id=user_id).order_by('-creation_date')
        return Liste

