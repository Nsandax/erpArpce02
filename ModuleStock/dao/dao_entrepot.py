from __future__ import unicode_literals
from ModuleStock.models import Model_Entrepot
from django.utils import timezone

class dao_entrepot(object):
	id = 0
	designation = ''
	designation_court = ''
	est_principal = False
	services_ref_id = None

	@staticmethod
	def toList():
		return Model_Entrepot.objects.all()

	@staticmethod
	def toCreate(designation,designation_court,est_principal,services_ref_id):
		try:
			entrepot = dao_entrepot()
			entrepot.designation = designation
			entrepot.designation_court = designation_court
			entrepot.est_principal = est_principal
			entrepot.services_ref_id = services_ref_id
			return entrepot
		except Exception as e:
			print('ERREUR LORS DE LA CREATION DE LA ENTREPOT')
			print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_Entrepot):
		try:
			entrepot  = Model_Entrepot()
			entrepot.designation = objet_dao_Entrepot.designation
			entrepot.designation_court = objet_dao_Entrepot.designation_court
			entrepot.est_principal = objet_dao_Entrepot.est_principal
			entrepot.services_ref_id = objet_dao_Entrepot.services_ref_id
			entrepot.auteur_id = auteur.id
			entrepot.save()
			return entrepot
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA ENTREPOT')
			#print(e)
			return None

	@staticmethod
	def toUpdate(id, objet_dao_Entrepot):
		try:
			entrepot = Model_Entrepot.objects.get(pk = id)
			entrepot.designation =objet_dao_Entrepot.designation
			entrepot.designation_court =objet_dao_Entrepot.designation_court
			entrepot.est_principal =objet_dao_Entrepot.est_principal
			entrepot.services_ref_id =objet_dao_Entrepot.services_ref_id
			entrepot.save()
			return entrepot
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA ENTREPOT')
			#print(e)
			return None

	@staticmethod
	def toGet(id):
		try:
			return Model_Entrepot.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toDelete(id):
		try:
			entrepot = Model_Entrepot.objects.get(pk = id)
			entrepot.delete()
			return True
		except Exception as e:
			return False