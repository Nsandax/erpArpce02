from __future__ import unicode_literals
from ErpBackOffice.models import Model_Requete_demande
from django.utils import timezone

class dao_requete_demande(object):
	id = 0
	designation=''
	type_requete=''
	description=''
	auteur_id = 0

	@staticmethod
	def toListRequeteDemande():
		return Model_Requete_demande.objects.all().order_by('-id')

	@staticmethod
	def toCreateRequeteDemande(designation,type_requete,description):
		try:
			requete_demande = dao_requete_demande()
			requete_demande.designation = designation
			requete_demande.type_requete = type_requete
			requete_demande.description = description
			return requete_demande
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA REQUETE_DEMANDE')
			#print(e)
			return None

	@staticmethod
	def toSaveRequeteDemande(auteur,objet_dao_Requete_demande):
		try:
			requete_demande  = Model_Requete_demande()
			requete_demande.designation =objet_dao_Requete_demande.designation
			requete_demande.type_requete =objet_dao_Requete_demande.type_requete
			requete_demande.description =objet_dao_Requete_demande.description
			requete_demande.creation_demande = timezone.now()
			requete_demande.auteur_id = auteur.id
			requete_demande.save()
			return requete_demande
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA REQUETE_DEMANDE')
			#print(e)
			return None

	@staticmethod
	def toUpdateRequeteDemande(id, objet_dao_Requete_demande):
		try:
			requete_demande = Model_Requete_demande.objects.get(pk = id)
			requete_demande.designation =objet_dao_Requete_demande.designation
			requete_demande.type_requete =objet_dao_Requete_demande.type_requete
			requete_demande.description =objet_dao_Requete_demande.description
			requete_demande.save()
			return requete_demande
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA REQUETE_DEMANDE')
			#print(e)
			return None
	@staticmethod
	def toGetRequeteDemande(id):
		try:
			return Model_Requete_demande.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteRequeteDemande(id):
		try:
			requete_demande = Model_Requete_demande.objects.get(pk = id)
			requete_demande.delete()
			return True
		except Exception as e:
			return False