from __future__ import unicode_literals
from ModuleStock.models import Model_EmplacementStock
from django.utils import timezone

class dao_emplacementstock(object):
	id = 0
	designation = ''
	type_id = None
	entrepot_id = None
	couloir = 0
	rayon = 0
	hauteur = 0
	# parent_id = 0

	@staticmethod
	def toList():
		return Model_EmplacementStock.objects.all()

	@staticmethod
	def toCreate(designation,type_id,entrepot_id,couloir,rayon,hauteur):
		try:
			emplacementstock = dao_emplacementstock()
			emplacementstock.designation = designation
			emplacementstock.type_id = type_id
			emplacementstock.entrepot_id = entrepot_id
			emplacementstock.couloir = couloir
			emplacementstock.rayon = rayon
			emplacementstock.hauteur = hauteur
			# emplacementstock.parent_id = parent_id
			# if parent_id != 0 : emplacementstock.parent_id = parent_id
			return emplacementstock
		except Exception as e:
			print('ERREUR LORS DE LA CREATION DE LA EMPLACEMENTSTOCK')
			print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_Emplacementstock):
		try:
			emplacementstock  = Model_EmplacementStock()
			emplacementstock.designation = objet_dao_Emplacementstock.designation
			emplacementstock.type_id = objet_dao_Emplacementstock.type_id
			emplacementstock.entrepot_id = objet_dao_Emplacementstock.entrepot_id
			emplacementstock.couloir = objet_dao_Emplacementstock.couloir
			emplacementstock.rayon = objet_dao_Emplacementstock.rayon
			emplacementstock.hauteur = objet_dao_Emplacementstock.hauteur
			# emplacementstock.parent_id = objet_dao_Emplacementstock.parent_id
			emplacementstock.auteur_id = auteur.id
			emplacementstock.save()
			return emplacementstock
		except Exception as e:
			print('ERREUR LORS DE L ENREGISTREMENT DE LA EMPLACEMENTSTOCK')
			print(e)
			return None

	@staticmethod
	def toUpdate(id, objet_dao_Emplacementstock):
		try:
			emplacementstock = Model_EmplacementStock.objects.get(pk = id)
			emplacementstock.designation =objet_dao_Emplacementstock.designation
			emplacementstock.type_id =objet_dao_Emplacementstock.type_id
			emplacementstock.entrepot_id =objet_dao_Emplacementstock.entrepot_id
			emplacementstock.couloir =objet_dao_Emplacementstock.couloir
			emplacementstock.rayon =objet_dao_Emplacementstock.rayon
			emplacementstock.hauteur =objet_dao_Emplacementstock.hauteur
			# emplacementstock.parent_id =objet_dao_Emplacementstock.parent_id
			emplacementstock.save()
			return emplacementstock
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA EMPLACEMENTSTOCK')
			#print(e)
			return None

	@staticmethod
	def toGet(id):
		try:
			return Model_EmplacementStock.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toDelete(id):
		try:
			emplacementstock = Model_EmplacementStock.objects.get(pk = id)
			emplacementstock.delete()
			return True
		except Exception as e:
			return False