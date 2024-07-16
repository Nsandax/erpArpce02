from __future__ import unicode_literals
from ErpBackOffice.models import Model_Demande_achat
from django.utils import timezone

class dao_demande_achat(object):
	id = 0
	numero_demande=''
	date_demande='2010-01-01'
	description=''
	requete_id = 0
	employe_id = 0
	auteur_id = 0

	@staticmethod
	def toListDemandeAchat():
		return Model_Demande_achat.objects.all().order_by('-id')

	@staticmethod
	def toCreateDemandeAchat(numero_demande,date_demande,description,requete_id=0,employe_id=0):
		try:
			demande_achat = dao_demande_achat()
			demande_achat.numero_demande = numero_demande
			demande_achat.date_demande = date_demande
			demande_achat.description = description
			if employe_id != 0:
				demande_achat.employe_id = employe_id
			if requete_id != 0:
				demande_achat.requete_id = requete_id
			return demande_achat
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA DEMANDE_ACHAT')
			#print(e)
			return None

	@staticmethod
	def toSaveDemandeAchat(auteur,objet_dao_Demande_achat):
		try:
			demande_achat  = Model_Demande_achat()
			demande_achat.numero_demande =objet_dao_Demande_achat.numero_demande
			demande_achat.date_demande =objet_dao_Demande_achat.date_demande
			demande_achat.description =objet_dao_Demande_achat.description
			demande_achat.creation_date = timezone.now()
			demande_achat.auteur_id = auteur.id
			demande_achat.save()
			return demande_achat
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA DEMANDE_ACHAT')
			#print(e)
			return None

	@staticmethod
	def toUpdateDemandeAchat(id, objet_dao_Demande_achat):
		try:
			demande_achat = Model_Demande_achat.objects.get(pk = id)
			demande_achat.numero_demande =objet_dao_Demande_achat.numero_demande
			demande_achat.date_demande =objet_dao_Demande_achat.date_demande
			demande_achat.description =objet_dao_Demande_achat.description
			demande_achat.save()
			return demande_achat
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA DEMANDE_ACHAT')
			#print(e)
			return None
	@staticmethod
	def toGetDemandeAchat(id):
		try:
			return Model_Demande_achat.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteDemandeAchat(id):
		try:
			demande_achat = Model_Demande_achat.objects.get(pk = id)
			demande_achat.delete()
			return True
		except Exception as e:
			return False