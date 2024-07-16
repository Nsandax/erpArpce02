from __future__ import unicode_literals
from ErpBackOffice.models import Model_Transaction
from django.utils import timezone

class dao_transaction_client(object):
	id = 0
	status=''
	creation_date='2010-01-01'
	type_paiement=''
	sequence=0
	facture_client_id = 0
	auteur_id = 0
	est_validee =False



	@staticmethod
	def toListTransactionClient():
		return Model_Transaction.objects.all().order_by('-id')

	@staticmethod
	def toCreateTransactionClient(status,type_paiement,est_validee,sequence,facture_client_id=0 ):
		try:
			transaction_client = dao_transaction_client()
			transaction_client.status = status
			transaction_client.creation_date = creation_date
			transaction_client.type_paiement = type_paiement
			transaction_client.est_validee = est_validee
			transaction_client.sequence = sequence
			if facture_client_id != 0:
				transaction_client.facture_client_id = facture_client_id
			return transaction_client
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA TRANSACTION_CLIENT')
			#print(e)
			return None

	@staticmethod
	def toSaveTransactionClient(auteur,objet_dao_Transaction_client):
		try:
			transaction_client  = Model_Transaction()
			transaction_client.status =objet_dao_Transaction_client.status
			transaction_client.creation_date =timezone.now()
			transaction_client.type_paiement =objet_dao_Transaction_client.type_paiement
			transaction_client.est_validee =objet_dao_Transaction_client.est_validee
			transaction_client.sequence =objet_dao_Transaction_client.sequence
			transaction_client.facture_client_id = objet_dao_Transaction_client.facture_client_id
			transaction_client.auteur_id = auteur.id
			transaction_client.save()
			return transaction_client
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA TRANSACTION_CLIENT')
			#print(e)
			return None

	@staticmethod
	def toUpdateTransactionClient(id, objet_dao_Transaction_client):
		try:
			transaction_client = Model_Transaction.objects.get(pk = id)
			transaction_client.status =objet_dao_Transaction_client.status
			transaction_client.type_paiement =objet_dao_Transaction_client.type_paiement
			transaction_client.est_validee =objet_dao_Transaction_client.est_validee
			transaction_client.sequence =objet_dao_Transaction_client.sequence
			transaction_client.facture_client_id = objet_dao_Transaction_client.facture_client_id

			transaction_client.save()
			return transaction_client
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA TRANSACTION_CLIENT')
			#print(e)
			return None
	@staticmethod
	def toGetTransactionClient(id):
		try:
			return Model_Transaction.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteTransactionClient(id):
		try:
			transaction_client = Model_Transaction.objects.get(pk = id)
			transaction_client.delete()
			return True
		except Exception as e:
			return False