from __future__ import unicode_literals
from ErpBackOffice.models import Model_ClassificationProfessionelle
from django.utils import timezone


class dao_classification_professionnelle(object):
    id = 0
    designation = ''
    code = ""
    numero_reference = ""
    description = ''


    @staticmethod
    def toListClassificationProfessionnelle():
        return Model_ClassificationProfessionelle.objects.all().order_by('-id')

    @staticmethod
    def toCreateClassificationProfessionnelle(designation,code, numero_reference, description):
        try:
            classification_professionnelle = dao_classification_professionnelle()
            classification_professionnelle.designation = designation
            classification_professionnelle.code = code
            classification_professionnelle.numero_reference = numero_reference
            classification_professionnelle.description = description
            return classification_professionnelle
        except Exception as e:
            # print("ERREUR CREATION OBJET COMPTE", e)
            return None


    @staticmethod
    def toSaveClassificationProfessionnelle(auteur, objet_dao_Banque):
        try:
            classification_professionnelle  = Model_ClassificationProfessionelle()
            classification_professionnelle.designation = objet_dao_Banque.designation
            classification_professionnelle.code = objet_dao_Banque.code
            classification_professionnelle.numero_reference = objet_dao_Banque.numero_reference
            classification_professionnelle.description = objet_dao_Banque.description
            classification_professionnelle.created_at = timezone.now()
            classification_professionnelle.updated_at = timezone.now()
            classification_professionnelle.auteur_id = auteur.id
            classification_professionnelle.save()
            # #print("CREATION TO SAVE COMPTE", banque)
            return classification_professionnelle
        except Exception as e:
            # print("ERREUR TO SAVE COMPTE", e)
            return None

    @staticmethod
    def toUpdateClassificationProfessionnelle(id, objet_dao_Banque):
        try:
            classification_professionnelle = Model_ClassificationProfessionelle.objects.get(pk = id)
            classification_professionnelle.designation = objet_dao_Banque.designation
            classification_professionnelle.code = objet_dao_Banque.code
            classification_professionnelle.numero_reference = objet_dao_Banque.numero_reference
            classification_professionnelle.description = objet_dao_Banque.description
            classification_professionnelle.updated_at = timezone.now()
            classification_professionnelle.auteur_id = auteur.id
            classification_professionnelle.save()
            return banque
        except Exception as e:
            return None


    @staticmethod
    def toGetClassificationProfessionnelle(id):
        try:
            return Model_ClassificationProfessionelle.objects.get(pk = id)
        except Exception as e:
            return None

    @staticmethod
    def toDeleteClassificationProfessionnelle(id):
        try:
            classification_professionnelle = Model_ClassificationProfessionelle.objects.get(pk = id)
            classification_professionnelle.delete()
            return True
        except Exception as e:
            return False


    @staticmethod
    def toGetOrCreateClassificationProfessionnelle(auteur, designation):
        try:
            # print('CLASSIFICATION SEND', designation)
            classification_professionnelle = Model_ClassificationProfessionelle.objects.filter(designation__icontains = designation).first()
            # print('CLASSIFICATION PRO', classification_professionnelle)
            if classification_professionnelle == None:
                classification = dao_classification_professionnelle()
                classification_professionnelle = classification.toCreateClassificationProfessionnelle(designation, "", None, "")
                classification_professionnelle = classification.toSaveClassificationProfessionnelle(auteur, classification_professionnelle)
                # print('CLASSIFICATION PRO', classification_professionnelle)
            return classification_professionnelle
        except Exception as e:
            # print("erreur on toGetOrCreateClassificationProfessionnelle", e)
            return None

