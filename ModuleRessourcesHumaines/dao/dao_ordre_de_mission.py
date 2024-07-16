from __future__ import unicode_literals
from ErpBackOffice.models import Model_Ordre_de_mission
from django.utils import timezone

class dao_ordre_de_mission(object):
	id = 0
	objet_mission = ''
	destination = ''
	numero_ordre = ''
	ligne_budgetaire_id = None
	moyen_transport = ''
	requete_id = None
	date_depart = '2010-01-01'
	date_retour = '2010-01-01'
	description = ''
	type = ''
	observation = ''
	auteur_id = None

	@staticmethod
	def toListOrdre_de_mission():
		return Model_Ordre_de_mission.objects.all().order_by('-id')

	@staticmethod
	def toListOrdreByUser(user_id):
		return Model_Ordre_de_mission.objects.filter(demandeur=user_id)

	@staticmethod
	def toCreateOrdre_de_mission(objet_mission,destination,moyen_transport,date_depart,date_retour,description,observation, type, requete_id,ligne_budgetaire_id):
		try:
			ordre_de_mission = dao_ordre_de_mission()
			ordre_de_mission.objet_mission = objet_mission
			ordre_de_mission.numero_ordre = dao_ordre_de_mission.toGenerateNumeroOrdre()
			ordre_de_mission.destination = destination
			ordre_de_mission.requete_id = requete_id
			ordre_de_mission.ligne_budgetaire_id = ligne_budgetaire_id
			ordre_de_mission.type = type
			ordre_de_mission.moyen_transport = moyen_transport
			ordre_de_mission.date_depart = date_depart
			ordre_de_mission.date_retour = date_retour
			ordre_de_mission.description = description
			ordre_de_mission.observation = observation
			return ordre_de_mission
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA ORDRE_DE_MISSION')
			#print(e)
			return None

	@staticmethod
	def toSaveOrdre_de_mission(auteur, objet_dao_Ordre_de_mission):
		try:
			ordre_de_mission  = Model_Ordre_de_mission()
			ordre_de_mission.objet_mission = objet_dao_Ordre_de_mission.objet_mission
			ordre_de_mission.destination = objet_dao_Ordre_de_mission.destination
			ordre_de_mission.numero_ordre = objet_dao_Ordre_de_mission.numero_ordre
			ordre_de_mission.moyen_transport = objet_dao_Ordre_de_mission.moyen_transport
			ordre_de_mission.requete_id = objet_dao_Ordre_de_mission.requete_id
			ordre_de_mission.ligne_budgetaire_id = objet_dao_Ordre_de_mission.ligne_budgetaire_id
			ordre_de_mission.type = objet_dao_Ordre_de_mission.type
			ordre_de_mission.date_depart = objet_dao_Ordre_de_mission.date_depart
			ordre_de_mission.date_retour = objet_dao_Ordre_de_mission.date_retour
			ordre_de_mission.description = objet_dao_Ordre_de_mission.description
			ordre_de_mission.observation = objet_dao_Ordre_de_mission.observation
			ordre_de_mission.created_at = timezone.now()
			ordre_de_mission.updated_at = timezone.now()
			ordre_de_mission.auteur_id = auteur.id

			ordre_de_mission.save()
			return ordre_de_mission
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE L\' ORDRE_DE_MISSION')
			#print(e)
			return None

	@staticmethod
	def toUpdateOrdre_de_mission(id, objet_dao_Ordre_de_mission):
		try:
			ordre_de_mission = Model_Ordre_de_mission.objects.get(pk = id)
			ordre_de_mission.objet_mission =objet_dao_Ordre_de_mission.objet_mission
			ordre_de_mission.destination =objet_dao_Ordre_de_mission.destination
			ordre_de_mission.moyen_transport =objet_dao_Ordre_de_mission.moyen_transport
			ordre_de_mission.date_depart =objet_dao_Ordre_de_mission.date_depart
			ordre_de_mission.ligne_budgetaire_id = objet_dao_Ordre_de_mission.ligne_budgetaire_id
			ordre_de_mission.type = objet_dao_Ordre_de_mission.type
			ordre_de_mission.numero_ordre = objet_dao_Ordre_de_mission.numero_ordre
			ordre_de_mission.requete_id = objet_dao_Ordre_de_mission.requete_id
			ordre_de_mission.date_retour =objet_dao_Ordre_de_mission.date_retour
			ordre_de_mission.description =objet_dao_Ordre_de_mission.description
			ordre_de_mission.observation =objet_dao_Ordre_de_mission.observation
			ordre_de_mission.updated_at = timezone.now()
			ordre_de_mission.save()
			return ordre_de_mission
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA ORDRE_DE_MISSION')
			#print(e)
			return None
	@staticmethod
	def toGetOrdre_de_mission(id):
		try:
			return Model_Ordre_de_mission.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toGetOrdre_de_missionByType(type_id):
		try:
			return Model_Ordre_de_mission.objects.get(type = type_id)
		except Exception as e:
			return None

	@staticmethod
	def toDeleteOrdre_de_mission(id):
		try:
			ordre_de_mission = Model_Ordre_de_mission.objects.get(pk = id)
			ordre_de_mission.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toGenerateNumeroOrdre():
		total_damandes = dao_ordre_de_mission.toListOrdre_de_mission().count()
		total_damandes = total_damandes + 1
		temp_numero = str(total_damandes)

		for i in range(len(str(total_damandes)), 4):
			temp_numero = "0" + temp_numero

		mois = timezone.now().month
		if mois < 10: mois = "0%s" % mois

		annee = int(timezone.now().year)- 2000

		#temp_numero = "EXPM%s%s%s" % (timezone.now().year, mois, temp_numero)
		temp_numero = "{}/ARPCE-DG/DAFC/SRHD/{}".format(temp_numero,annee)
		return temp_numero
