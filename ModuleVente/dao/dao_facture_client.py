# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ErpBackOffice.models import Model_Client
from ErpBackOffice.dao.dao_facture import dao_facture
from ErpBackOffice.models import Model_Facture
from django.db.models import Count
from ErpBackOffice.models import Model_Ligne_facture

class dao_facture_client(dao_facture):
    @staticmethod
    def toCreateFactureClient(date_facturation, numero_facture, montant, order_id, pos_id = 0, session_pos_id = 0):
        return dao_facture.toCreateFacture(date_facturation, numero_facture, montant, order_id, pos_id, session_pos_id)

    @staticmethod
    def toListFacturesClient():
        return Model_Facture.objects.filter(type = "CLIENT").order_by("-date_facturation")
    @staticmethod
    def toListFacturesCommande(commande_id):
        return Model_Facture.objects.filter(type = "CLIENT").filter(order_id = commande_id).order_by("-date_facturation")

    @staticmethod
    def toListFacturesClientNonSoldees():
        list = []
        for facture in dao_facture_client.toListFacturesClient() :
            if facture.est_soldee == False : list.append(facture)
        return list

    @staticmethod
    def toDeleteFactureClient(id):
        return dao_facture.toDeleteFacture(id)

    @staticmethod
    def toSaveFactureClient(auteur, objet_dao_facture):
        objet_dao_facture.type = "CLIENT"
        return dao_facture.toSaveFacture(auteur, objet_dao_facture)

    @staticmethod
    def toUpdateFactureClient(id, objet_dao_facture):
        objet_dao_facture.type = "CLIENT"
        return dao_facture.toUpdateFacture(id, objet_dao_facture)
    @staticmethod
    def toGetFactureClient(id):
        return dao_facture.toGetFacture(id)

    @staticmethod
    def toDeleteFactureClient(id):
        return dao_facture.toDeleteFacture(id)






