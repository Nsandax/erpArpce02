

from __future__ import unicode_literals
from ErpBackOffice.models import Model_Ligne_ordre_paiement
from django.utils import timezone

class dao_ligne_ordre_paiement(object):
	id = 0
	libelle = ''
	partenaire_id = ''
	facture_id = None
	montant = 0.0
	devise_id = None
	observation = ''
	ordre_paiement_id = None

	@staticmethod
	def toListLigne_ordre_paiement():
		return Model_Ligne_ordre_paiement.objects.all().order_by('-id')

	@staticmethod
	def toListLigneOfOrdrePaiement(ordre_paiement_id):
		return Model_Ligne_ordre_paiement.objects.filter( ordre_paiement_id = ordre_paiement_id)

	@staticmethod
	def toCreateLigne_ordre_paiement(libelle,partenaire_id,facture_id,montant,devise_id,observation, ordre_paiement_id = None):
		try:
			ligne_ordre_paiement = dao_ligne_ordre_paiement()
			ligne_ordre_paiement.libelle = libelle
			ligne_ordre_paiement.partenaire_id = partenaire_id
			ligne_ordre_paiement.facture_id = facture_id
			ligne_ordre_paiement.montant = montant
			ligne_ordre_paiement.devise_id = devise_id
			ligne_ordre_paiement.observation = observation
			ligne_ordre_paiement.ordre_paiement_id = ordre_paiement_id
			return ligne_ordre_paiement
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA LIGNE_ORDRE_PAIEMENT')
			#print(e)
			return None

	@staticmethod
	def toSaveLigne_ordre_paiement(auteur, objet_dao_Ligne_ordre_paiement):
		try:
			ligne_ordre_paiement  = Model_Ligne_ordre_paiement()
			ligne_ordre_paiement.libelle = objet_dao_Ligne_ordre_paiement.libelle
			ligne_ordre_paiement.partenaire_id = objet_dao_Ligne_ordre_paiement.partenaire_id
			ligne_ordre_paiement.facture_id = objet_dao_Ligne_ordre_paiement.facture_id
			ligne_ordre_paiement.montant = objet_dao_Ligne_ordre_paiement.montant
			ligne_ordre_paiement.devise_id = objet_dao_Ligne_ordre_paiement.devise_id
			ligne_ordre_paiement.observation = objet_dao_Ligne_ordre_paiement.observation
			ligne_ordre_paiement.ordre_paiement_id = objet_dao_Ligne_ordre_paiement.ordre_paiement_id
			ligne_ordre_paiement.created_at = timezone.now()
			ligne_ordre_paiement.updated_at = timezone.now()
			ligne_ordre_paiement.auteur_id = auteur.id

			ligne_ordre_paiement.save()
			return ligne_ordre_paiement
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA LIGNE_ORDRE_PAIEMENT')
			#print(e)
			return None

	@staticmethod
	def toUpdateLigne_ordre_paiement(id, objet_dao_Ligne_ordre_paiement):
		try:
			ligne_ordre_paiement = Model_Ligne_ordre_paiement.objects.get(pk = id)
			ligne_ordre_paiement.libelle =objet_dao_Ligne_ordre_paiement.libelle
			ligne_ordre_paiement.partenaire_id =objet_dao_Ligne_ordre_paiement.partenaire_id
			ligne_ordre_paiement.facture_id =objet_dao_Ligne_ordre_paiement.facture_id
			ligne_ordre_paiement.montant =objet_dao_Ligne_ordre_paiement.montant
			ligne_ordre_paiement.devise_id =objet_dao_Ligne_ordre_paiement.devise_id
			ligne_ordre_paiement.ordre_paiement_id = objet_dao_Ligne_ordre_paiement.ordre_paiement_id
			ligne_ordre_paiement.observation =objet_dao_Ligne_ordre_paiement.observation
			ligne_ordre_paiement.updated_at = timezone.now()
			ligne_ordre_paiement.save()
			return ligne_ordre_paiement
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA LIGNE_ORDRE_PAIEMENT')
			#print(e)
			return None
	@staticmethod
	def toGetLigne_ordre_paiement(id):
		try:
			return Model_Ligne_ordre_paiement.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteLigne_ordre_paiement(id):
		try:
			ligne_ordre_paiement = Model_Ligne_ordre_paiement.objects.get(pk = id)
			ligne_ordre_paiement.delete()
			return True
		except Exception as e:
			return False



















