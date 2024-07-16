from __future__ import unicode_literals
from ModuleStock.models import Model_Stockage
from django.utils import timezone

class dao_stockage(object):
	id = 0
	emplacement = None
	article = None
	quantite = 0.0
	unite = None

	@staticmethod
	def toList():
		return Model_Stockage.objects.all()

	@staticmethod
	def toCreate(emplacement_id,article_id,quantite,unite_id):
		try:
			stockage = dao_stockage()
			stockage.emplacement_id = emplacement_id
			stockage.article_id = article_id
			stockage.quantite = quantite
			stockage.unite_id = unite_id
			return stockage
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA STOCKAGE')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_Stockage):
		try:
			stockage  = Model_Stockage()
			stockage.emplacement_id = objet_dao_Stockage.emplacement_id
			stockage.article_id = objet_dao_Stockage.article_id
			stockage.quantite = objet_dao_Stockage.quantite
			stockage.unite_id = objet_dao_Stockage.unite_id
			stockage.auteur_id = auteur.id
			stockage.save()
			return stockage
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA STOCKAGE')
			#print(e)
			return None

	@staticmethod
	def toUpdate(id, objet_dao_Stockage):
		try:
			stockage = Model_Stockage.objects.get(pk = id)
			stockage.emplacement_id =objet_dao_Stockage.emplacement_id
			stockage.article_id =objet_dao_Stockage.article_id
			stockage.quantite =objet_dao_Stockage.quantite
			stockage.unite_id =objet_dao_Stockage.unite_id
			stockage.save()
			return stockage
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA STOCKAGE')
			#print(e)
			return None

	@staticmethod
	def toGet(id):
		try:
			return Model_Stockage.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toDelete(id):
		try:
			stockage = Model_Stockage.objects.get(pk = id)
			stockage.delete()
			return True
		except Exception as e:
			return False