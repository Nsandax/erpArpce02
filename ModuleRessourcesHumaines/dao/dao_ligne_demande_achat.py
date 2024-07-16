from __future__ import unicode_literals
from ErpBackOffice.models import Model_Ligne_demande_achat
from django.utils import timezone

class dao_ligne_demande_achat(object):
	id = 0
	quantite_demande=0
	prix_unitaire=0.0
	article_id = 0
	demande_id = 0
	auteur_id = 0

	@staticmethod
	def toListLigneDemandeAchat():
		return Model_Ligne_demande_achat.objects.all().order_by('-id')

	@staticmethod
	def toCreateLigneDemandeAchat(quantite_demande,prix_unitaire,article_id=0,demande_id=0):
		try:
			ligne_demande_achat = dao_ligne_demande_achat()
			ligne_demande_achat.quantite_demande = quantite_demande
			ligne_demande_achat.prix_unitaire = prix_unitaire
			if article_id != 0:
				ligne_demande_achat.article_id = article_id
			if demande_id != 0:
				ligne_demande_achat.demande_id = demande_id
			return ligne_demande_achat
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA LIGNE_DEMANDE_ACHAT')
			#print(e)
			return None

	@staticmethod
	def toSaveLigneDemandeAchat(auteur,objet_dao_Ligne_demande_achat):
		try:
			ligne_demande_achat  = Model_Ligne_demande_achat()
			ligne_demande_achat.quantite_demande =objet_dao_Ligne_demande_achat.quantite_demande
			ligne_demande_achat.prix_unitaire =objet_dao_Ligne_demande_achat.prix_unitaire
			ligne_demande_achat.creation_date =timezone.now()
			ligne_demande_achat.auteur_id = auteur.id
			ligne_demande_achat.save()
			return ligne_demande_achat
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA LIGNE_DEMANDE_ACHAT')
			#print(e)
			return None

	@staticmethod
	def toUpdateLigneDemandeAchat(id, objet_dao_Ligne_demande_achat):
		try:
			ligne_demande_achat = Model_Ligne_demande_achat.objects.get(pk = id)
			ligne_demande_achat.quantite_demande =objet_dao_Ligne_demande_achat.quantite_demande
			ligne_demande_achat.prix_unitaire =objet_dao_Ligne_demande_achat.prix_unitaire
			ligne_demande_achat.save()
			return ligne_demande_achat
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA LIGNE_DEMANDE_ACHAT')
			#print(e)
			return None
	@staticmethod
	def toGetLigneDemandeAchat(id):
		try:
			return Model_Ligne_demande_achat.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteLigneDemandeAchat(id):
		try:
			ligne_demande_achat = Model_Ligne_demande_achat.objects.get(pk = id)
			ligne_demande_achat.delete()
			return True
		except Exception as e:
			return False