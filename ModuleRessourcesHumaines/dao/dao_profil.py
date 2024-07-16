from __future__ import unicode_literals

from ErpBackOffice.models import Model_ProfilRH
from ErpBackOffice.dao.dao_personne import dao_personne

class dao_profil(object):
    id = 0
    date_engagement = None
    debut_service = None
    date_naissance = ""
    lieu_naissance = ""
    nationalite = ""
    numero_passeport = ""
    numero_identification = ""
    etat_civil = ""
    numero_ss = ""
    genre = ""
    matricule = ""
    email_professionnel = ""
    phone_professionnel = ""
    phone_personnel =""
    phone_professionnel2 = ""
    contrat =""
    genre = ""
    est_permanent = True
    auteur = 0

    @staticmethod
    def toCreateProfil(date_engagement, debut_service, date_naissance, lieu_naissance, nationalite, numero_passeport,numero_identification ,etat_civil , numero_ss, genre, matricule, email_professionnel, phone_professionnel, phone_personnel, phone_professionnel2, contrat, est_permanent):
        try:

            profil = dao_profil()
            profil.date_engagement = date_engagement
            profil.debut_service = debut_service
            profil.date_naissance = date_naissance
            profil.lieu_naissance = lieu_naissance
            profil.nationalite = nationalite
            profil.numero_passeport = numero_passeport
            profil.numero_identification = numero_identification
            profil.etat_civil = etat_civil
            profil.est_permanent = est_permanent
            profil.numero_ss = numero_ss
            profil.genre = genre
            profil.matricule = matricule
            profil.email_professionnel = email_professionnel
            profil.phone_professionnel = phone_professionnel
            profil.phone_personnel =phone_personnel
            profil.phone_professionnel2 = phone_professionnel2
            profil.contrat = contrat

            return profil
        except Exception as e:
            # print("ERREUR LORS DE LA CREATION DU PROFIL")
            # print(e)
            return None


    @staticmethod
    def toListProfil():
        return Model_ProfilRH.objects.all().order_by('-id')


    @staticmethod
    def toSaveProfil(auteur,object_dao_profil):
        try:
            profil = Model_ProfilRH()
            profil.date_engagement = object_dao_profil.date_engagement
            profil.debut_service = object_dao_profil.debut_service
            profil.date_naissance = object_dao_profil.date_naissance
            profil.lieu_naissance = object_dao_profil.lieu_naissance
            profil.nationalite = object_dao_profil.nationalite
            profil.numero_passeport = object_dao_profil.numero_passeport
            profil.numero_identification = object_dao_profil.numero_identification
            profil.etat_civil = object_dao_profil.etat_civil
            profil.est_permanent = True
            profil.numero_ss = object_dao_profil.numero_ss
            profil.genre = object_dao_profil.genre
            profil.matricule = object_dao_profil.matricule
            profil.email_professionnel = object_dao_profil.email_professionnel
            profil.phone_professionnel = object_dao_profil.phone_professionnel
            profil.phone_personnel =object_dao_profil.phone_personnel
            profil.phone_professionnel2 = object_dao_profil.phone_professionnel2
            profil.contrat = object_dao_profil.contrat
            profil.auteur_id = auteur.id

            profil.save()
            return profil
        except Exception as e:
            print("ERREUR LORS DU SAVE DU PROFIL")
            print(e)
            return None

    @staticmethod
    def toUpdateProfil(id, object_dao_profil):
        try:
            profil = Model_ProfilRH.objects.get(pk = id)
            profil.date_engagement = object_dao_profil.date_engagement
            profil.debut_service = object_dao_profil.debut_service
            profil.date_naissance = object_dao_profil.date_naissance
            profil.lieu_naissance = object_dao_profil.lieu_naissance
            profil.nationalite = object_dao_profil.nationalite
            profil.numero_passeport = object_dao_profil.numero_passeport
            profil.numero_identification = object_dao_profil.numero_identification
            profil.etat_civil = object_dao_profil.etat_civil
            profil.est_permanent = True
            profil.numero_ss = object_dao_profil.numero_ss
            profil.genre = object_dao_profil.genre
            profil.matricule = object_dao_profil.matricule
            profil.email_professionnel = object_dao_profil.email_professionnel
            profil.phone_professionnel = object_dao_profil.phone_professionnel
            profil.phone_personnel =object_dao_profil.phone_personnel
            profil.phone_professionnel2 = object_dao_profil.phone_professionnel2
            profil.contrat = object_dao_profil.contrat
            profil.save()
            return profil
        except Exception as e:
            # print("ERREUR LORS DE LA MISE A JOUR DU PROFIL")
            # print(e)
            return False

    @staticmethod
    def toGetProfil(id):
        try:
            return Model_ProfilRH.objects.get(pk = id)
        except Exception as e:
            return None

    @staticmethod
    def toDeleteProfil(id):
        try:
            profil = Model_ProfilRH.objects.get(pk = id)
            profil.delete()
            return True
        except Exception as e:
            return False



