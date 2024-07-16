from __future__ import unicode_literals
from ErpBackOffice.models import Model_Ligne_transfert
from django.utils import timezone

class dao_ligne_transfert(object):
	id = 0
	quantite_demandee=0
	quantite_fournie=0
	creation_date='2010-01-01'
	type=''
	bon_transfert_id=0
	stock_article_id = 0
	auteur_id = 0
	numero_serie = ""
	description = ""

	@staticmethod
	def toListLigneTransfert():
		return Model_Ligne_transfert.objects.all().order_by('-id')

	@staticmethod
	def toListLignesTransfert(bon_transfert_id):
		return Model_Ligne_transfert.objects.filter(bon_transfert_id = bon_transfert_id).order_by("-creation_date")

	@staticmethod
	def toCreateLigneTransfert(bon_transfert_id, stock_article_id, quantite_demandee, quantite_fournie, numero_serie, description, prix_unitaire = 0, prix_lot = 0,type = 0):
		try:
			ligne_transfert = dao_ligne_transfert()
			ligne_transfert.quantite_demandee = quantite_demandee
			ligne_transfert.quantite_fournie = quantite_fournie
			ligne_transfert.type = type
			ligne_transfert.bon_transfert_id = bon_transfert_id
			ligne_transfert.stock_article_id = stock_article_id
			ligne_transfert.numero_serie = numero_serie
			ligne_transfert.description = description
			return ligne_transfert
		except Exception as e:
			print('ERREUR LORS DE LA CREATION DE LA LIGNE_transfert')
			print(e)
			return None

	@staticmethod
	def toSaveLigneTransfert(auteur,objet_dao_Ligne_transfert):
		try:
			ligne_transfert  = Model_Ligne_transfert()
			ligne_transfert.quantite_demandee =objet_dao_Ligne_transfert.quantite_demandee
			ligne_transfert.quantite_fournie =objet_dao_Ligne_transfert.quantite_fournie
			ligne_transfert.creation_date =timezone.now()
			ligne_transfert.type =objet_dao_Ligne_transfert.type
			ligne_transfert.bon_transfert_id = objet_dao_Ligne_transfert.bon_transfert_id
			ligne_transfert.stock_article_id = objet_dao_Ligne_transfert.stock_article_id
			ligne_transfert.auteur_id = auteur.id
			ligne_transfert.numero_serie = objet_dao_Ligne_transfert.numero_serie
			ligne_transfert.description = objet_dao_Ligne_transfert.description
			ligne_transfert.save()
			return ligne_transfert
		except Exception as e:
			print('ERREUR LORS DE L ENREGISTREMENT DE LA LIGNE_transfert')
			print(e)
			return None

	@staticmethod
	def toUpdateLigneTransfert(id, objet_dao_Ligne_transfert):
		try:
			ligne_transfert = Model_Ligne_transfert.objects.get(pk = id)
			ligne_transfert.quantite_demandee =objet_dao_Ligne_transfert.quantite_demandee
			ligne_transfert.quantite_fournie =objet_dao_Ligne_transfert.quantite_fournie
			ligne_transfert.type =objet_dao_Ligne_transfert.type
			ligne_transfert.bon_transfert_id = objet_dao_Ligne_transfert.bon_transfert_id
			ligne_transfert.stock_article_id = objet_dao_Ligne_transfert.stock_article_id
			ligne_transfert.numero_serie = objet_dao_Ligne_transfert.numero_serie
			ligne_transfert.description = objet_dao_Ligne_transfert.description
			ligne_transfert.save()
			return ligne_transfert
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA LIGNE_transfert')
			#print(e)
			return None
	@staticmethod
	def toGetLigneTransfert(id):
		try:
			return Model_Ligne_transfert.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteLigneTransfert(id):
		try:
			ligne_transfert = Model_Ligne_transfert.objects.get(pk = id)
			ligne_transfert.delete()
			return True
		except Exception as e:
			return False