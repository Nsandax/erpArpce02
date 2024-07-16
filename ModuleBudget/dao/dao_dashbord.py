from __future__ import unicode_literals
from ErpBackOffice.models import Model_Transactionbudgetaire
from ErpBackOffice.models import Model_Bon_reception
from ErpBackOffice.models import Model_Budget
from ErpBackOffice.models import *
from ModuleAchat.dao.dao_bon_reception import dao_bon_reception
from ErpBackOffice.models import Model_LigneBudgetaire, Model_Contrat, Model_Demande_cotation, Model_Lettre_commande, Model_TypeMarche
from django.utils import timezone
from datetime import date, timedelta
from django.db.models import Count
from ModuleBudget.dao.dao_exercicebudgetaire import dao_exercicebudgetaire
import numpy as np
from dateutil.relativedelta import relativedelta
import collections, functools, operator
from operator import itemgetter
from django.db.models import Q



class dao_dashbord(object):

    @staticmethod
    def toGetLastBCMonth():
        try:
            # print('***YES***')
            data = []
            somme = 0
            state={"label": '', "value":0.0}

            Month = timezone.now().month
            year = timezone.now().year
            today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today_month = int(today.strftime('%m'))
            #6 Month Ago
            first_month = today - relativedelta(months=6)
            first_month = int(first_month.strftime('%m'))
            Bons = Model_Bon_reception.objects.filter(creation_date__year=year, creation_date__month__range=(first_month, today_month), is_actif=True)
            # print('*BON', Bons)
            for item in Bons:
                state={item.creation_date.strftime('%b'): 0}
                state[item.creation_date.strftime('%b')] = int(float(item.quantite_total))
                data.append(state)
            if data:
                result = dict(functools.reduce(operator.add, map(collections.Counter, data)))
                mois = list(result.keys())
                lesvaleurs = list(result.values())
                mois.reverse()
            else:
                lesvaleurs = []
                mois = []
            # print('*****Somme BC Par Mois', mois)
            # print('*****Somme BC Par value', lesvaleurs)
            Bon_by_currence_Month = dao_bon_reception.toGetBonReceptionCount()
            return mois,lesvaleurs,Bon_by_currence_Month
        except Exception as e:
            # print(e)
            return None,None,None


    @staticmethod
    def toGetCBValide():
        try:
            nbr = 0
            data = []
            somme = 0
            state={"label": '', "value":0.0}
            Month = timezone.now().month
            year = timezone.now().year
            today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today_day = int(today.strftime('%d'))
            # print('today', today_day)
            first_day_of_week = today - timedelta(days=3)
            first_day_of_week = int(first_day_of_week.strftime('%d'))
            # print('today', first_day_of_week)
            Bons = Model_Bon_reception.objects.filter(date_prevue__year=year, date_prevue__month=Month, date_prevue__day__range=(first_day_of_week, today_day), is_actif=True)
            # print('Bons', Bons)
            for item in Bons:
                state={item.date_prevue.strftime('%A'): 0.0}
                state[item.date_prevue.strftime('%A')] = int(float(item.quantite_total))
                data.append(state)
            # print('data',data)
            if data:
                # print('data',data)
                result = dict(functools.reduce(operator.add, map(collections.Counter, data)))
                lesjours = list(result.keys())
                lesvaleurs = list(result.values())
                # print('les jours:', lesjours)
                # print('les valeurs:', lesvaleurs)
            #NOMBRE BC VALIDE
            Bon = Model_Bon_reception.objects.all()
            for item in Bon:
                if item.etat != 'Créé' or item.etat == 'Approuvé':
                    nbr += 1
            # print('CB_Valide', nbr)
            return nbr,lesjours,lesvaleurs
        except Exception as e:
            # print(e)
            return 0,None,None

    @staticmethod
    def toGetLastpassebyMonth():
        try:
            data = []
            bnv = []
            state={"label": '', "value":0}
            lelo = timezone.now()
            Month = timezone.now().month
            year = timezone.now().year
            today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today_month = int(today.strftime('%m'))
            # print(today_month)
            #11 Month Ago
            first_month = today - relativedelta(months=11)
            # print('**FIRST MONTH', first_month)

            while first_month <= today:
                _month = int(first_month.strftime('%m'))
                _year = int(first_month.strftime('%Y'))
                Bons = Model_Bon_reception.objects.filter(date_reception__year=_year, date_reception__month=_month, etat = 'Approuvé', is_actif=True).count()
                Bon_non_valide = Model_Bon_reception.objects.filter(date_reception__year=_year, date_reception__month=_month, etat = 'Créé', is_actif=True).count()
                labal_month = first_month.strftime('%b')
                labex = str(labal_month) +' '+ str(_year)
                state={labex: Bons}
                data.append(state)
                bnv.append(Bon_non_valide)
                # print('periode', _month, _year)
                first_month = first_month + relativedelta(months=+1)

            #CETTE PARTIE DEMANDE A CE QU'ON SEPARE LES LABELS AVEC LES VALEURS
            if data:
                tampoM=[]
                tampoV=[]

                for item in data:
                    for state in item.keys():
                        tampoM.append(state)
                    for state in item.values():
                        tampoV.append(state)

            # print('***Bon Non Valide', bnv)

            return tampoM, tampoV, bnv
        except Exception as e:
            # print(e)
            return [],[],[]

    @staticmethod
    def getfrequenceContratYear():
        try:
            data = []
            state={"label": '', "value":0}
            lelo = timezone.now()
            Month = timezone.now().month
            year = timezone.now().year
            today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today_month = int(today.strftime('%m'))
            first_month = today - relativedelta(months=11)
            # print('*******CONTRAT YEAR *******************')
            while first_month <= today:
                _month = int(first_month.strftime('%m'))
                _year = int(first_month.strftime('%Y'))
                Bons = Model_Contrat.objects.filter(created_at__year=_year, created_at__month=_month, statut__designation='Contrat signé téléchargé').count()
                labal_month = first_month.strftime('%b')
                labex = str(labal_month) +' '+ str(_year)
                state={labex: Bons}
                data.append(state)
                # print('periode', _month, _year)
                first_month = first_month + relativedelta(months=+1)
            # print('DATA',data)
            #CETTE PARTIE DEMANDE A CE QU'ON SEPARE LES LABELS AVEC LES VALEURS
            if data:
                tampoM=[]
                tampoV=[]

                for item in data:
                    for state in item.keys():
                        tampoM.append(state)
                    for state in item.values():
                        tampoV.append(state)
            # print('**ata', data)
            # print('periode', tampoM)
            # print('value', tampoV)
            return tampoM, tampoV
        except Exception as e:
            return None,None

    @staticmethod
    def toGetBCbynumber(id):
        try:
            bc = dao_bon_reception.toGetBonReception(id)
            datebc = bc.date_prevue
            # print('la date prevue', datebc)
            # print('l\'année de la date prevue', datebc.year)
            # print('le mois de la date prevue', datebc.month)
            newlistbc = Model_Bon_reception.objects.filter(date_prevue__year = datebc.year, date_prevue__month=datebc.month, is_actif=True).order_by('-id')
            # print('new list bc by month', newlistbc)
            return newlistbc
        except Exception as e:
            # print(e)
            return None

    @staticmethod
    def toGetBudgetGlobal():
        listbudget =[]
        try:
            budget = Model_Budget.objects.all()
            budgetInvest = Model_Budget.objects.filter(categoriebudget__designation = 'Investissement')
            budgetRecette = Model_Budget.objects.filter(categoriebudget__designation = 'Recette')
            budgetExp = Model_Budget.objects.filter(categoriebudget__designation = 'Exploitation')
            somme = 0
            sommeIn = 0
            sommeRec = 0
            sommeExp = 0
            for item in budget:
                somme += item.solde
            for el in budgetInvest:
                sommeIn += el.solde
            for op in budgetRecette:
                sommeRec += op.solde
            for em in budgetExp:
                sommeExp += em.solde
            listbudget.append(sommeExp)
            listbudget.append(somme)
            listbudget.append(sommeIn)
            listbudget.append(sommeRec)
            return sommeExp, sommeRec, sommeIn, somme,listbudget
        except Exception as e:
            # print(e)
            return None, None, None, None,listbudget

    @staticmethod
    def toGetligneUsed():
        try:
            ExerciceBudgtaire = dao_exercicebudgetaire.toGetActiveExercicebudgetaire()
            print("EXECICE EN COURS", ExerciceBudgtaire)
            if ExerciceBudgtaire:
                return Model_Transactionbudgetaire.objects.filter(exercice_budgetaire_id = ExerciceBudgtaire.id).order_by('-id')
            else:
                return []
        except Exception as e:
            # print(e)
            return None

    @staticmethod
    def toGetMostLigneUsed():
        try:
            exercice = dao_exercicebudgetaire.toGetActiveExercicebudgetaire()
            lignesClass = []
            LigneBudgetaire = []
            transact =  Model_Transactionbudgetaire.objects.filter(exercice_budgetaire__id = exercice.id).values('ligne_budgetaire').annotate(ligne_count=Count('ligne_budgetaire')).order_by()
            ordonne =sorted(transact, key=itemgetter('ligne_count'), reverse=True)
            for item in ordonne:
                lignesClass.append(item['ligne_budgetaire'])

            # print('lignesClass', lignesClass)

            for item in lignesClass:
                smalligne = Model_LigneBudgetaire.objects.filter(id=item)
                # print('FOUND', smalligne)

                if smalligne:
                    LigneBudgetaire.append(smalligne)

            # print('LIGNE LE PLUS UTILISE', LigneBudgetaire)

            return LigneBudgetaire
        except Exception as e:
            return []



    @staticmethod
    def toGetTransactionbymonth():
        data = []
        somme = 0
        state={"label": '', "value":0.0}
        Month = timezone.now().month
        year = timezone.now().year
        today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_month = int(today.strftime('%m'))

        first_month = today - relativedelta(months=6)
        first_month = int(first_month.strftime('%m'))
        Bons = Model_Transactionbudgetaire.objects.filter(created_at__year=year, created_at__month__range=(first_month, today_month))
        for item in Bons:
            state={item.created_at.strftime('%b'): 0}
            state[item.created_at.strftime('%b')] = int(float(item.montant))
            data.append(state)
        if data:
            result = dict(functools.reduce(operator.add, map(collections.Counter, data)))
            mois = list(result.keys())
            lesvaleurs = list(result.values())
            mois.reverse()
        else:
            lesvaleurs = []
            mois = []
        # print('*****Somme BC Par Mois', mois)
        # print('*****Somme BC Par value', lesvaleurs)
        return mois,lesvaleurs

    @staticmethod
    def toGetCompareCBwithBR():
        try:
            data =[]
            Total = {}
            label = ''
            value = 0
            compteur = 0
            bons = Model_Bon_reception.objects.all()
            combinaison = Model_LigneBudgetaire.objects.all()
            for ligne in combinaison:
                for item in bons:
                    if item.ligne_budgetaire.id == ligne.id:
                        compteur += 1
                Total[ligne.code]= compteur
                compteur = 0
            data.append(Total)
            result = dict(functools.reduce(operator.add, map(collections.Counter, data)))
            # print('**data', result)
            return None
        except Exception as e:
            return None

    # ENCORE EN TEST
    @staticmethod
    def toGetMaxconsomme():
        try:
            occurence = Model_Transactionbudgetaire.objects.values("ligne_budgetaire_id").annotate(count=Count('ligne_budgetaire_id')).order_by("-count")
            return occurence
        except Exception as e:
            return None

    #NOT WORK
    @staticmethod
    def toGetBCRapproche():
        try:
            budget = Model_Facture.objects.filter(categoriebudget__designation = 'Exploitation')
            # for item in budget:
                # print('budget Exp',item.separateur_solde)
            return budget
        except Exception as e:
            # print(e)
            return None

    @staticmethod
    def toGetBudgetInfogeneral():
        try:
            sommeglobal = 0
            sommeEg = 0
            sommeDisp = 0
            sommeRallonge = 0
            budget = Model_Budget.objects.all()
            for item in budget:
                sommeglobal += item.solde
                sommeEg += item.montant_engage
                sommeDisp += item.montant_ligne_solde
                sommeRallonge += item.budgetRallonge

            pourcentageEG = (100 * sommeEg) / sommeglobal
            pourcentageDisp = (100 * sommeDisp) / sommeglobal
            sommeRallonge = (100 * sommeRallonge) / sommeglobal

            # print('budget global',sommeglobal)
            # print('budget Rallonge', sommeRallonge)
            # print('budget Engage pc',pourcentageEG)
            # print('budget dispo',pourcentageDisp)
            return sommeEg,sommeDisp,sommeRallonge
        except Exception as e:
            # print(e)
            return None


    @staticmethod
    def toGetMostUseLineBudgetaire():
        try:
            listligne = []
            newlist = []
            last = []
            dictligne = {}
            exerice = dao_exercicebudgetaire.toGetActiveExercicebudgetaire()
            if exerice:
                Lignes = Model_LigneBudgetaire.objects.filter(exericebudgetaires__id = exerice.id)
                for item in Lignes:
                    dictligne = {'id':0, 'value':0}
                    # print('first iteration', item.separateur_valeur_total_consommee)
                    dictligne["id"]= item
                    dictligne["value"]= item.separateur_valeur_total_consommee
                    listligne.append(dictligne)

                #Get Most Value
                # print('Les lignes budgetaires', listligne)
                ordonne =sorted(listligne, key=itemgetter('value'), reverse=True)
                # print('New Les lignes budgetaires', ordonne)

                # for i in len(taille):
                #     # newlist = ordonne[i]
                #     print(list(ordonne[i].keys()))
                for item in ordonne:
                    newlist.append(item['id'])

                # for i in range(3):
                #     last.append(newlist.i)
                # print('La plus consommée', newlist)

                return newlist
            else: return []
        except Exception as e:
            # print(e)
            return None

    @staticmethod
    def maximums(list,n=5):
        it = list[:]
        return [it.pop(it.index(max(it))) for i in range(10) if len(it)]


    @staticmethod
    def lastcontrat():
        Contrats = Model_Contrat.objects.all().order_by('-id')[:10]
        # print('Contrats', Contrats)
        return Contrats

    @staticmethod
    def contratSign():
        Contrats = Model_Contrat.objects.filter(Q(statut__designation = 'Contrat signé téléchargé') | Q(statut__designation = 'Fournitures livrées')
        | Q(statut__designation = 'Cloturé')| Q(statut__designation = 'Garantie de bonne exécution')| Q(statut__designation = 'Réception provisoire')
        | Q(statut__designation = 'Réception définitive')).order_by('-id')
        return Contrats

    @staticmethod
    def contratWaiting():
        Contrats = Model_Contrat.objects.filter(statut__designation = 'Créé').order_by('-id')
        return Contrats

    @staticmethod
    def lastlettreCommande():
        lettre = Model_Lettre_commande.objects.all().order_by('-id')[:10]
        # print('Contrats', Contrats)
        return lettre

    @staticmethod
    def GetlistProjets():
        projets = Model_Projet.objects.all().order_by('-id')[:5]
        return projets

    @staticmethod
    def SoldeContrat():
        try:
            contrat = Model_Contrat.objects.all()
            somme = 0
            devise =''
            sommeconsome = 0
            sommestay = 0
            for item in contrat:
                somme += item.montant
                devise = item.devise.symbole_devise
                sommeconsome += item.totalconsome
                sommestay += item.solde

            globalContrat = {
                'total': str(somme)+' '+devise,
                'totalconsomme': str(sommeconsome) +' '+devise,
                'totalstay': str(sommestay)+' '+devise
            }
            # print('***Global Contrat', globalContrat)
            return globalContrat
        except Exception as e:
            return None


    @staticmethod
    def SoldeProjet():
        try:
            # Gestion Projets
            somme = 0
            eng = 0
            real = 0
            dispo = 0
            projet = Model_LigneBudgetaire.objects.filter(type = 2)
            # print('****projet', projet)            
            devise =''
            for item in projet:
                somme = somme + float(item.montant_alloue)
                eng = eng + float(item.valeur_engagement)
                real = real +  float(item.valeur_reel)
                dispo = dispo + float(item.valeur_solde)
                devise = 'CFA'
            
            # print('somme', somme)
            # print('eng', eng)
            # print('dispo', dispo)

            projets ={
                'projet': projet,
                'engage':str(eng)+' '+devise,
                'realise': str(real)+' '+devise,
                'dispo': str(dispo)+' '+devise,
                'sommeprojets': str(somme)+' '+devise
            }
            # print('LES PROJETS', projets)

            return projets
        except Exception as e:
            return None

    @staticmethod
    def CountBC():
        try:
            bc = Model_Bon_reception.objects.all().count()
            return bc
        except Exception as e:
            return 0

    @staticmethod
    def totalBCRapproche():
        try:
            # print('BIGIN BC R')
            nbrrapproche = 0
            nbr_non_rapproche = 0
            nbrrapproche_part = 0
            montantBCR = 0
            montantBCNR = 0
            bc = Model_Bon_reception.objects.all()
            # print('**Resultat', bc)
            for item in bc:
                if item.statusRapprochement == 1:
                    nbrrapproche += 1
                elif item.statusRapprochement == 2:
                    nbr_non_rapproche += 1
                elif item.statusRapprochement == 0:
                    nbrrapproche_part += 1

                montantBCR += item.montant_rapproche
                montantBCNR += item.montant_non_rapproche

            lesTotalsBC = {
                'nbrrapproche':nbrrapproche,
                'nbr_non_rapproche':nbr_non_rapproche,
                'nbrrapproche_part':nbrrapproche_part,
                'montantBCR': montantBCR,
                'montantBCNR': montantBCNR
            }
            # print('**Resultat', lesTotalsBC)

            return lesTotalsBC
        except Exception as e:
            # print(e)
            return None


    @staticmethod
    def CountlettreC():
        try:
            lc = Model_Lettre_commande.objects.all().count()
            return lc
        except Exception as e:
            return 0


    @staticmethod
    def CountDC():
        try:
            Dc = Model_Demande_cotation.objects.all().count()
            return Dc
        except Exception as e:
            return 0


    @staticmethod
    def CountAppOffre():
        try:
            AF = Model_Avis_appel_offre.objects.all().count()
            return AF
        except Exception as e:
            return 0


    @staticmethod
    def getfrequencecontratMounth():
        try:
            data = []
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            data.append({"label": 'Echue', "value":0, "time": 'past',"color": '#3e95cd'})
            day_of_week = int(today.strftime('%w'))
            first_day_of_week = today + timedelta(days=-day_of_week+1)

            for i in range(-1,4):
                if i==0: label = 'Cette semaine'
                elif i==3: label = 'Non echue'
                else:
                    start_week = first_day_of_week + timedelta(days=i*7)
                    end_week = start_week + timedelta(days=6)
                    if start_week.month == end_week.month:
                        label = str(start_week.day) + '-' + str(end_week.day) + ' ' + end_week.strftime('%b')
                    else:
                        label = start_week.strftime('%d %b') + '-' + end_week.strftime('%d %b')
                data.append({"label":label,"value":0, "time": 'past' if i<0 else 'future', "color": '#8e5ea2'})

            start_date = (first_day_of_week + timedelta(days=-7))

            for i in range(0,6):
                try:
                    if i == 0:
                        contrat = Model_Contrat.objects.filter(created_at__lt = start_date).aggregate(total=Count('numero_reference'))#<
                        nbtotal = float(contrat["total"])
                    elif i == 5:
                        contrat = Model_Contrat.objects.filter(created_at__gte = start_date).aggregate(total=Count('numero_reference'))#>=
                        nbtotal = float(contrat["total"])
                    else:
                        next_date = start_date + timedelta(days=7)
                        contrat = Model_Contrat.objects.filter(created_at__range = [start_date, next_date]).aggregate(total=Count('numero_reference'))
                        nbtotal = float(contrat["total"])
                        start_date = next_date
                    data[i]['value'] = nbtotal
                except Exception as e:
                    #print('Erreur get montant HT: {}'.format(e))
                    data[i]['value'] = 0

            # print('****DATA STORAGE****', data)

            return data
            return None
        except Exception as e:
            return 0



