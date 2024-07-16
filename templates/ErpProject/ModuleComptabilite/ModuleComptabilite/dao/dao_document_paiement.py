from __future__ import unicode_literals
from ErpBackOffice.models import Model_Document
from django.utils import timezone

class dao_document_paiement(object):
    id = 0
    type_document = ""
    url_document = ""
    paiement_id = None
    description = ""
    auteur_id = None

    @staticmethod
    def toListDocuments():
        return Model_Document.objects.all().order_by('-id')


    @staticmethod
    def toCreateDocument(type_document, url_document, description, paiement_id = None):
        try:
            document = dao_document_paiement()
            document.type_document = type_document
            document.url_document = url_document
            document.paiement_id = paiement_id
            document.description = description
            return document
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DU DOCUMENT")
            #print(e)
            return None

    @staticmethod
    def toSaveDocument(auteur, objet_dao_document):
        try:
            document = Model_Document()
            document.type_document = objet_dao_document.type_document
            document.url_document = objet_dao_document.url_document
            document.paiement_id = objet_dao_document.paiement_id
            document.description = objet_dao_document.description
            document.auteur_id = auteur.id
            document.creation_date = timezone.now()
            document.save()
            return document
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return None

    @staticmethod
    def toUpdateDocument(id, objet_dao_document):
        try:
            document = Model_Document.objects.get(pk = id)
            document.type_document = objet_dao_document.type_document
            document.url_document = objet_dao_document.url_document
            document.paiement_id = objet_dao_document.paiement_id
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
    def toListDocumentbyPaiement(id):
        return Model_Document.objects.filter(paiement_id = id)

    @staticmethod
    def toDeleteDocument(id):
        try:
            document = Model_Document.objects.get(pk = id)
            document.delete()
            return True
        except Exception as e:
            return False
