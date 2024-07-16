from __future__ import unicode_literals
from ErpBackOffice.models import Model_LigneTraitementImmobilisation
from django.utils import timezone

class dao_ligne_traitementimmobilisation(object):
	id = 0
	immobilisation_id = None
	description = ''
	prix_vente = 0.0
	est_traite = False
	traitement_immobilisation_id = None

	@staticmethod
	def toListLigne_traitementimmobilisation():
		return Model_LigneTraitementImmobilisation.objects.all().order_by('-id')


	@staticmethod
	def toListLigneOfTraitement(traitement_immobilisation_id):
		return Model_LigneTraitementImmobilisation.objects.filter(traitement_immobilisation_id = traitement_immobilisation_id)

	@staticmethod
	def toListLigneOfTraitementNonTraite(traitement_immobilisation_id):
		return Model_LigneTraitementImmobilisation.objects.filter(traitement_immobilisation_id = traitement_immobilisation_id).filter(est_traite = False)

	@staticmethod
	def toCreateLigne_traitementimmobilisation(immobilisation_id,description,traitement_immobilisation_id, prix_vente = 0,est_traite = False):
		try:
			ligne_traitementimmobilisation = dao_ligne_traitementimmobilisation()
			ligne_traitementimmobilisation.immobilisation_id = immobilisation_id
			ligne_traitementimmobilisation.description = description
			ligne_traitementimmobilisation.prix_vente = prix_vente
			ligne_traitementimmobilisation.est_traite = est_traite
			ligne_traitementimmobilisation.traitement_immobilisation_id = traitement_immobilisation_id
			return ligne_traitementimmobilisation
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA LIGNE_TRAITEMENTIMMOBILISATION')
			#print(e)
			return None

	@staticmethod
	def toSaveLigne_traitementimmobilisation(auteur, objet_dao_Ligne_traitementimmobilisation):
		try:
			ligne_traitementimmobilisation  = Model_LigneTraitementImmobilisation()
			ligne_traitementimmobilisation.immobilisation_id = objet_dao_Ligne_traitementimmobilisation.immobilisation_id
			ligne_traitementimmobilisation.description = objet_dao_Ligne_traitementimmobilisation.description
			ligne_traitementimmobilisation.prix_vente = objet_dao_Ligne_traitementimmobilisation.prix_vente
			ligne_traitementimmobilisation.est_traite = objet_dao_Ligne_traitementimmobilisation.est_traite
			ligne_traitementimmobilisation.traitement_immobilisation_id = objet_dao_Ligne_traitementimmobilisation.traitement_immobilisation_id
			ligne_traitementimmobilisation.created_at = timezone.now()
			ligne_traitementimmobilisation.updated_at = timezone.now()
			ligne_traitementimmobilisation.auteur_id = auteur.id

			ligne_traitementimmobilisation.save()
			return ligne_traitementimmobilisation
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA LIGNE_TRAITEMENTIMMOBILISATION')
			#print(e)
			return None

	@staticmethod
	def toUpdateLigne_traitementimmobilisation(id, objet_dao_Ligne_traitementimmobilisation):
		try:
			ligne_traitementimmobilisation = Model_LigneTraitementImmobilisation.objects.get(pk = id)
			ligne_traitementimmobilisation.immobilisation_id =objet_dao_Ligne_traitementimmobilisation.immobilisation_id
			ligne_traitementimmobilisation.description =objet_dao_Ligne_traitementimmobilisation.description
			ligne_traitementimmobilisation.prix_vente =objet_dao_Ligne_traitementimmobilisation.prix_vente
			ligne_traitementimmobilisation.est_traite =objet_dao_Ligne_traitementimmobilisation.est_traite
			ligne_traitementimmobilisation.updated_at = timezone.now()
			ligne_traitementimmobilisation.traitement_immobilisation_id = objet_dao_Ligne_traitementimmobilisation.traitement_immobilisation_id
			ligne_traitementimmobilisation.save()
			return ligne_traitementimmobilisation
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA LIGNE_TRAITEMENTIMMOBILISATION')
			#print(e)
			return None
	@staticmethod
	def toGetLigne_traitementimmobilisation(id):
		try:
			return Model_LigneTraitementImmobilisation.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toDeleteLigne_traitementimmobilisation(id):
		try:
			ligne_traitementimmobilisation = Model_LigneTraitementImmobilisation.objects.get(pk = id)
			ligne_traitementimmobilisation.delete()
			return True
		except Exception as e:
			return False


	@staticmethod
	def toSetLigneTraitement(id):
		try:
			ligne_traitementimmobilisation = Model_LigneTraitementImmobilisation.objects.get(pk = id)
			ligne_traitementimmobilisation.est_traite = True
			ligne_traitementimmobilisation.save()
			return True
		except Exception as e:
			return False