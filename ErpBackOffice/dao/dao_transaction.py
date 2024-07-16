from __future__ import unicode_literals
from ErpBackOffice.models import Model_Transaction
from django.utils import timezone

class dao_transaction(object):
    reference = ""
    id = 0
    facture_id = 0
    statut = 0
    moyen_paiement = 0
    auteur_id = 0

    @staticmethod
    def toListTransactions():
        return Model_Transaction.objects.all()
        
    @staticmethod
    def toCreateTransaction(facture_id, statut, moyen_paiement, reference=""):
        try:
            transaction = dao_transaction()
            transaction.facture_id = facture_id
            transaction.statut = statut
            transaction.moyen_paiement = moyen_paiement
            if reference == None or reference == "": reference = dao_transaction.toGenerateNumero()
            transaction.reference = reference
                        
            return transaction
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE LA TRANSACTION")
            #print(e)
            return None
            
    @staticmethod
    def toSaveTransaction(auteur, objet_dao_transaction):
        try:
            transaction  = Model_Transaction()
            transaction.facture_id = objet_dao_transaction.facture_id
            transaction.statut = objet_dao_transaction.statut
            transaction.moyen_paiement = objet_dao_transaction.moyen_paiement
            transaction.reference = objet_dao_transaction.reference
            transaction.auteur_id = auteur.id
            transaction.save()

            return transaction
        except Exception as e:
            #print("ERREUR SAVE TRANSACTION")
            #print(e)
            return None

    @staticmethod
    def toUpdateTransaction(id, objet_dao_transaction):
        try:
            transaction = Model_Transaction.objects.get(pk = id)
            transaction.facture_id = objet_dao_transaction.facture_id
            transaction.statut = objet_dao_transaction.statut
            transaction.moyen_paiement = objet_dao_transaction.moyen_paiement
            transaction.save()
            return transaction
        except Exception as e:
            #print("ERREUR UPDATE TRANSACTION")
            #print(e)
            return None

    @staticmethod
    def toGetTransaction(id):
        try:
            return Model_Transaction.objects.get(pk = id)
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return None

    @staticmethod
    def toDeleteTransaction(id):
        try:
            transaction = Model_Transaction.objects.get(pk = id)
            transaction.delete()
            return True
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return False

    @staticmethod
    def toGenerateNumero():
        total = dao_transaction.toListTransactions().count()
        total = total + 1
        temp_numero = str(total)
        
        for i in range(len(str(total)), 4):
            temp_numero = "0" + temp_numero

        mois = timezone.now().month
        if mois < 10: mois = "0%s" % mois
        
        temp_numero = "TRANS-%s%s%s" % (timezone.now().year, mois, temp_numero)
        return temp_numero

    @staticmethod
    def toGetOrderMax():
        try:
            max = Model_Transaction.objects.all().count()
            max = max + 1
            return max
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return None