from __future__ import unicode_literals
from ErpBackOffice.models import Model_CompteBanque
from django.utils import timezone

class dao_compte_banque(object):
	id = 0
	designation = ''
	description = ''
	journal_id = None
	numero_compte = ""
	type_compte = ""
	banque_id = None
	compte_comptable_id = None

	@staticmethod
	def toListCompteBanque():
		return Model_CompteBanque.objects.all().order_by('-id')

	@staticmethod
	def toCreateCompteBanque(designation,description, numero_compte, type_compte, banque_id = None,journal_id = None, compte_comptable_id = None):
		try:
			banque = dao_compte_banque()
			banque.designation = designation
			banque.description = description
			banque.numero_compte = numero_compte
			banque.type_compte = type_compte
			banque.banque_id = banque_id
			banque.journal_id = journal_id
			banque.compte_comptable_id = compte_comptable_id
			return banque
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA BANQUE')
			#print(e)
			return None

	@staticmethod
	def toSaveCompteBanque(auteur, objet_dao_Banque):
		try:
			banque  = Model_CompteBanque()
			banque.designation = objet_dao_Banque.designation
			banque.description = objet_dao_Banque.description
			banque.journal_id = objet_dao_Banque.journal_id
			banque.numero_compte = objet_dao_Banque.numero_compte
			banque.type_compte = objet_dao_Banque.type_compte
			banque.banque_id = objet_dao_Banque.banque_id
			banque.compte_comptable_id = objet_dao_Banque.compte_comptable_id
			banque.created_at = timezone.now()
			banque.updated_at = timezone.now()
			banque.auteur_id = auteur.id

			banque.save()
			return banque
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA BANQUE')
			#print(e)
			return None

	@staticmethod
	def toUpdateCompteBanque(id, objet_dao_Banque):
		try:
			banque = Model_CompteBanque.objects.get(pk = id)
			banque.designation =objet_dao_Banque.designation
			banque.description =objet_dao_Banque.description
			banque.journal_id = objet_dao_Banque.journal_id
			banque.numero_compte = objet_dao_Banque.numero_compte
			banque.type_compte = objet_dao_Banque.type_compte
			banque.compte_comptable_id = objet_dao_Banque.compte_comptable_id
			banque.banque_id = objet_dao_Banque.banque_id
			banque.updated_at = timezone.now()
			banque.save()
			return banque
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA BANQUE')
			#print(e)
			return None
	@staticmethod
	def toGetCompteBanque(id):
		try:
			return Model_CompteBanque.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteCompteBanque(id):
		try:
			banque = Model_CompteBanque.objects.get(pk = id)
			banque.delete()
			return True
		except Exception as e:
			return False