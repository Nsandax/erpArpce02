from __future__ import unicode_literals
from ErpBackOffice.models import Model_Bon_livraison
from django.utils import timezone

class dao_bon_livraison(object):
	id = 0
	numero_livraison=''
	date_livraison='2010-01-01'
	quantite_demandee=0
	quantite_recue=0
	auteur_id = 0
	document_id = 0
	bon_commande_id = 0
	auteur_id = 0

	@staticmethod
	def toListBonLivraison():
		return Model_Bon_livraison.objects.all().order_by('-id')

	@staticmethod
	def toCreateBonLivraison(numero_livraison,date_livraison,quantite_demandee,quantite_recue, document_id = 0, bon_commande_id=0):
		try:
			bon_livraison = dao_bon_livraison()
			bon_livraison.numero_livraison = numero_livraison
			bon_livraison.date_livraison = date_livraison
			bon_livraison.quantite_demandee = quantite_demandee
			bon_livraison.quantite_recue = quantite_recue
			if document_id != 0:
				bon_livraison.document_id = document_id
			if bon_commande_id != 0:
				bon_livraison.bon_commande_id = bon_commande_id
			return bon_livraison
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA BON_LIVRAISON')
			#print(e)
			return None

	@staticmethod
	def toSaveBonLivraison(auteur,objet_dao_Bon_livraison):
		try:
			bon_livraison  = Model_Bon_livraison()
			bon_livraison.numero_livraison =objet_dao_Bon_livraison.numero_livraison
			bon_livraison.date_livraison =objet_dao_Bon_livraison.date_livraison
			bon_livraison.creation_date = timezone.now()
			bon_livraison.quantite_demandee =objet_dao_Bon_livraison.quantite_demandee
			bon_livraison.quantite_recue =objet_dao_Bon_livraison.quantite_recue
			bon_livraison.document_id = objet_dao_Bon_livraison.document_id
			bon_livraison.bon_commande_id = objet_dao_Bon_livraison.bon_commande_id
			bon_livraison.auteur_id = auteur.id
			bon_livraison.save()
			return bon_livraison
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA BON_LIVRAISON')
			#print(e)
			return None

	@staticmethod
	def toUpdateBonLivraison(id, objet_dao_Bon_livraison):
		try:
			bon_livraison = Model_Bon_livraison.objects.get(pk = id)
			bon_livraison.numero_livraison =objet_dao_Bon_livraison.numero_livraison
			bon_livraison.date_livraison =objet_dao_Bon_livraison.date_livraison
			bon_livraison.quantite_demandee =objet_dao_Bon_livraison.quantite_demandee
			bon_livraison.quantite_recue =objet_dao_Bon_livraison.quantite_recue
			bon_livraison.document_id = objet_dao_Bon_livraison.document_id
			bon_livraison.bon_commande_id = objet_dao_Bon_livraison.bon_commande_id
			bon_livraison.save()
			return bon_livraison
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA BON_LIVRAISON')
			#print(e)
			return None
	@staticmethod
	def toGetBonLivraison(id):
		try:
			return Model_Bon_livraison.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteBonLivraison(id):
		try:
			bon_livraison = Model_Bon_livraison.objects.get(pk = id)
			bon_livraison.delete()
			return True
		except Exception as e:
			return False