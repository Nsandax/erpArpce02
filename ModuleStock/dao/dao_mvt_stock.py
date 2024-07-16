from __future__ import unicode_literals
from ModuleStock.models import Model_Mvt_Stock
from django.utils import timezone

class dao_mvt_stock(object):
	id = 0
	type = None
	article = None
	series = None
	emplacement = None
	operation = None
	ajustement = None
	rebut = None
	document = ''
	quantite_initiale = 0.0
	unite_initiale = None
	quantite = 0.0
	unite = None
	est_fabrication = False
	est_destruction = False
	est_ajustement = False
	est_rebut = False

	@staticmethod
	def toList():
		return Model_Mvt_Stock.objects.all()

	@staticmethod
	def toCreate(type_id,article_id,series_id,emplacement_id,operation_id,ajustement_id,rebut_id,document,quantite_initiale,unite_initiale_id,quantite,unite_id,est_fabrication,est_destruction,est_ajustement,est_rebut):
		try:
			mvt_stock = dao_mvt_stock()
			mvt_stock.type_id = type_id
			mvt_stock.article_id = article_id
			mvt_stock.series_id = series_id
			mvt_stock.emplacement_id = emplacement_id
			mvt_stock.operation_id = operation_id
			mvt_stock.ajustement_id = ajustement_id
			mvt_stock.rebut_id = rebut_id
			mvt_stock.document = document
			mvt_stock.quantite_initiale = quantite_initiale
			mvt_stock.unite_initiale_id = unite_initiale_id
			mvt_stock.quantite = quantite
			mvt_stock.unite_id = unite_id
			mvt_stock.est_fabrication = est_fabrication
			mvt_stock.est_destruction = est_destruction
			mvt_stock.est_ajustement = est_ajustement
			mvt_stock.est_rebut = est_rebut
			return mvt_stock
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA MVT_STOCK')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_Mvt_stock):
		try:
			mvt_stock  = Model_Mvt_Stock()
			mvt_stock.type_id = objet_dao_Mvt_stock.type_id
			mvt_stock.article_id = objet_dao_Mvt_stock.article_id
			mvt_stock.series_id = objet_dao_Mvt_stock.series_id
			mvt_stock.emplacement_id = objet_dao_Mvt_stock.emplacement_id
			mvt_stock.operation_id = objet_dao_Mvt_stock.operation_id
			mvt_stock.ajustement_id = objet_dao_Mvt_stock.ajustement_id
			mvt_stock.rebut_id = objet_dao_Mvt_stock.rebut_id
			mvt_stock.document = objet_dao_Mvt_stock.document
			mvt_stock.quantite_initiale = objet_dao_Mvt_stock.quantite_initiale
			mvt_stock.unite_initiale_id = objet_dao_Mvt_stock.unite_initiale_id
			mvt_stock.quantite = objet_dao_Mvt_stock.quantite
			mvt_stock.unite_id = objet_dao_Mvt_stock.unite_id
			mvt_stock.est_fabrication = objet_dao_Mvt_stock.est_fabrication
			mvt_stock.est_destruction = objet_dao_Mvt_stock.est_destruction
			mvt_stock.est_ajustement = objet_dao_Mvt_stock.est_ajustement
			mvt_stock.est_rebut = objet_dao_Mvt_stock.est_rebut
			mvt_stock.auteur_id = auteur.id
			mvt_stock.save()
			return mvt_stock
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA MVT_STOCK')
			#print(e)
			return None

	@staticmethod
	def toUpdate(id, objet_dao_Mvt_stock):
		try:
			mvt_stock = Model_Mvt_Stock.objects.get(pk = id)
			mvt_stock.type_id =objet_dao_Mvt_stock.type_id
			mvt_stock.article_id =objet_dao_Mvt_stock.article_id
			mvt_stock.series_id =objet_dao_Mvt_stock.series_id
			mvt_stock.emplacement_id =objet_dao_Mvt_stock.emplacement_id
			mvt_stock.operation_id =objet_dao_Mvt_stock.operation_id
			mvt_stock.ajustement_id =objet_dao_Mvt_stock.ajustement_id
			mvt_stock.rebut_id =objet_dao_Mvt_stock.rebut_id
			mvt_stock.document =objet_dao_Mvt_stock.document
			mvt_stock.quantite_initiale =objet_dao_Mvt_stock.quantite_initiale
			mvt_stock.unite_initiale_id =objet_dao_Mvt_stock.unite_initiale_id
			mvt_stock.quantite =objet_dao_Mvt_stock.quantite
			mvt_stock.unite_id =objet_dao_Mvt_stock.unite_id
			mvt_stock.est_fabrication =objet_dao_Mvt_stock.est_fabrication
			mvt_stock.est_destruction =objet_dao_Mvt_stock.est_destruction
			mvt_stock.est_ajustement =objet_dao_Mvt_stock.est_ajustement
			mvt_stock.est_rebut =objet_dao_Mvt_stock.est_rebut
			mvt_stock.save()
			return mvt_stock
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA MVT_STOCK')
			#print(e)
			return None

	@staticmethod
	def toGet(id):
		try:
			return Model_Mvt_Stock.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toDelete(id):
		try:
			mvt_stock = Model_Mvt_Stock.objects.get(pk = id)
			mvt_stock.delete()
			return True
		except Exception as e:
			return False