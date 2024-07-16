from __future__ import unicode_literals
from ErpBackOffice.models import Model_Rebut
from django.utils import timezone

class dao_rebut(object):
	numero = ''
	article_id = 0
	serie_article_id = 0
	quantite = 0.0
	unite_id = 0
	emplacement_id = 0
	emplacement_rebut_id = 0
	document = ''

	@staticmethod
	def toList():
		try:
			return Model_Rebut.objects.all()
		except Exception as e:
			return []

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
			print('ERREUR LORS DE LA CREATION DE LA REBUT')
			print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_Rebut):
		try:
			rebut  = Model_Rebut()
			# print('SAVE 1')
			rebut.numero = objet_dao_Rebut.numero
			rebut.article_id = objet_dao_Rebut.article_id
			rebut.serie_article_id = objet_dao_Rebut.serie_article_id
			rebut.quantite = objet_dao_Rebut.quantite
			rebut.unite_id = objet_dao_Rebut.unite_id
			# print('SAVE 2')
			rebut.emplacement_id = objet_dao_Rebut.emplacement_id
			# print('SAVE 3')
			rebut.emplacement_rebut_id = objet_dao_Rebut.emplacement_rebut_id
			rebut.document = objet_dao_Rebut.document
			# print('SAVE 4')
			rebut.auteur_id = auteur
			# print('SAVE 5')
			rebut.save()
			return rebut
		except Exception as e:
			print('ERREUR LORS DE L ENREGISTREMENT DE LA REBUT')
			print(e)
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


	@staticmethod
	def toGenerateNumero():
		total_rebut = dao_rebut.toList().count()
		total_rebut = total_rebut + 1
		temp_numero = str(total_rebut)

		for i in range(len(str(total_rebut)), 4):
			temp_numero = "0" + temp_numero

		mois = timezone.now().month
		if mois < 10: mois = "0%s" % mois

		temp_numero = "RB-%s%s%s" % (timezone.now().year, mois, temp_numero)
		return temp_numero