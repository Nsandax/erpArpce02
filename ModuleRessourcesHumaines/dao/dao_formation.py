from __future__ import unicode_literals
from ErpBackOffice.models import Model_Formation
from django.utils import timezone
from django.db.models.functions import TruncMonth
from django.db.models import Count
from locale import atof, setlocale, LC_NUMERIC

class dao_formation(object):
	id = 0
	departement = ''
	theme = ''
	objectif = ''
	public_cible = ''
	annee = 0
	nombre_jour_formation = 0
	type = ''
	organisme_formation = ''
	localite_organisme = ''
	nombre_heure_par_jour = ''
	cout_formation = 0.0
	nombre_participant_par_jour = 0
	frais_mission_hebergement = 0.0
	frais_deplacement_ht = 0.0
	priorite = ''
	date_debut = '2010-01-01'
	date_fin = '2010-01-01'
	etat = ""

	cout_formation_effective = 0
	frais_mission_hebergement_effective = 0
	frais_deplacement_ht_effective = 0
	nombre_participant_par_jour_effective = 0


	@staticmethod
	def toListFormation():
		return Model_Formation.objects.all().order_by('-id')

	@staticmethod
	def toListFormationByAuteur(user_id):
		return Model_Formation.objects.filter(auteur_id=user_id)


	@staticmethod
	def toListFormationByStatus(status):
		return Model_Formation.objects.filter(etat = status)

	@staticmethod
	def toListFormationByStatusByAuteur(status, user_id):
		return Model_Formation.objects.filter(etat = status.filter(auteur_id=user_id))

	@staticmethod
	def toCreateFormation(departement,theme,objectif,public_cible,annee,nombre_jour_formation,type,organisme_formation,localite_organisme,nombre_heure_par_jour,cout_formation,nombre_participant_par_jour,frais_mission_hebergement,frais_deplacement_ht,priorite, date_debut, date_fin, etat=""):
		try:
			formation = dao_formation()
			formation.departement = departement
			formation.theme = theme
			formation.objectif = objectif
			formation.public_cible = public_cible
			formation.annee = annee
			formation.nombre_jour_formation = nombre_jour_formation
			formation.type = type
			formation.organisme_formation = organisme_formation
			formation.localite_organisme = localite_organisme
			formation.nombre_heure_par_jour = nombre_heure_par_jour
			formation.cout_formation = cout_formation
			formation.nombre_participant_par_jour = nombre_participant_par_jour
			formation.frais_mission_hebergement = frais_mission_hebergement
			formation.frais_deplacement_ht =frais_deplacement_ht
			formation.priorite = priorite
			formation.date_debut = date_debut
			formation.date_fin = date_fin
			formation.etat = etat
			return formation
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA FORMATION')
			#print(e)
			return None

	@staticmethod
	def toSaveFormation(auteur, objet_dao_Formation):
		try:
			formation  = Model_Formation()
			formation.departement = objet_dao_Formation.departement
			formation.theme = objet_dao_Formation.theme
			formation.objectif = objet_dao_Formation.objectif
			formation.public_cible = objet_dao_Formation.public_cible
			formation.annee = objet_dao_Formation.annee
			formation.nombre_jour_formation = objet_dao_Formation.nombre_jour_formation
			formation.type = objet_dao_Formation.type
			formation.organisme_formation = objet_dao_Formation.organisme_formation
			formation.localite_organisme = objet_dao_Formation.localite_organisme
			formation.nombre_heure_par_jour = objet_dao_Formation.nombre_heure_par_jour
			formation.cout_formation = objet_dao_Formation.cout_formation
			formation.nombre_participant_par_jour = objet_dao_Formation.nombre_participant_par_jour
			formation.frais_mission_hebergement = objet_dao_Formation.frais_mission_hebergement
			formation.frais_deplacement_ht = objet_dao_Formation.frais_deplacement_ht
			formation.priorite = objet_dao_Formation.priorite
			formation.date_debut = objet_dao_Formation.date_debut
			formation.date_fin = objet_dao_Formation.date_fin
			formation.etat = objet_dao_Formation.etat
			formation.created_at = timezone.now()
			formation.updated_at = timezone.now()
			formation.auteur_id = auteur.id

			formation.save()
			return formation
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA FORMATION')
			#print(e)
			return None

	@staticmethod
	def toUpdateFormation(id, objet_dao_Formation):
		try:
			formation = Model_Formation.objects.get(pk = id)
			formation.departement =objet_dao_Formation.departement
			formation.theme =objet_dao_Formation.theme
			formation.objectif =objet_dao_Formation.objectif
			formation.public_cible =objet_dao_Formation.public_cible
			formation.annee =objet_dao_Formation.annee
			formation.nombre_jour_formation =objet_dao_Formation.nombre_jour_formation
			formation.type =objet_dao_Formation.type
			formation.organisme_formation =objet_dao_Formation.organisme_formation
			formation.localite_organisme =objet_dao_Formation.localite_organisme
			formation.nombre_heure_par_jour =objet_dao_Formation.nombre_heure_par_jour
			formation.cout_formation =objet_dao_Formation.cout_formation
			formation.nombre_participant_par_jour =objet_dao_Formation.nombre_participant_par_jour
			formation.frais_mission_hebergement =objet_dao_Formation.frais_mission_hebergement
			formation.frais_deplacement_ht =objet_dao_Formation.frais_deplacement_ht
			formation.priorite =objet_dao_Formation.priorite
			formation.date_debut = objet_dao_Formation.date_debut
			formation.date_fin = objet_dao_Formation.date_fin
			formation.updated_at = timezone.now()
			formation.save()
			return formation
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA FORMATION')
			#print(e)
			return None


	@staticmethod
	def toUpdateStatusFormation(id, etat):
		try:
			formation = Model_Formation.objects.get(pk = id)
			formation.etat = etat
			formation.updated_at = timezone.now()
			formation.save()
			return formation
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA FORMATION')
			#print(e)
			return None


	@staticmethod
	def toRealiseFormation(id, cout_formation_effective,frais_mission_hebergement_effective,frais_deplacement_ht_effective,nombre_participant_par_jour_effective, etat=""):
		try:
			formation = Model_Formation.objects.get(pk = id)
			formation.theme=formation.theme
			formation.cout_formation_effective = cout_formation_effective
			formation.frais_deplacement_ht_effective = frais_deplacement_ht_effective
			formation.frais_mission_hebergement_effective = frais_mission_hebergement_effective
			formation.nombre_participant_par_jour_effective = nombre_participant_par_jour_effective
			formation.etat = etat
			formation.updated_at = timezone.now()
			formation.save()
			return formation
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA FORMATION')
			#print(e)
			return None


	@staticmethod
	def toGetFormation(id):
		try:
			return Model_Formation.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toGetformationById(id):
		try:
			return Model_Formation.objects.get(id = id)
		except Exception as e:
			return None

	@staticmethod
	def toDeleteFormation(id):
		try:
			formation = Model_Formation.objects.get(pk = id)
			formation.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toGetFormationByMounth():
		try:
			today = timezone.now().year
			#print('ANNEE ACTUELLE POUR FORMATION %s' %today)
			Listeformation = Model_Formation.objects.annotate(month=TruncMonth('date_debut')).values('month').annotate(total=Count('departement')).filter(annee = today)
			TableauFormation = [0,0,0,0,0,0,0,0,0,0,0,0]
			#print('Liste des Formation BD %s' %Listeformation)
			for item in Listeformation:
				if item["month"].month == 1:

					if item["total"] == 0:
						TableauFormation[0] = 0
					else:
						TableauFormation[0] = item["total"]
					continue
				elif item["month"].month == 2:
					if item["total"] == 0 :
						TableauFormation[1] = 0
					else:
						TableauFormation[1] = item["total"]
					continue
				elif item["month"].month == 3:
					if item["total"] == 0:
						TableauFormation[2] = 0
					else:
						TableauFormation[2] = item["total"]
					continue
				elif item["month"].month == 4:
					if item["total"] == 0:
						TableauFormation[3] = 0
					else:
						TableauFormation[3] = item["total"]
					continue
				elif item["month"].month == 5:
					if item["total"] == 0:
						TableauFormation[4] = 0
					else:
						TableauFormation[4] = item["total"]
					continue
				elif item["month"].month == 6:
					if item["total"] == 0:
						TableauFormation[5] = 0
					else:
						TableauFormation[5] = item["total"]
					continue
				elif item["month"].month == 7:
					if item["total"] == 0:
						TableauFormation[6] = 0
					else:
						TableauFormation[6] = item["total"]
					continue
				elif item["month"].month == 8:
					if item["total"] == 0:
						TableauFormation[7] = 0
					else:
						TableauFormation[7] = item["total"]
					continue
				elif item["month"].month == 9:
					if item["month"] == 0:
						TableauFormation[8] = 0
					else:
						TableauFormation[8] = item["total"]
					continue
				elif item["month"].month == 10:
					if item["month"] == 0:
						TableauFormation[9] = 0
					else:
						TableauFormation[9] = item["total"]
					continue
				elif item["month"].month == 11:
					if item["month"] == 0:
						TableauFormation[10] = 0
					else:
						TableauFormation[10] = item["total"]
					continue
				elif item["month"].month == 12:
					if item["month"] == 0:
						TableauFormation[11] = 0
					else:
						TableauFormation[11] = item["total"]
					continue
				else:
					pass
			#print('Liste des formations %s' %TableauFormation)
			return TableauFormation
		except Exception as e:
			#print("ERREER LISTEFORMATION BY MONTH")
			#print(e)
			pass
