from __future__ import unicode_literals
from ErpBackOffice.models import Model_Document
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.conf import settings
import os
from django.core.files.storage import default_storage

from ModuleArchivage.archive import archive
from ModuleArchivage.tasks import *

class dao_document(object):
    id = 0
    type_document = ""
    url_document = ""
    description = ""
    auteur_id = None
    content_type_id = None
    source_document_id = None


    @staticmethod
    def toListDocuments(objet_modele):
        content_type = ContentType.objects.get_for_model(objet_modele)
        return Model_Document.objects.filter(content_type_id = content_type.id, source_document_id = objet_modele.id)

   
    @staticmethod
    def toCreateDocument(type_document, url_document, description, objet_modele):
        try:
            content_type = ContentType.objects.get_for_model(objet_modele)
            document = dao_document()
            document.type_document = type_document
            document.url_document = url_document
            document.content_type_id = content_type.id
            document.source_document_id = objet_modele.id
            document.description = description 
            return document
        except Exception as e:
            print("ERREUR LORS DE LA CREATION DU DOCUMENT")
            print(e)
            return None
			
    @staticmethod
    def toSaveDocument(auteur, objet_dao_document):
        try:
            document = Model_Document()
            document.type_document = objet_dao_document.type_document
            #print('doc type %s'%( document.type_document))
            document.url_document = objet_dao_document.url_document
            #print('doc url_document %s' % (document.url_document))
            document.description = objet_dao_document.description 
            #print('doc description %s' % (document.description))
            document.content_type_id = objet_dao_document.content_type_id
            #print('doc content_type_id %s' % (document.content_type_id))
            document.source_document_id = objet_dao_document.source_document_id
            #print('doc source_document_id %s' % (document.source_document_id))
            document.auteur_id = auteur.id
            document.creation_date = timezone.now()
            document.save()
            return document
        except Exception as e:
            print("ERREUR")
            print(e)
            return None

    @staticmethod
    def toUpdateDocument(id, objet_dao_document):
        try:
            document = Model_Document.objects.get(pk = id)
            document.type_document = objet_dao_document.type_document
            document.url_document = objet_dao_document.url_document
            document.content_type_id = objet_dao_document.content_type_id
            document.source_document_id = objet_dao_document.source_document_id
            document.description = objet_dao_document.description 
            document.save()
            return document
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return None
	
    @staticmethod
    def toGetDocument(id):
        try:
            return Model_Document.objects.get(pk = id)
        except Exception as e:
            return None

    @staticmethod
    def toListDocumentbyObjetModele(objet_modele):
        content_type = ContentType.objects.get_for_model(objet_modele)
        return Model_Document.objects.filter(content_type_id = content_type.id,source_document_id = objet_modele.id)
  
    @staticmethod
    def toDeleteDocument(id):
        try:
            #print('dao id from view')
            document = Model_Document.objects.get(pk = id)
            #print('l id du doc a sup from dao %s'%(document.id))
            document.delete()
           
            return True
        except Exception as e:
            #print('erreur dao doc sup %s'%(e))
            return False
    
    @staticmethod
    def toUploadDocument(auteur, files, objet_modele):
        try:
            base_dir = settings.BASE_DIR
            media_dir = settings.MEDIA_ROOT
            media_url = settings.MEDIA_URL

            docs_dir = 'documents/'
            media_dir = media_dir + '/' + docs_dir
            #print("keols")

            for fichier in files:
                
                print("fichier", fichier)
                nom_fichier = fichier.name
                nom_fichier = nom_fichier[:75]
                print(nom_fichier)
                
                save_path = os.path.join(media_dir, str(nom_fichier))
                path = default_storage.save(save_path, fichier)
                url = media_url + docs_dir + str(nom_fichier)
                print(url)
                #print(bzb)
                document = dao_document.toCreateDocument(str(objet_modele._meta),url,"file downloaded", objet_modele)
                document = dao_document.toSaveDocument(auteur, document)

                #archive.archiver(document, str(nom_fichier),None,None,auteur.id,nom_fichier,None, True)               

            return document
                
        except Exception as e:
            print(e)
            return None
