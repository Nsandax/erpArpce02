from __future__ import unicode_literals
from ErpBackOffice.models import Model_Ecriture_analytique, Model_LigneBudgetaire, Model_Poste_budgetaire, Model_LignePosteBudgetaire
from django.utils import timezone

class dao_ecriture_analytique(object):
	id = 0
	libelle = ''
	compte_id = None
	centre_cout_id = None
	facture_id = None
	montant = 0
	devise_id = None
	ligne_budgetaire_id = None
	type = 1
	ecriture_comptable_id = None

	@staticmethod
	def toListEcriture_analytique():
		return Model_Ecriture_analytique.objects.all().order_by('-id')

	@staticmethod
	def toListEcritureAnalytiqueOfCentreCout(centre_cout_id, date_debut, date_fin):
		return Model_Ecriture_analytique.objects.filter(centre_cout_id = centre_cout_id).filter(created_at__gte = date_debut, created_at__lte = date_fin)

	@staticmethod
	def toListEcritureAnalytiqueOfLigneBudgetaire(ligne_budgetaire_id, date_debut, date_fin):
		return Model_Ecriture_analytique.objects.filter(ligne_budgetaire_id = ligne_budgetaire_id).filter(created_at__gte = date_debut, created_at__lte = date_fin)

	@staticmethod
	def toCreateEcriture_analytique(libelle,compte_id,centre_cout_id,facture_id, montant, devise_id = None, type = 2, ecriture_comptable_id = None):
		try:
			ecriture_analytique = dao_ecriture_analytique()
			ecriture_analytique.libelle = libelle
			ecriture_analytique.compte_id = compte_id
			ecriture_analytique.centre_cout_id = centre_cout_id
			ecriture_analytique.facture_id = facture_id
			ecriture_analytique.montant = montant
			ecriture_analytique.devise_id = devise_id
			ecriture_analytique.type = type
			ecriture_analytique.ecriture_comptable_id = ecriture_comptable_id
			#Retrieve ligne budgetaire concerné

			ecriture_analytique.ligne_budgetaire_id = dao_ecriture_analytique.toRetrieveLigneOfEcritureAnalytique(centre_cout_id,compte_id)

			return ecriture_analytique
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA ECRITURE_ANALYTIQUE')
			#print(e)
			return None

	@staticmethod
	def toSaveEcriture_analytique(auteur, objet_dao_Ecriture_analytique):
		try:
			ecriture_analytique  = Model_Ecriture_analytique()
			ecriture_analytique.libelle = objet_dao_Ecriture_analytique.libelle
			ecriture_analytique.compte_id = objet_dao_Ecriture_analytique.compte_id
			ecriture_analytique.centre_cout_id = objet_dao_Ecriture_analytique.centre_cout_id
			ecriture_analytique.facture_id = objet_dao_Ecriture_analytique.facture_id
			ecriture_analytique.montant = objet_dao_Ecriture_analytique.montant
			ecriture_analytique.devise_id = objet_dao_Ecriture_analytique.devise_id
			ecriture_analytique.type = objet_dao_Ecriture_analytique.type
			ecriture_analytique.ecriture_comptable_id = objet_dao_Ecriture_analytique.ecriture_comptable_id
			ecriture_analytique.created_at = timezone.now()
			ecriture_analytique.updated_at = timezone.now()
			ecriture_analytique.auteur_id = auteur.id

			ecriture_analytique.ligne_budgetaire_id = objet_dao_Ecriture_analytique.ligne_budgetaire_id

			ecriture_analytique.save()
			#print("lols")
			return ecriture_analytique
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA ECRITURE_ANALYTIQUE')
			#print(e)
			return None

	@staticmethod
	def toUpdateEcriture_analytique(id, objet_dao_Ecriture_analytique):
		try:
			ecriture_analytique = Model_Ecriture_analytique.objects.get(pk = id)
			ecriture_analytique.libelle =objet_dao_Ecriture_analytique.libelle
			ecriture_analytique.compte_id =objet_dao_Ecriture_analytique.compte_id
			ecriture_analytique.centre_cout_id =objet_dao_Ecriture_analytique.centre_cout_id
			ecriture_analytique.facture_id =objet_dao_Ecriture_analytique.facture_id
			ecriture_analytique.montant = objet_dao_Ecriture_analytique.montant
			ecriture_analytique.devise_id = objet_dao_Ecriture_analytique.devise_id
			ecriture_analytique.ecriture_comptable_id = objet_dao_Ecriture_analytique.ecriture_comptable_id
			ecriture_analytique.type = objet_dao_Ecriture_analytique.type
			ecriture_analytique.updated_at = timezone.now()
			ecriture_analytique.save()
			return ecriture_analytique
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA ECRITURE_ANALYTIQUE')
			#print(e)
			return None
	@staticmethod
	def toGetEcriture_analytique(id):
		try:
			return Model_Ecriture_analytique.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteEcriture_analytique(id):
		try:
			ecriture_analytique = Model_Ecriture_analytique.objects.get(pk = id)
			ecriture_analytique.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toRetrieveLigneOfEcritureAnalytique(centre_cout_id, compte_id):
		try:
			ligne_poste = Model_LignePosteBudgetaire.objects.filter(compte_id = compte_id).first()
			return Model_LigneBudgetaire.objects.filter(centre_cout_id = centre_cout_id).filter(poste_budgetaire = ligne_poste.poste_budgetaire_id).first().id
		except Exception as e:
			return None
