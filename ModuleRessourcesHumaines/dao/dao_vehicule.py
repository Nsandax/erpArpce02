from __future__ import unicode_literals
from ErpBackOffice.models import Model_Vehicule
from django.utils import timezone

class dao_vehicule(object):
	id = 0
	designation = ''
	marque = ''
	vehicule_model_id = None
	date_acquisition = '2010-01-01'
	image = ''
	reference_licence = ''
	document_id = None
	employe_id = None
	couleur = ''
	transmission = ''
	type_carburant = ''
	description = ''

	@staticmethod
	def toListVehicule():
		return Model_Vehicule.objects.all().order_by('-id')

	@staticmethod
	def toCreateVehicule(designation,marque,vehicule_model_id,date_acquisition,image,reference_licence,document_id,employe_id,couleur,transmission,type_carburant,description):
		try:
			vehicule = dao_vehicule()
			vehicule.designation = designation
			vehicule.marque = marque
			vehicule.vehicule_model_id = vehicule_model_id
			vehicule.date_acquisition = date_acquisition
			vehicule.image = image
			vehicule.reference_licence = reference_licence
			vehicule.document_id = document_id
			vehicule.employe_id = employe_id
			vehicule.couleur = couleur
			vehicule.transmission = transmission
			vehicule.type_carburant = type_carburant
			vehicule.description = description
			return vehicule
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA VEHICULE')
			#print(e)
			return None

	@staticmethod
	def toSaveVehicule(auteur, objet_dao_Vehicule):
		try:
			vehicule  = Model_Vehicule()
			vehicule.designation = objet_dao_Vehicule.designation
			vehicule.marque = objet_dao_Vehicule.marque
			vehicule.vehicule_model_id = objet_dao_Vehicule.vehicule_model_id
			vehicule.date_acquisition = objet_dao_Vehicule.date_acquisition
			vehicule.image = objet_dao_Vehicule.image
			vehicule.reference_licence = objet_dao_Vehicule.reference_licence
			vehicule.document_id = objet_dao_Vehicule.document_id
			vehicule.employe_id = objet_dao_Vehicule.employe_id
			vehicule.couleur = objet_dao_Vehicule.couleur
			vehicule.transmission = objet_dao_Vehicule.transmission
			vehicule.type_carburant = objet_dao_Vehicule.type_carburant
			vehicule.description = objet_dao_Vehicule.description
			vehicule.created_at = timezone.now()
			vehicule.updated_at = timezone.now()
			vehicule.auteur_id = auteur.id

			vehicule.save()
			return vehicule
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA VEHICULE')
			#print(e)
			return None

	@staticmethod
	def toUpdateVehicule(id, objet_dao_Vehicule):
		try:
			vehicule = Model_Vehicule.objects.get(pk = id)
			vehicule.designation =objet_dao_Vehicule.designation
			vehicule.marque =objet_dao_Vehicule.marque
			vehicule.vehicule_model_id =objet_dao_Vehicule.vehicule_model_id
			vehicule.date_acquisition =objet_dao_Vehicule.date_acquisition
			vehicule.image =objet_dao_Vehicule.image
			vehicule.reference_licence =objet_dao_Vehicule.reference_licence
			vehicule.document_id =objet_dao_Vehicule.document_id
			vehicule.employe_id =objet_dao_Vehicule.employe_id
			vehicule.couleur =objet_dao_Vehicule.couleur
			vehicule.transmission =objet_dao_Vehicule.transmission
			vehicule.type_carburant =objet_dao_Vehicule.type_carburant
			vehicule.description =objet_dao_Vehicule.description
			vehicule.updated_at = timezone.now()
			vehicule.save()
			return vehicule
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA VEHICULE')
			#print(e)
			return None
	@staticmethod
	def toGetVehicule(id):
		try:
			return Model_Vehicule.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteVehicule(id):
		try:
			vehicule = Model_Vehicule.objects.get(pk = id)
			vehicule.delete()
			return True
		except Exception as e:
			return False