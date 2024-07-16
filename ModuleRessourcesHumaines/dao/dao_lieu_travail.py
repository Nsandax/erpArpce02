from __future__ import unicode_literals
from ErpBackOffice.models import Model_LieuTravail
from django.utils import timezone


class dao_lieu_travail(object):
    designation = ''
    description = ''

    @staticmethod
    def toListLieuTravail():
        return Model_LieuTravail.objects.all().order_by('-id')

    @staticmethod
    def toCreateLieuTravail(designation,description):
        try:
            lieu = dao_lieu_travail()
            lieu.designation = designation
            lieu.description = description
            return lieu
        except Exception as e:
            # print('ERREUR LORS DE LA CREATION LIEU DE TRAVAIL')
            # print(e)
            return None

    @staticmethod
    def toSaveLieuTravail(auteur,objet_dao_lieu):
        try:
            lieu  = Model_LieuTravail()
            lieu.designation = objet_dao_lieu.designation
            lieu.description = objet_dao_lieu.description
            lieu.auteur_id = auteur.id
            lieu.save()
            return lieu
        except Exception as e:
            # print('ERREUR LORS DE L ENREGISTREMENT DU LIEU')
            # print(e)
            return None

    @staticmethod
    def toUpdateLieuTravail(id, objet_dao_lieu):
        try:
            lieu = Model_LieuTravail.objects.get(pk = id)
            lieu.designation =objet_dao_lieu.designation
            lieu.description = objet_dao_lieu.description
            lieu.save()
            return lieu
        except Exception as e:
            # print('ERREUR LORS DE LA MODIFICATION DU LIEU DE TRAVAIL')
            # print(e)
            return None

    @staticmethod
    def toGetLieuTravail(id):
        try:
            return Model_LieuTravail.objects.get(pk = id)
        except Exception as e:
            return None

    @staticmethod
    def toDeleteLieuTravail(id):
        try:
            lieu = Model_LieuTravail.objects.get(pk = id)
            lieu.delete()
            return True
        except Exception as e:
            return False

    @staticmethod
    def toGetOrCreateLieuTravail(auteur, libelle):
        try:
            lieu = Model_LieuTravail.objects.filter(designation__icontains = libelle).first()
            if not lieu:
                unlieu = dao_lieu_travail()
                lieu = unlieu.toCreateLieuTravail(libelle, "")
                lieu = unlieu.toSaveLieuTravail(auteur, lieu)
            return lieu
        except Exception as e:
            # print("Error toGetOrCreateLieuTravail", e)
            return None
