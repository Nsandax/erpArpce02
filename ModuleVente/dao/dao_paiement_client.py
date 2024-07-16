from __future__ import unicode_literals
from ErpBackOffice.models import Model_Paiement
from django.utils import timezone

class dao_paiement_client(object):
	id = 0
	montant=0.0
	date_paiement='2010-01-01'
	facture_client_id = 0
	document_id = 0
	devise_id = 0
	taux_id = 0
	transaction_client_id = 0
	auteur_id = 0
	is_complete = False

	@staticmethod
	def toListPaiementClient():
		return Model_Paiement.objects.all().order_by('-id')

	@staticmethod
	def toCreatePaiementClient(montant,date_paiement,is_complete,facture_client_id=0,document_id=0,devise_id=0,taux_id=0,transaction_client_id=0):
		try:
			paiement_client = dao_paiement_client()
			paiement_client.montant = montant
			paiement_client.date_paiement = date_paiement
			paiement_client.is_complete = is_complete
			if facture_client_id != 0:
				paiement_client.facture_client_id = facture_client_id
			if document_id != 0:
				paiement_client.document_id = document_id
			if devise_id != 0:
				paiement_client.devise_id = devise_id
			if taux_id != 0:
				paiement_client.taux_id = taux_id
			if transaction_client_id != 0:
				paiement_client.transaction_client_id = transaction_client_id
			return paiement_client
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA PAIEMENT_CLIENT')
			#print(e)
			return None

	@staticmethod
	def toSavePaiementClient(auteur,objet_dao_Paiement_client):
		try:
			paiement_client  = Model_Paiement()
			paiement_client.montant =objet_dao_Paiement_client.montant
			paiement_client.date_paiement =objet_dao_Paiement_client.date_paiement
			paiement_client.is_complete =objet_dao_Paiement_client.is_complete
			paiement_client.creation_date = timezone.now()
			paiement_client.facture_client_id = objet_dao_Paiement_client.facture_client_id
			paiement_client.document_id = objet_dao_Paiement_client.document_id
			paiement_client.devise_id = objet_dao_Paiement_client.devise_id
			paiement_client.taux_id = objet_dao_Paiement_client.taux_id
			paiement_client.transaction_client_id = objet_dao_Paiement_client.transaction_client_id
			paiement_client.auteur_id=auteur.id
			paiement_client.save()
			return paiement_client
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA PAIEMENT_CLIENT')
			#print(e)
			return None

	@staticmethod
	def toUpdatePaiementClient(id, objet_dao_Paiement_client):
		try:
			paiement_client = Model_Paiement.objects.get(pk = id)
			paiement_client.montant =objet_dao_Paiement_client.montant
			paiement_client.date_paiement =objet_dao_Paiement_client.date_paiement
			paiement_client.is_complete =objet_dao_Paiement_client.is_complete
			paiement_client.facture_client_id = objet_dao_Paiement_client.facture_client_id
			paiement_client.document_id = objet_dao_Paiement_client.document_id
			paiement_client.devise_id = objet_dao_Paiement_client.devise_id
			paiement_client.taux_id = objet_dao_Paiement_client.taux_id
			paiement_client.transaction_client_id = objet_dao_Paiement_client.transaction_client_id
			paiement_client.save()
			return paiement_client
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA PAIEMENT_CLIENT')
			#print(e)
			return None
	@staticmethod
	def toGetPaiementClient(id):
		try:
			return Model_Paiement.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeletePaiementClient(id):
		try:
			paiement_client = Model_Paiement.objects.get(pk = id)
			paiement_client.delete()
			return True
		except Exception as e:
			return False