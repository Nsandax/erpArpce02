from __future__ import unicode_literals
from ErpBackOffice.models import Model_Ligne_commande
from django.utils import timezone

class dao_ligne_commande(object):
	id = 0
	quantite_demandee=0
	quantite_fournie=0
	prix_unitaire=0.0
	prix_lot=0.0
	creation_date='2010-01-01'
	type=''
	bon_commande_id = 0
	stock_article_id = 0
	auteur_id = 0

	@staticmethod
	def toListLigneCommande():
		return Model_Ligne_commande.objects.all().order_by('-id')

	@staticmethod
	def toListLigneOfCommandes(id):
		try:
			lignes = Model_Ligne_commande.objects.filter(bon_commande = id)
			return lignes
		except Exception as e:
			return None

	@staticmethod
	def toCreateLigneCommande(quantite_demandee,quantite_fournie,prix_unitaire,prix_lot,type,bon_commande_id=0, stock_article_id = 0):
		try:
			ligne_commande = dao_ligne_commande()
			ligne_commande.quantite_demandee = quantite_demandee
			ligne_commande.quantite_fournie = quantite_fournie
			ligne_commande.prix_unitaire = prix_unitaire
			ligne_commande.prix_lot = prix_lot
			ligne_commande.type = type
			if bon_commande_id != 0:
				ligne_commande.bon_commande_id = bon_commande_id
			if stock_article_id != 0:
				ligne_commande.stock_article_id = stock_article_id
			return ligne_commande

		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA LIGNE_COMMANDE')
			#print(e)
			return None

	@staticmethod
	def toSaveLigneCommande(auteur,objet_dao_Ligne_commande):
		try:
			ligne_commande  = Model_Ligne_commande()
			ligne_commande.quantite_demandee =objet_dao_Ligne_commande.quantite_demandee
			ligne_commande.quantite_fournie =objet_dao_Ligne_commande.quantite_fournie
			ligne_commande.prix_unitaire =objet_dao_Ligne_commande.prix_unitaire
			ligne_commande.prix_lot =objet_dao_Ligne_commande.prix_lot
			ligne_commande.creation_date =timezone.now()
			ligne_commande.type =objet_dao_Ligne_commande.type
			ligne_commande.bon_commande_id = objet_dao_Ligne_commande.bon_commande_id
			ligne_commande.stock_article_id = objet_dao_Ligne_commande.stock_article_id
			ligne_commande.auteur_id =auteur.id
			ligne_commande.save()
			return ligne_commande
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA LIGNE_COMMANDE')
			#print(e)
			return None

	@staticmethod
	def toUpdateLigneCommande(id, objet_dao_Ligne_commande):
		try:
			ligne_commande = Model_Ligne_commande.objects.get(pk = id)
			ligne_commande.quantite_demandee =objet_dao_Ligne_commande.quantite_demandee
			ligne_commande.quantite_fournie =objet_dao_Ligne_commande.quantite_fournie
			ligne_commande.prix_unitaire =objet_dao_Ligne_commande.prix_unitaire
			ligne_commande.prix_lot =objet_dao_Ligne_commande.prix_lot
			ligne_commande.type =objet_dao_Ligne_commande.type
			ligne_commande.bon_commande_id = objet_dao_Ligne_commande.bon_commande_id
			ligne_commande.stock_article_id = objet_dao_Ligne_commande.stock_article_id
			ligne_commande.save()
			return ligne_commande
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA LIGNE_COMMANDE')
			#print(e)
			return None
	@staticmethod
	def toGetLigneCommande(id):
		try:
			return Model_Ligne_commande.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteLigneCommande(id):
		try:
			ligne_commande = Model_Ligne_commande.objects.get(pk = id)
			ligne_commande.delete()
			return True
		except Exception as e:
			return False