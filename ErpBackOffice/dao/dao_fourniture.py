# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from ModuleAchat.dao.dao_bon_reception import dao_bon_reception
from ErpBackOffice.models import Model_Bon_reception, Model_Article

class dao_fourniture(dao_bon_reception):
    @staticmethod
    def toCreateFourniture(numero_reception, est_realisee, fournisseur_id, demandeur_id , devise_id, condition_reglement_id, date_prevue, date_realisation, demande_achat_id = None, document_id = None, ligne_budgetaire_id = None):
        if numero == None or numero == "" : numero = dao_fourniture.toGenerateNumeroFourniture()
        return dao_bon_reception.toCreateBonReception(numero_reception,date_prevue,0, "", fournisseur_id, document_id, condition_reglement_id, demande_achat_id, ligne_budgetaire_id, est_realisee)

    @staticmethod
    def toListBonsAchat():
        return Model_Bon_reception.objects.filter(date_prevue__isnull = False,is_actif=True).order_by("-creation_date")

    @staticmethod
    def toListBonsAchatDuStatus(status):
        return Model_Bon_reception.objects.filter(date_prevue__isnull = False, is_actif=True).filter(etat = status).order_by("-creation_date")

    @staticmethod
    def toListBonsAchatEnAttente():
        return Model_Bon_reception.objects.filter(est_realisee = False, is_actif=True).filter(date_prevue__isnull = False).order_by("-creation_date")

    @staticmethod
    def toListBonsAchatFournisseur(fournisseur_id):
        return Model_Bon_reception.objects.filter(fournisseur_id = fournisseur_id, is_actif=True).order_by("-creation_date")

    @staticmethod
    def toListFournitures():
        return Model_Bon_reception.objects.filter(est_realisee = True, is_actif=True).order_by("-creation_date")

    @staticmethod
    def toListFournituresFacturables():
        list = []
        for fourniture in dao_fourniture.toListFournitures() :
            if fourniture.est_facturable == True : list.append(fourniture)
        return list

    @staticmethod
    def toListFournituresDuFournisseur(fournisseur_id):
        return Model_Bon_reception.objects.filter(est_realisee = True, is_actif=True).filter(fournisseur_id = fournisseur_id).order_by("-creation_date")

    @staticmethod
    def toListFournituresFacturablesDuFournisseur(fournisseur_id):
        list = []
        for fourniture in dao_fourniture.toListFournituresDuFournisseur(fournisseur_id) :
            if fourniture.est_facturable == True : list.append(fourniture)
        return list


    ##### Les listes by auteur

    @staticmethod
    def toListBonsAchatByAuteur(user_id):
        return Model_Bon_reception.objects.filter(date_prevue__isnull = False, is_actif=True).filter(auteur_id=user_id).order_by("-creation_date")

    @staticmethod
    def toListBonsAchatDuStatusByAuteur(status, user_id):
        return Model_Bon_reception.objects.filter(date_prevue__isnull = False, is_actif=True).filter(etat = status).filter(auteur_id=user_id).order_by("-creation_date")

    @staticmethod
    def toListBonsAchatEnAttenteByAuteur(user_id):
        return Model_Bon_reception.objects.filter(est_realisee = False, is_actif=True).filter(date_prevue__isnull = False).filter(auteur_id=user_id).order_by("-creation_date")

    @staticmethod
    def toListFournituresByAuteur(user_id):
        return Model_Bon_reception.objects.filter(est_realisee = True, is_actif=True).filter(auteur_id=user_id).order_by("-creation_date")

    @staticmethod
    def toListFournituresFacturablesByAuteur(user_id):
        list = []
        for fourniture in dao_fourniture.toListFournituresByAuteur(user_id) :
            if fourniture.est_facturable == True : list.append(fourniture)
        return list


    @staticmethod
    def toSaveFourniture(auteur, objet_dao_bon_reception):
        return dao_bon_reception.toSaveBonReception(auteur, objet_dao_bon_reception)

    @staticmethod
    def toUpdateFourniture(id, objet_dao_bon_reception):
        return dao_bon_reception.toUpdateBonReception(id, objet_dao_bon_reception)

    @staticmethod
    def toGetFourniture(id):
        return dao_bon_reception.toGetBonReception(id)

    @staticmethod
    def toDeleteFourniture(id):
        return dao_bon_reception.toDeleteBonReception(id)

    @staticmethod
    def toGenerateNumeroFourniture():
        total_fournitures = dao_fourniture.toListBonsAchat().count()
        total_fournitures = total_fournitures + 1
        temp_numero = str(total_fournitures)

        for i in range(len(str(total_fournitures)), 4):
            temp_numero = "0" + temp_numero

        mois = timezone.now().month
        if mois < 10: mois = "0%s" % mois

        temp_numero = "BC-%s%s%s" % (timezone.now().year, mois, temp_numero)
        return temp_numero

    @staticmethod
    def toGetNextId():
        total_fournitures = dao_fourniture.toListBonsAchat().count()
        total_fournitures = total_fournitures + 1

        if total_fournitures >= 1:
            return total_fournitures
        else:
            return 1