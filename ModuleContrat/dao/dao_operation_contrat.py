from __future__ import unicode_literals
from ErpBackOffice.models import Model_OperationContrat
from django.utils import timezone

class dao_operation_contrat(object):
	id = 0
	designation = ""
	contrat_id = ""
	categorie = ''
	type = 0.0
	valeur = None
	devise_id = ''
	reference_document = ""
	description = None


	@staticmethod
	def toListOperationContrats():
		return Model_OperationContrat.objects.all()

	@staticmethod
	def toCreateOperationContrat(designation, contrat_id, categorie, type, valeur, devise_id, description, reference_document):
		try:
			operation_contrat = dao_operation_contrat()
			operation_contrat.designation = designation
			operation_contrat.contrat_id = contrat_id
			operation_contrat.categorie = categorie
			operation_contrat.type = type
			operation_contrat.valeur = valeur
			operation_contrat.devise_id = devise_id
			operation_contrat.description = description
			operation_contrat.reference_document = reference_document

			return operation_contrat
		except Exception as e:
			print('ERREUR LORS DE LA CREATION DE LA CONTRAT')
			print(e)
			return None

	@staticmethod
	def toSaveOperationContrat(auteur, objet_dao_operation_contrat):
		try:
			operation_contrat  = Model_OperationContrat()
			operation_contrat.designation = objet_dao_operation_contrat.designation
			operation_contrat.contrat_id = objet_dao_operation_contrat.contrat_id
			operation_contrat.categorie = objet_dao_operation_contrat.categorie
			operation_contrat.type = objet_dao_operation_contrat.type
			operation_contrat.valeur = objet_dao_operation_contrat.valeur
			operation_contrat.devise_id = objet_dao_operation_contrat.devise_id
			operation_contrat.description = objet_dao_operation_contrat.description
			operation_contrat.reference_document = objet_dao_operation_contrat.reference_document
			operation_contrat.created_at = timezone.now()
			operation_contrat.updated_at = timezone.now()
			operation_contrat.auteur_id = auteur.id

			operation_contrat.save()
			return operation_contrat
		except Exception as e:
			print('ERREUR LORS DE L ENREGISTREMENT DE LA CONTRAT')
			print(e)
			return None

	@staticmethod
	def toUpdateOperationContrat(id, objet_dao_operation_contrat):
		try:
			operation_contrat = Model_OperationContrat.objects.get(pk = id)
			operation_contrat.designation = objet_dao_operation_contrat.designation
			operation_contrat.contrat_id = objet_dao_operation_contrat.contrat_id
			operation_contrat.categorie =objet_dao_operation_contrat.categorie
			operation_contrat.type =objet_dao_operation_contrat.type
			operation_contrat.valeur =objet_dao_operation_contrat.valeur
			operation_contrat.devise_id =objet_dao_operation_contrat.devise_id
			operation_contrat.description =objet_dao_operation_contrat.description
			operation_contrat.reference_document = objet_dao_operation_contrat.reference_document
			operation_contrat.updated_at = timezone.now()
			operation_contrat.save()
			return operation_contrat
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA CONTRAT')
			#print(e)
			return None
	@staticmethod
	def toGetOperationContrat(id):
		try:
			return Model_OperationContrat.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteOperationContrat(id):
		try:
			contrat = Model_OperationContrat.objects.get(pk = id)
			operation_contrat.delete()
			return True
		except Exception as e:
			return False