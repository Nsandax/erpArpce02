from __future__ import unicode_literals
from ErpBackOffice.models import Model_Dependant
from django.utils import timezone
import unidecode

class dao_dependant(object):
	id = 0
	nom_complet = ''
	type_dependance=''
	description=0
	creation_date=None
	date_naissance = None
	employe_id = None
	document_id = None
	auteur_id = None

	@staticmethod
	def toListDependant():
		return Model_Dependant.objects.all().order_by('-id')

	@staticmethod
	def toListDependantByEmploye(employe_id):
		return Model_Dependant.objects.filter(employe_id = employe_id)

	@staticmethod
	def toCreateDependant(nom_complet,type_dependance,description, employe_id=None, document_id=None, date_naissance = None):
		try:
			dependant = dao_dependant()
			dependant.nom_complet = unidecode.unidecode(nom_complet)
			dependant.type_dependance = type_dependance
			dependant.description = description
			dependant.employe_id = employe_id
			dependant.document_id = document_id
			dependant.date_naissance = date_naissance
			return dependant
		except Exception as e:
			# print('ERREUR LORS DE LA CREATION DE LA DEPENDANT')
			# print(e)
			return None

	@staticmethod
	def toSaveDependant(auteur,objet_dao_Dependant):
		try:
			dependant  = Model_Dependant()
			dependant.nom_complet = objet_dao_Dependant.nom_complet
			dependant.type_dependance =objet_dao_Dependant.type_dependance
			dependant.description =objet_dao_Dependant.description
			dependant.employe_id =objet_dao_Dependant.employe_id
			dependant.document_id = objet_dao_Dependant.document_id
			dependant.date_naissance = objet_dao_Dependant.date_naissance
			dependant.auteur_id = auteur.id
			dependant.creation_date=timezone.now()
			dependant.save()
			return dependant
		except Exception as e:
			# print('ERREUR LORS DE L ENREGISTREMENT DE LA DEPENDANT')
			# print(e)
			return None

	@staticmethod
	def toUpdateDependant(id, objet_dao_Dependant):
		try:
			dependant = Model_Dependant.objects.get(pk = id)
			dependant.nom_complet = objet_dao_Dependant.nom_complet
			dependant.type_dependance =objet_dao_Dependant.type_dependance
			dependant.description =objet_dao_Dependant.description
			dependant.employe_id =objet_dao_Dependant.employe_id
			dependant.document_id = objet_dao_Dependant.document_id
			dependant.date_naissance = objet_dao_Dependant.date_naissance
			dependant.save()
			return dependant
		except Exception as e:
			# print('ERREUR LORS DE LA MODIFICATION DE LA DEPENDANT')
			# print(e)
			return None
	@staticmethod
	def toGetDependant(id):
		try:
			return Model_Dependant.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toGetDependantByFullName(nom_complet):
		try:
			nom_complet = unidecode.unidecode(nom_complet)
			return Model_Dependant.objects.filter(nom_complet = nom_complet).first()
		except Exception as e:
			return None
	@staticmethod
	def toDeleteDependant(id):
		try:
			dependant = Model_Dependant.objects.get(pk = id)
			dependant.delete()
			return True
		except Exception as e:
			return False