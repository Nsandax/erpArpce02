from __future__ import unicode_literals
from ErpBackOffice.models import Model_Operationnalisation_module
from django.utils import timezone
import datetime


class dao_operationnalisation_module(object):
	id = 0
	designation = ''
	date_debut = '2010-01-01'
	date_fin = '2010-01-01'
	est_active = False
	est_cloture = False
	observation = ''
	module_id = None

	@staticmethod
	def toListOperationnalisation_module():
		return Model_Operationnalisation_module.objects.all()

	@staticmethod
	def toCreateOperationnalisation_module(designation,date_debut,date_fin,est_active,est_cloture,observation,module_id):
		try:
			operationnalisation_module = dao_operationnalisation_module()
			operationnalisation_module.designation = designation
			operationnalisation_module.date_debut = date_debut
			operationnalisation_module.date_fin = date_fin
			operationnalisation_module.est_active = est_active
			operationnalisation_module.est_cloture = est_cloture
			operationnalisation_module.observation = observation
			operationnalisation_module.module_id = module_id
			return operationnalisation_module
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA OPERATIONNALISATION_MODULE')
			#print(e)
			return None

	@staticmethod
	def toSaveOperationnalisation_module(auteur, objet_dao_Operationnalisation_module):
		try:
			operationnalisation_module  = Model_Operationnalisation_module()
			operationnalisation_module.designation = objet_dao_Operationnalisation_module.designation
			operationnalisation_module.date_debut = objet_dao_Operationnalisation_module.date_debut
			operationnalisation_module.date_fin = objet_dao_Operationnalisation_module.date_fin
			operationnalisation_module.est_active = objet_dao_Operationnalisation_module.est_active
			operationnalisation_module.est_cloture = objet_dao_Operationnalisation_module.est_cloture
			operationnalisation_module.observation = objet_dao_Operationnalisation_module.observation
			operationnalisation_module.module_id = objet_dao_Operationnalisation_module.module_id
			operationnalisation_module.created_at = timezone.now()
			operationnalisation_module.updated_at = timezone.now()
			operationnalisation_module.auteur_id = auteur.id

			operationnalisation_module.save()
			return operationnalisation_module
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA OPERATIONNALISATION_MODULE')
			#print(e)
			return None

	@staticmethod
	def toUpdateOperationnalisation_module(id, objet_dao_Operationnalisation_module):
		try:
			operationnalisation_module = Model_Operationnalisation_module.objects.get(pk = id)
			operationnalisation_module.designation =objet_dao_Operationnalisation_module.designation
			operationnalisation_module.date_debut =objet_dao_Operationnalisation_module.date_debut
			operationnalisation_module.date_fin =objet_dao_Operationnalisation_module.date_fin
			operationnalisation_module.est_active =objet_dao_Operationnalisation_module.est_active
			operationnalisation_module.est_cloture =objet_dao_Operationnalisation_module.est_cloture
			operationnalisation_module.observation =objet_dao_Operationnalisation_module.observation
			operationnalisation_module.module_id =objet_dao_Operationnalisation_module.module_id
			operationnalisation_module.updated_at = timezone.now()
			operationnalisation_module.save()
			return operationnalisation_module
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA OPERATIONNALISATION_MODULE')
			#print(e)
			return None
	@staticmethod
	def toGetOperationnalisation_module(id):
		try:
			return Model_Operationnalisation_module.objects.get(pk = id)
		except Exception as e:
			return None
	
	@staticmethod
	def toGetOperationnalisationModuleOf(module_id):
		try:
			return Model_Operationnalisation_module.objects.filter(module_id = module_id)
		except Exception as e:
			return None
	
	@staticmethod
	def toSetStatusOperationnalisation(id, status):
		try:
			operationnalisation_module =  Model_Operationnalisation_module.objects.get(pk = id)
			if status == 1:
				operationnalisation_module.est_active = True
				operationnalisation_module.est_cloture = False
				operationnalisation_module.save()
				return True
			elif status == 2:
				operationnalisation_module.est_cloture = True
				operationnalisation_module.est_active = False
				operationnalisation_module.save()
				return True
			return False
		except Exception as e:
			return False

	@staticmethod
	def toDeleteOperationnalisation_module(id):
		try:
			operationnalisation_module = Model_Operationnalisation_module.objects.get(pk = id)
			operationnalisation_module.delete()
			return True
		except Exception as e:
			return False