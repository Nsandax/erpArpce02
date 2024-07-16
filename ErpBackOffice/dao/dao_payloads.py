from __future__ import unicode_literals
from ErpBackOffice.models import Model_Payloads

class dao_payloads(object):
    id = 0
    paiement_id = 0
    logs = ""

    @staticmethod
    def toListPayloadsOf(paiement_id):
        return Model_Payloads.objects.filter(paiement_id = paiement_id)

    @staticmethod
    def toListPayloads():
        return Model_Payloads.objects.filter()
		
    @staticmethod
    def toCreatePayloads(paiement_id, logs):
        try:
            payloads = dao_payloads()
            payloads.paiement_id = paiement_id
            payloads.logs = logs                       
            return payloads
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DU PAYLOADS")
            #print(e)
            return None
			
    @staticmethod
    def toSavePayloads(objet_dao_payloads):
        try:
            payloads  = Model_Payloads()
            payloads.paiement_id = objet_dao_payloads.paiement_id
            #print("pay id %s" % objet_dao_payloads.paiement_id)
            #print("log %s" % objet_dao_payloads.logs)
            payloads.logs = objet_dao_payloads.logs
            payloads.save()
            
            #print("PAYLOAD SAVED")
            return payloads
        except Exception as e:
            #print("ERREUR SAVE DU PAYLOADS")
            #print(e)
            return None

    @staticmethod
    def toUpdatePayloads(id, objet_dao_payloads):
        try:
            payloads = Model_Payloads.objects.get(pk = id)
            payloads.paiement_id = objet_dao_payloads.paiement_id
            payloads.logs = objet_dao_payloads.logs       
            payloads.save()
            return True
        except Exception as e:
            #print("ERREUR DU UPDATE DU PAYLOADS")
            #print(e)
            return False
	
    @staticmethod
    def toGetPayloads(id):
        try:
            return Model_Payloads.objects.get(pk = id)
        except Exception as e:
            return None
			
    @staticmethod
    def toGetPayloadsOfPaiement(paiement_id):
        try:
            return Model_Payloads.objects.get(paiement_id = paiement_id)
        except Exception as e:
            return None

    @staticmethod
    def toDeletePayloads(id):
        try:
            payloads = Model_Payloads.objects.get(pk = id)
            payloads.delete()
            return True
        except Exception as e:
            return False