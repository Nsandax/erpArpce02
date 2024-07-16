from __future__ import unicode_literals
from ErpBackOffice.models import Model_OperationTresorerie
from django.utils import timezone

class dao_operationtresorerie(object):
	id = 0
	reference = ''
	journal_id = None
	caisse_id = None
	compte_banque_id = None
	type_operation = ''
	balance_initiale = 0.0
	solde = ''
	date_operation = '2010-01-01'
	date_comptable = '2010-01-01'
	devise_id = None
	taux_id = None
	description = ''

	@staticmethod
	def toListOperationtresorerie():
		return Model_OperationTresorerie.objects.all().order_by('-id')

	@staticmethod
	def toListOperationtresorerieNonCloture():
		return Model_OperationTresorerie.objects.exclude(etat = 'closed')

	@staticmethod
	def toListOperationOfBanqueNonCloture(compte_banque_id):
		return Model_OperationTresorerie.objects.filter(compte_banque_id = compte_banque_id).exclude(etat = 'closed')

	@staticmethod
	def toListOperationOfCaisseNonCloture(caisse_id):
		return Model_OperationTresorerie.objects.filter(caisse_id = caisse_id).exclude(etat = 'closed')

	@staticmethod
	def toListOperationtresorerieOfCaisse(caisse_id):
		return Model_OperationTresorerie.objects.filter(caisse_id = caisse_id)

	@staticmethod
	def toListOperationtresorerieOfBanque(compte_banque_id):
		return Model_OperationTresorerie.objects.filter(compte_banque_id = compte_banque_id)

	@staticmethod
	def toCreateOperationtresorerie(reference,journal_id,caisse_id,compte_banque_id,type_operation,balance_initiale,solde,date_operation,date_comptable,devise_id,taux_id,description):
		try:
			operationtresorerie = dao_operationtresorerie()
			operationtresorerie.reference = reference
			operationtresorerie.journal_id = journal_id
			operationtresorerie.caisse_id = caisse_id
			operationtresorerie.compte_banque_id = compte_banque_id
			operationtresorerie.type_operation = type_operation
			operationtresorerie.balance_initiale = balance_initiale
			operationtresorerie.solde = solde
			operationtresorerie.date_operation = date_operation
			operationtresorerie.date_comptable = date_comptable
			operationtresorerie.devise_id = devise_id
			operationtresorerie.taux_id = taux_id
			operationtresorerie.description = description
			return operationtresorerie
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA OPERATIONTRESORERIE')
			#print(e)
			return None

	@staticmethod
	def toSaveOperationtresorerie(auteur, objet_dao_Operationtresorerie):
		try:
			operationtresorerie  = Model_OperationTresorerie()
			operationtresorerie.reference = objet_dao_Operationtresorerie.reference
			operationtresorerie.journal_id = objet_dao_Operationtresorerie.journal_id
			operationtresorerie.caisse_id = objet_dao_Operationtresorerie.caisse_id
			operationtresorerie.compte_banque_id = objet_dao_Operationtresorerie.compte_banque_id
			operationtresorerie.type_operation = objet_dao_Operationtresorerie.type_operation
			operationtresorerie.balance_initiale = objet_dao_Operationtresorerie.balance_initiale
			operationtresorerie.solde = objet_dao_Operationtresorerie.solde
			operationtresorerie.date_operation = objet_dao_Operationtresorerie.date_operation
			operationtresorerie.date_comptable = objet_dao_Operationtresorerie.date_comptable
			operationtresorerie.devise_id = objet_dao_Operationtresorerie.devise_id
			operationtresorerie.taux_id = objet_dao_Operationtresorerie.taux_id
			operationtresorerie.description = objet_dao_Operationtresorerie.description
			operationtresorerie.created_at = timezone.now()
			operationtresorerie.updated_at = timezone.now()
			operationtresorerie.auteur_id = auteur.id

			operationtresorerie.save()
			return operationtresorerie
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA OPERATIONTRESORERIE')
			#print(e)
			return None

	@staticmethod
	def toUpdateOperationtresorerie(id, objet_dao_Operationtresorerie):
		try:
			operationtresorerie = Model_OperationTresorerie.objects.get(pk = id)
			operationtresorerie.reference =objet_dao_Operationtresorerie.reference
			operationtresorerie.journal_id =objet_dao_Operationtresorerie.journal_id
			operationtresorerie.caisse_id =objet_dao_Operationtresorerie.caisse_id
			operationtresorerie.compte_banque_id =objet_dao_Operationtresorerie.compte_banque_id
			operationtresorerie.type_operation =objet_dao_Operationtresorerie.type_operation
			operationtresorerie.balance_initiale =objet_dao_Operationtresorerie.balance_initiale
			operationtresorerie.solde =objet_dao_Operationtresorerie.solde
			operationtresorerie.date_operation =objet_dao_Operationtresorerie.date_operation
			operationtresorerie.date_comptable =objet_dao_Operationtresorerie.date_comptable
			operationtresorerie.devise_id =objet_dao_Operationtresorerie.devise_id
			operationtresorerie.taux_id =objet_dao_Operationtresorerie.taux_id
			operationtresorerie.description =objet_dao_Operationtresorerie.description
			operationtresorerie.updated_at = timezone.now()
			operationtresorerie.save()
			return operationtresorerie
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA OPERATIONTRESORERIE')
			#print(e)
			return None
	@staticmethod
	def toGetOperationtresorerie(id):
		try:
			return Model_OperationTresorerie.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toClosedOperationtresorerie(id):
		try:
			operation = Model_OperationTresorerie.objects.get(pk = id)
			operation.etat = "closed"
			operation.save()
			return True
		except Exception as e:
			#print("erreur",e)
			return False

	@staticmethod
	def toDeleteOperationtresorerie(id):
		try:
			operationtresorerie = Model_OperationTresorerie.objects.get(pk = id)
			operationtresorerie.delete()
			return True
		except Exception as e:
			return False


	@staticmethod
	def toUpdateSoldeOperationtresorerie(id, solde, billeterie_id):
		try:
			operationtresorerie = Model_OperationTresorerie.objects.get(pk = id)
			operationtresorerie.solde =solde
			operationtresorerie.billeterie_id = billeterie_id
			operationtresorerie.updated_at = timezone.now()
			operationtresorerie.save()
			return operationtresorerie
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA OPERATIONTRESORERIE')
			#print(e)
			return None

	@staticmethod
	def toCheckOperationtresorerieOfPoste(poste_id, filter):
		hasGotActiveOne = False
		reference = None
		try:
			if filter == 'caisse':
				operations = Model_OperationTresorerie.objects.filter(caisse_id = poste_id)
			elif filter == 'banque':
				operations = Model_OperationTresorerie.objects.filter(compte_banque_id = poste_id)

			#print("operations", operations)

			for operation in operations:
				if operation.etat == 'created':
					hasGotActiveOne = True
					reference = operation.reference
					break

			return hasGotActiveOne, reference

		except Exception as e:
			return hasGotActiveOne, reference


	@staticmethod
	def toGetLastOperationtresorerie(poste_id, filter):
		try:
			if filter == 'caisse':
				operation = Model_OperationTresorerie.objects.filter(caisse_id = poste_id).last()
			elif filter == 'banque':
				operation = Model_OperationTresorerie.objects.filter(compte_banque_id = poste_id).last()

			return operation
		except Exception as e:
			return None