from __future__ import unicode_literals
from ModuleRecouvrement.models import *
from ErpBackOffice.models import *
from django.utils import timezone

class dao_secteur_activite(object):
	designation = ''
	description = ''

	@staticmethod
	def toList(query=None):
		try:
			if query == None:
				return Model_Secteur_activite.objects.all().order_by('creation_date')

			return Model_Secteur_activite.objects.filter(Q(designation__icontains = query) | Q(description__icontains = query)).order_by('creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE SECTEUR_ACTIVITE')
			#print(e)
			return []

	@staticmethod
	def toCreate(designation = '', description = ''):
		try:
			secteur_activite = dao_secteur_activite()
			secteur_activite.designation = designation
			secteur_activite.description = description
			return secteur_activite
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA SECTEUR_ACTIVITE')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_secteur_activite):
		try:
			secteur_activite  = Model_Secteur_activite()
			secteur_activite.designation = objet_dao_secteur_activite.designation
			if objet_dao_secteur_activite.description != None : secteur_activite.description = objet_dao_secteur_activite.description
			if auteur != None : secteur_activite.auteur_id = auteur.id

			secteur_activite.save()

			return True, secteur_activite, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA SECTEUR_ACTIVITE')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_secteur_activite):
		try:
			secteur_activite = Model_Secteur_activite.objects.get(pk = id)
			secteur_activite.designation = objet_dao_secteur_activite.designation
			secteur_activite.description = objet_dao_secteur_activite.description
			secteur_activite.save()

			return True, secteur_activite, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA SECTEUR_ACTIVITE')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Secteur_activite.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Secteur_activite.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			secteur_activite = Model_Secteur_activite.objects.get(pk = id)
			secteur_activite.delete()
			return True
		except Exception as e:
			return False