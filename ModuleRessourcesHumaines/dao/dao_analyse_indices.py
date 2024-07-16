# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_Bareme
from django.utils import timezone
from datetime import date
from ErpBackOffice.models import  Model_Analyse_Personnel_Mouve
from ErpBackOffice.models import Model_Employe
from ErpBackOffice.models import Model_Analyse_indice_princsuivi
from ErpBackOffice.models import Model_Ligne_Formation
from ErpBackOffice.models import Model_Formation
from ErpBackOffice.models import Model_Unite_fonctionnelle
from django.db.models import Count
import numpy as np

class dao_analyse_indices(object):

    # This method return the List of Agents by year
    @staticmethod
    def toGet_Agent_by_Year():
        try:
            Year = timezone.now().year
            Nbre_Ag = []
            value = 0
            i = 2010
            while i <= Year:
                value += Model_Employe.objects.filter(date_entree__year = i).count()
                Nbre_Ag.append(value)
                value = 0
                i = i + 1
            #print('LES AGENST %s' %Nbre_Ag)
            return Nbre_Ag
        except Exception as e:
            #print(e)
            return Nbre_Ag

    # This method return thr List of Agents under 5 years old
    @staticmethod
    def toGet_Agent_moins_cinq_ans():
        try:
            duree = 0
            Agent = []
            Year = timezone.now().year
            i = 2010
            while i <= Year:
                employe = Model_Employe.objects.filter(date_entree__year__lte = i)
                for item in employe:
                    diff = i - item.date_entree.year
                    if diff < 5:
                        duree += 1
                    else:
                        duree += 0
                Agent.append(duree)
                duree = 0
                i = i + 1
            # #print('**DAO ANALYSE:GET AGENT AYANT MOINS 5ANS **%s' %Agent)
            return Agent
        except Exception as e:
            #print(e)
            return Agent

    # This method return the ratio of replacement
    @staticmethod
    def toGet_Ratio_remplacement():
        try:
            Ratio = []
            value = 0
            Ration_model = Model_Analyse_Personnel_Mouve.objects.all()
            for item in Ration_model:
                if item.arrivee != 0  and item.depart_definitif:
                    value = np.divide(item.arrivee, item.depart_definitif)
                else:
                    value = item.arrivee * item.depart_definitif

                Ratio.append(value)
            # #print('**DAO ANALYSE:GET RATIO REMPLACEMENT**%s' %Ratio)
            return Ratio
        except Exception as e:
            #print(e)
            return Ratio

    # This method return the entry rate of Agents
    @staticmethod
    def toGet_Taux_entree():
        try:
            Analyse_value = Model_Analyse_indice_princsuivi.objects.all()
            LesEntree = []
            Nbre_Ag = {}
            value = 0
            Year = timezone.now().year
            i = 2010
            while i <= Year:
                value += Model_Employe.objects.filter(date_entree__year = i).count()
                Nbre_Ag[i] = value
                value = 0
                i = i + 1

            for item, ele in zip(Analyse_value, Nbre_Ag):
                if item.nombre_entree != 0  and ele != 0:
                    val = np.divide(item.nombre_entree, ele)
                else:
                    val = item.nombre_entree * ele

                LesEntree.append(val)
            # #print('**DAO ANALYSE:GET TAUX ENTREE**%s' %LesEntree)
            return LesEntree
        except Exception as e:
            #print(e)
            return LesEntree

    # This method return the exit rate of Agents
    @staticmethod
    def toGet_Taux_sortie():
        try:
            Analyse_value = Model_Analyse_indice_princsuivi.objects.all()
            LeSortie = []
            Nbr_AGT = {}
            Year = timezone.now().year
            value = 0
            i = 2010
            while i <= Year:
                value += Model_Employe.objects.filter(date_entree__year = i).count()

                Nbr_AGT[i] = value
                value = 0
                i = i + 1

            for item, ele in zip(Analyse_value, Nbr_AGT):
                if item.nombre_sortie != 0  and ele != 0:
                    val = np.divide(item.nombre_sortie, ele)
                else:
                    val = item.nombre_sortie * ele

                LeSortie.append(val)
            # #print('**DAO ANALYSE:GET TAUX SORTIE**%s' %LeSortie)
            return LeSortie
        except Exception as e:
            #print(e)
            return LeSortie

    # This method return the turn over of Agents
    @staticmethod
    def toGet_Turn_over():
        try:
            Analyse_value = Model_Analyse_indice_princsuivi.objects.all()
            Turn = []
            Nbr_AGT = {}
            Year = timezone.now().year
            value = 0
            i = 2010
            while i <= Year:
                value += Model_Employe.objects.filter(date_entree__year = i).count()

                Nbr_AGT[i] = value
                value = 0
                i = i + 1

            for item, ele in zip(Analyse_value, Nbr_AGT):
                if ele != 0:
                    add_val = item.nombre_entree + item.nombre_sortie
                    val = np.divide(add_val, ele)
                else:
                    add_val = item.nombre_entree + item.nombre_sortie
                    val = add_val * ele

                Turn.append(val)
            # #print('**DAO ANALYSE:GET Turn_over**%s' %Turn)
            return Turn
        except Exception as e:
            #print(e)
            return Turn

    # This method return the main tracking clues
    @staticmethod
    def toGet_indices_principaux_suivi():
        try:
            return Model_Analyse_indice_princsuivi.objects.all()
        except Exception as e:
            #print(e)
            return None

    # This method return the seniority rate of Agents
    @staticmethod
    def toGet_taux_anciennete():
        try:
            Moyen_age = dao_analyse_indices.toGet_Agent_moins_cinq_ans()
            emploi_permet = Model_Analyse_Personnel_Mouve.objects.all()
            Tx_ancient = []

            for item, ele in zip(emploi_permet, Moyen_age):
                if ele != 0 and item.nombre_emploi_paye != 0:
                    val = np.divide(ele, item.nombre_emploi_paye)
                else:
                    val = ele * item.nombre_emploi_paye

                Tx_ancient.append(val)
            # #print('**DAO ANALYSE:GET TAUX ANCIENNETE**%s' %Tx_ancient)
            return Tx_ancient
        except Exception as e:
            #print(e)
            return Tx_ancient

    # This method return Agents Number by Category
    @staticmethod
    def toGet_Agent_cat():
        try:
            List_A = []
            List_B = []
            List_C = []
            List_D = []
            List_E = []
            List_F = []
            Year = timezone.now().year
            value = 0
            i = 2010
            while i <= Year:
                value_A = Model_Ligne_Formation.objects.filter(formation__annee = i, employe__categorie_employe__categorie = 'A').count()
                List_A.append(value_A)
                value_B = Model_Ligne_Formation.objects.filter(formation__annee = i, employe__categorie_employe__categorie = 'B').count()
                List_B.append(value_B)
                value_C = Model_Ligne_Formation.objects.filter(formation__annee = i, employe__categorie_employe__categorie = 'C').count()
                List_C.append(value_C)
                value_D = Model_Ligne_Formation.objects.filter(formation__annee = i, employe__categorie_employe__categorie = 'D').count()
                List_D.append(value_D)
                value_E = Model_Ligne_Formation.objects.filter(formation__annee = i, employe__categorie_employe__categorie = 'E').count()
                List_E.append(value_E)
                value_F = Model_Ligne_Formation.objects.filter(formation__annee = i, employe__categorie_employe__categorie = 'F').count()
                List_F.append(value_F)

                i = i + 1
            # #print('**DAO ANALYSE:GET AGENT BY CATEGORIE**%s' %List_A)
            return List_A, List_B, List_C, List_D, List_E, List_F
        except Exception as e:
            #print(e)
            return List_A


    # This method return The effectif of Category via Agent, Total Effectif and Taux de partenariat par catégorie
    @staticmethod
    def toGet_effectif_cat():
        try:
            Ag_A = []
            Ag_B = []
            Ag_C = []
            Ag_D = []
            Ag_E = []
            Ag_F = []
            Total = []
            Pat_formation = []
            Year = timezone.now().year
            value = 0
            i = 2010
            while i <= Year:
                value_A = Model_Employe.objects.filter(date_entree__year__lte = i, categorie_employe__categorie = 'A').count()
                Ag_A.append(value_A)
                value_B = Model_Employe.objects.filter(date_entree__year__lte = i, categorie_employe__categorie = 'B').count()
                Ag_B.append(value_B)
                value_C = Model_Employe.objects.filter(date_entree__year__lte = i, categorie_employe__categorie = 'C').count()
                Ag_C.append(value_C)
                value_D = Model_Employe.objects.filter(date_entree__year__lte = i, categorie_employe__categorie = 'D').count()
                Ag_D.append(value_D)
                value_E = Model_Employe.objects.filter(date_entree__year__lte = i, categorie_employe__categorie = 'E').count()
                Ag_E.append(value_E)
                value_F = Model_Employe.objects.filter(date_entree__year__lte = i, categorie_employe__categorie = 'F').count()
                Ag_F.append(value_F)
                #
                i = i + 1

            for elA,elB,elC,elD,elE,elF in zip(Ag_A, Ag_B, Ag_C, Ag_D, Ag_E, Ag_F):
                Total.append(elA + elB + elC + elD + elE + elF)

            Montant = Model_Analyse_indice_princsuivi.objects.all()
            for item, ele in zip(Montant,Total):
                if ele != 0 and item.montant_formation != 0:
                    val = np.divide(ele, item.montant_formation)
                else:
                    val = ele * item.montant_formation

                Pat_formation.append(val)

            # #print('**DAO ANALYSE:GET NUMBER AGENT BY CATEGORIE**%s' %Ag_A)
            # #print('**DAO ANALYSE:Total Number AGent by CAT**%s' %Total)
            # #print('**DAO ANALYSE:Taux Partenariat**%s' %Pat_formation)
            return Ag_A, Ag_B, Ag_C, Ag_D, Ag_E, Ag_F, Total, Pat_formation
        except Exception as e:
            #print(e)
            return Ag_A


    #This Method return the Training rate by professional family
    @staticmethod
    def toGet_training_prof_family():
        Liste_training = ['INFORMATIQUE', 'COMPTABILITE-FINANCES', 'CONTRÔLE DE GESTION', 'TELECOM', 'ECONOMIE', 'LOGISTIQUE', 'AFFAIRE JURIDIQUE', 'COMMUNICATION', 'POSTE']
        try:
            Year = timezone.now().year
            value = 0
            Tx_formation = []
            i = 2010
            while i <= Year:
                for item in Liste_training:
                    value += Model_Formation.objects.filter(date_debut__year = i, departement= item).count()

                Tx_formation.append(value)
                value = 0
                i = i + 1
            #print('**DAO ANALYSE:GET TRAINING PROFESSIONEL FAMILY**%s' %Tx_formation)
            return Tx_formation
        except Exception as e:
            #print(e)
            return Tx_formation


    # This method return the rate training by cat
    @staticmethod
    def toGet_training_by_cat():
        try:
            Year = timezone.now().year
            listTxInfo = []
            listTxRh = []
            listTxCompta = []
            i = 2010
            while i <= Year:
                Tx_Info = {'nbAge':0, 'nbJr':0}
                valueA = Model_Ligne_Formation.objects.values('formation__nombre_jour_formation').annotate(total=Count('employe_id')).filter(formation__annee = i,formation__departement='INFORMATIQUE')
                if valueA:
                    for value in valueA:
                        Tx_Info['nbAge'] = value['total']
                        Tx_Info['nbJr'] = value['formation__nombre_jour_formation']
                else :
                    Tx_Info['nbAge'] = 0
                    Tx_Info['nbJr'] = 0
                listTxInfo.append(Tx_Info)

                i = i + 1

            i = 2010
            while i <= Year:
                Tx_Rh = {'nbAge':0, 'nbJr':0}
                valueB = Model_Ligne_Formation.objects.values('formation__nombre_jour_formation').annotate(total=Count('employe_id')).filter(formation__annee = i,formation__departement='RESSOURCES HUMAINES')
                if valueB:
                    for value in valueB:
                        Tx_Rh['nbAge'] = value['total']
                        Tx_Rh['nbJr'] = value['formation__nombre_jour_formation']
                else :
                    Tx_Rh['nbAge'] = 0
                    Tx_Rh['nbJr'] = 0
                listTxRh.append(Tx_Rh)
                i = i + 1

            i = 2010
            while i <= Year:
                Tx_Compta = {'nbAge':0, 'nbJr':0}
                valueC = Model_Ligne_Formation.objects.values('formation__nombre_jour_formation').annotate(total=Count('employe_id')).filter(formation__annee = i,formation__departement='COMPTABILITE-FINANCES')
                if valueC:
                    for value in valueC:
                        Tx_Compta['nbAge'] = value['total']
                        Tx_Compta['nbJr'] = value['formation__nombre_jour_formation']
                else :
                    Tx_Compta['nbAge'] = 0
                    Tx_Compta['nbJr'] = 0
                listTxCompta.append(Tx_Compta)
                i = i + 1

            # #print('**DAO ANALYSE:GET TRAINING PROFESSIONEL FAMILY**%s' %listTxInfo)
            return listTxInfo, listTxRh, listTxCompta
        except Exception as e:
            #print(e)
            return listTxInfo, listTxRh, listTxCompta

    # This method return the rate training by cat
    @staticmethod
    def toGet_training_by_cat_s():
        try:
            Year = timezone.now().year
            listTxcg = []
            listTxtel = []
            listTxeco = []
            i = 2010
            while i <= Year:
                Tx_Cg = {'nbAge':0, 'nbJr':0}
                valueA = Model_Ligne_Formation.objects.values('formation__nombre_jour_formation').annotate(total=Count('employe_id')).filter(formation__annee = i,formation__departement='TELECOM')
                if valueA:
                    for value in valueA:
                        Tx_Cg['nbAge'] = value['total']
                        Tx_Cg['nbJr'] = value['formation__nombre_jour_formation']
                else :
                    Tx_Cg['nbAge'] = 0
                    Tx_Cg['nbJr'] = 0
                listTxcg.append(Tx_Cg)
                i = i + 1

            i = 2010
            while i <= Year:
                Tx_tel = {'nbAge':0, 'nbJr':0}
                valueB = Model_Ligne_Formation.objects.values('formation__nombre_jour_formation').annotate(total=Count('employe_id')).filter(formation__annee = i,formation__departement='RESSOURCES HUMAINES')
                if valueB:
                    for value in valueB:
                        Tx_tel['nbAge'] = value['total']
                        Tx_tel['nbJr'] = value['formation__nombre_jour_formation']
                else :
                    Tx_tel['nbAge'] = 0
                    Tx_tel['nbJr'] = 0
                listTxtel.append(Tx_tel)
                i = i + 1

            i = 2010
            while i <= Year:
                Tx_Eco = {'nbAge':0, 'nbJr':0}
                valueC = Model_Ligne_Formation.objects.values('formation__nombre_jour_formation').annotate(total=Count('employe_id')).filter(formation__annee = i,formation__departement='ECONOMIE')
                if valueC:
                    for value in valueC:
                        Tx_Eco['nbAge'] = value['total']
                        Tx_Eco['nbJr'] = value['formation__nombre_jour_formation']
                else :
                    Tx_Eco['nbAge'] = 0
                    Tx_Eco['nbJr'] = 0
                listTxeco.append(Tx_Eco)
                i = i + 1

            #print('**DAO ANALYSE:GET TRAINING PROFESSIONEL FAMILY**%s' %listTxcg)
            return listTxcg, listTxtel, listTxeco
        except Exception as e:
            #print(e)
            return listTxcg, listTxtel, listTxeco

    # This method return the rate training by cat   '', '', '', 'POSTE'
    @staticmethod
    def toGet_training_by_cat_s_s():
        try:
            Year = timezone.now().year
            listTxlg = []
            listTxaj = []
            listTxcom = []
            listTxposte = []
            i = 2010
            while i <= Year:
                Tx_lg = {'nbAge':0, 'nbJr':0}
                valueA = Model_Ligne_Formation.objects.values('formation__nombre_jour_formation').annotate(total=Count('employe_id')).filter(formation__annee = i,formation__departement='LOGISTIQUE')
                if valueA:
                    for value in valueA:
                        Tx_lg['nbAge'] = value['total']
                        Tx_lg['nbJr'] = value['formation__nombre_jour_formation']
                else :
                    Tx_lg['nbAge'] = 0
                    Tx_lg['nbJr'] = 0
                listTxlg.append(Tx_lg)
                i = i + 1

            i = 2010
            while i <= Year:
                Tx_AJ = {'nbAge':0, 'nbJr':0}
                valueB = Model_Ligne_Formation.objects.values('formation__nombre_jour_formation').annotate(total=Count('employe_id')).filter(formation__annee = i,formation__departement='AFFAIRE JURIDIQUE')
                if valueB:
                    for value in valueB:
                        Tx_AJ['nbAge'] = value['total']
                        Tx_AJ['nbJr'] = value['formation__nombre_jour_formation']
                else :
                    Tx_AJ['nbAge'] = 0
                    Tx_AJ['nbJr'] = 0
                listTxaj.append(Tx_AJ)
                i = i + 1

            i = 2010
            while i <= Year:
                Tx_com = {'nbAge':0, 'nbJr':0}
                valueC = Model_Ligne_Formation.objects.values('formation__nombre_jour_formation').annotate(total=Count('employe_id')).filter(formation__annee = i,formation__departement='COMMUNICATION')
                if valueC:
                    for value in valueC:
                        Tx_com['nbAge'] = value['total']
                        Tx_com['nbJr'] = value['formation__nombre_jour_formation']
                else :
                    Tx_com['nbAge'] = 0
                    Tx_com['nbJr'] = 0
                listTxcom.append(Tx_com)
                i = i + 1

            i = 2010
            while i <= Year:
                Tx_Post = {'nbAge':0, 'nbJr':0}
                valueC = Model_Ligne_Formation.objects.values('formation__nombre_jour_formation').annotate(total=Count('employe_id')).filter(formation__annee = i,formation__departement='POSTE')
                if valueC:
                    for value in valueC:
                        Tx_Post['nbAge'] = value['total']
                        Tx_Post['nbJr'] = value['formation__nombre_jour_formation']
                else :
                    Tx_Post['nbAge'] = 0
                    Tx_Post['nbJr'] = 0
                listTxposte.append(Tx_Post)
                i = i + 1

            #print('**DAO ANALYSE:GET TRAINING PROFESSIONEL FAMILY**%s' %listTxcg)
            return listTxlg, listTxaj, listTxcom, listTxposte
        except Exception as e:
            #print(e)
            return listTxlg, listTxaj, listTxcom, listTxposte


    # This method return the middle age of agent
    @staticmethod
    def toGet_meddle_age():
        try:
            Year = timezone.now().year
            Age_M = []
            somme = 0
            i = 2010
            while i <= Year:
                div = Model_Employe.objects.filter(date_entree__year = i).count()
                employe =  Model_Employe.objects.filter(date_entree__year = i)
                for item in employe:
                    if item is None:
                        item = 0
                        somme += (Year - item)
                    else:
                        somme += (Year - item.annee_naissance)

                if somme != 0 and div != 0:
                    resultat = np.divide(somme, div)
                else:
                    resultat = somme * div

                Age_M.append(resultat)
                somme = 0
                i = i + 1
            #print('**DAO ANALYSE:GET MIDDLE AGE**%s' %Age_M)
            return Age_M
        except Exception as e:
            #print(e)
            return Age_M

    @staticmethod
    def anciennete():
        try:
            Year = timezone.now().year
            List = []
            ancien = []
            i = 2010
            while i <= Year:
                div = Model_Employe.objects.filter( date_entree__year = i)
                if div:
                    for item in div:
                        List.append(Year - item.date_de_naissance.year)
                else:
                    List.append(0)
                # #print(i ,':', List)
                ancien.append(max(List))

                List = []
                i = i + 1
            # #print('**DAO ANALYSE INDICES: ANCIEN**%s' %ancien)
            return ancien
        except Exception as e:
            #print(e)
            return ancien

    @staticmethod
    def toget_last_indice_principal():
        try:
            Year = timezone.now().year
            Last = Model_Analyse_indice_princsuivi.objects.filter(annee = 2015)
            if Last:
                value_returTxD = Last.Taux_absenteisme_maladie_court
                value_returTxDv = Last.value_returTxD
            else:
                value_returTxD = 0.00
                value_returTxDv = 0.00

            #print('DAO INDICE PRINCIPAL', Last)
            return value_returTxD, value_returTxDv
        except Exception as e:
            #print(e)
            return 0, 0


    @staticmethod
    def toGet_agent_by_direction():
        try:
            Total = {'y':0, 'label':''}
            Data = []
            Departement = Model_Unite_fonctionnelle.objects.all()
            for item in Departement:
                Total = {'y':0, 'label':''}
                Employe = Model_Employe.objects.filter(unite_fonctionnelle = item.id).count()
                Total['y'] = Employe
                Total['label'] = item.libelle
                Data.append(Total)

            # #print('**DAO ANALYSE TOGET_AGENT_BY_DIRECT**',Data)
            # #print('**DAO ANALYSE TOGET_AGENT_BY_DIRECT Liste**',Total)
            return Data
        except Exception as e:
            #print(e)
            #print('**ERREUR DAO ANALYSE TOGET_AGENT_BY_DIRECT**',Data)
            return Data







