from __future__ import unicode_literals
from ErpBackOffice.models import Model_PaiementInterne
from django.utils import timezone

class dao_paiement_interne(object):
    id = 0
    designation = ""
    description = ""
    montant = 0
    devise_id =	0
    pret_id = 0
    conge_id = 0
    dossier_paie_id = 0
    item_bulletin_id = 0
    taux_id = 0
    etat = ""
    auteur_id = 0
    est_valide = False

    @staticmethod
    def toListPaiements():
        return Model_PaiementInterne.objects.all()

    @staticmethod
    def toListPaiementsValides():
        return Model_PaiementInterne.objects.filter(est_valide = True)

    @staticmethod
    def toListPaiementsOfPret(pret_id):
        return Model_PaiementInterne.objects.filter(pret_id = pret_id)

    @staticmethod
    def toListPaiementsOfConge(conge_id):
        return Model_PaiementInterne.objects.filter(conge_id = conge_id)

    @staticmethod
    def toListPaiementsOfDossierPaie(dossier_paie_id):
        return Model_PaiementInterne.objects.filter(dossier_paie_id = dossier_paie_id)

    @staticmethod
    def toListPaiementsOfItemBulletin(item_bulletin_id):
        return Model_PaiementInterne.objects.filter(item_bulletin_id = item_bulletin_id)

    @staticmethod
    def toCreatePaiement(montant, devise_id = None, pret_id = None, dossier_paie_id = None, item_bulletin_id = None, conge_id = None, taux_id = None, auteur_id = None, etat = "", designation = "", description ="", est_valide = False):
        try:
            paiement = dao_paiement_interne()
            if designation == None or designation == "": designation = dao_paiement_interne.toGenerateNumero()
            paiement.designation = designation
            paiement.description = description
            paiement.pret_id = pret_id
            paiement.conge_id = conge_id
            paiement.dossier_paie_id = dossier_paie_id
            paiement.item_bulletin_id = item_bulletin_id
            paiement.auteur_id = auteur_id
            paiement.devise_id = devise_id
            paiement.montant = montant 
            paiement.etat = etat 
            paiement.taux_id = taux_id 
            paiement.est_valide = est_valide 
            return paiement
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DU PAIEMENT")
            #print(e)
            return None
			
    @staticmethod
    def toSavePaiement(objet_dao_paiement_interne):
        try:
            paiement  = Model_PaiementInterne()
            paiement.designation = objet_dao_paiement_interne.designation
            paiement.description = objet_dao_paiement_interne.description
            paiement.pret_id = objet_dao_paiement_interne.pret_id
            paiement.conge_id = objet_dao_paiement_interne.conge_id
            paiement.dossier_paie_id = objet_dao_paiement_interne.dossier_paie_id
            paiement.item_bulletin_id = objet_dao_paiement_interne.item_bulletin_id
            paiement.auteur_id = objet_dao_paiement_interne.auteur_id
            paiement.devise_id = objet_dao_paiement_interne.devise_id
            paiement.montant = objet_dao_paiement_interne.montant 
            paiement.etat = objet_dao_paiement_interne.etat 
            paiement.taux_id = objet_dao_paiement_interne.taux_id 
            paiement.est_valide = objet_dao_paiement_interne.est_valide 
            paiement.save()

            return paiement
        except Exception as e:
            #print("ERREUR SAVE PAIEMENT")
            #print(e)
            return None

    @staticmethod
    def toUpdatePaiement(id, objet_dao_paiement_interne):
        try:
            paiement = Model_PaiementInterne.objects.get(pk = id)
            paiement.designation = objet_dao_paiement_interne.designation
            paiement.description = objet_dao_paiement_interne.description
            paiement.pret_id = objet_dao_paiement_interne.pret_id
            paiement.conge_id = objet_dao_paiement_interne.conge_id
            paiement.dossier_paie_id = objet_dao_paiement_interne.dossier_paie_id
            paiement.item_bulletin_id = objet_dao_paiement_interne.item_bulletin_id
            paiement.auteur_id = objet_dao_paiement_interne.auteur_id
            paiement.devise_id = objet_dao_paiement_interne.devise_id
            paiement.montant = objet_dao_paiement_interne.montant 
            paiement.etat = objet_dao_paiement_interne.etat 
            paiement.taux_id = objet_dao_paiement_interne.taux_id 
            paiement.est_valide = objet_dao_paiement_interne.est_valide
            paiement.save()
            return paiement
        except Exception as e:
            #print("ERREUR UPDATE PAIEMENT")
            #print(e)
            return None
	
    @staticmethod
    def toGetPaiement(id):
        try:
            return Model_PaiementInterne.objects.get(pk = id)
        except Exception as e:
            #print("ERREUR GET PAIEMENT")
            #print(e)
            return None

    @staticmethod
    def toDeletePaiement(id):
        try:
            paiement = Model_PaiementInterne.objects.get(pk = id)
            paiement.delete()
            return True
        except Exception as e:
            #print("ERREUR DELETE PAIEMENT")
            #print(e)
            return False

    @staticmethod
    def toGenerateNumero():
        total = dao_paiement_interne.toListPaiements().count()
        total = total + 1
        temp_numero = str(total)
        
        for i in range(len(str(total)), 4):
            temp_numero = "0" + temp_numero

        mois = timezone.now().month
        if mois < 10: mois = "0%s" % mois
        
        temp_numero = "PAY-INT-%s%s%s" % (timezone.now().year, mois, temp_numero)
        return temp_numero

    @staticmethod
    def toGetOrderMax():
        try:
            max = Model_PaiementInterne.objects.all().count()
            max = max + 1
            return max
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return None