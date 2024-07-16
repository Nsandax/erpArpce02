from __future__ import unicode_literals
from ErpBackOffice.models import Model_Activite
from django.utils import timezone

class dao_activite(object):
	id = 0
	code = ''
	designation = ''

	@staticmethod
	def toListActivite():
		return Model_Activite.objects.all().order_by('-id')

	@staticmethod
	def toCreateActivite(code,designation):
		try:
			activite = dao_activite()
			activite.code = code
			activite.designation = designation
			return activite
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA ACTIVITE')
			#print(e)
			return None

	@staticmethod
	def toSaveActivite(auteur, objet_dao_Activite):
		try:
			activite  = Model_Activite()
			activite.code = objet_dao_Activite.code
			activite.designation = objet_dao_Activite.designation
			activite.created_at = timezone.now()
			activite.updated_at = timezone.now()
			activite.auteur_id = auteur.id

			activite.save()
			return activite
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA ACTIVITE')
			#print(e)
			return None

	@staticmethod
	def toUpdateActivite(id, objet_dao_Activite):
		try:
			activite = Model_Activite.objects.get(pk = id)
			activite.code =objet_dao_Activite.code
			activite.designation =objet_dao_Activite.designation
			activite.updated_at = timezone.now()
			activite.save()
			return activite
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA ACTIVITE')
			#print(e)
			return None
	@staticmethod
	def toGetActivite(id):
		try:
			return Model_Activite.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteActivite(id):
		try:
			activite = Model_Activite.objects.get(pk = id)
			activite.delete()
			return True
		except Exception as e:
			return False