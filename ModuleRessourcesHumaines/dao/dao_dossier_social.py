# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_Dossier_Social
from django.utils import timezone

class dao_dossier_social(object):
    id = 0
    numero_dossier_social = None
    creation_date = None
    employe = None
    description = ""
    structure = ""
    lieu = ""
    sujet_plainte = None
    observation = ""
    responsable = None
    mail_envoyé = ""
    date_fermeture = None
    statut = 0
    alerte = False

    @staticmethod
    def toListDossierSocial():
        return Model_Dossier_Social.objects.all().order_by("numero_dossier_social")
    
    @staticmethod
    def toListDossierSocialByAuteur(user_id):
        return Model_Dossier_Social.objects.filter(auteur_id=user_id).order_by("numero_dossier_social")
    
    @staticmethod
    def toCreateDossierSocial(numero_dossier_social, description, structure, lieu = "", sujet_plainte = None, observation = "", employe = None, responsable = None, mail_envoyé = "", date_fermeture = None, statut = "", alerte = False):
        try:
            dossier_social = dao_dossier_social()
            dossier_social.numero_dossier_social = numero_dossier_social
            dossier_social.employe = employe
            dossier_social.description = description
            dossier_social.structure = structure
            dossier_social.lieu = lieu
            dossier_social.sujet_plainte = sujet_plainte
            dossier_social.observation = observation
            dossier_social.responsable = responsable
            dossier_social.mail_envoyé = mail_envoyé
            dossier_social.date_fermeture = date_fermeture
            dossier_social.statute = statut
            dossier_social.alerte = False

            return dossier_social
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DU DOSSIER SOCIAL")
            #print(e)
            return None

    @staticmethod
    def toSaveDossierSocial(auteur, dao_dossier_social_object):
        try:
            dossier_social = Model_Dossier_Social()
            dossier_social.numero_dossier_social = dao_dossier_social_object.numero_dossier_social
            dossier_social.employe = dao_dossier_social_object.employe
            dossier_social.description = dao_dossier_social_object.description
            dossier_social.structure = dao_dossier_social_object.structure
            dossier_social.lieu = dao_dossier_social_object.lieu
            dossier_social.sujet_plainte = dao_dossier_social_object.sujet_plainte
            dossier_social.responsable = dao_dossier_social_object.responsable
            dossier_social.mail_envoyé = dao_dossier_social_object.mail_envoyé
            dossier_social.date_fermeture = dao_dossier_social_object.date_fermeture
            dossier_social.statute = dao_dossier_social_object.statut
            dossier_social.creation_date = timezone.now()
            dossier_social.alerte = False
            dossier_social.auteur_id = auteur
            
            dossier_social.save()
            return dossier_social
        except Exception as e:
            #print("ERREUR LORS DU SAVE DOSSIER SOCIAL")
            #print(e)
            return None

    
    @staticmethod
    def toUpdateDossierSocial(id, dao_dossier_social_object):
        try:
            dossier_social = Model_Dossier_Social.objects.get(id=id)
            #print(dossier_social.numero_dossier_social)
            dossier_social.numero_dossier_social = dao_dossier_social_object.numero_dossier_social
            dossier_social.employe = dao_dossier_social_object.employe
            dossier_social.description = dao_dossier_social_object.description
            dossier_social.structure = dao_dossier_social_object.structure
            dossier_social.lieu = dao_dossier_social_object.lieu
            dossier_social.sujet_plainte = dao_dossier_social_object.sujet_plainte
            dossier_social.observation = dao_dossier_social_object.observation
            dossier_social.responsable = dao_dossier_social_object.responsable
            dossier_social.mail_envoyé = dao_dossier_social_object.mail_envoyé
            dossier_social.date_fermeture = dao_dossier_social_object.date_fermeture
            dossier_social.statute = dao_dossier_social_object.statut
            dossier_social.alerte = False
            dossier_social.save()
            return dossier_social
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR DU DOSSIER SOCIAL")
            #print(e)
            return None

    
    @staticmethod
    def toDeleteDossierSocial(dao_dossier_social_object):
        try:
            dossier_social = Model_Dossier_Social.objects.get(id = dao_dossier_social_object.id)
            dossier_social.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION DU DOSSIER SOCIAL")
            #print(e)
            return False

    
    @staticmethod
    def toGetDossierSocial(id):
        try:
            dossier_social = Model_Dossier_Social.objects.get(pk = id)
            return dossier_social
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE D'UN DOSSIER SOCIAL")
            #print(e)
            return None

    @staticmethod
    def toGenerateNumeroDossier():
        num = 0
        if Model_Dossier_Social.objects.all().count() != 0:
            #doss = Model_Dossier_Social.objects.latest('numero_dossier_social')
            num = int(Model_Dossier_Social.objects.all().count())
        num+= 1
        num = "00"+str(num)
        mois = timezone.now().month
        if mois < 10: mois = "0%s" % mois
		
        temp_numero = "DS-%s%s%s" % (timezone.now().year, mois, num)
        return temp_numero