from __future__ import unicode_literals
from ErpBackOffice.models import Model_Requete_competence
from django.utils import timezone

class dao_requete_competence(object):
	id = 0
	numero_requete = ''
	competence = ''
	observation = ''
	employe_id = None

	@staticmethod
	def toListRequete_competence():
		return Model_Requete_competence.objects.all().order_by('-id')

	@staticmethod
	def toCreateRequete_competence(numero_requete,competence,observation,employe_id):
		try:
			requete_competence = dao_requete_competence()
			requete_competence.numero_requete = numero_requete
			requete_competence.competence = competence
			requete_competence.observation = observation
			requete_competence.employe_id = employe_id
			return requete_competence
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA REQUETE_COMPETENCE')
			#print(e)
			return None

	@staticmethod
	def toSaveRequete_competence(auteur, objet_dao_Requete_competence):
		try:
			requete_competence  = Model_Requete_competence()
			requete_competence.numero_requete = objet_dao_Requete_competence.numero_requete
			requete_competence.competence = objet_dao_Requete_competence.competence
			requete_competence.observation = objet_dao_Requete_competence.observation
			requete_competence.employe_id = objet_dao_Requete_competence.employe_id
			requete_competence.created_at = timezone.now()
			requete_competence.updated_at = timezone.now()
			requete_competence.auteur_id = auteur.id

			requete_competence.save()
			return requete_competence
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA REQUETE_COMPETENCE')
			#print(e)
			return None

	@staticmethod
	def toUpdateRequete_competence(id, objet_dao_Requete_competence):
		try:
			requete_competence = Model_Requete_competence.objects.get(pk = id)
			requete_competence.numero_requete =objet_dao_Requete_competence.numero_requete
			requete_competence.competence =objet_dao_Requete_competence.competence
			requete_competence.observation =objet_dao_Requete_competence.observation
			requete_competence.employe_id =objet_dao_Requete_competence.employe_id
			requete_competence.updated_at = timezone.now()
			requete_competence.save()
			return requete_competence
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA REQUETE_COMPETENCE')
			#print(e)
			return None
	@staticmethod
	def toGetRequete_competence(id):
		try:
			return Model_Requete_competence.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteRequete_competence(id):
		try:
			requete_competence = Model_Requete_competence.objects.get(pk = id)
			requete_competence.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toGenerateNumeroRequete():
		total_requetes = dao_requete_competence.toListRequete_competence().count()
		total_requetes = total_requetes + 1
		temp_numero = str(total_requetes)

		for i in range(len(str(total_requetes)), 4):
			temp_numero = "0" + temp_numero

		mois = timezone.now().month
		if mois < 10: mois = "0%s" % mois

		temp_numero = "RQCMP-%s%s%s" % (timezone.now().year, mois, temp_numero)
		return temp_numero