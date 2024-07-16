from __future__ import unicode_literals
from ErpBackOffice.models import Model_Ordre_paiement
from django.utils import timezone

class dao_ordre_paiement(object):
	id = 0
	reference = ''
	type_paiement = 0
	date_echeance = '2010-01-01'
	compte_banque_id = None
	caisse_id = None
	description = ''

	@staticmethod
	def toListOrdre_paiement():
		return Model_Ordre_paiement.objects.all().order_by('-id')

	@staticmethod
	def toCreateOrdre_paiement(reference,type_paiement,date_echeance,compte_banque_id,caisse_id,description):
		try:
			ordre_paiement = dao_ordre_paiement()
			ordre_paiement.reference = reference
			ordre_paiement.type_paiement = type_paiement
			ordre_paiement.date_echeance = date_echeance
			ordre_paiement.compte_banque_id = compte_banque_id
			ordre_paiement.caisse_id = caisse_id
			ordre_paiement.description = description
			return ordre_paiement
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA ORDRE_PAIEMENT')
			#print(e)
			return None

	@staticmethod
	def toSaveOrdre_paiement(auteur, objet_dao_Ordre_paiement):
		try:
			ordre_paiement  = Model_Ordre_paiement()
			ordre_paiement.reference = objet_dao_Ordre_paiement.reference
			ordre_paiement.type_paiement = objet_dao_Ordre_paiement.type_paiement
			ordre_paiement.date_echeance = objet_dao_Ordre_paiement.date_echeance
			ordre_paiement.compte_banque_id = objet_dao_Ordre_paiement.compte_banque_id
			ordre_paiement.caisse_id = objet_dao_Ordre_paiement.caisse_id
			ordre_paiement.description = objet_dao_Ordre_paiement.description
			ordre_paiement.created_at = timezone.now()
			ordre_paiement.updated_at = timezone.now()
			ordre_paiement.auteur_id = auteur.id

			ordre_paiement.save()
			return ordre_paiement
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA ORDRE_PAIEMENT')
			#print(e)
			return None

	@staticmethod
	def toUpdateOrdre_paiement(id, objet_dao_Ordre_paiement):
		try:
			ordre_paiement = Model_Ordre_paiement.objects.get(pk = id)
			ordre_paiement.reference =objet_dao_Ordre_paiement.reference
			ordre_paiement.type_paiement =objet_dao_Ordre_paiement.type_paiement
			ordre_paiement.date_echeance =objet_dao_Ordre_paiement.date_echeance
			ordre_paiement.compte_banque_id =objet_dao_Ordre_paiement.compte_banque_id
			ordre_paiement.caisse_id =objet_dao_Ordre_paiement.caisse_id
			ordre_paiement.description =objet_dao_Ordre_paiement.description
			ordre_paiement.updated_at = timezone.now()
			ordre_paiement.save()
			return ordre_paiement
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA ORDRE_PAIEMENT')
			#print(e)
			return None
	@staticmethod
	def toGetOrdre_paiement(id):
		try:
			return Model_Ordre_paiement.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteOrdre_paiement(id):
		try:
			ordre_paiement = Model_Ordre_paiement.objects.get(pk = id)
			ordre_paiement.delete()
			return True
		except Exception as e:
			return False