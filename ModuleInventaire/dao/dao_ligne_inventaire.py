from __future__ import unicode_literals
from ErpBackOffice.models import Model_Ligne_inventaire
from django.utils import timezone
from django.db.models.functions import TruncMonth
from django.db.models import Count

class dao_ligne_inventaire(object):
	id = 0
	quantite_demandee=0
	quantite_fournie=0
	creation_date='2010-01-01'
	type=''
	bon_inventaire_id = 0
	stock_article_id = 0
	auteur_id = 0


	@staticmethod
	def toListLigneInventaire():
		return Model_Ligne_inventaire.objects.all().order_by('-id')

	@staticmethod
	def toListLignesInventaire(bon_inventaire_id):
		return Model_Ligne_inventaire.objects.filter(bon_inventaire_id = bon_inventaire_id).order_by("-creation_date")

	@staticmethod
	def toCreateLigneInventaire(quantite_demandee,quantite_fournie,prix_unitaire,prix_lot,type, bon_inventaire_id=None, stock_article_id=None):
		try:
			ligne_inventaire = dao_ligne_inventaire()
			ligne_inventaire.quantite_demandee = int(quantite_demandee)
			ligne_inventaire.quantite_fournie = int(quantite_fournie)
			ligne_inventaire.type = type
			ligne_inventaire.bon_inventaire_id = bon_inventaire_id
			ligne_inventaire.stock_article_id = stock_article_id
			return ligne_inventaire
		except Exception as e:
			print('ERREUR LORS DE LA CREATION DE LA LIGNE_inventaire')
			print(e)
			return None

	@staticmethod
	def toSaveLigneInventaire(auteur,objet_dao_Ligne_inventaire):
		try:
			ligne_inventaire  = Model_Ligne_inventaire()
			ligne_inventaire.quantite_demandee =objet_dao_Ligne_inventaire.quantite_demandee
			ligne_inventaire.quantite_fournie =objet_dao_Ligne_inventaire.quantite_fournie
			ligne_inventaire.creation_date =timezone.now()
			ligne_inventaire.type =objet_dao_Ligne_inventaire.type
			ligne_inventaire.bon_inventaire_id = objet_dao_Ligne_inventaire.bon_inventaire_id
			ligne_inventaire.stock_article_id = objet_dao_Ligne_inventaire.stock_article_id
			ligne_inventaire.auteur_id = auteur.id
			ligne_inventaire.save()
			return ligne_inventaire
		except Exception as e:
			print('ERREUR LORS DE L ENREGISTREMENT DE LA LIGNE_inventaire')
			print(e)
			return None

	@staticmethod
	def toUpdateLigneInventaire(id, objet_dao_Ligne_inventaire):
		try:
			ligne_inventaire = Model_Ligne_inventaire.objects.get(pk = id)
			ligne_inventaire.quantite_demandee =objet_dao_Ligne_inventaire.quantite_demandee
			ligne_inventaire.quantite_fournie =objet_dao_Ligne_inventaire.quantite_fournie
			ligne_inventaire.type =objet_dao_Ligne_inventaire.type
			ligne_inventaire.save()
			return ligne_inventaire
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA LIGNE_inventaire')
			#print(e)
			return None
	@staticmethod
	def toGetLigneInventaire(id):
		try:
			return Model_Ligne_inventaire.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteLigneInventaire(id):
		try:
			ligne_inventaire = Model_Ligne_inventaire.objects.get(pk = id)
			ligne_inventaire.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def ListeNumberInventoryByMunth(today = timezone.now().year):
		try:
			#print(' ListeNumberInventoryByMunth')

			ListeDemandeQuery = Model_Ligne_inventaire.objects.annotate(month=TruncMonth('creation_date')).values(
				'month').annotate(total=Count('quantite_demandee')).filter(creation_date__year=today)

			ListDemande = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
			for item in ListeDemandeQuery:
    				#print('yes')
    				if item["month"].month == 1:
    						if item["total"] == 0:
    								ListDemande[0] = 0
    						else:
    								ListDemande[0] = item["total"]
    						continue
    				if item["month"].month == 2:
    						if item["total"] == 0:
    								ListDemande[1] = 0
    						else:
    								ListDemande[1] = item["total"]
    						continue
    				elif item["month"].month == 3:
    						if item["total"] == 0:
    								ListDemande[2] = 0
    						else:
    								ListDemande[2] = item["total"]
    						continue
    				elif item["month"].month == 4:
    						if item["total"] == 0:
    								ListDemande[3] = 0
    						else:
    								ListDemande[3] == item["total"]
    						continue
    				elif item["month"].month == 5:
    						if item["total"] == 0:
    								ListDemande[4] = 0
    						else:
    								ListDemande[4] = item["total"]
    						continue
    				elif item["month"].month == 6:
    						if item["total"] == 0:
    								ListDemande[5] = 0
    						else:
    								ListDemande[5] = item["total"]
    						continue
    				elif item["month"].month == 7:
    						if item["total"] == 0:
    								ListDemande[6] = 0
    						else:
    								ListDemande[6] = item["total"]
    						continue
    				elif item["month"].month == 8:
    						if item["total"] == 0:
    								ListDemande[7] = 0
    						else:
    								ListDemande[7] = item["total"]
    						continue
    				elif item["month"].month == 9:
    						if item["total"] == 0:
    								ListDemande[8] = 0
    						else:
    								ListDemande[8] = item["total"]
    						continue
    				elif item["month"].month == 10:
    						if item["total"] == 0:
    								ListDemande[9] = 0
    						else:
    								ListDemande[9] = item["total"]
    						continue
    				elif item["month"].month == 11:
    						if item["total"] == 0:
    								ListDemande[10] = 0
    						else:
    								ListDemande[10] = item["total"]
    						continue
    				elif item["month"].month == 12:
    						if item["total"] == 0:
    								ListDemande[11] = 0
    						else:
    								ListDemande[11] = item["total"]
    						continue
    				else:
    						pass
			#print('Liste des CONGE %s' %(ListDemande))
			return ListDemande
		except Exception as e:
			#print("ERRER LISTECONGE BY MONTH")
			#print(e)
			pass

	@staticmethod
	def ListeNumberFournieByMunth(today = timezone.now().year):
		try:
			#print(' ListeNumberFournieByMunth')

			ListeDemandeQuery = Model_Ligne_inventaire.objects.annotate(month=TruncMonth('creation_date')).values(
				'month').annotate(total=Count('quantite_fournie')).filter(creation_date__year=today)

			ListDemande = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
			for item in ListeDemandeQuery:
    				#print('yes')
    				if item["month"].month == 1:
    						if item["total"] == 0:
    								ListDemande[0] = 0
    						else:
    								ListDemande[0] = item["total"]
    						continue
    				if item["month"].month == 2:
    						if item["total"] == 0:
    								ListDemande[1] = 0
    						else:
    								ListDemande[1] = item["total"]
    						continue
    				elif item["month"].month == 3:
    						if item["total"] == 0:
    								ListDemande[2] = 0
    						else:
    								ListDemande[2] = item["total"]
    						continue
    				elif item["month"].month == 4:
    						if item["total"] == 0:
    								ListDemande[3] = 0
    						else:
    								ListDemande[3] == item["total"]
    						continue
    				elif item["month"].month == 5:
    						if item["total"] == 0:
    								ListDemande[4] = 0
    						else:
    								ListDemande[4] = item["total"]
    						continue
    				elif item["month"].month == 6:
    						if item["total"] == 0:
    								ListDemande[5] = 0
    						else:
    								ListDemande[5] = item["total"]
    						continue
    				elif item["month"].month == 7:
    						if item["total"] == 0:
    								ListDemande[6] = 0
    						else:
    								ListDemande[6] = item["total"]
    						continue
    				elif item["month"].month == 8:
    						if item["total"] == 0:
    								ListDemande[7] = 0
    						else:
    								ListDemande[7] = item["total"]
    						continue
    				elif item["month"].month == 9:
    						if item["total"] == 0:
    								ListDemande[8] = 0
    						else:
    								ListDemande[8] = item["total"]
    						continue
    				elif item["month"].month == 10:
    						if item["total"] == 0:
    								ListDemande[9] = 0
    						else:
    								ListDemande[9] = item["total"]
    						continue
    				elif item["month"].month == 11:
    						if item["total"] == 0:
    								ListDemande[10] = 0
    						else:
    								ListDemande[10] = item["total"]
    						continue
    				elif item["month"].month == 12:
    						if item["total"] == 0:
    								ListDemande[11] = 0
    						else:
    								ListDemande[11] = item["total"]
    						continue
    				else:
    						pass
			#print('Liste des CONGE %s' % ListDemande)
			return ListDemande
		except Exception as e:
			#print("ERRER LISTECONGE BY MONTH")
			#print(e)
			pass
