# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.dao.dao_facture import dao_facture
from ErpBackOffice.models import Model_Facture
from ErpBackOffice.models import Model_Client
from django.db.models import Count
from ErpBackOffice.models import Model_Ligne_facture
from ErpBackOffice.models import Model_Paiement
from django.db.models import Avg, Max, Min, Sum


class dao_facture_client(dao_facture):

    @staticmethod
    def toCreateFactureClient(date_facturation, numero_facture, montant, bon_commande_id = None, journal_comptable_id = None, periode = "", document = "", client_id = None, lettrage_id = None, condition_reglement_id = None, montant_en_lettre = ""):
        return dao_facture.toCreateFacture(date_facturation, numero_facture, montant, bon_commande_id , None, journal_comptable_id, periode, document,None ,client_id, None, lettrage_id, condition_reglement_id)

    @staticmethod
    def toListFacturesClient():
        return Model_Facture.objects.filter(type = "CLIENT").order_by("-date_facturation")
    
    @staticmethod
    def toListFacturesAvoir():
        return Model_Facture.objects.filter(est_facture_avoir = True).order_by("-date_facturation")


    @staticmethod
    def toListFacturesClientOfClient(client_id):
        return Model_Facture.objects.filter(type = "CLIENT", client_id = client_id).order_by("-date_facturation")


    @staticmethod
    def toListFacturesCommande(commande_id):
        return Model_Facture.objects.filter(type = "CLIENT", bon_commande_id = commande_id).order_by("-date_facturation")

    @staticmethod
    def toListFacturesClientNonSoldees():
        list = []
        for facture in dao_facture_client.toListFacturesClient() :
            if facture.est_soldee == False : list.append(facture)
        return list

    @staticmethod
    def toListFacturesCommandeNonSoldees(commande_id):
        list = []
        for facture in dao_facture_client.toListFacturesCommande(commande_id) :
            if facture.est_soldee == True : list.append(facture)
        return list
       
    @staticmethod
    def toSaveFactureClient(auteur, objet_dao_facture):
        objet_dao_facture.type = "CLIENT"
        #print("lond")
        return dao_facture.toSaveFacture(auteur, objet_dao_facture)

    @staticmethod
    def toUpdateFactureClient(id, objet_dao_facture):
        objet_dao_facture.type = "CLIENT"
        #return dao_facture.toUpdateFacture(id, objet_dao_facture)
        return dao_facture.toUpdateFacture(id,objet_dao_facture)
    
    @staticmethod
    def toGetFactureClient(id):
        return dao_facture.toGetFacture(id)

    @staticmethod
    def toDeleteFactureClient(id):
        return dao_facture.toDeleteFacture(id)

    
    @staticmethod
    def toGetNextId():
        total_factures = dao_facture_client.toListFacturesClient().count()
        total_factures = total_factures + 1
        
        if total_factures >= 1:
            return total_factures
        else:
            return 1

    @staticmethod
    def toGetClient_Number_Article():
        try:
            #print('****CLIENT ARTICLES*****')
            client = Model_Client.objects.all()
            resultat = []
            Tableau_client = []
            Tableau_nbr_art_by_client = []
            for item in client:
                lignes= Model_Ligne_facture.objects.values('facture__client__nom_complet').order_by('facture__client_id').annotate(count=Count('article_id')).filter(facture__client_id=item.id)

                for ligne in lignes:
                    resultat.append(ligne)

            for item in resultat:
                Tableau_client.append(item["facture__client__nom_complet"])
                Tableau_nbr_art_by_client.append(item["count"])

            #print('les clients %s' %Tableau_client)
            #print('le nombre by client %s' %Tableau_nbr_art_by_client)

            return Tableau_client, Tableau_nbr_art_by_client
        except Exception as e:
            #print("ERREUR LISTE_CLIENT AND NOMBRE ARTICLE")
            #print(e)
            return [],[]

    # Methode qui recupere la somme de tous les paiements
    @staticmethod
    def toGetPaiementTotal():
        try:
            #print('****** Somme de Paiement Total *******')
            Somme_Total = Model_Paiement.objects.all().aggregate(Sum('montant'))
            #print('la somme total paiement %s' %Somme_Total)

            return Somme_Total
        except Exception as e:
            #print("ERREUR TOTAL DE PAIEMENT")
            #print(e)
            return 0
