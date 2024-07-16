from __future__ import unicode_literals
from ErpBackOffice.models import Model_Type_conge
from django.utils import timezone

class dao_type_conge(object):
	id = 0
	designation = ''
	nombre_limite = 0
	is_active = False
	max_leaves = 0
	leaves_taken = 0
	remaining = 0
	double_validation = False

	@staticmethod
	def toListType_conge():
		return Model_Type_conge.objects.all().order_by('-id')

	@staticmethod
	def toCreateType_conge(designation,nombre_limite,is_active,max_leaves,leaves_taken,remaining,double_validation):
		try:
			type_conge = dao_type_conge()
			type_conge.designation = designation
			type_conge.nombre_limite = nombre_limite
			type_conge.is_active = is_active
			type_conge.max_leaves = max_leaves
			type_conge.leaves_taken = leaves_taken
			type_conge.remaining = remaining
			type_conge.double_validation = double_validation
			return type_conge
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA TYPE_CONGE')
			#print(e)
			return None

	@staticmethod
	def toSaveType_conge(auteur, objet_dao_Type_conge):
		try:
			type_conge  = Model_Type_conge()
			type_conge.designation = objet_dao_Type_conge.designation
			type_conge.nombre_limite = objet_dao_Type_conge.nombre_limite
			type_conge.is_active = objet_dao_Type_conge.is_active
			type_conge.max_leaves = objet_dao_Type_conge.max_leaves
			type_conge.leaves_taken = objet_dao_Type_conge.leaves_taken
			type_conge.remaining = objet_dao_Type_conge.remaining
			type_conge.double_validation = objet_dao_Type_conge.double_validation
			type_conge.created_at = timezone.now()
			type_conge.updated_at = timezone.now()
			type_conge.auteur_id = auteur.id

			type_conge.save()
			return type_conge
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA TYPE_CONGE')
			#print(e)
			return None

	@staticmethod
	def toUpdateType_conge(id, objet_dao_Type_conge):
		try:
			type_conge = Model_Type_conge.objects.get(pk = id)
			type_conge.designation =objet_dao_Type_conge.designation
			type_conge.nombre_limite =objet_dao_Type_conge.nombre_limite
			type_conge.is_active =objet_dao_Type_conge.is_active
			type_conge.max_leaves =objet_dao_Type_conge.max_leaves
			type_conge.leaves_taken =objet_dao_Type_conge.leaves_taken
			type_conge.remaining =objet_dao_Type_conge.remaining
			type_conge.double_validation =objet_dao_Type_conge.double_validation
			type_conge.updated_at = timezone.now()
			type_conge.save()
			return type_conge
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA TYPE_CONGE')
			#print(e)
			return None

	@staticmethod
	def toGetType_conge(id):
		try:
			return Model_Type_conge.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toComputeDayOfTypeConge(id):
		try:
			untype =  Model_Type_conge.objects.get(pk = id)
			untype.leaves_taken += 1
			untype.remaining -= 1
			untype.save()
		except Exception as e:
			return None


	@staticmethod
	def toDeleteType_conge(id):
		try:
			type_conge = Model_Type_conge.objects.get(pk = id)
			type_conge.delete()
			return True
		except Exception as e:
			return False