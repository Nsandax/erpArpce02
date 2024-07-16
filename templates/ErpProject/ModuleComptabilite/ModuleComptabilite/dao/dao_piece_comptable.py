from __future__ import unicode_literals
from ErpBackOffice.models import Model_PieceComptable
from ModuleComptabilite.dao.dao_journal import dao_journal
from django.utils import timezone

class dao_piece_comptable(object):
	id = 0
	designation=''
	reference=''
	montant = 0.0
	description = ''
	date_piece = None
	journal_comptable_id = 0
	devise_id = 0
	facture_client_id = 0
	facture_fournisseur_id = 0
	bon_commande_id = 0
	lot_bulletin_id = None
	bon_reception_id = 0
	taux_id = 0
	partenaire_id = 0
	auteur_id = 0

	@staticmethod
	def toListPieceComptable():
		return Model_PieceComptable.objects.all().order_by('-id')

	@staticmethod
	def toCreatePieceComptable(designation, reference, montant, journal_comptable_id = None , date_piece = None,  partenaire_id = None, bon_commande_id = None, bon_reception_id = None, facture_id = None, description = "", devise_id = None, taux_id=None, lot_bulletin_id = None):
		try:
			piece_comptable = dao_piece_comptable()
			piece_comptable.designation = designation
			piece_comptable.reference = reference
			piece_comptable.montant = montant
			piece_comptable.description = description
			piece_comptable.date_piece = date_piece

			piece_comptable.journal_comptable_id = journal_comptable_id
			piece_comptable.devise_id = devise_id
			piece_comptable.taux_id = taux_id
			piece_comptable.facture_id = facture_id
			piece_comptable.bon_reception_id = bon_reception_id
			piece_comptable.bon_commande_id = bon_commande_id
			piece_comptable.partenaire_id = partenaire_id
			piece_comptable.lot_bulletin_id = lot_bulletin_id

			return piece_comptable
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA PIECE_COMPTABLE')
			#print(e)
			return None

	@staticmethod
	def toSavePieceComptable(auteur,objet_dao_piece_comptable):
		try:
			piece_comptable  = Model_PieceComptable()
			piece_comptable.designation =objet_dao_piece_comptable.designation
			piece_comptable.reference =objet_dao_piece_comptable.reference
			piece_comptable.montant = objet_dao_piece_comptable.montant
			piece_comptable.description =objet_dao_piece_comptable.description
			if objet_dao_piece_comptable.date_piece == None:
				piece_comptable.date_piece = timezone.now()
			else: piece_comptable.date_piece = objet_dao_piece_comptable.date_piece
			journal = dao_journal.toGetJournalDivers()
			if objet_dao_piece_comptable.journal_comptable_id == None and journal != None:
				piece_comptable.journal_comptable_id = journal.id
			else: piece_comptable.journal_comptable_id = objet_dao_piece_comptable.journal_comptable_id
			piece_comptable.devise_id = objet_dao_piece_comptable.devise_id
			piece_comptable.taux_id = objet_dao_piece_comptable.taux_id
			piece_comptable.facture_id = objet_dao_piece_comptable.facture_id
			piece_comptable.bon_reception_id = objet_dao_piece_comptable.bon_reception_id
			piece_comptable.bon_commande_id = objet_dao_piece_comptable.bon_commande_id
			piece_comptable.partenaire_id = objet_dao_piece_comptable.partenaire_id
			piece_comptable.lot_bulletin_id = objet_dao_piece_comptable.lot_bulletin_id
			piece_comptable.auteur_id =auteur.id
			piece_comptable.save()
			return piece_comptable
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA PIECE_COMPTABLE')
			#print(e)
			return None

	@staticmethod
	def toUpdatePieceComptable(id, objet_dao_piece_comptable):
		try:
			piece_comptable = Model_PieceComptable.objects.get(pk = id)
			piece_comptable.designation = objet_dao_piece_comptable.designation
			piece_comptable.reference = objet_dao_piece_comptable.reference
			piece_comptable.montant = objet_dao_piece_comptable.montant
			piece_comptable.description =objet_dao_piece_comptable.description
			piece_comptable.date_piece = objet_dao_piece_comptable.date_piece
			piece_comptable.journal_comptable_id = objet_dao_piece_comptable.journal_comptable_id
			piece_comptable.devise_id = objet_dao_piece_comptable.devise_id
			piece_comptable.taux_id = objet_dao_piece_comptable.taux_id
			piece_comptable.facture_id = objet_dao_piece_comptable.facturet_id
			piece_comptable.bon_reception_id = objet_dao_piece_comptable.bon_reception_id
			piece_comptable.bon_commande_id = objet_dao_piece_comptable.bon_commande_id
			piece_comptable.partenaire_id = objet_dao_piece_comptable.partenaire_id
			piece_comptable.lot_bulletin_id = objet_dao_piece_comptable.lot_bulletin_id

			piece_comptable.save()
			return piece_comptable
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA PIECE_COMPTABLE')
			#print(e)
			return None

	@staticmethod
	def toListPiecesComptables():
		try:
			return Model_PieceComptable.objects.all().order_by("-date_piece")
		except Exception as e:
			return []

	@staticmethod
	def toListPiecesComptablesDuJournal(journal_comptable_id):
		try:
			return Model_PieceComptable.objects.filter(journal_comptable_id = journal_comptable_id).order_by("-date_piece")
		except Exception as e:
			return []

	@staticmethod
	def toGetPieceComptable(id):
		try:
			return Model_PieceComptable.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toDeletePieceComptable(id):
		try:
			piece_comptable = Model_PieceComptable.objects.get(pk = id)
			piece_comptable.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toGetPieceComptableFromFacture(facture_id):
		try:
			piece_comptable = Model_PieceComptable.objects.filter(facture_id = facture_id).first()
			#print("la piece comptable",piece_comptable)
			return piece_comptable
		except Exception as e:
			return None
	
	@staticmethod
	def toGetPieceComptableFromLotBulletin(lot_bulletin_id):
		try:
			piece_comptable = Model_PieceComptable.objects.filter(lot_bulletin_id = lot_bulletin_id).first()
			#print("la piece comptable",piece_comptable)
			return piece_comptable
		except Exception as e:
			return None