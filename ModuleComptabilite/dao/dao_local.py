from __future__ import unicode_literals
from ErpBackOffice.models import Model_Local
from django.utils import timezone

class dao_local(object):
	id = 0
	designation = ''
	description = ''
	parent_id = 0

	@staticmethod
	def toListLocal():
		return Model_Local.objects.all().order_by('-id')

	@staticmethod
	def toCreateLocal(designation,description, type_local = 1, parent_id=0):
		try:
			local = dao_local()
			local.designation = designation
			local.description = description
			local.type_local = type_local
			if parent_id != 0 : local.parent_id = parent_id
			return local
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA LOCAL')
			#print(e)
			return None

	@staticmethod
	def toSaveLocal(auteur, objet_dao_Local):
		try:
			local  = Model_Local()
			local.designation = objet_dao_Local.designation
			local.description = objet_dao_Local.description
			local.type_local = objet_dao_Local.type_local
			local.parent_id = objet_dao_Local.parent_id
			local.created_at = timezone.now()
			local.updated_at = timezone.now()
			local.auteur_id = auteur.id

			local.save()
			return local
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA LOCAL')
			#print(e)
			return None

	@staticmethod
	def toUpdateLocal(id, objet_dao_Local):
		try:
			local = Model_Local.objects.get(pk = id)
			local.designation =objet_dao_Local.designation
			local.description =objet_dao_Local.description
			local.type_local = objet_dao_Local.type_local
			local.parent_id = objet_dao_Local.parent_id
			local.updated_at = timezone.now()
			local.save()
			return local
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA LOCAL')
			#print(e)
			return None
	@staticmethod
	def toGetLocal(id):
		try:
			return Model_Local.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteLocal(id):
		try:
			local = Model_Local.objects.get(pk = id)
			local.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toListLocalFilles(parent_id):
		return Model_Local.objects.filter(parent_id = parent_id).order_by("designation")