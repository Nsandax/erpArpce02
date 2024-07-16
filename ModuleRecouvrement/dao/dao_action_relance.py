from __future__ import unicode_literals
from ModuleRecouvrement.models import *
from ErpBackOffice.models import *
from django.utils import timezone

class dao_action_relance(object):
	designation = ''
	date_action = '2010-01-01'
	montant_action = 0.0
	type_action = ''
	observation = ''
	statut_action = 0
	dossier_recouvrement_id = None
	facture_id = None

	@staticmethod
	def toList(query=None):
		try:
			if query == None:
				return Model_Action_relance.objects.all().order_by('creation_date')

			return Model_Action_relance.objects.filter(Q(designation__icontains = query) | Q(montant_action__icontains = query) | Q(type_action__icontains = query) | Q(observation__icontains = query) | Q(statut_action__icontains = query)).order_by('creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE ACTION_RELANCE')
			#print(e)
			return []

	@staticmethod
	def toCreate(designation = '', date_action = None, montant_action = None, type_action = '', observation = '', statut_action = None, dossier_recouvrement_id = None, facture_id = None):
		try:
			action_relance = dao_action_relance()
			action_relance.designation = designation
			action_relance.date_action = date_action
			action_relance.montant_action = montant_action
			action_relance.type_action = type_action
			action_relance.observation = observation
			action_relance.statut_action = statut_action
			action_relance.dossier_recouvrement_id = dossier_recouvrement_id
			action_relance.facture_id = facture_id
			return action_relance
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA ACTION_RELANCE')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_action_relance):
		try:
			action_relance  = Model_Action_relance()
			action_relance.designation = objet_dao_action_relance.designation
			action_relance.date_action = objet_dao_action_relance.date_action
			if objet_dao_action_relance.montant_action != None : action_relance.montant_action = objet_dao_action_relance.montant_action
			if objet_dao_action_relance.type_action != None : action_relance.type_action = objet_dao_action_relance.type_action
			if objet_dao_action_relance.observation != None : action_relance.observation = objet_dao_action_relance.observation
			action_relance.statut_action = objet_dao_action_relance.statut_action
			action_relance.dossier_recouvrement_id = objet_dao_action_relance.dossier_recouvrement_id
			action_relance.facture_id = objet_dao_action_relance.facture_id
			if auteur != None : action_relance.auteur_id = auteur.id

			action_relance.save()

			return True, action_relance, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA ACTION_RELANCE')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_action_relance):
		try:
			action_relance = Model_Action_relance.objects.get(pk = id)
			action_relance.designation = objet_dao_action_relance.designation
			action_relance.date_action = objet_dao_action_relance.date_action
			action_relance.montant_action = objet_dao_action_relance.montant_action
			action_relance.type_action = objet_dao_action_relance.type_action
			action_relance.observation = objet_dao_action_relance.observation
			action_relance.statut_action = objet_dao_action_relance.statut_action
			action_relance.dossier_recouvrement_id = objet_dao_action_relance.dossier_recouvrement_id
			action_relance.facture_id = objet_dao_action_relance.facture_id
			action_relance.save()

			return True, action_relance, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA ACTION_RELANCE')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Action_relance.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Action_relance.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			action_relance = Model_Action_relance.objects.get(pk = id)
			action_relance.delete()
			return True
		except Exception as e:
			return False