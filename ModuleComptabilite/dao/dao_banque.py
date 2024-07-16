from __future__ import unicode_literals
from ErpBackOffice.models import Model_Banque, Model_CompteBanque, Model_OperationTresorerie
from django.utils import timezone

class dao_banque(object):
	id = 0
	designation = ''
	code = ''
	adresse = ''
	observation = ''

	@staticmethod
	def toListBank():
		return Model_Banque.objects.all().order_by('-id')

	@staticmethod
	def toCreateBank(designation,adresse = "",observation = "", code = ""):
		try:
			bank = dao_banque()
			bank.designation = designation
			bank.adresse = adresse
			bank.code = code
			bank.observation = observation
			return bank
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA BANK')
			#print(e)
			return None

	@staticmethod
	def toSaveBank(auteur, objet_dao_Bank):
		try:
			bank  = Model_Banque()
			bank.designation = objet_dao_Bank.designation
			bank.adresse = objet_dao_Bank.adresse
			bank.observation = objet_dao_Bank.observation
			bank.code = objet_dao_Bank.code
			bank.created_at = timezone.now()
			bank.updated_at = timezone.now()
			bank.auteur_id = auteur.id

			bank.save()
			return bank
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA BANK')
			#print(e)
			return None
	

	@staticmethod
	def toUpdateBank(id, objet_dao_Bank):
		try:
			bank = Model_Banque.objects.get(pk = id)
			bank.designation =objet_dao_Bank.designation
			bank.adresse =objet_dao_Bank.adresse
			bank.code = objet_dao_Bank.code
			bank.observation =objet_dao_Bank.observation
			bank.updated_at = timezone.now()
			bank.save()
			return bank
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA BANK')
			#print(e)
			return None
	@staticmethod
	def toGetBank(id):
		try:
			return Model_Banque.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toDeleteBank(id):
		try:
			bank = Model_Banque.objects.get(pk = id)
			bank.delete()
			return True
		except Exception as e:
			return False
	
	@staticmethod
	def toListBankSoldeOfPeriode(date_debut, date_fin):
		banks = []
		try:
			banques = Model_Banque.objects.all()
			for banque in banques:
				bank = {
					'designation':banque.designation,
					'solde':0
				}

				comptes = Model_CompteBanque.objects.filter(banque = banque)
				for compte in comptes:
					operations = Model_OperationTresorerie.objects.filter(compte_banque = compte).filter(date_operation__range=(date_debut,date_fin))
					for operation in operations:
						bank['solde'] += float(operation.solde)

				banks.append(bank)
			return banks
		except Exception as e:
			#print(e)
			return banks
	@staticmethod
	def toGetAdressBanque(designation_):
		try:
			return Model_Banque.objects.get(designation=designation_)
		except Exception as e:
			#print("toGetAdressBanque %s"%(e))
			pass
