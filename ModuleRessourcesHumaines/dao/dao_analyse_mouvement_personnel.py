
from __future__ import unicode_literals
from ErpBackOffice.models import Model_Analyse_Personnel_Mouve
from ErpBackOffice.models import Model_Employe
from django.utils import timezone
from django.db.models import Count
import numpy as np



class dao_analyse_mouvement_personnel(object):

    @staticmethod
    def toUpdateMouvement_personnel_masse_sal(year, masse_salariale):
        try:
            Mouvement = Model_Analyse_Personnel_Mouve.objects.get(annee = year)
            #print('**DAO ANALYSE UPDATE MASSE SAL %s' %Mouvement)
            Mouvement.masse_salariale =  masse_salariale
            Mouvement.save()
            return Mouvement
        except Exception as e:
            #print('ERREUR LORS DE LA MODIFICATION DE MOUVEMENT PERSONNE')
            #print(e)
            return None

    @staticmethod
    def toUpdateMouvement_personnelpropagation_stage(year, propagation_st):
        try:
            Mouvement = Model_Analyse_Personnel_Mouve.objects.get(annee = year)
            #print('**DAO ANALYSE UPDATE MASSE SAL %s' %Mouvement)
            Mouvement.prorogation_stage =  propagation_st
            Mouvement.save()
            return Mouvement
        except Exception as e:
            #print('ERREUR LORS DE LA MODIFICATION DE MOUVEMENT PERSONNE')
            #print(e)
            return None

    @staticmethod
    def toUpdateMouvement_personnel_total_mise_stage(year,total_stage):
        try:
            Mouvement = Model_Analyse_Personnel_Mouve.objects.get(annee = year)
            #print('**DAO ANALYSE UPDATE MISE EN STAGE %s' %Mouvement)
            Mouvement.total_mise_stage = total_stage
            Mouvement.save()
            return Mouvement
        except Exception as e:
            #print('ERREUR LORS DE LA MODIFICATION DE MOUVEMENT PERSONNE')
            #print(e)
            return None

    @staticmethod
    def toUpdateMouvement_personnel_Depart_Def(year,definitif):
        try:
            Mouvement = Model_Analyse_Personnel_Mouve.objects.get(annee = year)
            #print('**DAO ANALYSE UPDATE DEP DEF %s' %Mouvement)
            Mouvement.depart_definitif = definitif
            Mouvement.save()
            return Mouvement
        except Exception as e:
            #print('ERREUR LORS DE LA MODIFICATION DE MOUVEMENT PERSONNE')
            #print(e)
            return None

    @staticmethod
    def toUpdateMouvement_personnel_Depart_provoir(year,provoir):
        try:
            Mouvement = Model_Analyse_Personnel_Mouve.objects.get(annee = year)
            #print('**DAO ANALYSE UPDATE DEP DEF %s' %Mouvement)
            Mouvement.depart_provision = provoir
            Mouvement.save()
            return Mouvement
        except Exception as e:
            #print('ERREUR LORS DE LA MODIFICATION DE MOUVEMENT PERSONNE')
            #print(e)
            return None

    @staticmethod
    def toUpdateMouvement_personnel_eff_physique(year,eff):
        try:
            Mouvement = Model_Analyse_Personnel_Mouve.objects.get(annee = year)
            #print('**DAO ANALYSE UPDATE DEP DEF %s' %Mouvement)
            Mouvement.nombre_emploi_paye = eff
            Mouvement.save()
            return Mouvement
        except Exception as e:
            #print('ERREUR LORS DE LA MODIFICATION DE MOUVEMENT PERSONNE')
            #print(e)
            return None

    @staticmethod
    def toUpdateMouvement_personnel_Depart_vol(year,volontaire):
        try:
            Mouvement = Model_Analyse_Personnel_Mouve.objects.get(annee = year)
            #print('**DAO ANALYSE UPDATE DEP VOL %s' %volontaire)
            Mouvement.depart_volontaire = volontaire
            Mouvement.save()
            return Mouvement
        except Exception as e:
            #print('ERREUR LORS DE LA MODIFICATION DE MOUVEMENT PERSONNE')
            #print(e)
            return None


    @staticmethod
    def toUpdateMouvement_personnel_Demission(year,Demission):
        try:
            Mouvement = Model_Analyse_Personnel_Mouve.objects.get(annee = year)
            #print('**DAO ANALYSE UPDATE DEP DEF %s' %Mouvement)
            Mouvement.demission = Demission
            Mouvement.save()
            return Mouvement
        except Exception as e:
            #print('ERREUR LORS DE LA MODIFICATION DE MOUVEMENT PERSONNE')
            #print(e)
            return None

    @staticmethod
    def toUpdateMouvement_personnel_arriver(year,arriver):
        try:
            Mouvement = Model_Analyse_Personnel_Mouve.objects.get(annee = year)
            #print('**DAO ANALYSE UPDATE DEP DEF %s' %Mouvement)
            Mouvement.arrivee = arriver
            Mouvement.save()
            return Mouvement
        except Exception as e:
            #print('ERREUR LORS DE LA MODIFICATION DE MOUVEMENT PERSONNE')
            #print(e)
            return None

    @staticmethod
    def toUpdateMouvement_personnel_poste_vacant_by_mob(year,post_vac):
        try:
            Mouvement = Model_Analyse_Personnel_Mouve.objects.get(annee = year)
            #print('**DAO ANALYSE UPDATE DEP DEF %s' %Mouvement)
            Mouvement.poste_vacant_by_mob = post_vac
            Mouvement.save()
            return Mouvement
        except Exception as e:
            #print('ERREUR LORS DE LA MODIFICATION DE MOUVEMENT PERSONNE')
            #print(e)
            return None

    @staticmethod
    def toUpdateMouvement_personnel_poste_vacant_pouvu(year,post_vac):
        try:
            Mouvement = Model_Analyse_Personnel_Mouve.objects.get(annee = year)
            #print('**DAO ANALYSE UPDATE DEP DEF %s' %Mouvement)
            Mouvement.poste_vacant_pouvu = post_vac
            Mouvement.save()
            return Mouvement
        except Exception as e:
            #print('ERREUR LORS DE LA MODIFICATION DE MOUVEMENT PERSONNE')
            #print(e)
            return None

    @staticmethod
    def toUpdateMouvement_personnel_recru_emploi_permanent(year,post_vac):
        try:
            Mouvement = Model_Analyse_Personnel_Mouve.objects.get(annee = year)
            #print('**DAO ANALYSE UPDATE DEP DEF %s' %Mouvement)
            Mouvement.recru_emploi_permanent = post_vac
            Mouvement.save()
            return Mouvement
        except Exception as e:
            #print('ERREUR LORS DE LA MODIFICATION DE MOUVEMENT PERSONNE')
            #print(e)
            return None

    @staticmethod
    def toUpdateMouvement_personnel_concours(year,post_vac):
        try:
            Mouvement = Model_Analyse_Personnel_Mouve.objects.get(annee = year)
            #print('**DAO ANALYSE UPDATE DEP DEF %s' %Mouvement)
            Mouvement.concours = post_vac
            Mouvement.save()
            return Mouvement
        except Exception as e:
            #print('ERREUR LORS DE LA MODIFICATION DE MOUVEMENT PERSONNE')
            #print(e)
            return None

    @staticmethod
    def toUpdateMouvement_personnel_mutation(year,post_vac):
        try:
            Mouvement = Model_Analyse_Personnel_Mouve.objects.get(annee = year)
            #print('**DAO ANALYSE UPDATE DEP DEF %s' %Mouvement)
            Mouvement.mutation = post_vac
            Mouvement.save()
            return Mouvement
        except Exception as e:
            #print('ERREUR LORS DE LA MODIFICATION DE MOUVEMENT PERSONNE')
            #print(e)
            return None

    @staticmethod
    def toUpdateMouvement_personnel_detachement(year,post_vac):
        try:
            Mouvement = Model_Analyse_Personnel_Mouve.objects.get(annee = year)
            #print('**DAO ANALYSE UPDATE DEP DEF %s' %Mouvement)
            Mouvement.detachement = post_vac
            Mouvement.save()
            return Mouvement
        except Exception as e:
            #print('ERREUR LORS DE LA MODIFICATION DE MOUVEMENT PERSONNE')
            #print(e)
            return None

    @staticmethod
    def toUpdateMouvement_personnel_total_recru(year,post_vac):
        try:
            Mouvement = Model_Analyse_Personnel_Mouve.objects.get(annee = year)
            #print('**DAO ANALYSE UPDATE DEP DEF %s' %Mouvement)
            Mouvement.total_recru = post_vac
            Mouvement.save()
            return Mouvement
        except Exception as e:
            #print('ERREUR LORS DE LA MODIFICATION DE MOUVEMENT PERSONNE')
            #print(e)
            return None

    @staticmethod
    def toUpdateMouvement_personnel_recru_direct(year,post_vac):
        try:
            Mouvement = Model_Analyse_Personnel_Mouve.objects.get(annee = year)
            #print('**DAO ANALYSE UPDATE DEP DEF %s' %Mouvement)
            Mouvement.recru_direct = post_vac
            Mouvement.save()
            return Mouvement
        except Exception as e:
            #print('ERREUR LORS DE LA MODIFICATION DE MOUVEMENT PERSONNE')
            #print(e)
            return None

    @staticmethod
    def toUpdateMouvement_personnel_interimaire(year,post_vac):
        try:
            Mouvement = Model_Analyse_Personnel_Mouve.objects.get(annee = year)
            #print('**DAO ANALYSE UPDATE DEP DEF %s' %Mouvement)
            Mouvement.interimaire = post_vac
            Mouvement.save()
            return Mouvement
        except Exception as e:
            #print('ERREUR LORS DE LA MODIFICATION DE MOUVEMENT PERSONNE')
            #print(e)
            return None


    @staticmethod
    def toGet_numberofAgentPermanent():
        try:
            Year = timezone.now().year
            somme = 0
            Agent_Permanent = []
            i = 2010
            while i <= Year:
                somme +=Model_Employe.objects.filter(est_permanent = True, date_entree__year = i).count()

                Agent_Permanent.append(somme)
                somme = 0
                i = i + 1
            # #print('**DAO EMPLOYE Agent Permanent Par Année ** %s' %Agent_Permanent)
            return Agent_Permanent
        except Exception as e:
            #print("ERREUR Agent Permanent Par Année ")
            #print(e)
            return Agent_Permanent


    @staticmethod
    def toGet_Personnel_Mouvement():
        try:
            List = Model_Analyse_Personnel_Mouve.objects.all()
            # #print('*MOUVEMENT PERSONNE** %s' %List)
            return List
        except Exception as e:
            #print("ERREUR GET MOUVEMENT PERSONNEL %s" %e)
            return List

    @staticmethod
    def toget_last_Mouvement_Personnel():
        try:
            Year = timezone.now().year
            Last = Model_Analyse_Personnel_Mouve.objects.filter(annee = Year).last()
            if Last:
                value_returTxD = Last.Tx_depart
                value_returTxDv = Last.Tx_depart_volontaire
                value.returTxSt = Last.Taux_prop_stage
            else:
                value_returTxD = 0.00
                value_returTxDTxDv = 0.00
                value_returTxSt = 0.00

            # #print('DAO MOUVEMENT PERSONNEL', Last)
            return value_returTxD, value_returTxDTxDv, value_returTxSt
        except Exception as e:
            #print(e)
            return 0,0,0