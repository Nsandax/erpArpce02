from __future__ import unicode_literals
from ErpBackOffice.models import Model_Paiement
from ErpBackOffice.models import Model_Facture
from django.utils import timezone

class dao_paiement(object):
    id = 0
    designation = ""
    description = ""
    transaction_id = 0
    facture_id = 0
    journal_id = 0
    partenaire_id = 0
    auteur_id = 0
    type_paiement = 0
    montant = 0
    est_lettre = False
    est_valide = False
    devise_id =	0
    date_paiement = ""	
    type = ""

    @staticmethod
    def toListPaiements():
        return Model_Paiement.objects.all()
    
    @staticmethod
    def toListPaiementOfFacture(facture_id):
        return Model_Paiement.objects.filter(facture_id = facture_id)
    
    @staticmethod
    def toCheckPaiementSoldeOfFacture(facture_id, montant_facture):
        paiements = Model_Paiement.objects.filter(facture_id = facture_id)
        somme = 0
        for paiement in paiements:
            somme += paiement.montant
        if somme >= montant_facture:
            return True
        else:
            return False



    @staticmethod
    def toListPaiementsValides():
        return Model_Paiement.objects.filter(est_valide = True)

    @staticmethod
    def toListPaiementsOf(facture_id):
        return Model_Paiement.objects.filter(facture_id = facture_id)

    @staticmethod
    def toListPaiementsClient():
        return Model_Paiement.objects.filter(type = "Paiement client")

    @staticmethod
    def toListPaiementsFournisseur():
        return Model_Paiement.objects.filter(type = "Paiement fournisseur")

    @staticmethod
    def toListPaiementsTransfert():
        return Model_Paiement.objects.filter(type_paiement = 3)

    @staticmethod
    def toCreatePaiement(transaction_id,date_paiement, facture_id, devise_id, montant, type_paiement, journal_id = None, partenaire_id = None, auteur_id = None, designation = "", description ="", est_lettre = False, est_valide = False):
        try:
            paiement = dao_paiement()
            if designation == None or designation == "": designation = dao_paiement.toGenerateNumero()
            paiement.designation = designation
            paiement.description = description
            paiement.transaction_id = transaction_id
            paiement.facture_id = facture_id
            paiement.journal_id = journal_id
            paiement.partenaire_id = partenaire_id
            paiement.auteur_id = auteur_id
            paiement.type_paiement = type_paiement
            paiement.date_paiement = date_paiement
            paiement.devise_id = devise_id
            paiement.montant = montant 
            paiement.est_lettre = est_lettre 
            paiement.est_valide = est_valide 
            return paiement
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DU PAIEMENT")
            #print(e)
            return None
			
    @staticmethod
    def toSavePaiement(objet_dao_paiement):
        try:
            paiement  = Model_Paiement()
            paiement.designation = objet_dao_paiement.designation
            paiement.description = objet_dao_paiement.description
            paiement.transaction_id = objet_dao_paiement.transaction_id
            paiement.facture_id = objet_dao_paiement.facture_id
            paiement.journal_id = objet_dao_paiement.journal_id
            paiement.partenaire_id = objet_dao_paiement.partenaire_id
            paiement.auteur_id = objet_dao_paiement.auteur_id
            paiement.type_paiement = objet_dao_paiement.type_paiement
            paiement.date_paiement = objet_dao_paiement.date_paiement
            paiement.devise_id = objet_dao_paiement.devise_id
            paiement.montant = objet_dao_paiement.montant
            paiement.est_lettre = objet_dao_paiement.est_lettre 
            paiement.est_valide = objet_dao_paiement.est_valide 
            paiement.save()

            #print("PAIEMENT SAVE OK")
            return paiement
        except Exception as e:
            #print("ERREUR SAVE PAIEMENT")
            #print(e)
            return None

    @staticmethod
    def toUpdatePaiement(id, objet_dao_paiement):
        try:
            paiement = Model_Paiement.objects.get(pk = id)
            paiement.designation = objet_dao_paiement.designation
            paiement.description = objet_dao_paiement.description
            paiement.transaction_id = objet_dao_paiement.transaction_id
            paiement.facture_id = objet_dao_paiement.facture_id
            paiement.journal_id = objet_dao_paiement.journal_id
            paiement.partenaire_id = objet_dao_paiement.partenaire_id
            paiement.auteur_id = objet_dao_paiement.auteur_id
            paiement.type_paiement = objet_dao_paiement.type_paiement
            paiement.date_paiement = objet_dao_paiement.date_paiement
            paiement.devise_id = objet_dao_paiement.devise_id
            paiement.montant = objet_dao_paiement.montant 
            paiement.est_lettre = objet_dao_paiement.est_lettre
            paiement.est_valide = objet_dao_paiement.est_valide
            paiement.save()
            return paiement
        except Exception as e:
            #print("ERREUR UPDATE PAIEMENT")
            #print(e)
            return None
	
    @staticmethod
    def toGetPaiement(id):
        try:
            return Model_Paiement.objects.get(pk = id)
        except Exception as e:
            #print("ERREUR GET PAIEMENT")
            #print(e)
            return None

    @staticmethod
    def toDeletePaiement(id):
        try:
            paiement = Model_Paiement.objects.get(pk = id)
            paiement.delete()
            return True
        except Exception as e:
            #print("ERREUR DELETE PAIEMENT")
            #print(e)
            return False

    @staticmethod
    def toGenerateNumero():
        total = dao_paiement.toListPaiements().count()
        total = total + 1
        temp_numero = str(total)
        
        for i in range(len(str(total)), 4):
            temp_numero = "0" + temp_numero

        mois = timezone.now().month
        if mois < 10: mois = "0%s" % mois
        
        temp_numero = "PAY-%s%s%s" % (timezone.now().year, mois, temp_numero)
        return temp_numero

    @staticmethod
    def toGetOrderMax():
        try:
            max = Model_Paiement.objects.all().count()
            max = max + 1
            return max
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return None