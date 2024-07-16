from __future__ import unicode_literals
from ErpBackOffice.models import Model_Document, Model_Dossier
from django.utils import timezone
from django.core.files.storage import default_storage
from django.utils import timezone
from django.db.models.functions import TruncMonth
from django.db.models import Count

class dao_document(object):
	id = 0
	type_document = ''
	url_document = ''
	numero_document = ''
	description = ''
	est_verifie = False
	status = ''
	metadonnees = ''
	dossier_id = None

	@staticmethod
	def toListDocument():
		return Model_Document.objects.all().order_by('-id')
	@staticmethod
	def toListDocumentWithoutDossier():
		return Model_Document.objects.all().exclude(dossier__isnull=False)
	@staticmethod
	def toListDocumentLinkedInRoot():
		return Model_Document.objects.filter(dossier__id=2)

	@staticmethod
	def toCreateDocument(type_document,url_document,numero_document,description,est_verifie,status,metadonnees,dossier_id):
		try:
			document = dao_document()
			document.type_document = type_document
			document.url_document = url_document
			document.numero_document = numero_document
			document.description = description
			document.est_verifie = est_verifie
			document.status = status
			document.metadonnees = metadonnees
			document.dossier_id = dossier_id
			return document
		except Exception as e:
			print('ERREUR LORS DE LA CREATION DE LA DOCUMENT')
			print(e)
			return None

	@staticmethod
	def toSaveDocument(auteur_id, objet_dao_Document):
		try:
			document  = Model_Document()
			document.type_document = objet_dao_Document.type_document
			document.url_document = objet_dao_Document.url_document
			document.numero_document = objet_dao_Document.numero_document
			document.description = objet_dao_Document.description
			document.est_verifie = objet_dao_Document.est_verifie
			document.status = objet_dao_Document.status
			document.metadonnees = objet_dao_Document.metadonnees
			document.dossier_id = objet_dao_Document.dossier_id
			document.created_at = timezone.now()
			document.updated_at = timezone.now()
			document.auteur_id = auteur_id

			document.save()
			return document
		except Exception as e:
			print('ERREUR LORS DE L ENREGISTREMENT DE LA DOCUMENT')
			print(e)
			return None

	@staticmethod
	def toUpdateDocument(id, objet_dao_Document):
		try:
			document = Model_Document.objects.get(pk = id)
			document.type_document =objet_dao_Document.type_document
			document.url_document =objet_dao_Document.url_document
			document.numero_document =objet_dao_Document.numero_document
			document.description =objet_dao_Document.description
			document.est_verifie =objet_dao_Document.est_verifie
			document.status =objet_dao_Document.status
			document.metadonnees =objet_dao_Document.metadonnees
			document.dossier_id =objet_dao_Document.dossier_id
			document.updated_at = timezone.now()
			document.save()
			return document
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA DOCUMENT')
			#print(e)
			return None
	@staticmethod
	def toGetDocument(id):
		try:
			return Model_Document.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteDocument(id):
		try:
			document = Model_Document.objects.get(pk = id)
			document.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toUploadDocument(id, dossier_id, file):
		try:
			document = Model_Document.objects.get(pk = id)
			dossier = Model_Dossier.objects.get(pk = dossier_id)
			extension = file.split('.')
			file_dir = dossier.url_dossier + "\\fichier {0}".format(document.numero_document) + "."+extension
			path = default_storage.save(file_dir, file)
			document.url_document = file_dir
			document.save()
			return True
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA DOCUMENT')
			#print(e)
			return False

	@staticmethod
	def ListeNumberofDoc(today=timezone.now().year):
		try:
			#print(' ListeNumberofDirectories')

			listeDoc = Model_Document.objects.annotate(month=TruncMonth('created_at')).values(
				'month').annotate(total=Count('url_document')).filter(created_at__year=today)

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
			#print('Liste des document %s' % ListDemande)
			return ListDemande
		except Exception as e:
			#print("ERRER LISTECONGE BY MONTH")
			#print(e)
			pass
