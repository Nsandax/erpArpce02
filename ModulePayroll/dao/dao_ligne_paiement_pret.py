from __future__ import unicode_literals
from ErpBackOffice.models import Model_LignePaiementPret
from django.utils import timezone


class dao_ligne_paiement_pret(object):
	id = 0
	designation = None
	pret_id = None
	montant = None
	devise_id = None
	est_success = None
	description = None
	rubrique_id = None
	dossier_paie_id = None

	@staticmethod
	def toListLignePaiementPret():
		return Model_LignePaiementPret.objects.all().order_by('-id')
	
	@staticmethod
	def toListLignePaiementOfPret(pret_id):
		return Model_LignePaiementPret.objects.filter(pret_id = pret_id).order_by('-id')

	@staticmethod
	def toCreateLignePaiementPret(designation, montant, devise_id, pret_id, est_success, description, dossier_paie_id = None):
		try:
			ligne_paiement_pret = dao_ligne_paiement_pret()
			ligne_paiement_pret.designation = designation
			ligne_paiement_pret.montant = montant
			ligne_paiement_pret.devise_id = devise_id
			ligne_paiement_pret.pret_id = pret_id
			ligne_paiement_pret.est_success = est_success
			ligne_paiement_pret.description = description
			ligne_paiement_pret.dossier_paie_id = dossier_paie_id
			return ligne_paiement_pret
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA PRET')
			#print(e)
			return None

	@staticmethod
	def toSaveLignePaiementPret(auteur,objet_dao_ligne_paiement_pret):
		try:
			ligne_paiement_pret = Model_LignePaiementPret()
			ligne_paiement_pret.designation = objet_dao_ligne_paiement_pret.designation
			ligne_paiement_pret.montant = objet_dao_ligne_paiement_pret.montant
			ligne_paiement_pret.devise_id = objet_dao_ligne_paiement_pret.devise_id
			ligne_paiement_pret.pret_id = objet_dao_ligne_paiement_pret.pret_id
			ligne_paiement_pret.est_success = objet_dao_ligne_paiement_pret.est_success
			ligne_paiement_pret.description = objet_dao_ligne_paiement_pret.description
			ligne_paiement_pret.dossier_paie_id = objet_dao_ligne_paiement_pret.dossier_paie_id
			ligne_paiement_pret.created_at = timezone.now()
			#ligne_paiement_pret.auteur_id = auteur.id
			ligne_paiement_pret.save()
			return ligne_paiement_pret
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA PRET')
			#print(e)
			return None

	@staticmethod
	def toUpdateLignePaiementPret(id, objet_dao_ligne_paiement_pret):
		try:
			ligne_paiement_pret = Model_LignePaiementPret.objects.get(pk = id)
			ligne_paiement_pret.designation = objet_dao_ligne_paiement_pret.designation
			ligne_paiement_pret.montant = objet_dao_ligne_paiement_pret.montant
			ligne_paiement_pret.devise_id = objet_dao_ligne_paiement_pret.devise_id
			ligne_paiement_pret.pret_id = objet_dao_ligne_paiement_pret.pret_id
			ligne_paiement_pret.est_success = objet_dao_ligne_paiement_pret.est_success
			ligne_paiement_pret.description = objet_dao_ligne_paiement_pret.description
			ligne_paiement_pret.dossier_paie_id = objet_dao_ligne_paiement_pret.dossier_paie_id
			ligne_paiement_pret.updated_at = timezone.now()
			ligne_paiement_pret.save()
			return ligne_paiement_pret
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA PRET')
			#print(e)
			return None
	@staticmethod
	def toGetLignePaiementPret(id):
		try:
			return Model_LignePaiementPret.objects.get(pk = id)
		except Exception as e:
			return None
	
	@staticmethod
	def toListLignePaiementByPretAndDossierPaie(pret_id, dossier_paie_id):
		try:
			return Model_LignePaiementPret.objects.filter(pret_id = pret_id).filter(dossier_paie_id = dossier_paie_id)
		except Exception as e:
			return None

	@staticmethod
	def toDeleteLignePaiementPret(id):
		try:
			ligne_paiement_pret = Model_LignePaiementPret.objects.get(pk = id)
			ligne_paiement_pret.delete()
			return True
		except Exception as e:
			return False