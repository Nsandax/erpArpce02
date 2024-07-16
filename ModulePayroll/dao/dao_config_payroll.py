# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_Config_Payroll, Model_Organisation
from django.utils import timezone

class dao_config_payroll(object):
    id = 0
    taux_cnss = ""
    nbre_max_jours_travailles = ""
    nbre_mensualite = 10
    taux_interet = 0
    est_active = True
    organisation_id = None
    
    @staticmethod
    def toListConfigPayroll():
        return Model_Config_Payroll.objects.all().order_by("-id")
    
    @staticmethod
    def toCreateConfigPayroll(taux_cnss, nbre_max_jours_travailles, nbre_mensualite, taux_interet, est_active = True, organisation_id = None):
        try:
            config_payroll = dao_config_payroll()
            config_payroll.taux_cnss = taux_cnss
            config_payroll.nbre_max_jours_travailles = nbre_max_jours_travailles
            config_payroll.nbre_mensualite = nbre_mensualite
            config_payroll.taux_interet = taux_interet
            config_payroll.est_active = est_active
            config_payroll.organisation_id = organisation_id
            return config_payroll
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION")
            #print(e)
            return None

    @staticmethod
    def toSaveConfigPayroll(dao_config_payroll_object):
        try:
            config_payroll = Model_Config_Payroll()
            config_payroll.taux_cnss = dao_config_payroll_object.taux_cnss
            config_payroll.nbre_max_jours_travailles = dao_config_payroll_object.nbre_max_jours_travailles
            config_payroll.nbre_mensualite = dao_config_payroll_object.nbre_mensualite
            config_payroll.taux_interet = dao_config_payroll_object.taux_interet
            config_payroll.est_active = dao_config_payroll_object.est_active
            config_payroll.organisation_id = dao_config_payroll.organisation_id
            config_payroll.creation_date = timezone.now()
            config_payroll.save()
            return config_payroll
        except Exception as e:
            #print("ERREUR LORS DU SAVE")
            #print(e)
            return None
    

    @staticmethod
    def toUpdateOrSaveConfigPayroll(dao_config_payroll_object):
        try:
            previous_config = dao_config_payroll.toGetMainConfigPayroll()
            if previous_config:
                previous_config.taux_cnss = dao_config_payroll_object.taux_cnss
                previous_config.nbre_max_jours_travailles = dao_config_payroll_object.nbre_max_jours_travailles
                previous_config.nbre_mensualite = dao_config_payroll_object.nbre_mensualite
                previous_config.taux_interet = dao_config_payroll_object.taux_interet
                previous_config.est_active = dao_config_payroll_object.est_active
                previous_config.update_date = timezone.now()
                previous_config.save()
            else:
                organisation = Model_Organisation.objects.filter(est_active = True)[0]
                config_payroll = Model_Config_Payroll()
                config_payroll.taux_cnss = dao_config_payroll_object.taux_cnss
                config_payroll.nbre_max_jours_travailles = dao_config_payroll_object.nbre_max_jours_travailles
                config_payroll.nbre_mensualite = dao_config_payroll_object.nbre_mensualite
                config_payroll.taux_interet = dao_config_payroll_object.taux_interet
                config_payroll.est_active = dao_config_payroll_object.est_active
                config_payroll.organisation_id = organisation.id
                config_payroll.creation_date = timezone.now()
                config_payroll.save()
            return config_payroll
        except Exception as e:
            #print("ERREUR LORS DU SAVE")
            #print(e)
            return None

    
    @staticmethod
    def toUpdateConfigPayroll(id, objet_config_payroll):
        try:
            config_payroll = Model_Config_Payroll.objects.get(pk = id)
            config_payroll.taux_cnss = objet_config_payroll.taux_cnss
            config_payroll.nbre_max_jours_travailles = objet_config_payroll.nbre_max_jours_travailles
            config_payroll.nbre_mensualite = objet_config_payroll.nbre_mensualite
            config_payroll.taux_interet = objet_config_payroll.taux_interet
            config_payroll.est_active = objet_config_payroll.est_active
            config_payroll.organisation_id = dao_config_payroll.organisation_id
            config_payroll.update_date = timezone.now()
            config_payroll.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR")
            #print(e)
            return False

    
    @staticmethod
    def toDeleteConfigPayroll(objet_config_payroll):
        try:
            config_payroll = Model_Config_Payroll.objects.get(pk = objet_config_payroll.id)
            config_payroll.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION")
            #print(e)
            return False

    
    @staticmethod
    def toGetConfigPayroll(id):
        try:
            config_payroll = Model_Config_Payroll.objects.get(pk = id)
            return config_payroll
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE")
            #print(e)
            return None
    
    @staticmethod
    def toGetMainConfigPayroll():
        try:
            organisation = Model_Organisation.objects.filter(est_active = True)[0]
            return Model_Config_Payroll.objects.filter(est_active = True, organisation = organisation ).first()
        except Exception as e:
            return None
    

    @staticmethod
    def toUpdateConfigNbrMensualiteTauxInteret(nbr_mensualite, taux_interet):
        try:
            config_payroll = dao_config_payroll.toGetMainConfigPayroll()
            config_payroll.nbre_mensualite = nbr_mensualite
            config_payroll.taux_interet = taux_interet
            config_payroll.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR")
            #print(e)
            return False