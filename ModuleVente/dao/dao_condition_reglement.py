from __future__ import unicode_literals
from ErpBackOffice.models import Model_Condition_reglement
from django.utils import timezone

class dao_condition_reglement(object):
	id = 0
	designation=''
	nombre_jour=0
	creation_date='2010-01-01'
	auteur_id = 0


	@staticmethod
	def toListConditionReglement():
		return Model_Condition_reglement.objects.all().order_by('-id')

	@staticmethod
	def toCreateConditionReglement(designation,nombre_jour):
		try:
			condition_reglement = dao_condition_reglement()
			condition_reglement.designation = designation
			condition_reglement.nombre_jour = nombre_jour
			return condition_reglement
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA CONDITION_REGLEMENT')
			#print(e)
			return None

	@staticmethod
	def toSaveConditionReglement(auteur,objet_dao_Condition_reglement):
		try:
			condition_reglement  = Model_Condition_reglement()
			condition_reglement.designation =objet_dao_Condition_reglement.designation
			condition_reglement.nombre_jour =objet_dao_Condition_reglement.nombre_jour
			condition_reglement.creation_date =timezone.now()
			condition_reglement.auteur_id=auteur.id
			condition_reglement.save()
			return condition_reglement
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA CONDITION_REGLEMENT')
			#print(e)
			return None

	@staticmethod
	def toUpdateConditionReglement(id, objet_dao_Condition_reglement):
		#print("touché")
		try:
			condition_reglement = Model_Condition_reglement.objects.get(pk = id)
			condition_reglement.designation =objet_dao_Condition_reglement.designation
			condition_reglement.nombre_jour =objet_dao_Condition_reglement.nombre_jour
		
			condition_reglement.save()
			return True
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA CONDITION_REGLEMENT')
			#print(e)
			return False


	@staticmethod
	def toGetConditionReglement(id):
		try:
			return Model_Condition_reglement.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteConditionReglement(id):
		try:
			condition_reglement = Model_Condition_reglement.objects.get(pk = id)
			condition_reglement.delete()
			return True
		except Exception as e:
			return False