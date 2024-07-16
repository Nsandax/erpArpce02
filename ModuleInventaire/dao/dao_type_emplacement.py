from __future__ import unicode_literals
from ErpBackOffice.models import Model_TypeEmplacement
from django.utils import timezone

class dao_type_emplacement(object):
	id = 0
	designation=''
	creation_date='2010-01-01'
	auteur_id = 0
	est_system = False

	@staticmethod
	def toListTypeEmplacement():
		return Model_TypeEmplacement.objects.all().order_by('-id')

	@staticmethod
	def toCreateTypeEmplacement(designation,est_system):
		try:
			type_emplacement = dao_type_emplacement()
			type_emplacement.designation = designation
			type_emplacement.est_system = est_system
			return type_emplacement
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA TYPE_EMPLACEMENT')
			#print(e)
			return None

	@staticmethod
	def toSaveTypeEmplacement(auteur,objet_dao_Type_emplacement):
		try:
			type_emplacement  = Model_TypeEmplacement()
			type_emplacement.designation =objet_dao_Type_emplacement.designation
			type_emplacement.est_system =objet_dao_Type_emplacement.est_system
			type_emplacement.creation_date =timezone.now()
			type_emplacement.auteur_id =auteur.id
			type_emplacement.save()
			return type_emplacement
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA TYPE_EMPLACEMENT')
			#print(e)
			return None

	@staticmethod
	def toUpdateTypeEmplacement(id, objet_dao_Type_emplacement):
		try:
			type_emplacement = Model_TypeEmplacement.objects.get(pk = id)
			type_emplacement.designation =objet_dao_Type_emplacement.designation
			type_emplacement.est_system =objet_dao_Type_emplacement.est_system
			type_emplacement.save()
			return type_emplacement
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA TYPE_EMPLACEMENT')
			#print(e)
			return None
	@staticmethod
	def toGetTypeEmplacement(id):
		try:
			return Model_TypeEmplacement.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteTypeEmplacement(id):
		try:
			type_emplacement = Model_TypeEmplacement.objects.get(pk = id)
			type_emplacement.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toGetTypeEmplacementEntree():
		try:
			return Model_TypeEmplacement.objects.get(designation = "IN")
		except Exception as e:
			return None

	@staticmethod
	def toGetTypeEmplacementReserve():
		try:
			return Model_TypeEmplacement.objects.get(designation = "RESERVE")
		except Exception as e:
			return None


	@staticmethod
	def toGetTypeEmplacementEntrepot():
		try:
			return Model_TypeEmplacement.objects.get(designation = "ENTREPOT")
		except Exception as e:
			return None


	@staticmethod
	def toGetTypeEmplacementStock():
		try:
			return Model_TypeEmplacement.objects.get(designation = "STOCK")
		except Exception as e:
			return None

	@staticmethod
	def toGetTypeEmplacementInterne():
		try:
			return Model_TypeEmplacement.objects.get(designation = "INTERNAL")
		except Exception as e:
			return None
