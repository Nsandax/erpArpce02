from __future__ import unicode_literals
from ErpBackOffice.models import Model_Caisse, Model_OperationTresorerie
from django.utils import timezone

class dao_caisse(object):
	id = 0
	designation = ''
	description = ''
	responsable_id = None
	journal_id = None
	compte_comptable_id = None

	@staticmethod
	def toListCaisse():
		return Model_Caisse.objects.all().order_by('-id')

	@staticmethod
	def toCreateCaisse(designation,description,responsable_id, journal_id = None, compte_comptable_id = None):
		try:
			caisse = dao_caisse()
			caisse.designation = designation
			caisse.description = description
			caisse.responsable_id = responsable_id
			caisse.journal_id = journal_id
			caisse.compte_comptable_id = compte_comptable_id
			return caisse
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA CAISSE')
			#print(e)
			return None

	@staticmethod
	def toSaveCaisse(auteur, objet_dao_Caisse):
		try:
			caisse  = Model_Caisse()
			caisse.designation = objet_dao_Caisse.designation
			caisse.description = objet_dao_Caisse.description
			caisse.responsable_id = objet_dao_Caisse.responsable_id
			caisse.journal_id = objet_dao_Caisse.journal_id
			caisse.compte_comptable_id =  objet_dao_Caisse.compte_comptable_id
			caisse.created_at = timezone.now()
			caisse.updated_at = timezone.now()
			caisse.auteur_id = auteur.id

			caisse.save()
			return caisse
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA CAISSE')
			#print(e)
			return None

	@staticmethod
	def toUpdateCaisse(id, objet_dao_Caisse):
		try:
			caisse = Model_Caisse.objects.get(pk = id)
			caisse.designation =objet_dao_Caisse.designation
			caisse.description =objet_dao_Caisse.description
			caisse.responsable_id =objet_dao_Caisse.responsable_id
			caisse.compte_comptable_id = objet_dao_Caisse.compte_comptable_id
			caisse.journal_id = objet_dao_Caisse.journal_id
			caisse.updated_at = timezone.now()
			caisse.save()
			return caisse
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA CAISSE')
			#print(e)
			return None
	@staticmethod
	def toGetCaisse(id):
		try:
			return Model_Caisse.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteCaisse(id):
		try:
			caisse = Model_Caisse.objects.get(pk = id)
			caisse.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toListCaisseSoldeOfPeriode(date_debut, date_fin):
		cais = []
		try:
			caisses = Model_Caisse.objects.all()
			for caisse in caisses:
				unecaisse = {
					'designation':caisse.designation,
					'solde':0
				}

				operations = Model_OperationTresorerie.objects.filter(caisse = caisse).filter(date_operation__range=(date_debut,date_fin))
				for operation in operations:
					unecaisse['solde'] += float(operation.solde)

				cais.append(unecaisse)
			return cais
		except Exception as e:
			#print(e)
			return cais