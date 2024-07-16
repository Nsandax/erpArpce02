from __future__ import unicode_literals
from ModuleRecouvrement.models import *
from ErpBackOffice.models import *
from django.utils import timezone

class dao_scenario_relance(object):
	designation = ''
	description = ''

	@staticmethod
	def toList(query=None):
		try:
			if query == None:
				return Model_Scenario_relance.objects.all().order_by('creation_date')

			return Model_Scenario_relance.objects.filter(Q(designation__icontains = query) | Q(description__icontains = query)).order_by('creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE SCENARIO_RELANCE')
			#print(e)
			return []

	@staticmethod
	def toCreate(designation = '', description = ''):
		try:
			scenario_relance = dao_scenario_relance()
			scenario_relance.designation = designation
			scenario_relance.description = description
			return scenario_relance
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA SCENARIO_RELANCE')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_scenario_relance):
		try:
			scenario_relance  = Model_Scenario_relance()
			scenario_relance.designation = objet_dao_scenario_relance.designation
			if objet_dao_scenario_relance.description != None : scenario_relance.description = objet_dao_scenario_relance.description
			if auteur != None : scenario_relance.auteur_id = auteur.id

			scenario_relance.save()

			return True, scenario_relance, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA SCENARIO_RELANCE')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_scenario_relance):
		try:
			scenario_relance = Model_Scenario_relance.objects.get(pk = id)
			scenario_relance.designation = objet_dao_scenario_relance.designation
			scenario_relance.description = objet_dao_scenario_relance.description
			scenario_relance.save()

			return True, scenario_relance, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA SCENARIO_RELANCE')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Scenario_relance.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Scenario_relance.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			scenario_relance = Model_Scenario_relance.objects.get(pk = id)
			scenario_relance.delete()
			return True
		except Exception as e:
			return False