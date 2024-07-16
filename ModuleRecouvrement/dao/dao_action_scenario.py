from __future__ import unicode_literals
from ModuleRecouvrement.models import *
from ErpBackOffice.models import *
from django.utils import timezone

class dao_action_scenario(object):
	designation = ''
	nb_jours = 0
	type_action = ''
	scenario_id = None
	est_automatique = False
	description = ''
	sujet = ''
	message = ''
	langue = ''

	@staticmethod
	def toList(query=None):
		try:
			if query == None:
				return Model_Action_scenario.objects.all().order_by('creation_date')

			return Model_Action_scenario.objects.filter(Q(designation__icontains = query) | Q(nb_jours__icontains = query) | Q(type_action__icontains = query) | Q(description__icontains = query) | Q(sujet__icontains = query) | Q(message__icontains = query) | Q(langue__icontains = query)).order_by('creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE ACTION_SCENARIO')
			#print(e)
			return []

	@staticmethod
	def toCreate(designation = '', nb_jours = None, type_action = '', scenario_id = None, est_automatique = None, description = '', sujet = '', message = '', langue = ''):
		try:
			action_scenario = dao_action_scenario()
			action_scenario.designation = designation
			action_scenario.nb_jours = nb_jours
			action_scenario.type_action = type_action
			action_scenario.scenario_id = scenario_id
			action_scenario.est_automatique = est_automatique
			action_scenario.description = description
			action_scenario.sujet = sujet
			action_scenario.message = message
			action_scenario.langue = langue
			return action_scenario
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA ACTION_SCENARIO')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_action_scenario):
		try:
			action_scenario  = Model_Action_scenario()
			action_scenario.designation = objet_dao_action_scenario.designation
			action_scenario.nb_jours = objet_dao_action_scenario.nb_jours
			action_scenario.type_action = objet_dao_action_scenario.type_action
			action_scenario.scenario_id = objet_dao_action_scenario.scenario_id
			if objet_dao_action_scenario.est_automatique != None : action_scenario.est_automatique = objet_dao_action_scenario.est_automatique
			if objet_dao_action_scenario.description != None : action_scenario.description = objet_dao_action_scenario.description
			if objet_dao_action_scenario.sujet != None : action_scenario.sujet = objet_dao_action_scenario.sujet
			if objet_dao_action_scenario.message != None : action_scenario.message = objet_dao_action_scenario.message
			if objet_dao_action_scenario.langue != None : action_scenario.langue = objet_dao_action_scenario.langue
			if auteur != None : action_scenario.auteur_id = auteur.id

			action_scenario.save()

			return True, action_scenario, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA ACTION_SCENARIO')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_action_scenario):
		try:
			action_scenario = Model_Action_scenario.objects.get(pk = id)
			action_scenario.designation = objet_dao_action_scenario.designation
			action_scenario.nb_jours = objet_dao_action_scenario.nb_jours
			action_scenario.type_action = objet_dao_action_scenario.type_action
			action_scenario.scenario_id = objet_dao_action_scenario.scenario_id
			action_scenario.est_automatique = objet_dao_action_scenario.est_automatique
			action_scenario.description = objet_dao_action_scenario.description
			action_scenario.sujet = objet_dao_action_scenario.sujet
			action_scenario.message = objet_dao_action_scenario.message
			action_scenario.langue = objet_dao_action_scenario.langue
			action_scenario.save()

			return True, action_scenario, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA ACTION_SCENARIO')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Action_scenario.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Action_scenario.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			action_scenario = Model_Action_scenario.objects.get(pk = id)
			action_scenario.delete()
			return True
		except Exception as e:
			return False