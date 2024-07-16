from __future__ import unicode_literals
from ErpBackOffice.models import Model_Ligne_transfert
from ErpBackOffice.models import Model_Ligne_bon_retour
from django.utils import timezone

class dao_ligne_bon_retour(object):
	id = 0
	quantite_demandee=0
	quantite_fournie=0
	creation_date='2022-03-09'
	type=''
	bon_retour_id=0
	stock_article_id = 0
	auteur_id = 0
	numero_serie = ""
	description = ""

	@staticmethod
	def toListLigneBonRetour():
		return Model_Ligne_bon_retour.objects.all().order_by('-id')

	@staticmethod
	def toListLignesBonRetour(bon_retour_id):
		return Model_Ligne_bon_retour.objects.filter(bon_retour_id = bon_retour_id).order_by("-creation_date")

	@staticmethod
	def toCreateLigneBonRetour(bon_retour_id, stock_article_id, quantite_demandee, quantite_fournie, numero_serie, description, prix_unitaire = 0, prix_lot = 0,type = 0):
		try:
			ligne_bon_retour = dao_ligne_bon_retour()
			ligne_bon_retour.quantite_demandee = quantite_demandee
			ligne_bon_retour.quantite_fournie = quantite_fournie
			ligne_bon_retour.type = type
			ligne_bon_retour.bon_retour_id = bon_retour_id
			ligne_bon_retour.stock_article_id = stock_article_id
			ligne_bon_retour.numero_serie = numero_serie
			ligne_bon_retour.description = description
			return ligne_bon_retour
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA LIGNE_BON_RETOUR')
			#print(e)
			return None

	@staticmethod
	def toSaveLigneBonRetour(auteur,objet_dao_Ligne_Bon_Retour):
		try:
			ligne_bon_retour  = Model_Ligne_bon_retour()
			ligne_bon_retour.quantite_demandee =objet_dao_Ligne_Bon_Retour.quantite_demandee
			ligne_bon_retour.quantite_fournie =objet_dao_Ligne_Bon_Retour.quantite_fournie
			ligne_bon_retour.creation_date =timezone.now()
			ligne_bon_retour.type =objet_dao_Ligne_Bon_Retour.type
			ligne_bon_retour.bon_retour_id = objet_dao_Ligne_Bon_Retour.bon_retour_id
			ligne_bon_retour.stock_article_id = objet_dao_Ligne_Bon_Retour.stock_article_id
			ligne_bon_retour.auteur_id = auteur.id
			ligne_bon_retour.numero_serie = objet_dao_Ligne_Bon_Retour.numero_serie
			ligne_bon_retour.description = objet_dao_Ligne_Bon_Retour.description
			ligne_bon_retour.save()
			return ligne_bon_retour
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA LIGNE_BON_RETOUR')
			#print(e)
			return None

	@staticmethod
	def toUpdateLigneBonRetour(id, objet_dao_ligne_bon_retour):
		try:
			ligne_bon_retour = Model_Ligne_bon_retour.objects.get(pk = id)
			ligne_bon_retour.quantite_demandee =objet_dao_ligne_bon_retour.quantite_demandee
			ligne_bon_retour.quantite_fournie =objet_dao_ligne_bon_retour.quantite_fournie
			ligne_bon_retour.type =objet_dao_ligne_bon_retour.type
			ligne_bon_retour.bon_retour_id = objet_dao_ligne_bon_retour.bon_retour_id
			ligne_bon_retour.stock_article_id = objet_dao_ligne_bon_retour.stock_article_id
			ligne_bon_retour.numero_serie = objet_dao_ligne_bon_retour.numero_serie
			ligne_bon_retour.description = objet_dao_ligne_bon_retour.description
			ligne_bon_retour.save()
			return ligne_bon_retour
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA LIGNE_BON_RETOUR')
			#print(e)
			return None
	@staticmethod
	def toGetLigneBonRetour(id):
		try:
			return Model_Ligne_bon_retour.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteLigneBonRetour(id):
		try:
			ligne_bon_retour = Model_Ligne_bon_retour.objects.get(pk = id)
			ligne_bon_retour.delete()
			return True
		except Exception as e:
			return False