from __future__ import unicode_literals
from ErpBackOffice.models import Model_Ligne_OperationTresorerie, Model_EcritureComptable
from django.utils import timezone

class dao_ligne_operation_tresorerie(object):
	id = 0
	reference = ''
	libelle = ''
	partenaire_id = None
	montant = 0.0
	devise_id = None
	taux_id = None
	type_operation = 1
	description = ''
	operation_tresorerie_id = None
	date_ligne_operation = None

	@staticmethod
	def toListLigne_operation_tresorerie():
		return Model_Ligne_OperationTresorerie.objects.all().order_by('-id')

	@staticmethod
	def toCreateLigne_operation_tresorerie(reference,libelle,partenaire_id,montant,devise_id,taux_id,type_operation,description,operation_tresorerie_id=None,date_ligne_operation=None):
		try:
			ligne_operation_tresorerie = dao_ligne_operation_tresorerie()
			ligne_operation_tresorerie.reference = reference
			ligne_operation_tresorerie.libelle = libelle
			ligne_operation_tresorerie.partenaire_id = partenaire_id
			ligne_operation_tresorerie.montant = montant
			ligne_operation_tresorerie.devise_id = devise_id
			ligne_operation_tresorerie.taux_id = taux_id
			ligne_operation_tresorerie.type_operation = type_operation
			ligne_operation_tresorerie.description = description
			ligne_operation_tresorerie.operation_tresorerie_id = operation_tresorerie_id
			#print("operation tresorerie", operation_tresorerie_id)
			ligne_operation_tresorerie.date_ligne_operation = date_ligne_operation
			return ligne_operation_tresorerie
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA LIGNE_operation_tresorerie')
			#print(e)
			return None

	@staticmethod
	def toSaveLigne_operation_tresorerie(auteur, objet_dao_Ligne_operation_tresorerie):
		try:
			ligne_operation_tresorerie  = Model_Ligne_OperationTresorerie()
			ligne_operation_tresorerie.reference = objet_dao_Ligne_operation_tresorerie.reference
			ligne_operation_tresorerie.libelle = objet_dao_Ligne_operation_tresorerie.libelle
			ligne_operation_tresorerie.partenaire_id = objet_dao_Ligne_operation_tresorerie.partenaire_id
			ligne_operation_tresorerie.montant = objet_dao_Ligne_operation_tresorerie.montant
			ligne_operation_tresorerie.devise_id = objet_dao_Ligne_operation_tresorerie.devise_id
			ligne_operation_tresorerie.taux_id = objet_dao_Ligne_operation_tresorerie.taux_id
			ligne_operation_tresorerie.type_operation = objet_dao_Ligne_operation_tresorerie.type_operation
			ligne_operation_tresorerie.description = objet_dao_Ligne_operation_tresorerie.description
			print("operation tresorerie", objet_dao_Ligne_operation_tresorerie.operation_tresorerie_id)
			ligne_operation_tresorerie.operation_tresorerie_id = objet_dao_Ligne_operation_tresorerie.operation_tresorerie_id
			ligne_operation_tresorerie.date_ligne_operation = objet_dao_Ligne_operation_tresorerie.date_ligne_operation
			ligne_operation_tresorerie.created_at = timezone.now()
			ligne_operation_tresorerie.updated_at = timezone.now()
			#ligne_operation_tresorerie.auteur_id = auteur.id

			ligne_operation_tresorerie.save()
			return ligne_operation_tresorerie
		except Exception as e:
			print('ERREUR LORS DE L ENREGISTREMENT DE LA LIGNE_operation_tresorerie')
			print(e)
			return None

	@staticmethod
	def toUpdateLigne_operation_tresorerie(id, objet_dao_Ligne_operation_tresorerie):
		try:
			ligne_operation_tresorerie = Model_Ligne_OperationTresorerie.objects.get(pk = id)
			#print(ligne_operation_tresorerie)
			ligne_operation_tresorerie.reference =objet_dao_Ligne_operation_tresorerie.reference
			ligne_operation_tresorerie.libelle =objet_dao_Ligne_operation_tresorerie.libelle
			ligne_operation_tresorerie.partenaire_id =objet_dao_Ligne_operation_tresorerie.partenaire_id
			ligne_operation_tresorerie.montant =objet_dao_Ligne_operation_tresorerie.montant
			ligne_operation_tresorerie.devise_id =objet_dao_Ligne_operation_tresorerie.devise_id
			ligne_operation_tresorerie.taux_id =objet_dao_Ligne_operation_tresorerie.taux_id
			ligne_operation_tresorerie.type_operation =objet_dao_Ligne_operation_tresorerie.type_operation
			ligne_operation_tresorerie.description =objet_dao_Ligne_operation_tresorerie.description
			#print("operation tresorerie", objet_dao_Ligne_operation_tresorerie.operation_tresorerie_id)
			ligne_operation_tresorerie.operation_tresorerie_id = objet_dao_Ligne_operation_tresorerie.operation_tresorerie_id
			ligne_operation_tresorerie.date_ligne_operation = objet_dao_Ligne_operation_tresorerie.date_ligne_operation
			ligne_operation_tresorerie.updated_at = timezone.now()
			ligne_operation_tresorerie.save()
			return ligne_operation_tresorerie
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA LIGNE_operation_tresorerie')
			#print(e)
			return None
	@staticmethod
	def toGetLigne_operation_tresorerie(id):
		try:
			return Model_Ligne_OperationTresorerie.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListLigneTresorerieofOperation(operation_tresorerie_id):
		try:
			return Model_Ligne_OperationTresorerie.objects.filter(operation_tresorerie_id = operation_tresorerie_id)
		except Exception as e:
			return None

	@staticmethod
	def toListLigneTresorerieofOperationNonLettre(operation_tresorerie_id):
		try:
			return Model_Ligne_OperationTresorerie.objects.filter(operation_tresorerie_id = operation_tresorerie_id).filter(est_lettre = False)
		except Exception as e:
			return None

	@staticmethod
	def toDeleteLigne_operation_tresorerie(id):
		try:
			ligne_operation_tresorerie = Model_Ligne_OperationTresorerie.objects.get(pk = id)
			ligne_operation_tresorerie.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toSetLigneLettrage(id, lettrage_id, facture_id=None):
		try:
			ligne_operation_tresorerie = Model_Ligne_OperationTresorerie.objects.get(pk = id)
			ligne_operation_tresorerie.est_lettre = True
			ligne_operation_tresorerie.facture_id = facture_id
			ligne_operation_tresorerie.lettrage_id = lettrage_id
			ligne_operation_tresorerie.save()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toListLignesFromAccountBank(compte_banque_id):
		tableauLignes = []
		tableauLettres = []

		try:

			Lignes = {
				'date':'',
				'libelle': '',
				'debit':0,
                'credit':0,
                }
			Lettres = {
				'date':'',
				'libelle': '',
				'debit':0,
                'credit':0,
                }
			lignes =  Model_Ligne_OperationTresorerie.objects.filter(operation_tresorerie__compte_banque_id = compte_banque_id)
			for ligne in lignes:
				Lignes['date'] = ligne.date_ligne_operation
				Lignes['libelle'] = ligne.libelle
				if ligne.type_operation == 1:
					Lignes['debit'] += ligne.montant
				elif ligne.type_operation == 2:
					Lignes['credit'] += ligne.montant

				tableauLignes.append(Lignes)

				if ligne.est_lettre:
					#print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
					Lettres['date'] = ligne.date_ligne_operation
					Lettres['libelle'] = ligne.libelle
					if ligne.type_operation == 1:
						Lettres['debit'] += ligne.montant
					elif ligne.type_operation == 2:
						Lettres['credit'] += ligne.montant
					tableauLettres.append(Lettres)



			return tableauLignes, tableauLettres

		except Exception as e:
			return tableauLignes, tableauLettres

	@staticmethod
	def toListLignesRapprochementBancaire(compte_banque_id, date_debut=None, date_fin=None):
		tableauLignes = []
		tableauEcritures = []

		try:

			if date_debut and date_fin:
				lignes =  Model_Ligne_OperationTresorerie.objects.filter(operation_tresorerie__compte_banque_id = compte_banque_id).filter(date_ligne_operation__range=(date_debut,date_fin))
			else:
				#print("No date given")
				lignes =  Model_Ligne_OperationTresorerie.objects.filter(operation_tresorerie__compte_banque_id = compte_banque_id)
			#print("lignes", lignes)
			for ligne in lignes:
				#print("ligne ", ligne)
				#print("est lettre",ligne.est_lettre)
				if ligne.est_lettre and ligne.lettrage:
					Lignes = {
						'date':'',
						'libelle': '',
						'debit':0,
						'credit':0,
						}
					Ecritures = {
						'date':'',
						'libelle': '',
						'debit':0,
						'credit':0,
						}
					#print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
					Lignes['date'] = ligne.date_ligne_operation
					Lignes['libelle'] = ligne.libelle
					if ligne.type_operation == 1:
						Lignes['debit'] = ligne.montant
						ecriture = Model_EcritureComptable.objects.filter(lettrage_id = ligne.lettrage_id).filter(montant_credit = 0).first()
						Ecritures["debit"] = ecriture.montant_debit
					elif ligne.type_operation == 2:
						Lignes['credit'] = ligne.montant
						ecriture = Model_EcritureComptable.objects.filter(lettrage_id = ligne.lettrage_id).filter(montant_debit = 0).first()
						#print("ecriture")
						Ecritures["credit"] = ecriture.montant_credit
					tableauLignes.append(Lignes)

					Ecritures["date"] = ecriture.date_creation
					Ecritures['libelle'] = ecriture.compte.numero + ": " + ecriture.designation + '( Pièce: ' + ecriture.piece_comptable.reference + ')'
					tableauEcritures.append(Ecritures)


			return tableauLignes, tableauEcritures

		except Exception as e:
			#print(e)
			return tableauLignes, tableauEcritures