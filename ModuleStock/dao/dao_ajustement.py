from __future__ import unicode_literals
from ModuleStock.models import Model_Ajustement
from django.utils import timezone

class dao_ajustement(object):
	id = 0
	reference = ''
	emplacement = None
	statut = None
	inventaire_de = 0
	document = ''

	@staticmethod
	def toList():
		return Model_Ajustement.objects.all()

	@staticmethod
	def toCreate(reference,emplacement_id,statut_id,inventaire_de,document):
		try:
			ajustement = dao_ajustement()
			ajustement.reference = reference
			ajustement.emplacement_id = emplacement_id
			ajustement.statut_id = statut_id
			ajustement.inventaire_de = inventaire_de
			ajustement.document = document
			return ajustement
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA AJUSTEMENT')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_Ajustement):
		try:
			ajustement  = Model_Ajustement()
			ajustement.reference = objet_dao_Ajustement.reference
			ajustement.emplacement_id = objet_dao_Ajustement.emplacement_id
			ajustement.statut_id = objet_dao_Ajustement.statut_id
			ajustement.inventaire_de = objet_dao_Ajustement.inventaire_de
			ajustement.document = objet_dao_Ajustement.document
			ajustement.auteur_id = auteur.id
			ajustement.save()
			return ajustement
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA AJUSTEMENT')
			#print(e)
			return None

	@staticmethod
	def toUpdate(id, objet_dao_Ajustement):
		try:
			ajustement = Model_Ajustement.objects.get(pk = id)
			ajustement.reference =objet_dao_Ajustement.reference
			ajustement.emplacement_id =objet_dao_Ajustement.emplacement_id
			ajustement.statut_id =objet_dao_Ajustement.statut_id
			ajustement.inventaire_de =objet_dao_Ajustement.inventaire_de
			ajustement.document =objet_dao_Ajustement.document
			ajustement.save()
			return ajustement
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA AJUSTEMENT')
			#print(e)
			return None

	@staticmethod
	def toGet(id):
		try:
			return Model_Ajustement.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toDelete(id):
		try:
			ajustement = Model_Ajustement.objects.get(pk = id)
			ajustement.delete()
			return True
		except Exception as e:
			return False