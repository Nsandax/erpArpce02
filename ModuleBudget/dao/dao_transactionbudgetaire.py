from __future__ import unicode_literals
from ErpBackOffice.models import Model_Transactionbudgetaire, Model_LigneBudgetaire
from django.utils import timezone
from ErpBackOffice.utils.separateur import makeFloat
from ModuleBudget.dao.dao_exercicebudgetaire import dao_exercicebudgetaire
from ModuleBudget.dao.dao_ligne_budgetaire import dao_ligne_budgetaire
from ModuleAchat.dao.dao_ligne_reception import dao_ligne_reception
from ErpBackOffice.dao.dao_devise import dao_devise
from ModuleComptabilite.dao.dao_ligne_facture import dao_ligne_facture

class dao_transactionbudgetaire(object):
	id = 0
	designation = ''
	montant = 0.0
	description = 0
	devise_id = None
	compte_comptable_id = None
	employe_id = None
	type_id = None
	ligne_id = None
	typetransactionbudgetaire = None
	status = 0
	bon_reception_id = None
	facture_id = None

	@staticmethod
	def toListTransactionbudgetaire():
		return Model_Transactionbudgetaire.objects.all().order_by('-id')

	@staticmethod
	def toListTransactionbudgetaireOfAnneeActive():
		return Model_Transactionbudgetaire.objects.filter( exercice_budgetaire = dao_exercicebudgetaire.toGetActiveExercicebudgetaire()).order_by("-id")

	@staticmethod
	def toListTransactionBudgetaireOfFacture(facture_id):
		return Model_Transactionbudgetaire.objects.filter(facture_id = facture_id)

	@staticmethod
	def toListOfCombinaison(ligne_id):
		return Model_Transactionbudgetaire.objects.filter(ligne_budgetaire = ligne_id)
	@staticmethod
	def toListOfCombinaisonOfAnneeActive(ligne_id):
		return Model_Transactionbudgetaire.objects.filter(ligne_budgetaire = ligne_id, exercice_budgetaire = dao_exercicebudgetaire.toGetActiveExercicebudgetaire()).order_by("-id")

	@staticmethod
	def toCreateTransactionbudgetaire(designation,montant,description,devise_id,compte_comptable_id, employe_id, ligne_id, type_id, status =0, bon_reception_id = None, facture_id = None):
		try:
			transactionbudgetaire = dao_transactionbudgetaire()
			transactionbudgetaire.designation = designation
			transactionbudgetaire.montant = montant
			transactionbudgetaire.description = description
			transactionbudgetaire.devise_id = devise_id
			transactionbudgetaire.compte_comptable_id = compte_comptable_id
			transactionbudgetaire.employe_id = employe_id
			transactionbudgetaire.ligne_id = ligne_id
			transactionbudgetaire.type_id = type_id
			transactionbudgetaire.status = status
			transactionbudgetaire.bon_reception_id = bon_reception_id
			transactionbudgetaire.facture_id = facture_id
			return transactionbudgetaire
		except Exception as e:
			print('ERREUR LORS DE LA CREATION DE LA TRANSACTIONBUDGETAIRE')
			print(e)
			return None

	@staticmethod
	def toSaveTransactionbudgetaire(auteur, objet_dao_Transactionbudgetaire):
		try:
			transactionbudgetaire  = Model_Transactionbudgetaire()
			transactionbudgetaire.designation = objet_dao_Transactionbudgetaire.designation
			transactionbudgetaire.montant = objet_dao_Transactionbudgetaire.montant
			transactionbudgetaire.description = objet_dao_Transactionbudgetaire.description
			transactionbudgetaire.devise_id = objet_dao_Transactionbudgetaire.devise_id
			transactionbudgetaire.compte_comptable_id = objet_dao_Transactionbudgetaire.compte_comptable_id
			transactionbudgetaire.employe_id = objet_dao_Transactionbudgetaire.employe_id
			transactionbudgetaire.ligne_budgetaire_id = objet_dao_Transactionbudgetaire.ligne_id
			transactionbudgetaire.typetransactionbudgetaire = objet_dao_Transactionbudgetaire.type_id
			transactionbudgetaire.auteur_id = auteur.id
			transactionbudgetaire.status = objet_dao_Transactionbudgetaire.status
			#retrieving annee exercice budgetaire
			exercice_budgetaire = dao_exercicebudgetaire.toGetActiveExercicebudgetaire()
			transactionbudgetaire.exercice_budgetaire = exercice_budgetaire
			transactionbudgetaire.bon_reception_id = objet_dao_Transactionbudgetaire.bon_reception_id
			transactionbudgetaire.facture_id = objet_dao_Transactionbudgetaire.facture_id
			transactionbudgetaire.save()
	


			return transactionbudgetaire
		except Exception as e:
			print('ERREUR LORS DE L ENREGISTREMENT DE LA TRANSACTIONBUDGETAIRE')
			print(e)
			return None

	@staticmethod
	def toUpdateTransactionbudgetaire(id, objet_dao_Transactionbudgetaire):
		try:
			transactionbudgetaire = Model_Transactionbudgetaire.objects.get(pk = id)
			transactionbudgetaire.designation =objet_dao_Transactionbudgetaire.designation
			transactionbudgetaire.montant =objet_dao_Transactionbudgetaire.montant
			transactionbudgetaire.description =objet_dao_Transactionbudgetaire.description
			transactionbudgetaire.devise_id =objet_dao_Transactionbudgetaire.devise_id
			transactionbudgetaire.compte_comptable_id =objet_dao_Transactionbudgetaire.compte_comptable_id
			transactionbudgetaire.ligne_budgetaire_id = objet_dao_Transactionbudgetaire.ligne_id
			transactionbudgetaire.typetransactionbudgetaire = objet_dao_Transactionbudgetaire.type_id
			transactionbudgetaire.status = objet_dao_Transactionbudgetaire.status
			transactionbudgetaire.bon_reception_id = objet_dao_Transactionbudgetaire.bon_reception_id
			transactionbudgetaire.facture_id = objet_dao_Transactionbudgetaire.facture_id
			transactionbudgetaire.save()
			return transactionbudgetaire
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA TRANSACTIONBUDGETAIRE')
			#print(e)
			return None
	@staticmethod
	def toGetTransactionbudgetaire(id):
		try:
			return Model_Transactionbudgetaire.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toDeleteTransactionbudgetaire(id):
		try:
			transactionbudgetaire = Model_Transactionbudgetaire.objects.get(pk = id)
			transactionbudgetaire.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toGetTransactionbudgetaireOfBonCommande(id):
		try:
			return Model_Transactionbudgetaire.objects.get(bon_commande_id = id)
		except Exception as e:
			return None
	
	@staticmethod
	def toListTransactionSansBC():
		try:
			return Model_Transactionbudgetaire.objects.filter(bon_reception = None, typetransactionbudgetaire = 1 )
		except Exception as e:
			return None

	@staticmethod
	def toListTransactionbudgetaireOfBonCommande(id):
		try:
			return Model_Transactionbudgetaire.objects.filter(bon_commande_id = id)
		except Exception as e:
			return None

	@staticmethod
	def toUpdateStatusOnReelOfTransactionbudgetaire(id):
		try:
			transactionbudgetaire = Model_Transactionbudgetaire.objects.get(pk = id)
			transactionbudgetaire.status = 2
			transactionbudgetaire.save()
			return transactionbudgetaire
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA TRANSACTIONBUDGETAIRE')
			#print(e)
			return None


	@staticmethod
	def toCancelEngagement(auteur,bon_reception):
		try:
			transactions = Model_Transactionbudgetaire.objects.filter(bon_reception_id = bon_reception.id)
			#print("we are here")
			for transaction in transactions:
				montant_neg = float(transaction.montant) * (-1)
				transactionBudgetaire = dao_transactionbudgetaire.toCreateTransactionbudgetaire("Annulation Engagement Paiement bon de commande "+bon_reception.numero_reception,montant_neg,"Ecritures d'annulation des engagements ",transaction.devise_id,transaction.compte_comptable_id,auteur.id,transaction.ligne_id,1)
				transactionBudgetaire = dao_transactionbudgetaire.toSaveTransactionbudgetaire(auteur,transactionBudgetaire)
				transactionBudgetaire.bon_reception = bon_reception
				transactionBudgetaire.save()
			return True
		except Exception as e:
			return False


	@staticmethod
	def toCancelEngagementTransaction(bon_reception_id):
		try:
			transactionbudgetaire = Model_Transactionbudgetaire.objects.filter(bon_reception_id = bon_reception_id).filter(status = 1)
			for transaction in transactionbudgetaire:
				transaction.status = 3
				transaction.save()
			return True
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA TRANSACTIONBUDGETAIRE')
			#print(e)
			return False
	
	#####FONCTION OPERATIONNELLE WORKFLOW#############
	@staticmethod
	def toCreateTransactionEngagementBudgetaire(auteur,bon_commande):
		'''Fonction de création d'une transaction budgétaire à partir d'un bon de commande'''
		#Recuperation des lignes du bon de reception/ bon de commande
		try:
			lignes = dao_ligne_reception.toListLigneOfReceptionsSortByLigneBudgetaire(bon_commande.id)
			devise = dao_devise.toGetDeviseReference()
			print(bon_commande, devise, lignes)

			for ligne in lignes:
				montant_total = ligne['montant_total']
				ligne_budgetaire_id = ligne['ligne_budgetaire_id']
				ligne_budgetaire = dao_ligne_budgetaire.toGetLigneBudgetaire(ligne_budgetaire_id)
				transactionBudgetaire = dao_transactionbudgetaire.toCreateTransactionbudgetaire(f"Engagement Paiement bon de commande {bon_commande.numero_reception}",montant_total,"",devise.id,ligne_budgetaire.compte_comptable.id,auteur.id,ligne_budgetaire_id,1,1, bon_commande.id)
				transactionBudgetaire = dao_transactionbudgetaire.toSaveTransactionbudgetaire(auteur, transactionBudgetaire)
				transactionBudgetaire.save()
				return transactionBudgetaire
			return True
		except Exception as e:
			return False
	
	@staticmethod
	def toCreateTransactionReelBudgetaire(auteur, facture, list_ligne_bon_commande_id = None):
		'''Fonction de création de Réel pour une facture. La fonction prend une facture et une 
		liste de ligne du bon de commande (id) pour le test optionnel de l'équivalence entre les lignes de 
		factures et les lignes de bon commande '''
		try:
			lignes_factures = dao_ligne_facture.toListLigneOfFacture(facture.id)
			for i in range(0, len(lignes_factures)) :
				#Test de l'équivalence d'une ligne de commande à une ligne de facture pr retrouver la ligne budgetaire
				#Et donner aux lignes qui n'ont pas de combinaison budgetaire spécifique, la ligne budgetaire du bon de commande géneral
				try:
					ligne_commande_id = list_ligne_bon_commande_id[i]
					if ligne_commande_id: ligne_budgetaire = dao_ligne_reception.toGetLigneReception(ligne_commande_id).ligne_budgetaire
					else: ligne_budgetaire = facture.bon_reception.ligne_budgetaire
				except Exception:
					ligne_budgetaire = facture.bon_reception.ligne_budgetaire


				ligne_facture = lignes_factures[i]
				montant_total = makeFloat(ligne_facture.quantite_demande) * makeFloat(ligne_facture.prix_unitaire) #+ makeFloat(ligne_facture.ligne_montant_taxe)
				transactionBudgetaire = dao_transactionbudgetaire.toCreateTransactionbudgetaire("Paiement Réel du bon de commande {0} via la facture {1}".format(facture.bon_reception.numero_reception, facture.numero_facture),montant_total,"",facture.devise_id,ligne_facture.compte_comptable_id,auteur.id,ligne_budgetaire.id,1,2, facture.bon_reception_id, facture.id)
				transactionBudgetaire = dao_transactionbudgetaire.toSaveTransactionbudgetaire(auteur,transactionBudgetaire)
				transactionBudgetaire.save()
			return dao_transactionbudgetaire.toCancelEngagementTransaction(facture.bon_reception_id)
		except Exception as e:
			return False
		
	
	@staticmethod
	def toCreateTransactionReelBCNull(auteur, facture):
		'''Fonction de création de Réel pour une facture ne disposant pas d'un lien avec le Bon de commande. '''
		try:
			lignes_factures = dao_ligne_facture.toListLigneOfFacture(facture.id)
			for i in range(0, len(lignes_factures)) :				
				ligne_facture = lignes_factures[i]
				montant_total = makeFloat(ligne_facture.quantite_demande) * makeFloat(ligne_facture.prix_unitaire) #+ makeFloat(ligne_facture.ligne_montant_taxe)
				transactionBudgetaire = dao_transactionbudgetaire.toCreateTransactionbudgetaire(f"Paiement Réel sans BC de la facture {facture.numero_facture}",montant_total,"",facture.devise_id,ligne_facture.compte_comptable_id,auteur.id,None,1,2, None, facture.id)
				transactionBudgetaire = dao_transactionbudgetaire.toSaveTransactionbudgetaire(auteur,transactionBudgetaire)
				transactionBudgetaire.save()
			return True
		except Exception as e:
			return False
		
	@staticmethod
	def toSetRapprochementTransaction(transaction_id, bon_reception, ligne_budgetaire_id):
		try:
			transactionbudgetaire = Model_Transactionbudgetaire.objects.get(pk = transaction_id)
			transactionbudgetaire.designation = f"Paiement Réel du bon de commande {bon_reception.numero_reception} via la facture {transactionbudgetaire.facture.numero_facture} "
			transactionbudgetaire.ligne_budgetaire_id = ligne_budgetaire_id
			transactionbudgetaire.bon_reception_id = bon_reception.id
			transactionbudgetaire.save()
			return True
		except Exception as e:
			return False

		
