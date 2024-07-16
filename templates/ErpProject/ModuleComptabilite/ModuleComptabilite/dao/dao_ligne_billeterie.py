from __future__ import unicode_literals
from ErpBackOffice.models import Model_Billeterie, Model_LigneBilleterie
from django.utils import timezone

class dao_ligne_billeterie(object):
	id = 0
	billet = ''
	valeur = 0
	sous_total = 0
	billeterie_id = None


	@staticmethod
	def toListLigneBillerie():
		return Model_LigneBilleterie.objects.all().order_by('-id')

	@staticmethod
	def toCreateLigneBilleterie(billet, valeur, sous_total, billeterie_id):
		try:
			ligne_billeterie = dao_ligne_billeterie()
			ligne_billeterie.billet = billet
			ligne_billeterie.valeur = valeur
			ligne_billeterie.sous_total = sous_total
			ligne_billeterie.billeterie_id  =billeterie_id
			return ligne_billeterie
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA ligne_billeterie')
			#print(e)
			return None

	@staticmethod
	def toSaveLigneBilleterie(auteur, objet_dao_ligne_billeterie):
		try:
			ligne_billeterie  = Model_LigneBilleterie()
			ligne_billeterie.billet = objet_dao_ligne_billeterie.billet
			ligne_billeterie.valeur = objet_dao_ligne_billeterie.valeur
			ligne_billeterie.sous_total = objet_dao_ligne_billeterie.sous_total
			ligne_billeterie.billeterie_id = objet_dao_ligne_billeterie.billeterie_id
			ligne_billeterie.created_at = timezone.now()
			ligne_billeterie.updated_at = timezone.now()
			ligne_billeterie.auteur_id = auteur.id

			ligne_billeterie.save()
			return ligne_billeterie
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA ligne_billeterie')
			#print(e)
			return None

	@staticmethod
	def toUpdateLigneBilleterie(id, objet_dao_ligne_billeterie):
		try:
			ligne_billeterie = Model_LigneBilleterie.objects.get(pk = id)
			ligne_billeterie.billet = objet_dao_ligne_billeterie.billet
			ligne_billeterie.valeur = objet_dao_ligne_billeterie.valeur
			ligne_billeterie.billeterie_id = objet_dao_ligne_billeterie.billeterie_id
			ligne_billeterie.sous_total = objet_dao_ligne_billeterie.sous_total
			ligne_billeterie.updated_at = timezone.now()
			ligne_billeterie.save()
			return ligne_billeterie
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA ligne_billeterie')
			#print(e)
			return None
	@staticmethod
	def toGetLigneBilleterie(id):
		try:
			return Model_LigneBilleterie.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toGetLigneFromBilleterie(billeterie_id):
		try:
			return Model_LigneBilleterie.objects.filter(billeterie_id = billeterie_id)
		except Exception as e:
			return None

	@staticmethod
	def toDeleteLigneBilleterie(id):
		try:
			ligne_billeterie = Model_LigneBilleterie.objects.get(pk = id)
			ligne_billeterie.delete()
			return True
		except Exception as e:
			return False
