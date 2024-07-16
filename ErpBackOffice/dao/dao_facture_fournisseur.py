# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.dao.dao_facture import dao_facture
from ErpBackOffice.models import Model_Facture

class dao_facture_fournisseur(dao_facture):

    @staticmethod
    def toCreateFactureFournisseur(date_facturation, numero_facture, montant, bon_reception_id = None, journal_comptable_id = None, periode = "", document = "", fournisseur_id = None, facture_mere_id = None, lettrage_id = None, condition_reglement_id = None, montant_en_lettre = ""):
        return dao_facture.toCreateFacture(date_facturation, numero_facture, montant, None, bon_reception_id, journal_comptable_id, periode, document, fournisseur_id, None , facture_mere_id, lettrage_id, condition_reglement_id)

    @staticmethod
    def toListFacturesFournisseur():
        return Model_Facture.objects.filter(type = "FOURNISSEUR").order_by("-pk")
    
    @staticmethod
    def toListFacturesFournisseurMere():
        return Model_Facture.objects.filter(type = "FOURNISSEUR", facture_mere = None).order_by("-pk")
    
    @staticmethod
    def toListFacturesFournisseurAcompte():
        return Model_Facture.objects.filter(type = "FOURNISSEUR", est_facture_acompte = True).order_by("-pk")
    
    @staticmethod
    def toListFacturesFournisseurOfFournisseur(fournisseur_id):
        return Model_Facture.objects.filter(type = "FOURNISSEUR", fournisseur_id = fournisseur_id).order_by("-pk")
    
    @staticmethod
    def toListFacturesFourniture(fourniture_id):
        return Model_Facture.objects.filter(type = "FOURNISSEUR", bon_reception_id = fourniture_id).order_by("-date_facturation")

    @staticmethod
    def toListFacturesFournisseurNonSoldees():
        list = []
        for facture in dao_facture_fournisseur.toListFacturesFournisseur() :
            if facture.est_soldee == False : list.append(facture)
        return list
    
    @staticmethod
    def toListFacturesFournisseurNonSoldeesOfFournisseur(fournisseur_id):
        list = []
        for facture in dao_facture_fournisseur.toListFacturesFournisseurOfFournisseur(fournisseur_id) :
            if facture.est_soldee == False : list.append(facture)
        return list

    @staticmethod
    def toListFacturesFournitureNonSoldees(fourniture_id):
        list = []
        for facture in dao_facture_fournisseur.toListFacturesFourniture(fourniture_id) :
            if facture.est_soldee == True : list.append(facture)
        return list
       
    @staticmethod
    def toSaveFactureFournisseur(auteur, objet_dao_facture):
        objet_dao_facture.type = "FOURNISSEUR"
        return dao_facture.toSaveFacture(auteur, objet_dao_facture)

    @staticmethod
    def toUpdateFactureFournisseur(id, objet_dao_facture):
        objet_dao_facture.type = "FOURNISSEUR"
        #return dao_facture.toUpdateFacture(id, objet_dao_facture)
        return dao_facture.toUpdateFacture(id,objet_dao_facture)
    
    @staticmethod
    def toGetFactureFournisseur(id):
        return dao_facture.toGetFacture(id)

    @staticmethod
    def toDeleteFactureFournisseur(id):
        return dao_facture.toDeleteFacture(id)

    
    @staticmethod
    def toGetNextId():
        total_factures = dao_facture_fournisseur.toListFacturesFournisseur().count()
        total_factures = total_factures + 1
        
        if total_factures >= 1:
            return total_factures
        else:
            return 1