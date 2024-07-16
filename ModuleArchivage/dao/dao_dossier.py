from __future__ import unicode_literals
from ErpBackOffice.models import Model_Dossier
from django.utils import timezone
import os.path
from django.utils import timezone
from django.db.models.functions import TruncMonth
from django.db.models import Count

class dao_dossier(object):
	id = 0
	designation = ''
	description = ''
	url_dossier = ""
	dossier_id = None

	@staticmethod 
	def toListDossier():
		return Model_Dossier.objects.all()#.order_by('-id')

	@staticmethod 
	def toListDossierChildbyId(id):
		try:
			return Model_Dossier.objects.get(pk=id)#.order_by('-id')
		except Exception as e:
			#print('VALEUR ',e)
			return None

	@staticmethod 
	def toListDossier_childRoot():
		return Model_Dossier.objects.filter(dossier__id=2)

	@staticmethod
	def toCreateDossier(designation,description,dossier_id):
		try:
			dossier = dao_dossier()
			dossier.designation = designation
			dossier.description = description
			dossier.dossier_id = dossier_id
			return dossier
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA DOSSIER')
			#print(e)
			return None

	@staticmethod
	def toSaveDossier(auteur, objet_dao_Dossier):
		try:
			dossier  = Model_Dossier()
			dossier.designation = objet_dao_Dossier.designation
			dossier.description = objet_dao_Dossier.description
			dossier.dossier_id = objet_dao_Dossier.dossier_id
			dossier.created_at = timezone.now()
			dossier.updated_at = timezone.now()
			dossier.auteur_id = auteur.id
			dossier.save()
			#undossier = dao_dossier()
			#undossier.toUpdateUrl(dossier.id, dossier.dossier_id)
			return dossier
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA DOSSIER')
			#print(e)
			return None

	@staticmethod
	def toUpdateDossier(id, objet_dao_Dossier):
		try:
			dossier = Model_Dossier.objects.get(pk = id)
			dossier.designation =objet_dao_Dossier.designation
			dossier.description =objet_dao_Dossier.description
			dossier.dossier_id =objet_dao_Dossier.dossier_id
			dossier.updated_at = timezone.now()
			dossier.save()
			return dossier
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA DOSSIER')
			#print(e)
			return None
	@staticmethod
	def toGetDossier(id):
		try:
			return Model_Dossier.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteDossier(id):
		try:
			dossier = Model_Dossier.objects.get(pk = id)
			dossier.delete()
			return True
		except Exception as e:
			return False
	@staticmethod
	def toUpdateUrl(id, dossier_id):
		try:
			dossier = Model_Dossier.objects.get(pk = id)
			if dossier_id == None:
				dossier.url_dossier = "\\FILES\\{0}".format(dossier.designation.lower())
			else:
				dossier2 = Model_Dossier.objects.get(pk = dossier_id)
				dossier.url_dossier = dossier2.url_dossier + "\\{0}".format(dossier.designation.lower())
			dossier.save()
			path = os.path.abspath(os.path.curdir)
			path = path + dossier.url_dossier
			os.makedirs(path)
			return True
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA DOSSIER')
			#print(e)
			return False
	@staticmethod
	def ListeNumberofDirectories(today = timezone.now().year):
		try:
			#print(' ListeNumberofDirectories')

			listeDoc = Model_Dossier.objects.annotate(month=TruncMonth('created_at')).values(
				'month').annotate(total=Count('designation')).filter(created_at__year=today)

			ListDemande = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
			for item in listeDoc:
    				#print('yes')
    				if item["month"].month == 1:
    						if item["total"] == 0:
    								ListDemande[0] = 0
    						else:
    								ListDemande[0] = item["total"]
    						continue
    				if item["month"].month == 2:
    						if item["total"] == 0:
    								ListDemande[1] = 0
    						else:
    								ListDemande[1] = item["total"]
    						continue
    				elif item["month"].month == 3:
    						if item["total"] == 0:
    								ListDemande[2] = 0
    						else:
    								ListDemande[2] = item["total"]
    						continue
    				elif item["month"].month == 4:
    						if item["total"] == 0:
    								ListDemande[3] = 0
    						else:
    								ListDemande[3] == item["total"]
    						continue
    				elif item["month"].month == 5:
    						if item["total"] == 0:
    								ListDemande[4] = 0
    						else:
    								ListDemande[4] = item["total"]
    						continue
    				elif item["month"].month == 6:
    						if item["total"] == 0:
    								ListDemande[5] = 0
    						else:
    								ListDemande[5] = item["total"]
    						continue
    				elif item["month"].month == 7:
    						if item["total"] == 0:
    								ListDemande[6] = 0
    						else:
    								ListDemande[6] = item["total"]
    						continue
    				elif item["month"].month == 8:
    						if item["total"] == 0:
    								ListDemande[7] = 0
    						else:
    								ListDemande[7] = item["total"]
    						continue
    				elif item["month"].month == 9:
    						if item["total"] == 0:
    								ListDemande[8] = 0
    						else:
    								ListDemande[8] = item["total"]
    						continue
    				elif item["month"].month == 10:
    						if item["total"] == 0:
    								ListDemande[9] = 0
    						else:
    								ListDemande[9] = item["total"]
    						continue
    				elif item["month"].month == 11:
    						if item["total"] == 0:
    								ListDemande[10] = 0
    						else:
    								ListDemande[10] = item["total"]
    						continue
    				elif item["month"].month == 12:
    						if item["total"] == 0:
    								ListDemande[11] = 0
    						else:
    								ListDemande[11] = item["total"]
    						continue
    				else:
    						pass
			#print('Liste des dossier %s' %ListDemande)
			return ListDemande
		except Exception as e:
			#print("ERRER LISTECONGE BY MONTH")
			#print(e)
			pass
