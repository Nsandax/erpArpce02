from __future__ import unicode_literals
from ModuleStock.models import Model_Ligne_Ajustement
from django.utils import timezone

class dao_ligne_ajustement(object):
	id = 0
	ajustement = None
	article = None
	series = None
	quantite_theorique = 0.0
	quantite_reelle = 0.0
	unite = None
	fait = False

	@staticmethod
	def toList():
		return Model_Ligne_Ajustement.objects.all()

	@staticmethod
	def toCreate(ajustement_id,article_id,series_id,quantite_theorique,quantite_reelle,unite_id,fait):
		try:
			ligne_ajustement = dao_ligne_ajustement()
			ligne_ajustement.ajustement_id = ajustement_id
			ligne_ajustement.article_id = article_id
			ligne_ajustement.series_id = series_id
			ligne_ajustement.quantite_theorique = quantite_theorique
			ligne_ajustement.quantite_reelle = quantite_reelle
			ligne_ajustement.unite_id = unite_id
			ligne_ajustement.fait = fait
			return ligne_ajustement
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA LIGNE_AJUSTEMENT')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_Ligne_ajustement):
		try:
			ligne_ajustement  = Model_Ligne_Ajustement()
			ligne_ajustement.ajustement_id = objet_dao_Ligne_ajustement.ajustement_id
			ligne_ajustement.article_id = objet_dao_Ligne_ajustement.article_id
			ligne_ajustement.series_id = objet_dao_Ligne_ajustement.series_id
			ligne_ajustement.quantite_theorique = objet_dao_Ligne_ajustement.quantite_theorique
			ligne_ajustement.quantite_reelle = objet_dao_Ligne_ajustement.quantite_reelle
			ligne_ajustement.unite_id = objet_dao_Ligne_ajustement.unite_id
			ligne_ajustement.fait = objet_dao_Ligne_ajustement.fait
			ligne_ajustement.auteur_id = auteur.id
			ligne_ajustement.save()
			return ligne_ajustement
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA LIGNE_AJUSTEMENT')
			#print(e)
			return None

	@staticmethod
	def toUpdate(id, objet_dao_Ligne_ajustement):
		try:
			ligne_ajustement = Model_Ligne_Ajustement.objects.get(pk = id)
			ligne_ajustement.ajustement_id =objet_dao_Ligne_ajustement.ajustement_id
			ligne_ajustement.article_id =objet_dao_Ligne_ajustement.article_id
			ligne_ajustement.series_id =objet_dao_Ligne_ajustement.series_id
			ligne_ajustement.quantite_theorique =objet_dao_Ligne_ajustement.quantite_theorique
			ligne_ajustement.quantite_reelle =objet_dao_Ligne_ajustement.quantite_reelle
			ligne_ajustement.unite_id =objet_dao_Ligne_ajustement.unite_id
			ligne_ajustement.fait =objet_dao_Ligne_ajustement.fait
			ligne_ajustement.save()
			return ligne_ajustement
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA LIGNE_AJUSTEMENT')
			#print(e)
			return None

	@staticmethod
	def toGet(id):
		try:
			return Model_Ligne_Ajustement.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toDelete(id):
		try:
			ligne_ajustement = Model_Ligne_Ajustement.objects.get(pk = id)
			ligne_ajustement.delete()
			return True
		except Exception as e:
			return False