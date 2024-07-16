from __future__ import unicode_literals
from ErpBackOffice.models import Model_Immobilier
from django.utils import timezone

class dao_immobilier(object):
	id = 0
	numero_identification = ''
	article_id = None
	employe_id = None
	unite_fonctionelle_id = None

	@staticmethod
	def toListImmobilier():
		return Model_Immobilier.objects.all().order_by('-id')

	@staticmethod
	def toCreateImmobilier(numero_identification,article_id,employe_id,unite_fonctionelle_id):
		try:
			immobilier = dao_immobilier()
			immobilier.numero_identification = numero_identification
			immobilier.article_id = article_id
			immobilier.employe_id = employe_id
			immobilier.unite_fonctionelle_id = unite_fonctionelle_id
			return immobilier
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA IMMOBILIER')
			#print(e)
			return None

	@staticmethod
	def toSaveImmobilier(auteur, objet_dao_Immobilier):
		try:
			immobilier  = Model_Immobilier()
			immobilier.numero_identification = objet_dao_Immobilier.numero_identification
			immobilier.article_id = objet_dao_Immobilier.article_id
			immobilier.employe_id = objet_dao_Immobilier.employe_id
			immobilier.unite_fonctionelle_id = objet_dao_Immobilier.unite_fonctionelle_id
			immobilier.created_at = timezone.now()
			immobilier.updated_at = timezone.now()
			immobilier.auteur_id = auteur.id

			immobilier.save()
			return immobilier
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA IMMOBILIER')
			#print(e)
			return None

	@staticmethod
	def toUpdateImmobilier(id, objet_dao_Immobilier):
		try:
			immobilier = Model_Immobilier.objects.get(pk = id)
			immobilier.numero_identification =objet_dao_Immobilier.numero_identification
			immobilier.article_id =objet_dao_Immobilier.article_id
			immobilier.employe_id =objet_dao_Immobilier.employe_id
			immobilier.unite_fonctionelle_id =objet_dao_Immobilier.unite_fonctionelle_id
			immobilier.updated_at = timezone.now()
			immobilier.save()
			return immobilier
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA IMMOBILIER')
			#print(e)
			return None
	@staticmethod
	def toGetImmobilier(id):
		try:
			return Model_Immobilier.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteImmobilier(id):
		try:
			immobilier = Model_Immobilier.objects.get(pk = id)
			immobilier.delete()
			return True
		except Exception as e:
			return False