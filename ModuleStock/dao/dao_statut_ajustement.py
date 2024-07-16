from __future__ import unicode_literals
from ModuleStock.models import Model_Statut_Ajustement
from django.utils import timezone

class dao_statut_ajustement(object):
	id = 0
	designation = ''

	@staticmethod
	def toList():
		return Model_Statut_Ajustement.objects.all()

	@staticmethod
	def toCreate(designation):
		try:
			statut_ajustement = dao_statut_ajustement()
			statut_ajustement.designation = designation
			return statut_ajustement
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA STATUT_AJUSTEMENT')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_Statut_ajustement):
		try:
			statut_ajustement  = Model_Statut_Ajustement()
			statut_ajustement.designation = objet_dao_Statut_ajustement.designation
			statut_ajustement.auteur_id = auteur.id
			statut_ajustement.save()
			return statut_ajustement
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA STATUT_AJUSTEMENT')
			#print(e)
			return None

	@staticmethod
	def toUpdate(id, objet_dao_Statut_ajustement):
		try:
			statut_ajustement = Model_Statut_Ajustement.objects.get(pk = id)
			statut_ajustement.designation =objet_dao_Statut_ajustement.designation
			statut_ajustement.save()
			return statut_ajustement
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA STATUT_AJUSTEMENT')
			#print(e)
			return None

	@staticmethod
	def toGet(id):
		try:
			return Model_Statut_Ajustement.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toDelete(id):
		try:
			statut_ajustement = Model_Statut_Ajustement.objects.get(pk = id)
			statut_ajustement.delete()
			return True
		except Exception as e:
			return False