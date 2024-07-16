from __future__ import unicode_literals
from ErpBackOffice.models import Model_Vehicule_model
from django.utils import timezone

class dao_vehicule_model(object):
	id = 0
	nom = ''
	type = ''
	logo = ''
	description = ''

	@staticmethod
	def toListVehicule_model():
		return Model_Vehicule_model.objects.all().order_by('-id')

	@staticmethod
	def toCreateVehicule_model(nom,type,logo,description):
		try:
			vehicule_model = dao_vehicule_model()
			vehicule_model.nom = nom
			vehicule_model.type = type
			vehicule_model.logo = logo
			vehicule_model.description = description
			return vehicule_model
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA VEHICULE_MODEL')
			#print(e)
			return None

	@staticmethod
	def toSaveVehicule_model(auteur, objet_dao_Vehicule_model):
		try:
			vehicule_model  = Model_Vehicule_model()
			vehicule_model.nom = objet_dao_Vehicule_model.nom
			vehicule_model.type = objet_dao_Vehicule_model.type
			vehicule_model.logo = objet_dao_Vehicule_model.logo
			vehicule_model.description = objet_dao_Vehicule_model.description
			vehicule_model.created_at = timezone.now()
			vehicule_model.updated_at = timezone.now()
			vehicule_model.auteur_id = auteur.id

			vehicule_model.save()
			return vehicule_model
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA VEHICULE_MODEL')
			#print(e)
			return None

	@staticmethod
	def toUpdateVehicule_model(id, objet_dao_Vehicule_model):
		try:
			vehicule_model = Model_Vehicule_model.objects.get(pk = id)
			vehicule_model.nom =objet_dao_Vehicule_model.nom
			vehicule_model.type =objet_dao_Vehicule_model.type
			vehicule_model.logo =objet_dao_Vehicule_model.logo
			vehicule_model.description =objet_dao_Vehicule_model.description
			vehicule_model.updated_at = timezone.now()
			vehicule_model.save()
			return vehicule_model
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA VEHICULE_MODEL')
			#print(e)
			return None
	@staticmethod
	def toGetVehicule_model(id):
		try:
			return Model_Vehicule_model.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteVehicule_model(id):
		try:
			vehicule_model = Model_Vehicule_model.objects.get(pk = id)
			vehicule_model.delete()
			return True
		except Exception as e:
			return False