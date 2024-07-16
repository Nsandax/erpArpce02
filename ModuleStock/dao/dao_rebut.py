from __future__ import unicode_literals
from ModuleStock.models import Model_Rebut
from django.utils import timezone

class dao_rebut(object):
	id = 0
	numero = ''
	article = None
	serie_article = None
	quantite = 0.0
	unite = None
	emplacement = None
	emplacement_rebut = None
	document = ''

	@staticmethod
	def toList():
		return Model_Rebut.objects.all()

	@staticmethod
	def toCreate(numero,article_id,serie_article_id,quantite,unite_id,emplacement_id,emplacement_rebut_id,document,):
		try:
			rebut = dao_rebut()
			rebut.numero = numero
			rebut.article_id = article_id
			rebut.serie_article_id = serie_article_id
			rebut.quantite = quantite
			rebut.unite_id = unite_id
			rebut.emplacement_id = emplacement_id
			rebut.emplacement_rebut_id = emplacement_rebut_id
			rebut.document = document
			return rebut
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA REBUT')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_Rebut):
		try:
			rebut  = Model_Rebut()
			rebut.numero = objet_dao_Rebut.numero
			rebut.article_id = objet_dao_Rebut.article_id
			rebut.serie_article_id = objet_dao_Rebut.serie_article_id
			rebut.quantite = objet_dao_Rebut.quantite
			rebut.unite_id = objet_dao_Rebut.unite_id
			rebut.emplacement_id = objet_dao_Rebut.emplacement_id
			rebut.emplacement_rebut_id = objet_dao_Rebut.emplacement_rebut_id
			rebut.document = objet_dao_Rebut.document
			rebut.auteur_id = auteur.id
			rebut.save()
			return rebut
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA REBUT')
			#print(e)
			return None

	@staticmethod
	def toUpdate(id, objet_dao_Rebut):
		try:
			rebut = Model_Rebut.objects.get(pk = id)
			rebut.numero =objet_dao_Rebut.numero
			rebut.article_id =objet_dao_Rebut.article_id
			rebut.serie_article_id =objet_dao_Rebut.serie_article_id
			rebut.quantite =objet_dao_Rebut.quantite
			rebut.unite_id =objet_dao_Rebut.unite_id
			rebut.emplacement_id =objet_dao_Rebut.emplacement_id
			rebut.emplacement_rebut_id =objet_dao_Rebut.emplacement_rebut_id
			rebut.document =objet_dao_Rebut.document
			rebut.save()
			return rebut
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA REBUT')
			#print(e)
			return None

	@staticmethod
	def toGet(id):
		try:
			return Model_Rebut.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toDelete(id):
		try:
			rebut = Model_Rebut.objects.get(pk = id)
			rebut.delete()
			return True
		except Exception as e:
			return False