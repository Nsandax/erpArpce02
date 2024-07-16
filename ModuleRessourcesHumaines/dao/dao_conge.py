from __future__ import unicode_literals
from ErpBackOffice.models import Model_Conge
from django.utils import timezone
from django.db.models.functions import TruncMonth 
from django.db.models import Count

class dao_conge(object):
	id = 0
	description = ''
	etat = ''
	employe_id = None
	user_id = None
	date_from = '2010-01-01'
	date_to = '2010-01-01'
	type_conge_id = None
	type = ''
	nombre_jour = 0
	nombre_jour_temp = 0
	observation = ''

	@staticmethod
	def toListConge():
		return Model_Conge.objects.all().order_by('-id')
	@staticmethod
	def toListCongeofType(type_conge_id):
		return Model_Conge.objects.filter(type_conge_id = type_conge_id)
	@staticmethod
	def toListCongeInitie():
		return Model_Conge.objects.filter(etat = "initié")
	@staticmethod
	def toListCongeApprouve():
		return Model_Conge.objects.filter(etat = "Demande de congé validée")
	@staticmethod
	def toListCongeRejete():
		return Model_Conge.objects.filter(etat = "Demande de congé réfusé")

	@staticmethod
	def ListeNumberCongeByMunth():
		try:

			today = timezone.now().year
			ListeQuery =Model_Conge.objects.annotate(month=TruncMonth('date_from')).values('month').annotate(total=Count('numero_conge')).filter(date_from__year = today)
			# #print('Liste des Conge BD %s' %ListeQuery)
			ListConge = [0,0,0,0,0,0,0,0,0,0,0,0]
			ListeCongoBD = [{'x':0,'y':1},{'x':0,'y':2},{'x':0,'y':3},{'x':0,'y':4},{'x':0,'y':5},{'x':0,'y':6},{'x':0,'y':7},{'x':0,'y':8},{'x':0,'y':9},{'x':0,'y':10},{'x':0,'y':11},{'x':0,'y':12}]
			for item in ListeQuery:

				if item["month"].month==1:
					if item["total"] == 0:
							ListConge[0] = 0
					else:
							ListConge[0] = item["total"]
					continue
				if item["month"].month==2:
					if item["total"] == 0:
							ListConge[1] = 0
					else:
							ListConge[1] = item["total"]
					continue
				elif item["month"].month == 3:
					if item["total"] == 0:
							ListConge[2] = 0
					else:
							ListConge[2] = item["total"]
					continue
				elif item["month"].month == 4:
					if item["total"] == 0:
							ListConge[3] = 0
					else:
							ListConge[3] == item["total"]
					continue
				elif item["month"].month == 5:
					if item["total"] == 0:
							ListConge[4] = 0
					else:
							ListConge[4] = item["total"]
					continue
				elif item["month"].month == 6:
					if item["total"] == 0:
							ListConge[5] = 0
					else:
							ListConge[5] = item["total"]
					continue
				elif item["month"].month == 7:
					if item["total"] == 0:
							ListConge[6] = 0
					else:
							ListConge[6] = item["total"]
					continue
				elif item["month"].month == 8:
					if item["total"] == 0:
						ListConge[7] = 0
					else:
							ListConge[7] = item["total"]
					continue
				elif item["month"].month == 9:
					if item["total"] == 0:
							ListConge[8] = 0
					else:
							ListConge[8] = item["total"]
					continue
				elif item["month"].month == 10:
					if item["total"] == 0:
							ListConge[9] = 0
					else:
							ListConge[9] = item["total"]
					continue
				elif item["month"].month == 11:
					if item["total"] == 0:
							ListConge[10] = 0
					else:
							ListConge[10] = item["total"]
					continue
				elif item["month"].month == 12:
					if item["total"] == 0:
							ListConge[11] = 0
					else:
							ListConge[11] = item["total"]
					continue
				else:
					pass
			# #print('Liste des CONGE %s' %ListConge)
			# #print('Liste des CONGE %s' %ListeQuery)
			for item in ListeQuery:
				#print('yes')
				if item["month"].month==1:
					x = 0
					if item["total"] == 0:
							x = 0
					else:
							x = item["total"]

					datatampon = {"x": item["month"].month,'y' : x}
					ListeCongoBD.pop(0)
					ListeCongoBD.insert(0,datatampon)
					continue
				if item["month"].month==2:
					x = 0
					if item["total"] == 0:
							x = 0
					else:
							x = item["total"]

					datatampon = {"x": item["month"].month,'y' : x}
					ListeCongoBD.pop(1)
					ListeCongoBD.insert(1,datatampon)
					continue
				elif item["month"].month == 3:
					if item["total"] == 0:
							x = 0
					else:
							x = item["total"]

					datatampon = {"x": item["month"].month,'y' : x}
					ListeCongoBD.pop(2)
					ListeCongoBD.insert(2,datatampon)
					continue
				elif item["month"].month == 4:
					if item["total"] == 0:
							x = 0
					else:
							x = item["total"]

					datatampon = {"x": item["month"].month,'y' : x}
					ListeCongoBD.pop(3)
					ListeCongoBD.insert(3,datatampon)
					continue
				elif item["month"].month == 5:
					if item["total"] == 0:
							x = 0
					else:
							x = item["total"]

					datatampon = {"x": item["month"].month,'y' : x}
					ListeCongoBD.pop(4)
					ListeCongoBD.insert(4,datatampon)
					continue
				elif item["month"].month == 6:
					if item["total"] == 0:
							x = 0
					else:
							x = item["total"]

					datatampon = {"x": item["month"].month,'y' : x}
					ListeCongoBD.pop(5)
					ListeCongoBD.insert(5,datatampon)
					continue
				elif item["month"].month == 7:
					if item["total"] == 0:
							x = 0
					else:
							x = item["total"]

					datatampon = {"x": item["month"].month,'y' : x}
					ListeCongoBD.pop(6)
					ListeCongoBD.insert(6,datatampon)
					continue
				elif item["month"].month == 8:
					if item["total"] == 0:
							x = 0
					else:
							x = item["total"]

					datatampon = {"x": item["month"].month,'y' : x}
					ListeCongoBD.pop(7)
					ListeCongoBD.insert(7,datatampon)
					continue
				elif item["month"].month == 9:
					if item["total"] == 0:
							x = 0
					else:
							x = item["total"]

					datatampon = {"x": item["month"].month,'y' : x}
					ListeCongoBD.pop(8)
					ListeCongoBD.insert(8,datatampon)
					continue
				elif item["month"].month == 10:
					if item["total"] == 0:
							x = 0
					else:
							x = item["total"]

					datatampon = {"x": item["month"].month,'y' : x}
					ListeCongoBD.pop(9)
					ListeCongoBD.insert(9,datatampon)
					continue
				elif item["month"].month == 11:
					if item["total"] == 0:
							x = 0
					else:
							x = item["total"]

					datatampon = {"x": item["month"].month,'y' : x}
					ListeCongoBD.pop(10)
					ListeCongoBD.insert(10,datatampon)
					continue
				elif item["month"].month == 12:
					if item["total"] == 0:
							x = 0
					else:
							x = item["total"]

					datatampon = {"x": item["month"].month,'y' : x}
					ListeCongoBD.pop(11)
					ListeCongoBD.insert(11,datatampon)
					continue
				else:
					pass

			# for item in ListeQuery:
			# 	x = 0
			# 	if item["total"] == 0:
			# 		x = 0
			# 	else:
			# 		x = item["total"]

			# 	datatampon = {"x": item["month"].month,'y' : x}
			# 	ListeCongoBD.append(datatampon)
			#
			# #print('Liste des CONGE %s' %ListeCongoBD)
			return ListConge, ListeCongoBD
		except Exception as e:
			#print("ERRER LISTECONGE BY MONTH")
			#print(e)
			pass


	@staticmethod
	def toListCongeApayer():
		result_list = []
		conges = Model_Conge.objects.filter(etat = "accordé")
		for item in conges :
			if item.allocation_paye == False :
				result_list.append(item)
		return result_list

	@staticmethod
	def toCreateConge(description,numero_conge,employe_id,user_id,date_from,date_to,type_conge_id,type,nombre_jour,nombre_jour_temp,observation):
		try:
			conge = dao_conge()
			conge.description = description
			conge.numero_conge = numero_conge
			conge.employe_id = employe_id
			conge.user_id = user_id
			conge.date_from = date_from
			conge.date_to = date_to
			conge.type_conge_id = type_conge_id
			conge.type = type
			conge.nombre_jour = nombre_jour
			conge.nombre_jour_temp = nombre_jour_temp
			conge.observation = observation
			return conge
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA CONGE')
			#print(e)
			return None


	@staticmethod
	def toSaveConge(auteur, objet_dao_Conge):
		try:
			conge  = Model_Conge()
			conge.description = objet_dao_Conge.description
			conge.numero_conge = objet_dao_Conge.numero_conge
			conge.employe_id = objet_dao_Conge.employe_id
			conge.user_id = objet_dao_Conge.user_id
			conge.date_from = objet_dao_Conge.date_from
			conge.date_to = objet_dao_Conge.date_to
			conge.type_conge_id = objet_dao_Conge.type_conge_id
			conge.type = objet_dao_Conge.type
			conge.nombre_jour = objet_dao_Conge.nombre_jour
			conge.nombre_jour_temp = objet_dao_Conge.nombre_jour_temp
			conge.observation = objet_dao_Conge.observation
			conge.created_at = timezone.now()
			conge.updated_at = timezone.now()
			conge.auteur_id = auteur.id

			conge.save()
			return conge
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA CONGE')
			#print(e)
			return None

	@staticmethod
	def toUpdateConge(id, objet_dao_Conge):
		try:
			conge = Model_Conge.objects.get(pk = id)
			conge.description =objet_dao_Conge.description
			conge.numero_conge =objet_dao_Conge.numero_conge
			conge.employe_id =objet_dao_Conge.employe_id
			conge.user_id =objet_dao_Conge.user_id
			conge.date_from =objet_dao_Conge.date_from
			conge.date_to =objet_dao_Conge.date_to
			conge.type_conge_id =objet_dao_Conge.type_conge_id
			conge.type =objet_dao_Conge.type
			conge.nombre_jour =objet_dao_Conge.nombre_jour
			conge.nombre_jour_temp =objet_dao_Conge.nombre_jour_temp
			conge.observation =objet_dao_Conge.observation
			conge.updated_at = timezone.now()
			conge.save()
			return conge
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA CONGE')
			#print(e)
			return None
	@staticmethod
	def toGetConge(id):
		try:
			return Model_Conge.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteConge(id):
		try:
			conge = Model_Conge.objects.get(pk = id)
			conge.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toGenerateNumeroDemandeConge():
		total_demande = dao_conge.toListConge().count()
		total_demande = total_demande + 1
		temp_numero = str(total_demande)

		for i in range(len(str(total_demande)), 4):
			temp_numero = "0" + temp_numero

		mois = timezone.now().month
		if mois < 10: mois = "0%s" % mois

		temp_numero = "DEM-%s%s%s" % (timezone.now().year, mois, temp_numero)
		return temp_numero


