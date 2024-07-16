from __future__ import unicode_literals
from ErpBackOffice.utils.auth import auth
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.template import loader
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils import timezone
from django.core import serializers
from random import randint
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from ErpBackOffice.utils.identite import identite
from ErpBackOffice.utils.tools import ErpModule
from ErpBackOffice.dao.dao_model import dao_model
from ErpBackOffice.utils.print import weasy_print
import datetime
import json
import os
from django.db import transaction
from ModuleInventaire.dao.dao_utils import dao_utils
from ErpBackOffice.models import Model_Transactionbudgetaire
from ErpBackOffice.dao.dao_wkf_historique_expression import dao_wkf_historique_expression
from ErpBackOffice.dao.dao_wkf_historique_bon_transfert import dao_wkf_historique_bon_transfert
from ModuleInventaire.dao.dao_document_bon_transfert import dao_document_bon_transfert
from ModuleInventaire.dao.dao_document_bon_entree import dao_document_bon_entree

from ErpBackOffice.utils.separateur import makeFloat, makeStringFromFloatExcel, makeInt, makeIntId
from ModuleComptabilite.dao.dao_immobilisation import dao_immobilisation
from ModuleInventaire.dao.dao_traitement_immobilisation import dao_traitement_immobilisation
from ModuleInventaire.dao.dao_ligne_traitementimmobilisation import dao_ligne_traitementimmobilisation
from ErpBackOffice.dao.dao_document import dao_document
from ModuleRessourcesHumaines.dao.dao_organisation import dao_organisation
from ErpBackOffice.utils.pagination import pagination
from ErpBackOffice.utils.print import weasy_print

#Import from ErpBackOffice
from ErpBackOffice.dao.dao_personne import dao_personne
from ErpBackOffice.dao.dao_place import dao_place
from ErpBackOffice.dao.dao_compte import dao_compte
from ErpBackOffice.dao.dao_module import dao_module
from ErpBackOffice.dao.dao_role import dao_role
from ErpBackOffice.dao.dao_groupe_permission import dao_groupe_permission
from ErpBackOffice.dao.dao_devise import dao_devise
from ErpBackOffice.dao.dao_fourniture import dao_fourniture
from ErpBackOffice.dao.dao_ligne_fourniture import dao_ligne_fourniture
from ErpBackOffice.dao.dao_bon_special import dao_bon_special
from ErpBackOffice.dao.dao_item_bon_special import dao_item_bon_special
from ErpBackOffice.dao.dao_taux import dao_taux
from ErpBackOffice.models import Model_Article, Model_Bon_transfert, Model_Categorie, Model_Emplacement, Model_Mouvement_stock, Model_StockArticle
from ErpBackOffice.dao.dao_wkf_workflow import dao_wkf_workflow
from ErpBackOffice.dao.dao_wkf_etape import dao_wkf_etape
from ErpBackOffice.dao.dao_wkf_historique_demande import dao_wkf_historique_demande
from ErpBackOffice.dao.dao_wkf_historique_reception import dao_wkf_historique_reception
from ErpBackOffice.dao.dao_wkf_historique_reception import dao_wkf_historique_reception
from ErpBackOffice.dao.dao_wkf_historique_bon_entree_depot import dao_wkf_historique_bon_entree_depot
from ErpBackOffice.dao.dao_wkf_transition import dao_wkf_transition
from ErpBackOffice.dao.dao_wkf_condition import dao_wkf_condition
from ErpBackOffice.dao.dao_wkf_approbation import dao_wkf_approbation

from ModuleBudget.dao.dao_transactionbudgetaire import dao_transactionbudgetaire
#Import From Module Achat
from ModuleAchat.dao.dao_categorie_article import dao_categorie_article
from ModuleAchat.dao.dao_categorie import dao_categorie
from ModuleAchat.dao.dao_article import dao_article
from ModuleAchat.dao.dao_stock_article import dao_stock_article
from ModuleAchat.dao.dao_type_article import dao_type_article
from ModuleAchat.dao.dao_fournisseur_article import dao_fournisseur_article
from ModuleAchat.dao.dao_fournisseur import dao_fournisseur
from ModuleAchat.dao.dao_unite import dao_unite
from ModuleAchat.dao.dao_unite_achat_article import dao_unite_achat_article
from ModuleAchat.dao.dao_ligne_reception import dao_ligne_reception
from ModuleAchat.dao.dao_condition_reglement import dao_condition_reglement
from ModuleAchat.dao.dao_demande_achat import dao_demande_achat
from ModuleAchat.dao.dao_expression_besoin import dao_expression_besoin
from ModuleAchat.dao.dao_ligne_expression import dao_ligne_expression

from ModuleConversation.dao.dao_notification import dao_notification
from ModuleInventaire.dao.dao_asset_historique import dao_asset_historique

#Import From Ressources Humaines
from ModuleRessourcesHumaines.dao.dao_employe import dao_employe
from ModuleRessourcesHumaines.dao.dao_unite_fonctionnelle import dao_unite_fonctionnelle
from ErpBackOffice.utils.wkf_task import wkf_task


#POUR LOGGING
import logging, inspect
monLog = logging.getLogger('logger')
module= "ModuleInventaire"
var_module_id = 7

# Create your views here.

# Import du Module Inventaire
from ModuleInventaire.dao.dao_bon_inventaire import dao_bon_inventaire
from ModuleInventaire.dao.dao_bon_transfert import dao_bon_transfert
from ModuleInventaire.dao.dao_ligne_transfert import dao_ligne_transfert
from ModuleInventaire.dao.dao_ligne_inventaire import dao_ligne_inventaire
from ModuleInventaire.dao.dao_mouvement_stock import dao_mouvement_stock
from ModuleInventaire.dao.dao_emplacement import dao_emplacement
from ModuleInventaire.dao.dao_type_emplacement import dao_type_emplacement
from ModuleInventaire.dao.dao_operation_stock import dao_operation_stock
from ModuleInventaire.dao.dao_asset import dao_asset
from ErpBackOffice.dao.dao_droit import dao_droit
from ModuleConversation.dao.dao_notification import dao_notification
from ModuleConversation.dao.dao_temp_notification import dao_temp_notification
from ModuleInventaire.dao.dao_bon_retour import dao_bon_retour
from ModuleInventaire.dao.dao_ligne_retour import dao_ligne_bon_retour
from ModuleInventaire.dao.dao_rebut import dao_rebut
#from ModuleInventaire.dao.dao_stock_article import dao_stock_article
# Tableau de board
def get_dashboard(request):
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(7, request)
    if response != None:
        return response

    temp_notif_list = None
    temp_notif_count = 0
    NombreArticle = 0
    NombreTranfert = None
    NombreInventaire = 0
    OperationStock = None
    MouvementStock = None
    Article = None
    BonEntree = None
    model = None
    total_reception_bon = 0

    if auth.toCheckAdmin("Inventaire", utilisateur):

        model = dao_operation_stock.toListOperationsStockOfInventaire()
        total_reception_bon = dao_fourniture.toListBonsAchatEnAttente().count()

        #WAY OF NOTIFCATION
        module_name = "MODULE_INVENTAIRE"
        NombreTranfert = dao_bon_transfert.toListBonOfTypeBonTransmission()
        NombreSortie = dao_bon_transfert.toListBonOfTypeSortieMaterielle()
        NombreInventaire = dao_bon_inventaire.toListBonInventaire().count()
        OperationStock = dao_operation_stock.toListOperationsStock()
        MouvementStock = dao_mouvement_stock.toListMouvementStock()
        BonEntree = dao_bon_special.toListBonsEntrees()

    else:
        model = dao_operation_stock.toListOperationsStockOfInventaireByAuteur(utilisateur.id)
        total_reception_bon = dao_fourniture.toListBonsAchatEnAttenteByAuteur(utilisateur.id).count()

        #WAY OF NOTIFCATION
        module_name = "MODULE_INVENTAIRE"

        NombreTranfert = dao_bon_transfert.toListBonOfTypeBonTransmissionByAuteur(utilisateur.id)

        NombreSortie = dao_bon_transfert.toListBonOfTypeSortieMaterielleByAuteur(utilisateur.id)
        NombreInventaire = dao_bon_inventaire.toListBonInventaireByAuteur(utilisateur.id).count()
        OperationStock = dao_operation_stock.toListOperationsStockByAuteur(utilisateur.id)
        MouvementStock = dao_mouvement_stock.toListMouvementStockByAuteur(utilisateur.id)
        BonEntree = dao_bon_special.toListBonsEntreesByAuteur(utilisateur.id)

    Article = dao_emplacement.toListEmplacement()
    NombreArticle = dao_article.toListArticles().count()
    temp_notif_list = dao_temp_notification.toGetListTempNotificationUnread(identite.utilisateur(request).id, module_name)
    temp_notif_count = temp_notif_list.count()
    listNumber=dao_ligne_inventaire.ListeNumberInventoryByMunth()
    fourni=dao_ligne_inventaire.ListeNumberFournieByMunth()
    all_inventory=dao_ligne_inventaire.toListLigneInventaire()
    sortiMat = dao_bon_transfert.toListBonOfTypeSortieMaterielle().count()
    groupe_permission = dao_groupe_permission.toGetGroupePermissionDeLaPersonne(utilisateur.id)
    print("****groupe_permission.designation", groupe_permission)
    if groupe_permission != None:
        if groupe_permission.designation == 'Chef de bureau exploitation MG' or groupe_permission.designation == 'Chef de service MG':
            template = loader.get_template('ErpProject/ModuleInventaire/dashboard_SMG.html')
        elif groupe_permission.designation == "Assistant MG":
            template = loader.get_template('ErpProject/ModuleInventaire/dashboard_SMG.html')
        elif groupe_permission.designation == "Chef de bureau exploitation SI":
            template = loader.get_template('ErpProject/ModuleInventaire/dashboard_SI.html')
        else:
            template = loader.get_template('ErpProject/ModuleInventaire/index.html')
    else:
        template = loader.get_template('ErpProject/ModuleInventaire/index.html')

    year=[]
    for item in all_inventory:
        year.append(item.creation_date.year)

    year=set(year)

    context ={
        'modules':modules,'sous_modules':sous_modules,
        'title' : 'Tableau de Bord',
        'model' : model,
        'utilisateur' : utilisateur,
        'temp_notif_count':temp_notif_count,
        'temp_notif_list': temp_notif_list,
        'actions': auth.toGetActions(modules,utilisateur),
        'organisation': dao_organisation.toGetMainOrganisation(),
        'modules' : modules,
        "total_reception_bon" : total_reception_bon,
        'module' : ErpModule.MODULE_INVENTAIRE,
        'menu' : 2,
        'NombreArticle' : NombreArticle,
        'NombreTranfert' : NombreTranfert.count(),
        'ListeTransfert' : NombreTranfert[:5],
        'ListeSortie' : NombreSortie[:5],
        'NombreInventaire' : NombreInventaire,
        'OperationStock' : OperationStock[:3],
        'MouvementStock' : MouvementStock[:4],
        'Article' : Article[:3],
        'BonEntree' : BonEntree.count(),
        'ListeBon' : BonEntree[:5],
        'listNumber': listNumber,
        'fourni': fourni,
        'all_inventory': year,
        'sortiMat': sortiMat

    }
    # template = loader.get_template('ErpProject/ModuleInventaire/index.html')
    # template = loader.get_template('ErpProject/ModuleInventaire/dashboard_SMG.html')
    return HttpResponse(template.render(context, request))
# Tableau de board
def get_inventer_to_dashbord(request):
    try:
        mYear=request.GET['year']
        data=[]
        listNumber=dao_ligne_inventaire.ListeNumberInventoryByMunth(mYear)
        listNumberFournie=dao_ligne_inventaire.ListeNumberFournieByMunth(mYear)
        data=[listNumber,listNumberFournie]

        return JsonResponse(data, safe=False)
    except Exception as e:
        ##print("probleme get_inventer_to_dashbord %s"%(e))
        return JsonResponse([], safe=False)


def get_update_notification(request,ref):
	dao_temp_notification.toUpdateTempNotificationRead(ref)
	return get_dashboard(request)

# BON INVENTAIRE
def get_lister_bon_inventaire(request):
    permission_number = 38
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
    if response != None:
        return response

    #model = dao_bon_inventaire.toListBonInventaire()

    # model = dao_bon_inventaire.toListBonInventaire()
    #*******Filtre sur les règles **********#
    model = dao_model.toListModel(dao_bon_inventaire.toListBonInventaire(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#

    try:
	    view = str(request.GET.get("view","list"))
    except Exception as e:
	    view = "list"

    #Pagination
    model = pagination.toGet(request, model)

    context = {'modules':modules,'sous_modules':sous_modules,'title' : 'Liste des ajustements de stock','model' : model,'utilisateur' : utilisateur,
    'actions':auth.toGetActions(modules,utilisateur),'view' : view,
		'organisation': dao_organisation.toGetMainOrganisation(),
    'modules' : modules,'module' : ErpModule.MODULE_INVENTAIRE,'menu' : 2}
    template = loader.get_template('ErpProject/ModuleInventaire/bon_inventaire/list.html')
    return HttpResponse(template.render(context, request))

def get_creer_bon_inventaire(request):
    try:
        permission_number = 37
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        ##print("mam")
        type_emplacement_entrepot = dao_type_emplacement.toGetTypeEmplacementEntrepot()
        ##print(type_emplacement_entrepot)
        entrepot = dao_emplacement.toGetEmplacementEntrepot(type_emplacement_entrepot)

        if utilisateur.unite_fonctionnelle:
            if utilisateur.unite_fonctionnelle.emplacement != None:
                emplacements = dao_emplacement.toListEmplacementOfId(utilisateur.unite_fonctionnelle.emplacement.id)
            else:
                emplacements = dao_emplacement.toListEmplacementsInEntrepot(entrepot.id)
        else:
            emplacements = dao_emplacement.toListEmplacementsInEntrepot(entrepot.id)


        context = {
            'title' : 'Nouvel inventaire',
            'emplacements' : emplacements,
            'articles' : dao_article.toListArticlesStockables(),
            'categories' : dao_categorie_article.toListCategoriesArticle(),
            'utilisateur' : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
            'sous_modules': sous_modules,
            'organisation': dao_organisation.toGetMainOrganisation(),
            'modules' : modules,
            'module' : ErpModule.MODULE_INVENTAIRE,
            'menu' : 2
        }
        template = loader.get_template('ErpProject/ModuleInventaire/bon_inventaire/add.html')
        return HttpResponse(template.render(context, request))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_bon_inventaire'))

def get_demarrer_bon_inventaire(request):
    try:
        permission_number = 38
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        ##print("inventaire de", request.POST)
        inventaire_de = int(request.POST["inventaire_de"])
        # print('-----INVENTAIRE DE', inventaire_de)
        emplacement_id = int(request.POST["emplacement_id"])
        # print('-----EMPLACEMENT DE', emplacement_id)

        unite_fonctionnelle = dao_unite_fonctionnelle.toGetUniteFonctionnelleOfEmplacement(emplacement_id)
        ##print("Demarrer inventaire")

        emplacementsba = dao_emplacement.toGetEmplacementBySBA()

        #Par rapport aux choix du type d'inventaire, on recupère les données appropriées
        # inventaire_de = 0
        if inventaire_de == 0:
            articles = dao_article.toListArticlesOfServiceReferent(unite_fonctionnelle.id)
            categorie = None
            article = None
            categories = None
            # print('***JE SUIS DANS 0')

        if emplacementsba.id == emplacement_id :
            articles = dao_article.toListArticlesNonService()
            categorie = None
            article = None
            categories = None

        elif inventaire_de == 1:
            categorie_id = int(request.POST["categorie_id"])
            categorie = dao_categorie_article.toGetCagorieArticle(categorie_id)
            articles = dao_article.toListArticlesStockablesOfCategorie(categorie_id)
            article = None
            categories = None
            # print('***JE SUIS DANS 1')
        elif inventaire_de == 2:
            article_id = int(request.POST["article_id"])
            # print('Article ID', article_id)
            articles = dao_article.toListArticlesStockablesOfId(article_id)
            # print('articles', articles)
            article = dao_article.toGetArticle(article_id)
            categorie = None
            categories = None
            # print('***JE SUIS DANS 2')
        elif inventaire_de == 3:
            articles = dao_article.toListArticlesStockables()
            article = None
            categorie = None
            categories = dao_categorie_article.toListCategoriesArticle()
            # print('***JE SUIS DANS 3')

        emplacement = dao_emplacement.toGetEmplacement(emplacement_id)

        context = {
            'sous_modules':sous_modules,
            'title' : "Valider l'inventaire",
            "articles" : articles,
            "article" : article,
            "categorie" : categorie,
            "categories" : categories,
            "emplacement" : emplacement,
            "inventaire_de" : inventaire_de,
            "utilisateur" : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		    'organisation': dao_organisation.toGetMainOrganisation(),
            "modules" : modules ,
            "module" : ErpModule.MODULE_INVENTAIRE,
            'menu' : 6
        }
        template = loader.get_template("ErpProject/ModuleInventaire/bon_inventaire/validate.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_add_bon_inventaire'))


def get_lister_stock_emplacement(request):
    permission_number = 38
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
    if response != None:
        return response

    #type_emplacement_entrepot = dao_type_emplacement.toGetTypeEmplacementEntrepot()
    #warehouses = dao_unite_fonctionnelle.toListServiceHavingWareHouses()
    #*******Filtre sur les règles **********#
    model = dao_model.toListModel(dao_unite_fonctionnelle.toListServiceHavingWareHouses(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
    try:
	    view = str(request.GET.get("view","list"))
    except Exception as e:
	    view = "list"

    #Pagination
    model = pagination.toGet(request, model)

    context = {
        'sous_modules':sous_modules,
        'title' : "Liste des emplacements de stock",
        'model' : model,
        "utilisateur" : utilisateur,
        'view' : view,
        'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
        "modules" : modules,
        "module" : ErpModule.MODULE_INVENTAIRE,
        'menu': 9
    }
    template = loader.get_template("ErpProject/ModuleInventaire/stock/list.html")
    return HttpResponse(template.render(context, request))

def get_lister_asset_emplacement(request):
    permission_number = 38
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
    if response != None:
        return response

    #type_emplacement_entrepot = dao_type_emplacement.toGetTypeEmplacementEntrepot()
    # warehouses = dao_unite_fonctionnelle.toListServiceHavingWareHouses()
    #*******Filtre sur les règles **********#
    model = dao_model.toListModel(dao_unite_fonctionnelle.toListServiceHavingWareHouses(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#

    try:
	    view = str(request.GET.get("view","list"))
    except Exception as e:
	    view = "list"

    #Pagination
    model = pagination.toGet(request, model)

    context = {
        'sous_modules':sous_modules,
        'title' : "Liste des services référents",
        'model' : model,
        "utilisateur" : utilisateur,
        'view' : view,
        'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
        "modules" : modules,
        "module" : ErpModule.MODULE_INVENTAIRE,
        'menu': 9
    }
    template = loader.get_template("ErpProject/ModuleInventaire/asset_emplacement/list.html")
    return HttpResponse(template.render(context, request))

def get_details_stock_emplacement(request,ref):
    try:
        permission_number = 38
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response
        #on recupère l'Identifiant du service référent
        ref=int(ref)
        service_referent = dao_unite_fonctionnelle.toGetUniteFonctionnelle(ref)
        print("***SERVICE FIND", service_referent)

        if service_referent.emplacement.type_emplacement.designation == "IN":
            articles = dao_article.toListArticlesNonService()
        else:
            articles  = dao_article.toListArticlesOfServiceReferent(service_referent.id)
            print("***SERVICE ARTICLES", articles)

        try:
	        view = str(request.GET.get("view","list"))
        except Exception as e:
	        view = "list"

        historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,service_referent)

        context = {
            'sous_modules':sous_modules,
            'title' : "Lister le stock de " + service_referent.emplacement.designation,
            "articles": articles,
            "service_referent": service_referent,
            "utilisateur" : utilisateur,
            'ref': ref,
            'view' : view,
            "historique": historique,
            "etapes_suivantes": etapes_suivantes,
            "signee": signee,
            "content_type_id": content_type_id,
            "documents": documents,
            "roles": groupe_permissions,
            'actions':auth.toGetActions(modules,utilisateur),
		    'organisation': dao_organisation.toGetMainOrganisation(),
            "modules" : modules ,
            "module" : ErpModule.MODULE_INVENTAIRE,
            'menu' : 6
        }
        template = loader.get_template("ErpProject/ModuleInventaire/stock/item.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_stock_emplacements'))



def get_details_asset_emplacement(request,ref):
    try:
        permission_number = 38
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        #on recupère l'Identifiant du service référent
        ref=int(ref)

        if ref == 0:
            assets = dao_asset.toListAsset()
            # print('**Les assets sont:',assets)
            model = dao_model.toListModel(assets, permission_number, groupe_permissions, identite.utilisateur(request))
            title="Liste de tous les assets"
        else:
            service_referent = dao_unite_fonctionnelle.toGetUniteFonctionnelle(ref)
            print('***SERVICE REFERENT', service_referent)
            title= "Lister le stock de " + service_referent.emplacement.designation
            assets = dao_asset.toGetAssetByEmplacement(service_referent.emplacement_id)
            # print('ASSET', assets)
            #*******Filtre sur les règles **********#
            model = dao_model.toListModel(assets, permission_number, groupe_permissions, identite.utilisateur(request))
            #******* End Regle *******************#
            #Traitement des vues
        try:
            view = str(request.GET.get("view","list"))
        except Exception as e:
            view = "list"
        #Pagination
        model = pagination.toGet(request, model)
        historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,service_referent)

        context = {
            'sous_modules':sous_modules,
            'title' : title,
            "assets": model,
            "utilisateur" : utilisateur,
            "historique": historique,
            "etapes_suivantes": etapes_suivantes,
            "signee": signee,
            "content_type_id": content_type_id,
            "documents": documents,
            "roles": groupe_permissions,
            'view' : view,
            'ref':ref,
            'actions':auth.toGetActions(modules,utilisateur),
		    'organisation': dao_organisation.toGetMainOrganisation(),
            "modules" : modules ,
            "module" : ErpModule.MODULE_INVENTAIRE,
            'menu' : 6
        }
        template = loader.get_template("ErpProject/ModuleInventaire/asset_emplacement/item.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_stock_emplacements'))


@transaction.atomic
def post_creer_bon_inventaire(request):
    sid = transaction.savepoint()
    try:
        auteur = identite.utilisateur(request)
        numero_inventaire = request.POST['numero_inventaire']
        montant_global = 0
        date_inventaire = request.POST['date_inventaire']
        # LA DATE EST AU FORMAT : dd/mm/yyyy
        # ON PROCEDE A LA CONVERSION DU STRING EN DATETIME
        date_inventaire = timezone.datetime(int(date_inventaire[6:10]), int(date_inventaire[3:5]), int(date_inventaire[0:2]))
        est_realisee = True
        quantite = 0
        description = ""
        status = ""
        employe_id = auteur.id
        emplacement_id = request.POST['emplacement_id']
        reference_document = request.POST["reference_document"]



        #CREATION INVENTAIRE
        ##print("*************")
        bon_inventaire = dao_bon_inventaire.toCreateBonInventaire(numero_inventaire, date_inventaire ,employe_id, emplacement_id, status, description, montant_global, est_realisee, quantite)
        bon_inventaire = dao_bon_inventaire.toSaveBonInventaire(auteur,bon_inventaire)
        print("*************bon_inventaire", bon_inventaire)

        if bon_inventaire != None :
            print("Inventaire cree")
            list_article_id = request.POST.getlist('article_id', None)
            list_quantite_theorique = request.POST.getlist("quantite_demandee", None)
            list_quantite_reelle = request.POST.getlist("quantite_fournie", None)
            ##print("Nombre Article: ", list_article_id)
            print("Nombre qte theorique: ", list_quantite_theorique)
            print("Nombre qte reelle", list_quantite_reelle)
            ##print(bzb)
            qtt = 0
            for i in range(0, len(list_article_id)) :
                article_id = int(list_article_id[i])
                ##print("list_quantite_theorique:")
                ##print(list_quantite_theorique[i])
                ##print("list_quantite_reelle:")
                ##print(list_quantite_reelle[i])
                quantite_theorique = makeFloat(list_quantite_theorique[i])
                if quantite_theorique == 'INFINIE': 
                    qtt = 0
                    quantite_theorique=makeFloat(qtt)
                quantite_reelle = makeFloat(list_quantite_reelle[i])

                article = dao_article.toGetArticle(article_id)
                #On recupere le stock de l'article dans l'emplacement indiqué
                les_stocks = dao_stock_article.toListStocksOfArticleInEmplacement(article_id, emplacement_id)
                if les_stocks:
                    stock = les_stocks[0]
                    print("article", article)
                    ##print("article id", article_id)
                    #SI QTE REELLE DIFFERENT DE QTE THEORIQUE, ON MODIFIE LE STOCK DE L'EMPLACEMENT, ON CREE UN MOUVEMENT DE STOCK
                    if stock.quantite_disponible != quantite_reelle:
                        obj_dao_stock = dao_stock_article.toCreateStockArticle(article_id,quantite_reelle, emplacement_id)
                        stock_article = dao_stock_article.toUpdateStockArticle(stock.id, obj_dao_stock)
                        print("Stock Article", stock_article)

                        #ENREGISTRER LE MOUVEMENT
                        quantite_mouvement = quantite_reelle - stock.quantite_disponible
                        if quantite_mouvement > 0:
                            mouvement_stock = dao_mouvement_stock.toCreateMouvementStock(quantite_mouvement,"","INVENTAIRE",None,stock.id,None,None,bon_inventaire.id)
                        else:
                            quantite_mouvement = abs(quantite_mouvement)
                            mouvement_stock = dao_mouvement_stock.toCreateMouvementStock(quantite_mouvement,"","INVENTAIRE",stock.id,None,None,None,bon_inventaire.id)
                        mv = dao_mouvement_stock.toSaveMouvementStock(auteur, mouvement_stock)
                        print("mouvement id",mv)

                    #CREATION LIGNE INVENTAIRE
                    item_order = dao_ligne_inventaire.toCreateLigneInventaire(quantite_theorique,quantite_reelle,0,0,"INVENTAIRE", bon_inventaire.id, stock.id)
                    ligne_inventaire = dao_ligne_inventaire.toSaveLigneInventaire(auteur, item_order)
                    print("Ligne inventaire {0} creee ".format(ligne_inventaire.id))
            transaction.savepoint_commit(sid)
            messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
            return HttpResponseRedirect(reverse('module_inventaire_detail_bon_inventaire',args=(bon_inventaire.id,)))
        else:
            transaction.savepoint_rollback(sid)
            messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la création du bon")
            return HttpResponseRedirect(reverse('module_inventaire_add_bon_inventaire'))
    except Exception as e:
        module='ModuleInventaire'
        auteur = identite.utilisateur(request)
        monLog.error("{} :: {}::\nErreur lors du post: \n {}".format(auteur.nom_complet, module, e))
        ##print('Erreur lors du post')
        ##print(e)
        messages.add_message(request, messages.ERROR,e)
        return HttpResponseRedirect(reverse('module_inventaire_add_bon_inventaire'))

def get_details_bon_inventaire(request,ref):
    try:
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(7, request)

        if response != None:
            return response

        ref=int(ref)
        bon_inventaire=dao_bon_inventaire.toGetBonInventaire(ref)
        lignes = dao_ligne_inventaire.toListLignesInventaire(bon_inventaire.id)
        mouvements = dao_mouvement_stock.toListMouvementStockOfIventaire(bon_inventaire.id)
        historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,bon_inventaire)

        context = {
            'title' : "Details inventaire %s" % bon_inventaire.numero_inventaire,
            'model' : bon_inventaire,
            'utilisateur' : utilisateur,
             "historique": historique,
            "etapes_suivantes": etapes_suivantes,
            "signee": signee,
            "content_type_id": content_type_id,
            "documents": documents,
            "roles": groupe_permissions,
            'actions':auth.toGetActions(modules,utilisateur),
            'organisation': dao_organisation.toGetMainOrganisation(),
            'sous_modules': sous_modules,
            'modules' : modules,
            'module' : ErpModule.MODULE_INVENTAIRE,
            'lignes' : lignes,
            'mouvements' : mouvements,
            'menu' : 4
        }
        template = loader.get_template('ErpProject/ModuleInventaire/bon_inventaire/item.html')
        return HttpResponse(template.render(context, request))
    except Exception as e:
        auteur = identite.utilisateur(request)
        module='ModuleInventaire'
        monLog.error("{} :: {}::\nERREUR LORS DU CHARGEMENT DES DETAILS\n {}".format(auteur.nom_complet, module, e))
        monLog.debug("Info")
        ##print('Erreut Get Detail')
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_bon_inventaire'))


@transaction.atomic
def post_valider_inventaire_initial(request):
    ##print("Début Inventaire Initial 9*************************************************************")
    article_id = int(request.POST["article_id"])
    sid = transaction.savepoint()
    try:

        auteur = identite.utilisateur(request)
        date_inventaire = timezone.now()
        article = request.POST["article"]
        numero_inventaire = "Inventaire initial %s du %s - %s" % (article, date_inventaire.strftime("%d/%m/%Y"), date_inventaire.strftime("%H:%M:%S"))
        emplacement_id = int(request.POST["emplacement_id"])

        quantite_theorique = request.POST["quantite_theorique"]
        quantite_reelle = request.POST["quantite_reelle"]
        employe_id = auteur.id

        #CREATION INVENTAIRE
        bon_inventaire = dao_bon_inventaire.toCreateBonInventaire( numero_inventaire, date_inventaire ,employe_id, emplacement_id )
        bon_inventaire = dao_bon_inventaire.toSaveBonInventaire(auteur,bon_inventaire)

        if bon_inventaire != None :
            ##print("Inventaire cree")
            article = dao_article.toGetArticle(article_id)
            les_stocks = dao_stock_article.toListStocksOfArticleInEmplacement(article_id, emplacement_id)

            if les_stocks:
                stock = les_stocks[0]
                #SI QTE REELLE DIFFERENT DE QTE THEORIQUE, ON MODIFIE LE STOCK DE L'EMPLACEMENT, ON CREE UN MOUVEMENT DE STOCK
                if stock.quantite_disponible != quantite_reelle:
                    quantite_dispo = stock.quantite_disponible
                    obj_dao_stock = dao_stock_article.toCreateStockArticle(article_id, quantite_reelle, emplacement_id)
                    obj = dao_stock_article.toUpdateStockArticle(stock.id, obj_dao_stock)
                    # ##print("stock article {0} modifie ".format(stock.id))

                    #ENREGISTRER LE MOUVEMENT
                    # ##print("Inventaire mouvement stock 0", quantite_reelle)
                    quantite_mouvement = float(quantite_reelle) - quantite_dispo
                    # ##print("Inventaire mouvement stock 1", quantite_mouvement)
                    if quantite_mouvement > 0:
                        mouvement_stock = dao_mouvement_stock.toCreateMouvementStock(quantite_mouvement,"","INVENTAIRE",None,stock.id,None,None,bon_inventaire.id)
                        # ##print("Inventaire mouvement stock 1")
                    else:
                        quantite_mouvement = abs(quantite_mouvement)
                        mouvement_stock = dao_mouvement_stock.toCreateMouvementStock(quantite_mouvement,"","INVENTAIRE",stock.id,None,None,None,bon_inventaire.id)
                        ##print("Inventaire mouvement stock 2")
                    mouvement_stock = dao_mouvement_stock.toSaveMouvementStock(auteur, mouvement_stock)
                    ##print("mouvement stock {0} cree ".format(mouvement_stock.id))
            else:
                stock = dao_stock_article.toCreateStockArticle(article_id, quantite_reelle, emplacement_id)
                stock = dao_stock_article.toSaveStockArticle(stock)
                #ENREGISTRER LE MOUVEMENT
                quantite_mouvement = quantite_reelle
                if quantite_mouvement > 0:
                    mouvement_stock = dao_mouvement_stock.toCreateMouvementStock(quantite_mouvement,"","INVENTAIRE",None,stock.id,None,None,bon_inventaire.id)
                else:
                    quantite_mouvement = abs(quantite_mouvement)
                    mouvement_stock = dao_mouvement_stock.toCreateMouvementStock(quantite_mouvement,"","INVENTAIRE",stock.id,None,None,None,bon_inventaire.id)
                mouvement_stock = dao_mouvement_stock.toSaveMouvementStock(auteur, mouvement_stock)
                # ##print("mouvement stock {0} cree ".format(mouvement_stock.id))

            #CREATION LIGNE INVENTAIRE
            ##print("Qte Theorique", quantite_theorique)
            ##print("Qte Reelle", quantite_reelle)
            item_order = dao_ligne_inventaire.toCreateLigneInventaire(quantite_theorique,quantite_reelle,0,0,"INVENTAIRE", bon_inventaire.id, stock.id)
            ligne_inventaire = dao_ligne_inventaire.toSaveLigneInventaire(auteur, item_order)
            ##print("Ligne inventaire {0} creee ".format(ligne_inventaire.id))
            transaction.savepoint_commit(sid)
            return HttpResponseRedirect(reverse('module_inventaire_list_bon_inventaire'))
        else:
            transaction.savepoint_rollback(sid)
            return HttpResponseRedirect(reverse("module_inventaire_details_article", args=(article_id,)))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        transaction.savepoint_rollback(sid)
        messages.error(request,e)
        return HttpResponseRedirect(reverse("module_inventaire_details_article", args=(article_id,)))

# BON TRANSFERT
def get_lister_bon_transfert(request):
    permission_number = 45
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
    if response != None:
        return response

    title = "Liste des bons de transmission"

    if auth.toCheckAdmin("Inventaire", utilisateur):
        transferts = dao_bon_transfert.toListBonTransfert()
        #Type d'operation = Transfert interne
        operation_stock = dao_operation_stock.toGetOperationTransmission()
        transferts = dao_bon_transfert.toListTransfertsDuType(operation_stock.id)


    else:
        transferts = dao_bon_transfert.toListBonTransfertByAuteur(utilisateur.id)
        #Type d'operation = Transfert interne
        operation_stock = dao_operation_stock.toGetOperationTransmission()
        transferts = dao_bon_transfert.toListTransfertsDuType(operation_stock.id)


    # model = dao_article.toListArticles()

    #*******Filtre sur les règles **********#
    model = dao_model.toListModel(dao_article.toListArticles(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
    try:
	    view = str(request.GET.get("view","list"))
    except Exception as e:
	    view = "list"

    #Pagination
    transferts = pagination.toGet(request, transferts)

    context = {
        'sous_modules':sous_modules,
        'title' : title,
        'emplacements' : dao_emplacement.toListEmplacement(),
        'articles' : model,
        'transfert' : transferts,
        'view' : view,
        'categories' : dao_categorie_article.toListCategoriesArticle(),
        'utilisateur' : utilisateur,
        'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
        'modules' : modules,
        'module' : ErpModule.MODULE_INVENTAIRE,
        'menu' : 4
        }
    template = loader.get_template('ErpProject/ModuleInventaire/bon_transfert/list.html')
    return HttpResponse(template.render(context, request))

def get_creer_bon_transfert(request):
    try:
        permission_number = 46
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        type_emplacement= dao_type_emplacement.toGetTypeEmplacementEntree()
        emplacement = dao_emplacement.toGetEmplacementEntree(type_emplacement)
        services_referents = dao_unite_fonctionnelle.toListUniteFonctionnelleWHNoneService()

        #Liste des chargements des demandes en fonction de la demande rattachée au bon d'entrée ou sinon,
        # proposez toutes les demandes en attentes de traitement
        try:
            doc_id = request.POST["doc_id"]
            demandes_achat = dao_demande_achat.toListDemandeOfBonEntree(doc_id)
        except Exception as e:
            demandes_achat = dao_demande_achat.toListDemandesOfBonTransmission()

        context = {
            'sous_modules':sous_modules,
            'title' : "Nouveau bon de transmission",
            'serviceSMG':dao_unite_fonctionnelle.toGetUniteFonctionnelleOfEmplacement(emplacement.id),
            'type_emplacement_entre': dao_type_emplacement.toGetTypeEmplacementEntree(),
            'type_emplacement_stock': dao_type_emplacement.toGetTypeEmplacementStock(),
            'operation' : dao_operation_stock.toGetOperationTransmission(),
            'categories' : dao_categorie_article.toListCategoriesArticle(),
            'articles' : dao_article.toListArticlesStockables(),
            'demandes_achat':demandes_achat,
            'services_referents':services_referents,
            'utilisateur' : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
            'modules' : modules,
            'module' : ErpModule.MODULE_INVENTAIRE,
            'menu' : 4
        }
        template = loader.get_template('ErpProject/ModuleInventaire/bon_transfert/add.html')
        return HttpResponse(template.render(context, request))
    except Exception as e:
        auteur = identite.utilisateur(request)
        module='ModuleInventaire'
        monLog.error("{} :: {}::\nERREUR LORS DU CHARGEMENT dE LA PAGE DE CREATION BON TRANSFERT\n {}".format(auteur.nom_complet, module, e))
        monLog.debug("Info")
        ##print('Erreur creer bon transfert')
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_bon_transfert'))

def get_valider_bon_transfert(request):
    try:
        #Test de la validité de la date en fonction de l'activation d'une période dans un module
        if not auth.toPostValidityDate(var_module_id, request.POST["date_prevue"]): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")

        ##print('*****GET VALIDER BON TRANSFERT*******')
        permission_number = 46
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        operation_stock_id = int(request.POST["operation_stock_id"])
        operation_stock = dao_operation_stock.toGetOperationStock(operation_stock_id)

        demande_achat_id = int(request.POST["demande_achat_id"])
        demande_achat = dao_demande_achat.toGetDemande(demande_achat_id)

        emplacement_origine_id = int(request.POST["emplacement_origine_id"])
        emplacement_origine = dao_emplacement.toGetEmplacement(emplacement_origine_id)

        emplacement_destination_id = int(request.POST["emplacement_destination_id"])
        emplacement_destination = dao_emplacement.toGetEmplacement(emplacement_destination_id)

        date_prevu = request.POST["date_prevue"]

        context = {
            'sous_modules':sous_modules,
            'title' : "Valider le bon de transmission",
            "emplacement_origine" : emplacement_origine,
            "demande_achat":demande_achat,
            "emplacement_destination" : emplacement_destination,
            'operation_stock' : operation_stock,
            "utilisateur" : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		    'organisation': dao_organisation.toGetMainOrganisation(),
            "modules" : modules ,
            "module" : ErpModule.MODULE_INVENTAIRE,
            'menu' : 4,
            'date_prevu': date_prevu
        }
        template = loader.get_template("ErpProject/ModuleInventaire/bon_transfert/validate.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_add_bon_transfert'))

@transaction.atomic
def post_valider_bon_transfert(request):
    ''' Cette fonction crée un objet de type bon de transfert, mets à jour le statut du wkf de la demande d'achat si elle est attachée;
    La realisation effective du transfert des articles se fait dans la fonction post_realiser
    '''
    sid = transaction.savepoint()
    try:
        ##print('*****POST VALIDER BON TRANSFERT*******')
        numero_transfert = request.POST['numero']
        date_transfert = request.POST["date_prevue"]
        ##print('*****VALIDER BON TRANSFERT1*******', date_transfert)
        date_transfert = timezone.datetime(int(date_transfert[6:10]), int(date_transfert[3:5]), int(date_transfert[0:2]))
        ##print('*****VALIDER BON TRANSFERT2*******')
        emplacement_origine_id = int(request.POST["emplacement_origine_id"])
        emplacement_destination_id = int(request.POST["emplacement_destination_id"])

        operation_stock_id = int(request.POST["operation_stock_id"])
        ##print('*****VALIDER BON TRANSFERT3*******')
        reference_document = request.POST["reference_document"]
        demande_achat_id = request.POST["demande_achat_id"]
        description = ""
        auteur = identite.utilisateur(request)
        employe_id = auteur.id

        ##print("mama")
        bon_transfert = dao_bon_transfert.toCreateBonTransfert(numero_transfert, False, date_transfert, "BON TRANSMISSION",operation_stock_id, emplacement_origine_id,emplacement_destination_id,employe_id, reference_document, description)
        bon_transfert = dao_bon_transfert.toSaveBonTransfert(auteur, bon_transfert)
        #Ajout traitement service referent necessaire pour le worflow
        #Recuperation du service referent destinataire
        #Enregistrement du services ref en fonction de l'emplacement destinataire
        service_referent = dao_unite_fonctionnelle.toGetUniteFonctionnelleOfEmplacement(emplacement_destination_id)
        bon_transfert.services_ref = service_referent
        bon_transfert.save()
        #Fin traitement complementaire important pr Worflow

        ##print("geag")
        ##print(demande_achat_id)

        if ((demande_achat_id != 0) and (demande_achat_id != "") and (demande_achat_id != None)):
            bon_transfert.demande_achat_id = demande_achat_id
            bon_transfert.save()
            demande_achat = dao_demande_achat.toGetDemande(demande_achat_id)

            #Flow de transition
            wkf_task.passingStepWorkflow(auteur,demande_achat)
            bon_entree = dao_bon_special.toGetBonEntreeOfDemande(demande_achat.id)
            wkf_task.passingStepWorkflow(auteur, bon_entree)

            #Mise à jour de la demande d'achat

        if bon_transfert != None :
            ##print("Ligne transfert {0} creee ".format(bon_transfert.id))
            list_article_id = request.POST.getlist('article_id', None)
            list_quantite_demandee = request.POST.getlist("quantite_demandee", None)
            list_quantite_fournie = request.POST.getlist("quantite_fournie", None)
            list_description = request.POST.getlist("description", None)
            for i in range(0, len(list_article_id)) :
                article_id = int(list_article_id[i])
                quantite_demandee = makeFloat(list_quantite_demandee[i])
                quantite_fournie = makeFloat(list_quantite_fournie[i])
                description = list_description[i]

                article = dao_article.toGetArticle(article_id)
                les_stocks = dao_stock_article.toListStocksOfArticleInEmplacement(article_id, emplacement_origine_id)
                stock = les_stocks[0]

                ligne_transfert = dao_ligne_transfert.toCreateLigneTransfert(bon_transfert.id, stock.id, quantite_demandee, quantite_fournie,'',description)
                ligne_transfert = dao_ligne_transfert.toSaveLigneTransfert(auteur, ligne_transfert)
                ##print("Ligne transfert {0} creee ".format(ligne_transfert.id))

            # WORKFLOWS INITIALS
            type_document = "Bon de transmission"
            wkf_task.initializeWorkflow(auteur,bon_transfert, type_document)

            transaction.savepoint_commit(sid)
            messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
            return HttpResponseRedirect(reverse('module_inventaire_detail_bon_transfert', args=(bon_transfert.id,)))
        else:
            transaction.savepoint_rollback(sid)
            return HttpResponseRedirect(reverse('module_inventaire_list_bon_transfert'))

    except Exception as e:
        module='ModuleInventaire'
        auteur = identite.utilisateur(request)
        monLog.error("{} :: {}::\nErreur lors de l'enregistrement\n {}".format(auteur.nom_complet, module, e))
        ##print('Erreur lors de l enregistrement')
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_add_bon_transfert'))

def get_realiser_bon_transfert(request, ref):
    try:
        permission_number = 46
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response
        ref = int(ref)
        bon_transfert = dao_bon_transfert.toGetBonTransfert(ref)

        if bon_transfert.est_realisee == True: return HttpResponseRedirect(reverse('module_inventaire_list_bon_inventaire'))

        lignes = dao_ligne_transfert.toListLignesTransfert(bon_transfert.id)
        item = lignes[0]
        stock = dao_stock_article.toGetStockArticle(item.stock_article_id)
        emplacement_origine = dao_emplacement.toGetEmplacement(stock.emplacement_id)
        mybon_transfert = dao_bon_transfert.toGetBonTransfert(ref)
        emplacement_destination = dao_emplacement.toGetEmplacement(mybon_transfert.emplacement_destination.id)
        # print('EMP Origine', dao_unite_fonctionnelle.toGetUniteFonctionnelleOfEmplacement(emplacement_origine.id))
        # print('EMP Dest', dao_unite_fonctionnelle.toGetUniteFonctionnelleOfEmplacement(emplacement_destination.id))
        context = {
            'sous_modules':sous_modules,
            'title' : "Bon de transmission N°%s" % bon_transfert.numero_transfert,
            'model' : bon_transfert,
            'lignes' : lignes,
            #"emplacement_origine" : emplacement_origine,
            "service_referent_origine" : dao_unite_fonctionnelle.toGetUniteFonctionnelleOfEmplacement(emplacement_origine.id),
            "service_referent_destination" : dao_unite_fonctionnelle.toGetUniteFonctionnelleOfEmplacement(emplacement_destination.id),
            "agents" : dao_employe.toListEmployesActifs(),
            "utilisateur" : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		    'organisation': dao_organisation.toGetMainOrganisation(),
            "modules" : modules ,
            "module" : ErpModule.MODULE_INVENTAIRE,
            'menu' : 4
        }
        template = loader.get_template("ErpProject/ModuleInventaire/bon_transfert/release.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_bon_transfert'))

@transaction.atomic
def post_realiser_bon_transfert(request):
    sid = transaction.savepoint()
    ordre_id = int(request.POST["ordre_id"])
    try:
        auteur = identite.utilisateur(request)
        responsable_id = int(request.POST["responsable_id"])
        est_realisee = True

        bon_transfert = dao_bon_transfert.toGetBonTransfert(ordre_id)
        operation_stock = dao_operation_stock.toGetOperationStock(bon_transfert.operation_stock_id)
        emplacement_destination = dao_emplacement.toGetEmplacement(bon_transfert.emplacement_destination_id)
        list_ligne_id = request.POST.getlist('ligne_id', None)
        list_quantite_fournie = request.POST.getlist("quantite_fournie", None)
        ##print(len(list_ligne_id))
        ##print(len(list_quantite_fournie))
        ##print("Panda Djila")
        for i in range(0, len(list_ligne_id)):
            ligne_id = int(list_ligne_id[i])
            quantite_recue = makeFloat(list_quantite_fournie[i])

            ligne_transfert = dao_ligne_transfert.toGetLigneTransfert(ligne_id)
            #Si la quantité demandée est superieure à la somme des quantitées déjà fournies, on n'est réalise pas pcq on n'a pas encore tout reçu
            if quantite_recue > ligne_transfert.quantite_fournie :
                messages.add_message(request, messages.ERROR,'La quantité entrée est supérieure à celle attendue')
                return HttpResponseRedirect(reverse('module_inventaire_realiser_bon_transfert', args=(ordre_id,)))
            #if ligne_transfert.quantite_demandee > ligne_transfert.quantite_fournie + quantite_fournie : est_realisee = False

            # On ajoute la nouvelle quantité reçue
            ligne_transfert.quantite_fournie = quantite_recue
            dao_ligne_transfert.toUpdateLigneTransfert(ligne_id, ligne_transfert)

            # On recuper le stock de l'article dans l'emplacement de destination pour transfert
            stock_depart = dao_stock_article.toGetStockArticle(ligne_transfert.stock_article_id)
            ##print("stock depart",stock_depart)
            list_stocks_destination = dao_stock_article.toListStocksOfArticleInEmplacement(stock_depart.article_id, emplacement_destination.id)
            if list_stocks_destination: stock_destination = list_stocks_destination[0]
            else:
                # Si il ya pas de stock pour cet article dans cet emplacement, on crée un nouveau stock
                ##print("creatio stock")
                ##print("empladement destination", emplacement_destination)
                stock_destination = dao_stock_article.toCreateStockArticle(stock_depart.article_id,0,emplacement_destination.id)
                stock_destination = dao_stock_article.toSaveStockArticle(stock_destination)

            ##print("stock_destination", stock_destination)
            # DIMINUTION DE LA QUANTITE DU STOCK D'ORIGINE
            stock_depart.quantite_disponible = stock_depart.quantite_disponible - quantite_recue
            dao_stock_article.toUpdateStockArticle(stock_depart.id, stock_depart)

            # AUGMENTATION DE LA QUANTITE DU STOCK DE DESTINATION
            stock_destination.quantite_disponible = stock_destination.quantite_disponible + quantite_recue
            dao_stock_article.toUpdateStockArticle(stock_destination.id, stock_destination)

            #ENREGISTRER LE MOUVEMENT
            if quantite_recue > 0:
                mouvement_stock = dao_mouvement_stock.toCreateMouvementStock(quantite_recue,"","TRANSFERT",stock_depart.id, stock_destination.id,None,None,None,ordre_id)
                dao_mouvement_stock.toSaveMouvementStock(auteur, mouvement_stock)

        bon_transfert.est_realisee = est_realisee
        if est_realisee == True :
            bon_transfert.date_realisation = timezone.now()

        bon_transfert.responsable_id = responsable_id
        is_done = dao_bon_transfert.toUpdateBonTransfert(ordre_id, bon_transfert)

        #Flow
        wkf_task.passingStepWorkflow(auteur,bon_transfert)

        if is_done == True :
            transaction.savepoint_commit(sid)
            return HttpResponseRedirect(reverse('module_inventaire_detail_bon_transfert', args=(ordre_id,)))
        else:
            transaction.savepoint_rollback(sid)
            return HttpResponseRedirect(reverse('module_inventaire_realiser_bon_transfert', args=(ordre_id,)))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        transaction.savepoint_rollback(sid)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_realiser_bon_transfert', args=(ordre_id,)))


def get_to_asset_of_bon_transfert(request):
    sid = transaction.savepoint()
    ordre_id = int(request.POST["doc_id"])
    try:
        permission_number = 46
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        dico_asset = {}
        auteur = identite.utilisateur(request)
        est_realisee = True

        bon_transfert = dao_bon_transfert.toGetBonTransfert(ordre_id)
        emplacement_origine = dao_emplacement.toGetEmplacement(bon_transfert.emplacement_origine_id)
        emplacement_destination = dao_emplacement.toGetEmplacement(bon_transfert.emplacement_destination_id)
        list_ligne_id = request.POST.getlist('ligne_id', None)
        list_quantite_fournie = request.POST.getlist("quantite_fournie", None)

        is_done = True
        lignes = dao_ligne_transfert.toListLignesTransfert(ordre_id)
        for ligne in lignes:
            dico_asset[ligne.article_identifiant] = dao_asset.toGetAssetByArticleOfEmplacement(ligne.article_identifiant, emplacement_origine.id)

        if is_done == True :

            lignes = dao_ligne_transfert.toListLignesTransfert(ordre_id)
            bon_transfert = dao_bon_transfert.toGetBonTransfert(ordre_id)
            #serv_ref_id = request.POST["service_referent_id"]
            service_referent = dao_unite_fonctionnelle.toGetUniteFonctionnelleOfEmplacement(bon_transfert.emplacement_destination_id)
            context = {
                'sous_modules':sous_modules,
                'title' : "Affecter les assets relatifs au bon N°%s" % bon_transfert.numero_transfert,
                'model' : bon_transfert,
                'lignes' : lignes,
                "service_referent" : service_referent,
                "dico_asset":dico_asset,
                "utilisateur" : utilisateur,
                "module" : ErpModule.MODULE_INVENTAIRE,
                'actions':auth.toGetActions(modules,utilisateur),
		        'organisation': dao_organisation.toGetMainOrganisation(),
                "modules": modules,
                'roles':groupe_permissions,
                'ordre_id':ordre_id,
                'list_quantite_fournie':list_quantite_fournie,
                'menu' : 11
            }

            template = loader.get_template("ErpProject/ModuleInventaire/bon_transfert/affect.html")
            return HttpResponse(template.render(context, request))
        else:

            return HttpResponseRedirect(reverse('module_inventaire_realiser_transfert_internal', args=(ordre_id,)))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_realiser_transfert_internal', args=(ordre_id,)))

@transaction.atomic
def post_to_asset_of_bon_transfert(request):
    sid = transaction.savepoint()
    ordre_id = int(request.POST["ordre_id"])
    try:
        ##print("ensemble a la fin")

        auteur = identite.utilisateur(request)
        bon_transfert = dao_bon_transfert.toGetBonTransfert(ordre_id)

        #Flow
        bon_transfert = dao_bon_transfert.toGetBonTransfert(ordre_id)
        wkf_task.passingStepWorkflow(auteur,bon_transfert)


        #Traitement des assets
        ##print("tranquil")


        list_asset_id = request.POST.getlist('asset_id', None)
        #service_ref_id = request.POST["service_referent_id"]
        #service_referent = dao_unite_fonctionnelle.toGetUniteFonctionnelle(service_ref_id)
        service_referent = dao_unite_fonctionnelle.toGetUniteFonctionnelleOfEmplacement(bon_transfert.emplacement_destination_id)
        ##print("service ref", service_referent, service_referent.id)
        for i in range(0, len(list_asset_id)):
            ##print("inside ")
            asset_id = list_asset_id[i]
            ##print(asset_id)
            asset = dao_asset.toUpdateAssetAffectation(asset_id,None, service_referent.emplacement_id)
            asset_historique = dao_asset_historique.toCreateAssetHistorique(bon_transfert.numero_transfert,"",asset_id,bon_transfert,None)
            asset_historique = dao_asset_historique.toSaveAssetHistorique(auteur,asset_historique)
            ##print("asset", asset)
            ##print(asset_historique)

        ##print(erreur)



        transaction.savepoint_commit(sid)
        return HttpResponseRedirect(reverse('module_inventaire_detail_bon_transfert', args=(ordre_id,)))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        transaction.savepoint_rollback(sid)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_detail_bon_transfert', args=(ordre_id,)))


def get_details_bon_transfert(request,ref):
    try:
        permission_number = 45
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response
        ref=int(ref)
        bon_transfert=dao_bon_transfert.toGetBonTransfert(ref)
        est_integrale = True
        lignes = dao_ligne_transfert.toListLignesTransfert(ref)
        for ligne in lignes:
            if ligne.quantite_demandee > ligne.quantite_fournie:
                est_integrale = False
                break
        item = lignes[0]

        historique, transition_etape_suivant, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,bon_transfert)
        titre_document = "APERCU DE L'ETAT DE RECEPTION"
        est_printable = False
        #Si fin de processus d'arbitrage
        if (bon_transfert.statut.designation == "Bon de reception créé") or (bon_transfert.statut.designation == "Articles enregistrés"):
            titre_document = "BON DE RECEPTION"
            est_printable = True
            est_integrale = True

        historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,bon_transfert)

        context = {
            'sous_modules':sous_modules,
            'title' : bon_transfert.numero_transfert,
            'model' : bon_transfert,
            'titre_document': titre_document,
            'lignes' : lignes,
            "historique": historique,
            "etapes_suivantes": etapes_suivantes,
            "signee": signee,
            "content_type_id": content_type_id,
            "documents": documents,
            "roles": groupe_permissions,
            'est_printable':est_printable,
            'est_integrale':est_integrale,
            'content_type_id':content_type_id,
            'historique':historique,
            'roles':groupe_permissions,
            'documents':documents,
            'etapes_suivantes':transition_etape_suivant,
            'service_referent_origine' : dao_unite_fonctionnelle.toGetUniteFonctionnelleOfEmplacement(bon_transfert.emplacement_origine.id),
            'service_referent_beneficiaire':dao_unite_fonctionnelle.toGetUniteFonctionnelleOfEmplacement(bon_transfert.emplacement_destination.id),
            'utilisateur' : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		    'organisation': dao_organisation.toGetMainOrganisation(),
            'modules' : modules,
            'module' : ErpModule.MODULE_INVENTAIRE,
            'menu' : 11
        }
        template = loader.get_template('ErpProject/ModuleInventaire/bon_transfert/item.html')
        return HttpResponse(template.render(context, request))
    except Exception as e:
        auteur = identite.utilisateur(request)
        module='ModuleInventaire'
        monLog.error("{} :: {}::\nERREUR LORS DU CHARGEMENT DES DETAILS\n {}".format(auteur.nom_complet, module, e))
        monLog.debug("Info")
        ##print('Erreut Get Detail')
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_bon_transfert'))

def get_completer_bon_transfert(request, ref):
    try:
        permission_number = 45
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        ref = int(ref)
        bon_transfert = dao_bon_transfert.toGetBonTransfert(ref)
        est_integrale = True
        lignes = dao_ligne_transfert.toListLignesTransfert(bon_transfert.id)
        for ligne in lignes:
            if ligne.quantite_demandee > ligne.quantite_fournie:
                est_integrale = False
                break
        ##print(bon_transfert)
        if ((bon_transfert.est_realisee == True) and (est_integrale == True)) : return HttpResponseRedirect(reverse('module_inventaire_list_bon_inventaire'))

        item = lignes[0]
        stock = dao_stock_article.toGetStockArticle(item.stock_article_id)
        emplacement_origine = dao_emplacement.toGetEmplacement(stock.emplacement_id)
        context = {
            'sous_modules':sous_modules,
            'title' : "Bon de transmission N°%s" % bon_transfert.numero_transfert,
            'model' : bon_transfert,
            'lignes' : lignes,
            "emplacement_origine" : emplacement_origine,
            "agents" : dao_employe.toListEmployesActifs(),
            "utilisateur" : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
            "modules" : modules ,
            "module" : ErpModule.MODULE_INVENTAIRE,
            'menu' : 4
        }
        template = loader.get_template("ErpProject/ModuleInventaire/bon_transfert/complete.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_bon_transfert'))


@transaction.atomic
def post_completer_bon_transfert(request):
    sid = transaction.savepoint()
    ordre_id = int(request.POST["ordre_id"])
    try:
        auteur = identite.utilisateur(request)
        responsable_id = int(request.POST["responsable_id"])
        est_realisee = True
        ##print("nakati")

        bon_transfert = dao_bon_transfert.toGetBonTransfert(ordre_id)
        operation_stock = dao_operation_stock.toGetOperationStock(bon_transfert.operation_stock_id)
        emplacement_destination = dao_emplacement.toGetEmplacement(bon_transfert.emplacement_destination_id)
        list_ligne_id = request.POST.getlist('ligne_id', None)
        list_quantite_fournie = request.POST.getlist("quantite_fournie", None)
        ##print(len(list_ligne_id))
        ##print(len(list_quantite_fournie))
        for i in range(0, len(list_ligne_id)):
            ligne_id = int(list_ligne_id[i])
            quantite_recue = makeFloat(list_quantite_fournie[i])

            ligne_transfert = dao_ligne_transfert.toGetLigneTransfert(ligne_id)
            #Si la quantité demandée est superieure à la somme des quantitées déjà fournies, on n'est réalise pas pcq on n'a pas encore tout reçu
            if (quantite_recue + ligne_transfert.quantite_fournie) > ligne_transfert.quantite_demandee : return HttpResponseRedirect(reverse('module_inventaire_compleyer_bon_transfert', args=(ordre_id,)))
            #if ligne_transfert.quantite_demandee > ligne_transfert.quantite_fournie + quantite_fournie : est_realisee = False

            # On ajoute la nouvelle quantité reçue
            ##print(ligne_transfert.quantite_fournie)
            ligne_transfert.quantite_fournie = ligne_transfert.quantite_fournie + quantite_recue
            ##print(quantite_recue)
            ##print(ligne_transfert.quantite_fournie)
            #breakpoint
            dao_ligne_transfert.toUpdateLigneTransfert(ligne_id, ligne_transfert)

            # On recuper le stock de l'article dans l'emplacement de destination pour transfert
            stock_depart = dao_stock_article.toGetStockArticle(ligne_transfert.stock_article_id)
            list_stocks_destination = dao_stock_article.toListStocksOfArticleInEmplacement(stock_depart.article_id, emplacement_destination.id)
            if list_stocks_destination: stock_destination = list_stocks_destination[0]
            else:
                # Si il ya pas de stock pour cet article dans cet emplacement, on crée un nouveau stock
                stock_destination = dao_stock_article.toCreateStockArticle(0, emplacement_destination.id, stock_depart.article_id)
                stock_destination = dao_stock_article.toSaveStockArticle(auteur, stock_destination)

            # DIMINUTION DE LA QUANTITE DU STOCK D'ORIGINE
            stock_depart.quantite_disponible = stock_depart.quantite_disponible - quantite_recue
            dao_stock_article.toUpdateStockArticle(stock_depart.id, stock_depart)

            # AUGMENTATION DE LA QUANTITE DU STOCK DE DESTINATION
            stock_destination.quantite_disponible = stock_destination.quantite_disponible + quantite_recue
            dao_stock_article.toUpdateStockArticle(stock_destination.id, stock_destination)

            #ENREGISTRER LE MOUVEMENT
            if quantite_recue > 0:
                mouvement_stock = dao_mouvement_stock.toCreateMouvementStock(quantite_recue,"","TRANSFERT",stock_depart.id, stock_destination.id,None,None,None,ordre_id)
                dao_mouvement_stock.toSaveMouvementStock(auteur, mouvement_stock)

        bon_transfert.est_realisee = est_realisee
        if est_realisee == True :
            bon_transfert.date_realisation = timezone.now()

        bon_transfert.employe_id = responsable_id
        is_done = dao_bon_transfert.toUpdateBonTransfert(ordre_id, bon_transfert)


        if is_done == True :
            transaction.savepoint_commit(sid)
            return HttpResponseRedirect(reverse('module_inventaire_detail_bon_transfert', args=(ordre_id,)))
        else:
            transaction.savepoint_rollback(sid)
            return HttpResponseRedirect(reverse('module_inventaire_compleyer_bon_transfert', args=(ordre_id,)))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        transaction.savepoint_rollback(sid)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_completer_bon_transfert', args=(ordre_id,)))


@transaction.atomic
def post_workflow_bon_transfert(request):
    sid = transaction.savepoint()
    try:
        utilisateur_id = request.user.id
        auteur = identite.utilisateur(request)
        base_dir = settings.BASE_DIR
        media_dir = settings.MEDIA_ROOT
        media_url = settings.MEDIA_URL
        etape_id = request.POST["etape_id"]
        transfert_id = request.POST["doc_id"]

        ##print("print 1 %s %s %s" % (utilisateur_id, etape_id, transfert_id))

        employe = dao_employe.toGetEmployeFromUser(utilisateur_id)
        etape = dao_wkf_etape.toGetEtapeWorkflow(etape_id)
        bon_transfert = dao_bon_transfert.toGetBonTransfert(transfert_id)

        service_ref = dao_unite_fonctionnelle.toGetUniteFonctionnelleOfEmplacement(bon_transfert.emplacement_destination.id)
        ##print("service ", service_ref)


        ##print("print 2 %s %s %s " % (employe, etape, bon_transfert))


        if (bon_transfert.statut.designation == "Crée"):
            transitions_etapes_suivantes = dao_wkf_etape.toListEtapeSuivante(bon_transfert.statut_id)
            ##print("abba")
        else:
            transitions_etapes_suivantes = dao_wkf_etape.toListEtapeSuivante(bon_transfert.statut_id, service_ref.id)
            ##print("asjdksdjs")

        ##print("transition", transitions_etapes_suivantes)

        for item in transitions_etapes_suivantes:
            ##print("mammaamamma")
            if item.condition.designation == "Upload":
                ##print("Upload")
                if 'file_upload' in request.FILES:
                    nom_fichier = request.FILES['file_upload']
                    doc = dao_document.toUploadDocument(auteur, nom_fichier, bon_transfert)

                    bon_transfert.statut_id = etape.id
                    bon_transfert.etat = etape.designation
                    bon_transfert.save()
                    document = dao_document_bon_transfert.toCreateDocument("Bon de sortie de matériel",doc.url_document, bon_transfert.etat,transfert_id)
                    document = dao_document_bon_transfert.toSaveDocument(auteur, document)

                    ##print("docu saved")
                else:
                    pass

            else:
                ##print("haut")
                # Gestion des transitions dans le document
                bon_transfert.statut_id = etape.id
                bon_transfert.etat = etape.designation
                ##print("haut", bon_transfert)

                ##print("haut")

        bon_transfert.save()
        historique = dao_wkf_historique_bon_transfert.toCreateHistoriqueWorkflow(employe.id, etape.id, bon_transfert.id)
        historique = dao_wkf_historique_bon_transfert.toSaveHistoriqueWorkflow(historique)
        ##print("ho", historique)

        if historique != None :
            transaction.savepoint_commit(sid)
            #return HttpResponseRedirect(reverse('module_achat_details_bon_achat', args=(demande.id,)))
            ##print("OKAY")
            return HttpResponseRedirect(reverse('module_inventaire_detail_bon_transfert', args=(transfert_id,)))
        else:
            transaction.savepoint_rollback(sid)
            return HttpResponseRedirect(reverse('module_inventaire_detail_bon_transfert', args=(transfert_id,)))

    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        transaction.savepoint_rollback(sid)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_bon_transfert'))

# MOUVEMENTS DE STOCK CONTROLLER
def get_lister_mouvement_stock(request):
    permission_number = 51
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
    if response != None:
        return response

    #model = dao_mouvement_stock.toListMouvementStock()

    # model = dao_mouvement_stock.toListMouvementStock()
    #*******Filtre sur les règles **********#
    model = dao_model.toListModel(dao_mouvement_stock.toListMouvementStock(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
    context = {
        'sous_modules':sous_modules,
        'title' : "Liste des mouvements de stock",
        'model' : model,
        'utilisateur' : utilisateur,
        'modules' : modules,
        'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
        'module' : ErpModule.MODULE_INVENTAIRE,
        'menu' : 2
    }
    template = loader.get_template('ErpProject/ModuleInventaire/mouvement_stock/list.html')
    return HttpResponse(template.render(context, request))


def get_details_mouvement_stock(request,ref):
    try:
        permission_number = 51
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        ref=int(ref)
        mouvement_stock=dao_mouvement_stock.toGetMouvementStock(ref)
        historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,mouvement_stock)

        context = {
            'sous_modules':sous_modules,
            'title' : 'Details d une mouvement_stock',
            'mouvement_stock' : mouvement_stock,
            'utilisateur' : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		    'organisation': dao_organisation.toGetMainOrganisation(),
            'modules' : modules,
            'module' : ErpModule.MODULE_INVENTAIRE,
            "historique": historique,
            "etapes_suivantes": etapes_suivantes,
            "signee": signee,
            "content_type_id": content_type_id,
            "documents": documents,
            "roles": groupe_permissions,
            'menu' : 4
        }
        template = loader.get_template('ErpProject/ModuleInventaire/mouvement_stock/item.html')
        return HttpResponse(template.render(context, request))
    except Exception as e:
        auteur = identite.utilisateur(request)
        module='ModuleInventaire'
        monLog.error("{} :: {}::\nERREUR LORS DU CHARGEMENT DES DETAILS\n {}".format(auteur.nom_complet, module, e))
        monLog.debug("Info")
        ##print('Erreut Get Detail')
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_mouvement_stock'))

def get_lister_mouvements_stock_article(request, ref):
    try:
        permission_number = 52
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        mouvements = []
        ref = int(ref)
        # models = dao_mouvement_stock.toListMouvementStock()
        #*******Filtre sur les règles **********#
        models = dao_model.toListModel(dao_mouvement_stock.toListMouvementStock(), permission_number, groupe_permissions, identite.utilisateur(request))
	    #******* End Regle *******************#
        for model in models :
            if model.article.id == ref: mouvements.append(model)

        context = {
            'sous_modules':sous_modules,
            'title' : "Liste des mouvements de stock",
            'model' : mouvements,
            "utilisateur" : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
            "modules" : modules ,
            "module" : ErpModule.MODULE_INVENTAIRE,
            'menu': 7
        }
        template = loader.get_template("ErpProject/ModuleInventaire/mouvement_stock/article/list.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_details_article'), args=(ref,))


# ARTICLES STOCKABLES CONTROLLER
def get_lister_articles_stockables(request):
    permission_number = 41
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
    if response != None:
        return response

    model = dao_article.toListArticlesStockables()
    print("****LES ARTICLES STOCKABLE", model)

    #*******Filtre sur les règles **********#
    models = dao_model.toListModel(model, permission_number, groupe_permissions, identite.utilisateur(request))
    #******* End Regle *******************#
    try:
        view = str(request.GET.get("view","list"))
    except Exception as e:
        view = "list"

    #Pagination
    model = pagination.toGet(request, model)

    context = {
        'sous_modules':sous_modules,
        'title' : "Liste des articles stockables",
        'model' : model,
        'types_article' : dao_type_article.toListTypesArticle(),
        'devise_ref' : dao_devise.toGetDeviseReference(),
        "modules" : modules ,
        'view' : view,
        'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
        'utilisateur':utilisateur,
        "module" : ErpModule.MODULE_INVENTAIRE,
        'menu' : 5
    }
    template = loader.get_template("ErpProject/ModuleInventaire/article/list.html")
    return HttpResponse(template.render(context, request))

def get_creer_article(request):
    permission_number = 42
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
    if response != None:
        return response

    if utilisateur.unite_fonctionnelle != None:
        dep_entrepots = dao_unite_fonctionnelle.toListOfOneUniteFonctionnelle(utilisateur.unite_fonctionnelle.id)
    else:
        dep_entrepots = dao_unite_fonctionnelle.toListUniteFonctionnelleWH()

    context = {
        'sous_modules':sous_modules,
        'title' : 'Nouvel article',
        'unites' : dao_unite.toListUnite(),
        'fournisseurs' : dao_fournisseur.toListFournisseursActifs(),
        'types_article' : dao_type_article.toListTypesArticle(),
        'categories' : dao_categorie_article.toListCategoriesArticle(),
        'devise_ref' : dao_devise.toGetDeviseReference(),
        'warehouses':dep_entrepots,
        "modules" : modules ,
        'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
        'utilisateur': utilisateur,
        "module" : ErpModule.MODULE_INVENTAIRE,
        'menu' : 5
    }
    template = loader.get_template("ErpProject/ModuleInventaire/article/add.html")
    return HttpResponse(template.render(context, request))

@transaction.atomic
def post_creer_article(request):
    sid = transaction.savepoint()
    try:
        auteur = identite.utilisateur(request)
        base_dir = settings.BASE_DIR
        media_dir = settings.MEDIA_ROOT
        media_url = settings.MEDIA_URL
        designation = request.POST["designation"]
        unite_id = request.POST["unite_id"]

        est_vendable = False
        if "est_vendable" in request.POST : est_vendable = True

        est_achetable = False
        if "est_achetable" in  request.POST : est_achetable = True

        est_manufacturable = False
        if "est_manufacturable" in request.POST : est_manufacturable = True

        est_stockable = False
        if "est_stockable" in request.POST : est_stockable = True

        est_amortissable = False
        if "est_amortissable" in request.POST : est_amortissable = True

        designation_court = request.POST["designation_court"]
        code_article = request.POST["code_article"]
        code_barre = ""
        type_article = int(request.POST["type_article"])
        categorie_id = int(request.POST["categorie_id"])
        prix_unitaire = makeFloat(request.POST["prix_unitaire_article"])
        service_ref_id = int(request.POST['service_ref_id'])
        image = ""

        ##print("TYPE ARTICLE %s" % type_article)
        ##print("CATEGORIE ARTICLE %s" % categorie_id)


        article = dao_article.toCreateArticle(image, designation, unite_id, est_vendable, est_achetable, est_manufacturable, est_stockable, designation_court, code_article, code_barre, type_article, categorie_id, prix_unitaire, None, est_amortissable,service_ref_id)
        article = dao_article.toSaveArticle(auteur, article)

        ##print("ARTICLES SAVED %s" % article)


        if article != None :

            # CREATION DES STOCKS POUR L'ARTICLE
            # SCTOCK EMPLACEMENT D'ENTREE
            '''if article.est_achetable == True :
                type_emplacement = dao_type_emplacement.toGetTypeEmplacementEntree()
                ##print("type empl %s" % type_emplacement)
                emplacement = dao_emplacement.toGetEmplacementEntree(type_emplacement)
                ##print("emplace %s" % emplacement)
                stock_entrant = dao_stock_article.toCreateStockArticle(article.id, 0, emplacement.id, 0)
                ##print("stock %s" % stock_entrant)
                dao_stock_article.toSaveStockArticle(stock_entrant)
                ##print("EMPLE ENTREE ")

            # SCTOCK EMPLACEMENT DE RESERVE
            if article.est_manufacturable == True :
                type_emplacement = dao_type_emplacement.toGetTypeEmplacementReserve()
                emplacement = dao_emplacement.toGetEmplacementReserve(type_emplacement)
                stock_reserve = dao_stock_article.toCreateStockArticle(article.id, 0, emplacement.id, 0)
                dao_stock_article.toSaveStockArticle(stock_reserve)
                ##print("RESERVE")

            ##print("STOCK EMPLACEMENT")
            # SCTOCK EMPLACEMENT DE STOCKAGE
            type_emplacement = dao_type_emplacement.toGetTypeEmplacementStock()
            ##print("type empla %s" % type_emplacement)
            emplacements = dao_emplacement.toGetEmplacementStock(type_emplacement).filter(designation = "Stockage")
            for item in emplacements:
                ##print("empla %s" % item)
                stock_stockage = dao_stock_article.toCreateStockArticle(article.id, 0, item.id, 0)
                dao_stock_article.toSaveStockArticle(stock_stockage)
                break'''

            if type_article != "2":
                emplacement_mg = dao_emplacement.toGetEmplacementMoyensGeneraux()
                ##print("emplace", emplacement_mg)
                ##print(emplacement_mg.id)
                stock_article = dao_stock_article.toCreateStockArticle(article.id,0,emplacement_mg.id)
                stock_article = dao_stock_article.toSaveStockArticle(stock_article)

                unite_fonctionnelle = dao_unite_fonctionnelle.toGetUniteFonctionnelle(service_ref_id)
                ##print("unit",unite_fonctionnelle)
                stock_article = dao_stock_article.toCreateStockArticle(article.id,0,unite_fonctionnelle.emplacement_id)
                stock_article = dao_stock_article.toSaveStockArticle(stock_article)
                ##print(buzoba)

            ##print("CREATION UNITE")

            # CREATION DE L'UNITE D'ACHAT
            unite_achat = dao_unite_achat_article.toCreateUniteAchat(article.id, article.unite_id)
            unite_achat = dao_unite_achat_article.toSaveUniteAchat(auteur, unite_achat)

            ##print("FIN CREATION UNITE")


            if 'image_upload' in request.FILES:
                file = request.FILES["image_upload"]
                article_img_dir = 'articles/'
                media_dir = media_dir + '/' + article_img_dir
                save_path = os.path.join(media_dir, str(article.id) + ".jpg")
                path = default_storage.save(save_path, file)
                #On affecte le chemin de l'Image
                article.image = media_url + article_img_dir + str(article.id) + ".jpg"
                article.save()
            transaction.savepoint_commit(sid)
            messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
            return HttpResponseRedirect(reverse("module_inventaire_details_article", args=(article.id,)))
        else:
            messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de l'opération")
            transaction.savepoint_rollback(sid)
            return HttpResponseRedirect(reverse('module_inventaire_add_article'))
    except Exception as e:
        auteur = identite.utilisateur(request)
        module='ModuleInventaire'
        monLog.error("{} :: {}::\nERREUR LORS DU POST CREATION ARTICLE\n {}".format(auteur.nom_complet, module, e))
        monLog.debug("Info")
        ##print('Erreut Post Creer Article')
        ##print(e)
        transaction.savepoint_rollback(sid)
        messages.add_message(request, messages.ERROR,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_articles'))

def get_modifier_article(request, ref):
    try:
        permission_number = 43
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        id = int(ref)
        article = dao_article.toGetArticle(id)
        unite_fonctionnelle = dao_unite_fonctionnelle.toListUniteFonctionnelleWH()
        context = {
            'sous_modules':sous_modules,
            'title' : 'Modifier %s' % article.designation,
            'model' : article,
            'unites' : dao_unite.toListUnite(),
            'fournisseurs' : dao_fournisseur.toListFournisseursActifs(),
            'types_article' : dao_type_article.toListTypesArticle(),
            'categories' : dao_categorie_article.toListCategoriesArticle(),
            'devise_ref' : dao_devise.toGetDeviseReference(),
            "unite_fonctionnelle": unite_fonctionnelle,
            'utilisateur': utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
            "modules" : modules ,
            "module" : ErpModule.MODULE_INVENTAIRE,
            'menu' : 5
        }
        template = loader.get_template("ErpProject/ModuleInventaire/article/update.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_articles_stockables'))

@transaction.atomic
def post_modifier_article(request):
    sid = transaction.savepoint()
    id = int(request.POST["ref"])
    try:
        auteur = identite.utilisateur(request)
        base_dir = settings.BASE_DIR
        media_dir = settings.MEDIA_ROOT
        media_url = settings.MEDIA_URL
        designation = request.POST["designation"]
        unite_id = request.POST["unite_id"]

        est_vendable = False
        if "est_vendable" in request.POST : est_vendable = True

        est_achetable = False
        if "est_achetable" in  request.POST : est_achetable = True

        est_manufacturable = False
        if "est_manufacturable" in request.POST : est_manufacturable = True

        est_stockable = False
        if "est_stockable" in request.POST : est_stockable = True

        est_amortissable = False
        if "est_amortissable" in request.POST : est_amortissable = True

        designation_court = request.POST["designation_court"]
        code_article = request.POST["code_article"]
        code_barre = request.POST["code_barre"]
        type_article = int(request.POST["type_article"])
        categorie_id = int(request.POST["categorie_id"])
        prix_unitaire = makeFloat(request.POST["prix_unitaire_article"])
        service_ref_id = int(request.POST['service_ref_id'])
        if 'image_upload' in request.FILES:
            file = request.FILES["image_upload"]
            article_img_dir = 'articles/'
            media_dir = media_dir + '/' + article_img_dir
            save_path = os.path.join(media_dir, str(id) + ".jpg")
            if default_storage.exists(save_path):
                default_storage.delete(save_path)
            path = default_storage.save(save_path, file)
            #default_storage.delete(path)
            #On affecte le chemin de l'Image
            image = media_url + article_img_dir + str(id) + ".jpg"
        else : image = ""

        article = dao_article.toCreateArticle(image, designation, unite_id, est_vendable, est_achetable, est_manufacturable, est_stockable, designation_court, code_article, code_barre, type_article, categorie_id, prix_unitaire, est_amortissable= est_amortissable, unite_fonctionnelle_id= service_ref_id)
        is_done = dao_article.toUpdateArticle(id, article)

        if is_done == True :
            transaction.savepoint_commit(sid)
            messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
            return HttpResponseRedirect(reverse("module_inventaire_details_article", args=(id,)))
        else :
            transaction.savepoint_rollback(sid)
            messages.add_message(request, messages.ERROR, "Une erreur est survenue lors l'opération !")
            return HttpResponseRedirect(reverse("module_inventaire_update_article", args=(id,)))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        transaction.savepoint_rollback(sid)
        messages.add_message(request, messages.ERROR,e)
        return HttpResponseRedirect(reverse('module_inventaire_update_article'), args=(id,))

def get_details_article(request, ref):
    try:
        permission_number = 41
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        type_emplacement_entrepot = dao_type_emplacement.toGetTypeEmplacementEntrepot()
        entrepot = dao_emplacement.toGetEmplacementEntrepot(type_emplacement_entrepot)

        ref = int(ref)
        article = dao_article.toGetArticle(ref)
        historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,article)

        context = {
            'sous_modules':sous_modules,
            'title' : article.designation,
            'model' : article,
            "historique": historique,
            "etapes_suivantes": etapes_suivantes,
            "signee": signee,
            "content_type_id": content_type_id,
            "documents": documents,
            "roles": groupe_permissions,
            'emplacements' : dao_emplacement.toListEmplacementsInEntrepot(entrepot.id),
            'types_article' : dao_type_article.toListTypesArticle(),
            'devise_ref' : dao_devise.toGetDeviseReference(),
            'fournisseurs_article' : dao_fournisseur_article.toListFournisseursOf(article.id),
            'utilisateur': utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
            "modules" : modules ,
            "module" : ErpModule.MODULE_INVENTAIRE,
            'menu' : 5
        }
        template = loader.get_template("ErpProject/ModuleInventaire/article/item.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        ##print("ERREUR on details article")
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_articles_stockables'))


def get_details_article_fourni(request):
    data = {}
    try:
        article_id = int(request.GET["ref"])
        article = dao_article.toGetArticle(article_id)
        type_emplacement = dao_type_emplacement.toGetTypeEmplacementEntree()
        emplacement = dao_emplacement.toGetEmplacementEntree(type_emplacement)
        les_stocks = dao_stock_article.toListStocksOfArticleInEmplacement(article_id, emplacement.id)
        stock = les_stocks[0]

        data = {
            "designation" : article.designation,
            "stock_article_id" : stock.id,
            "prix_unitaire" : article.prix_unitaire
        }
        return JsonResponse(data, safe=False)
    except Exception as e:
        ##print(e)
        return JsonResponse(data, safe=False)

def get_article_of_emplacement(request):
    data = {}
    try:
        article_id = int(request.GET["ref"])
        emplacement_id = int(request.GET["ref_emplacement"])
        article = dao_article.toGetArticle(article_id)
        ##print("Article",article)
        ##print("Emplacement",emplacement_id)
        quantite_theorique = dao_stock_article.toGetQuantiteStockOfEmplacement(article_id, emplacement_id)
        #quantite_theorique = dao_stock_article.toGetQuantiteStockOfEmplacement(article, emplacement_id)
        ##print("Qte theorique",quantite_theorique)
        type_emplacement = dao_type_emplacement.toGetTypeEmplacementEntree()
        emplacement = dao_emplacement.toGetEmplacementEntree(type_emplacement)
        les_stocks = dao_stock_article.toListStocksOfArticleInEmplacement(article_id, emplacement.id)
        stock = les_stocks[0]
        unite = dao_unite.toGetUnite(article.unite_id)

        data = {
            "designation" : article.designation,
            "stock_article_id" : stock.id,
            "quantite_theorique" : quantite_theorique,
            "prix_unitaire" : article.prix_unitaire,
            "symbole_unite" : unite.symbole_unite
        }
        return JsonResponse(data, safe=False)
    except Exception as e:
        ##print(e)
        return JsonResponse(data, safe=False)

# EMPLACEMENT CONTROLLER
def get_lister_entrepots(request):
    permission_number = 52
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
    if response != None:
        return response

    type_emplacement_entrepot = dao_type_emplacement.toGetTypeEmplacementEntrepot()
    #*******Filtre sur les règles **********#
    model = dao_model.toListModel(dao_emplacement.toListEmplacementsOfType(type_emplacement_entrepot.id), permission_number, groupe_permissions, identite.utilisateur(request))
    #******* End Regle *******************#
    context = {
        'modules':modules,'sous_modules':sous_modules,
        'title' : "Liste des entrepôts",
        'model' : model,
        "utilisateur" : utilisateur,
        'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
        "modules" : modules ,
        "module" : ErpModule.MODULE_INVENTAIRE,
        'menu': 8
    }
    template = loader.get_template("ErpProject/ModuleInventaire/emplacement/entrepot/list.html")
    return HttpResponse(template.render(context, request))

def get_lister_emplacements(request):
    permission_number = 56
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
    if response != None:
        return response

    #type_emplacement_entrepot = dao_type_emplacement.toGetTypeEmplacementEntrepot()
    #*******Filtre sur les règles **********#
    model = dao_model.toListModel(dao_emplacement.toListEmplacement(), permission_number, groupe_permissions, identite.utilisateur(request))
    #******* End Regle *******************#
    context = {
        'modules':modules,'sous_modules':sous_modules,
        'title' : "Liste des emplacements",
        'model' : model,
        "utilisateur" : utilisateur,
        'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
        "modules" : modules ,
        "module" : ErpModule.MODULE_INVENTAIRE,
        'menu': 9
    }
    template = loader.get_template("ErpProject/ModuleInventaire/emplacement/list.html")
    return HttpResponse(template.render(context, request))

def get_lister_articles_in_emplacement(request):
    try:
        ##print("emplacement_id")
        emplacement_id = int(request.GET["ref"])
        ##print(emplacement_id)
        emplacement = dao_emplacement.toGetEmplacement(emplacement_id)
        les_stocks = dao_stock_article.toListStocksInEmplacement(emplacement.id)

        data = []

        for item in les_stocks:
            element = {
                "designation" : item.article.designation,
                "id" : item.article.id,
                "categorie_id" : item.article.categorie_id
            }
            data.append(element)
        return JsonResponse(data, safe=False)
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        return JsonResponse([], safe=False)


# TYPE OPERATIONS STOCK CONTROLLER
def get_lister_operations_stock(request):
    permission_number = 60
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
    if response != None:
        return response
    #model = dao_operation_stock.toListOperationsStockOfInventaire()
    # model = dao_operation_stock.toListOperationsStockOfInventaire()
    #*******Filtre sur les règles **********#
    model = dao_model.toListModel(dao_operation_stock.toListOperationsStockOfInventaire(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
    context = {
        'modules':modules,'sous_modules':sous_modules,
        'title' : "Liste des opérations stocks",
        'model' : model,
        "utilisateur" : utilisateur,
        'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
        "modules" : modules ,
        "module" : ErpModule.MODULE_INVENTAIRE,
        'menu' : 10
    }
    template = loader.get_template("ErpProject/ModuleInventaire/operations/list.html")
    return HttpResponse(template.render(context,request))

def get_creer_operations_stock(request):
    permission_number = 61
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
    if response != None:
        return response

    context = {
        'modules':modules,'sous_modules':sous_modules,
        'title' : "Nouvelle opération stock",
        "utilisateur" : utilisateur,
        'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
        "modules" : modules ,
        "module" : ErpModule.MODULE_INVENTAIRE,
        'menu' : 10
    }
    template = loader.get_template("ErpProject/ModuleInventaire/operations/add.html")
    return HttpResponse(template.render(context,request))


def post_creer_operations_stock(request):
    try:
        auteur = identite.utilisateur(request)
        designation = request.POST["designation"]
        reference = request.POST["reference"]
        type = request.POST["type"]
        sequence = request.POST["sequence"]

        operation = dao_operation_stock.toCreateOperationStock(designation, reference, type, sequence)
        operation = dao_operation_stock.toSaveOperationStock(operation)

        if operation != None :
            messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
            return HttpResponseRedirect(reverse("module_inventaire_details_operations_stock", args=(operation.id,)))
        else :
            messages.add_message(request, messages.ERROR, "Une erreur est survenue lors l'opération !")
            return HttpResponseRedirect(reverse('module_inventaire_add_operations_stock'))
    except Exception as e:
        messages.add_message(request, messages.ERROR,e)
        return HttpResponseRedirect(reverse('module_inventaire_add_operations_stock'))

def get_details_operations_stock(request, ref):

    try:
        permission_number =60
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        ref = int(ref)
        operation = dao_operation_stock.toGetOperationStock(ref)
        historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,operation)

        context = {
            'modules':modules,'sous_modules':sous_modules,
            'title' : operation.designation,
            "historique": historique,
            "etapes_suivantes": etapes_suivantes,
            "signee": signee,
            "content_type_id": content_type_id,
            "documents": documents,
            "roles": groupe_permissions,
            'model' : operation,
            "utilisateur" : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		    'organisation': dao_organisation.toGetMainOrganisation(),
            "modules" : modules ,
            "module" : ErpModule.MODULE_INVENTAIRE,
            'menu' : 10
        }
        template = loader.get_template("ErpProject/ModuleInventaire/operations/item.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_operations_stock'))

def get_modifier_operations_stock(request, ref):

    try:
        permission_number = 62
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        id = int(ref)
        model = dao_operation_stock.toGetOperationStock(id)
        context = {
            'modules':modules,'sous_modules':sous_modules,
            'title' : "Modifier l'opération stock %s" % model.designation,
            'model' : model,
            "utilisateur" : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		    'organisation': dao_organisation.toGetMainOrganisation(),
            "modules" : modules ,
            "module" : ErpModule.MODULE_INVENTAIRE,
            'menu' : 10
        }
        template = loader.get_template("ErpProject/ModuleInventaire/operations/update.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_operations_stock'))

def post_modifier_operations_stock(request):
    id = int(request.POST["ref"])
    try:
        auteur = identite.utilisateur(request)
        designation = request.POST["designation"]
        reference = request.POST["reference"]
        type = request.POST["type"]
        sequence = request.POST["sequence"]

        operation = dao_operation_stock.toCreateOperationStock(designation, reference, type, sequence)
        is_done = dao_operation_stock.toUpdateOperationStock(id, operation)

        if is_done == True :
            messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
            return HttpResponseRedirect(reverse("module_inventaire_details_operations_stock", args=(id,)))
        else :
            messages.add_message(request, messages.ERROR, "Une erreur est survenue lors l'opération !")
            return HttpResponseRedirect(reverse('module_inventaire_update_operations_stock', args=(id,)))
    except Exception as e:
        ##print("ERREUR !")
        ##print(e)
        messages.add_message(request, messages.ERROR,e)
        return HttpResponseRedirect(reverse('module_inventaire_update_operations_stock', args=(id,)))

#CONFIGURATION CONTROLLER
def get_configuration(request):
    try:
        permission_number = -1
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        #ref = int(ref)
        #condition_reglement = dao_condition_reglement.toGetConditionReglement(ref)
        context = {
            'modules':modules,'sous_modules':sous_modules,
            'title' : 'Paramètrage' ,
            #'model' : condition_reglement,
            "utilisateur" : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		    'organisation': dao_organisation.toGetMainOrganisation(),
            "modules" : modules ,
            "module" : ErpModule.MODULE_INVENTAIRE,
            'menu' : 6
        }
        template = loader.get_template("ErpProject/ModuleInventaire/configuration/index.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_configuration'))

def post_modifier_configuration(request):
    id = int(request.POST["ref"])
    try:
        auteur = identite.utilisateur(request)
        designation = request.POST["designation"]

        categorie = dao_categorie.toCreateCategorie(designation)
        is_done = dao_categorie_article.toUpdateCategorieArticle(id, categorie)

        if is_done == True : return HttpResponseRedirect(reverse("module_inventaire_configuration", args=(id,)))
        else : return HttpResponseRedirect(reverse('module_inventaire_configuration', args=(id,)))
    except Exception as e:
        ##print("ERREUR !")
        ##print(e)
        messages.add_message(request, messages.ERROR,e)
        return HttpResponseRedirect(reverse('module_inventaire_configuration'))


# FOURNITURE CONTROLLER ----- Demande mr Thomas "déplacer Article entrant dans Inventaire"
def get_lister_fournitures(request):
    permission_number = 64
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
    if response != None:
        return response
    #model = dao_fourniture.toListFournitures()
    # model = dao_fourniture.toListFournitures()
    #*******Filtre sur les règles **********#
    model = dao_model.toListModel(dao_fourniture.toListFournitures(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
    context = {
        'modules':modules,'sous_modules':sous_modules,
        'title' : "Liste des articles à recevoir",
        'model' : model,
        "utilisateur" : utilisateur,
        'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
        "modules" : modules,
        "module" : ErpModule.MODULE_INVENTAIRE,
        'menu' : 1
    }
    template = loader.get_template("ErpProject/ModuleInventaire/fourniture/list.html")
    return HttpResponse(template.render(context, request))

def get_details_fourniture(request, ref):

    try:
        permission_number = 64
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response


        ref = int(ref)
        bon_reception = dao_fourniture.toGetFourniture(ref)
        title = "Fourniture"
        if bon_reception.numero_reception != None and bon_reception.numero_reception != "" : title = title + " liée au bon d'achat n°%s" % bon_reception.numero_reception

        lignes = dao_ligne_fourniture.toListLignesFourniture(bon_reception.id)
        historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,bon_reception)

        context = {
            'modules':modules,'sous_modules':sous_modules,
            'title' : title,
            'model' : bon_reception,
            "historique": historique,
            "etapes_suivantes": etapes_suivantes,
            "signee": signee,
            "content_type_id": content_type_id,
            "documents": documents,
            "roles": groupe_permissions,
            'lignes' : lignes,
            "utilisateur" : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
            "modules" : modules,
            "module" : ErpModule.MODULE_INVENTAIRE,
            'menu' : 1
        }
        template = loader.get_template("ErpProject/ModuleInventaire/fourniture/item.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_fournitures'))

def get_print_rapport_details_fourniture(request, ref):

    try:
        permission_number = 64
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response


        ref = int(ref)
        bon_reception = dao_fourniture.toGetFourniture(ref)
        title = "Fourniture"
        if bon_reception.numero_reception != None and bon_reception.numero_reception != "" : title = title + " liée au bon d'achat n°%s" % bon_reception.numero_reception

        lignes = dao_ligne_fourniture.toListLignesFourniture(bon_reception.id)
        context = {
            'modules':modules,'sous_modules':sous_modules,
            'title' : title,
            'model' : bon_reception,
            'lignes' : lignes,
            "utilisateur" : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
            "modules" : modules,
            "module" : ErpModule.MODULE_INVENTAIRE,
            'menu' : 1
        }
        return weasy_#print("ErpProject/ModuleInventaire/reporting/detail_fournisseur.html", "detail_fournisseur.pdf", context)

    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_fournitures'))
def get_creer_fourniture(request):
    permission_number = 65
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
    if response != None:
        return response

    context = {
        'modules':modules,'sous_modules':sous_modules,
        'title' : "Réception d'article",
        'agents' : dao_employe.toListEmployesActifs(),
        'fournisseurs' : dao_fournisseur.toListFournisseursActifs(),
        'articles' : dao_article.toListArticlesAchetables(),
        'categories' : dao_categorie_article.toListCategoriesArticle(),
        'devises' : dao_devise.toListDevisesActives(),
        'conditions_reglement' : dao_condition_reglement.toListConditionsReglement(),
        "utilisateur" : utilisateur,
        'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
        "modules" : modules,
        "module" : ErpModule.MODULE_INVENTAIRE,
        'menu' : 1
    }
    template = loader.get_template("ErpProject/ModuleInventaire/fourniture/add.html")
    return HttpResponse(template.render(context, request))

def get_valider_fourniture(request):

    try:
        permission_number = 65
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        fournisseur_id = int(request.POST["fournisseur_id"])
        fournisseur = dao_fournisseur.toGetFournisseur(fournisseur_id)

        receveur_id = int(request.POST["receveur_id"])
        receveur = dao_employe.toGetEmploye(receveur_id)

        devise_id = int(request.POST["devise_id"])
        devise = dao_devise.toGetDevise(devise_id)

        condition_reglement_id = int(request.POST["condition_reglement_id"])
        condition_reglement = dao_condition_reglement.toGetConditionReglement(condition_reglement_id)

        context = {
            'modules':modules,'sous_modules':sous_modules,
            'title' : "Valider Réception d'article",
            "fournisseur" : fournisseur,
            "receveur" : receveur,
            "devise" : devise,
            "condition_reglement" : condition_reglement,
            "utilisateur" : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
            "modules" : modules,
            "module" : ErpModule.MODULE_INVENTAIRE,
            'menu' : 1
        }
        template = loader.get_template("ErpProject/ModuleInventaire/fourniture/validate.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_add_fourniture'))

@transaction.atomic
def post_valider_fourniture(request):
    sid = transaction.savepoint()
    try:
        auteur = identite.utilisateur(request)
        devise_id = int(request.POST["devise_id"])
        condition_reglement_id = int(request.POST["condition_reglement_id"])
        fournisseur_id = int(request.POST["fournisseur_id"])

        reference_document = request.POST["reference_document"]

        journal_id = 0

        devise_ref = dao_devise.toGetDeviseReference()
        taux_id = 0
        if devise_id != devise_ref.id:
            taux = dao_taux.toGetTauxbyDeviseArrive(devise_id)
            if taux != None: taux_id = taux.id

        objet_dao_fourniture = dao_fourniture.toCreateFourniture("", True, fournisseur_id, None , devise_id, condition_reglement_id, None, timezone.now())
        fourniture = dao_fourniture.toSaveFourniture(auteur, objet_dao_fourniture)
        if fourniture != None :
            list_article_id = request.POST.getlist('article_id', None)
            list_quantite_fournie = request.POST.getlist("quantite_fournie", None)
            list_prix_unitaire = request.POST.getlist("prix_unitaire", None)
            list_prix_lot = request.POST.getlist("prix_lot", None)

            for i in range(0, len(list_article_id)) :
                article_id = int(list_article_id[i])
                quantite_fournie = makeFloat(list_quantite_fournie[i])
                prix_unitaire = makeFloat(list_prix_unitaire[i])
                prix_lot = makeFloat(list_prix_lot[i])

                article = dao_article.toGetArticle(article_id)
                type_emplacement = dao_type_emplacement.toGetTypeEmplacementEntree()
                emplacement = dao_emplacement.toGetEmplacementEntree(type_emplacement)
                les_stocks = dao_stock_article.toListStocksOfArticleInEmplacement(article_id, emplacement.id)
                stock = les_stocks[0]

                unite_achat = dao_unite_achat_article.toGetUniteAchatOfArticle(article.id, article.unite_id)
                unite_achat_id = unite_achat.id if unite_achat else None

                ligne_fourniture = dao_ligne_reception.toCreateLigneReception(fourniture.id, article_id, 0,0,'','',  prix_unitaire, unite_achat_id, quantite_fournie, stock.id)
                ligne_fourniture = dao_ligne_fourniture.toSaveLigneFourniture(auteur, ligne_fourniture)

                # AUGMENTATION DE LA QUANTITE DU STOCK CONCERNE
                stock.quantite_disponible = stock.quantite_disponible + quantite_fournie
                dao_stock_article.toUpdateStockArticle(ligne_fourniture.stock_article_id, stock)

                #ENREGISTRER LE MOUVEMENT
                mouvement_stock = dao_mouvement_stock.toCreateMouvementStock(quantite_fournie,"","ACHAT",0, ligne_fourniture.stock_article_id,None,fourniture.id)
                mouvement_stock = dao_mouvement_stock.toSaveMouvementStock(auteur, mouvement_stock)

            # CREER L'ORDRE DE TRANSFERT
            operation_reception = dao_operation_stock.toGetOperationReceptionArticles()
            type_emplacement = dao_type_emplacement.toGetTypeEmplacementStock()
            emplacement = dao_emplacement.toGetEmplacementStock(type_emplacement)

            transfert = dao_bon_transfert.toCreateBonTransfert(None, False, '', timezone.now(), operation_reception.id, None,emplacement.id)
            transfert = dao_bon_transfert.toSaveBonTransfert(auteur, transfert)

            lignes_fourniture = dao_ligne_fourniture.toListLignesFourniture(fourniture.id)

            for item in lignes_fourniture:
                ligne_transfert = dao_ligne_transfert.toCreateLigneTransfert(transfert.id, item.stock_article_id, 0, item.quantite_fournie,'','')
                ligne_transfert = dao_ligne_transfert.toSaveLigneTransfert(auteur, ligne_transfert)


            # ON CREE LE BON ENTREE STOCK
            bon_special = dao_bon_special.toCreateBonSpecial("", fourniture.id, reference_document, fourniture.devise_id, fourniture.receveur_id)
            bon_special = dao_bon_special.toSaveBonSpecial(auteur, bon_special)
            for item in lignes_fourniture:
                item_bon_special = dao_item_bon_special.toCreateItemBonSpecial(bon_special.id, item.article_id, item.quantite_demandee, item.quantite_fournie, item.unite)
                item_bon_special = dao_item_bon_special.toSaveItemBonSpecial(auteur, item_bon_special)

            transaction.savepoint_commit(sid)
            #return HttpResponseRedirect(reverse('module_inventaire_details_fourniture', args=(fourniture.id,)))
            return HttpResponseRedirect(reverse('module_inventaire_details_bons_entrees', args=(bon_special.id,)))
        else:
            transaction.savepoint_rollback(sid)
            return HttpResponseRedirect(reverse('module_inventaire_add_fourniture'))

    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        transaction.savepoint_rollback(sid)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_add_fourniture'))

def get_lister_lignes_fourniture(request):
    data = {}
    try:
        lignes = []
        id = int(request.GET["ref"])
        fourniture = dao_fourniture.toGetFourniture(id)
        lignes_fourniture = dao_ligne_fourniture.toListLignesFourniture(fourniture.id)
        for item in lignes_fourniture :
            ligne = {
                "ligne_id" : item.id,
                "nom_article" : item.stock_article.article.designation,
                "quantite_fournie" : item.quantite_fournie,
                "prix_unitaire" : item.prix_unitaire,
                "prix_lot" : item.prix_lot,
                "symbole_unite" : item.unite_achat.unite.symbole_unite
            }
            lignes.append(ligne)
        data = {
            "prix_total" : fourniture.prix_total,
            "symbole_devise" : fourniture.devise.symbole_devise,
            "reference_document" : fourniture.reference_document,
            "lignes" : lignes
        }
        return JsonResponse(data, safe=False)
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        return JsonResponse(data, safe=False)

# BON ACHAT EN ATTENTE DE RECEPTION CONTROLLER
def get_lister_bons_reception(request):
    permission_number = 71
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
    if response != None:
        return response

    #model = dao_fourniture.toListBonsAchatEnAttente()

    # model = dao_fourniture.toListBonsAchatEnAttente()
    #*******Filtre sur les règles **********#
    model = dao_model.toListModel(dao_fourniture.toListBonsAchatEnAttente(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#

    context = {
        'modules':modules,'sous_modules':sous_modules,
        'title' : "Liste des bons à receptionner",
        'model' : model,
        "utilisateur" : utilisateur,
        "modules" : modules,
        'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
        "module" : ErpModule.MODULE_INVENTAIRE,
        'menu' : 1
    }
    template = loader.get_template("ErpProject/ModuleInventaire/bons/list.html")
    return HttpResponse(template.render(context, request))

def get_details_bon_reception(request, ref):

    try:
        permission_number = 71
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        ref = int(ref)
        bon_reception = dao_fourniture.toGetFourniture(ref)
        lignes = dao_ligne_fourniture.toListLignesFourniture(bon_reception.id)
        historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,bon_reception)

        context = {
            'modules':modules,'sous_modules':sous_modules,
            'title' : "Bon de commande N°%s" % bon_reception.numero_reception,
            'model' : bon_reception,
            'lignes' : lignes,
            "historique": historique,
            "etapes_suivantes": etapes_suivantes,
            "signee": signee,
            "content_type_id": content_type_id,
            "documents": documents,
            "roles": groupe_permissions,
            "utilisateur" : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		    'organisation': dao_organisation.toGetMainOrganisation(),
            "modules" : modules,
            "module" : ErpModule.MODULE_INVENTAIRE,
            'menu' : 1
        }
        template = loader.get_template("ErpProject/ModuleInventaire/bons/item.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_bon_receptions'))


def get_receptionner_bon_reception(request, ref):

    try:
        permission_number = 71
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        ref = int(ref)
        bon_reception = dao_fourniture.toGetFourniture(ref)
        if bon_reception.est_realisee == True : return HttpResponseRedirect(reverse('module_achat_list_bons_achat'))

        lignes = dao_ligne_fourniture.toListLignesFourniture(bon_reception.id)
        context = {
            'title' : "Bon de reception relatif au bon de commande N°%s" % bon_reception.numero_reception,
            'model' : bon_reception,
            'lignes' : lignes,
            'agents' : dao_employe.toListEmployesActifs(),
            "utilisateur" : utilisateur,
            'sous_modules':sous_modules,
            'actions':auth.toGetActions(modules,utilisateur),
		    'organisation': dao_organisation.toGetMainOrganisation(),
            "modules" : modules,
            "module" : ErpModule.MODULE_INVENTAIRE,
            'menu' : 1
        }
        template = loader.get_template("ErpProject/ModuleInventaire/bons/receive.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_bon_receptions'))

@transaction.atomic
def post_receptionner_bon_reception(request):
    sid = transaction.savepoint()
    bon_id = int(request.POST["bon_id"])
    try:
        #Test de la validité de la date en fonction de l'activation d'une période dans un module
        if not auth.toPostValidityDate(var_module_id, datetime.datetime.now().strftime("%d/%m/%Y")): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")

        auteur = identite.utilisateur(request)
        receveur_id = int(request.POST["receveur_id"])
        reference_document = request.POST["reference_document"]
        commentaire = request.POST["commentaire"]
        est_realisee = True


        bon_reception = dao_fourniture.toGetFourniture(bon_id)
        ##print("Bon achat {0} recupere ".format(bon_reception.id))
        list_ligne_id = request.POST.getlist('ligne_id', None)
        list_quantite_fournie = request.POST.getlist("quantite_fournie", None)

        for i in range(0, len(list_ligne_id)) :
            ligne_id = int(list_ligne_id[i])
            quantite_fournie = makeFloat(list_quantite_fournie[i])

            #On recupère l'objet de la ligne fourniture
            ligne_fourniture = dao_ligne_fourniture.toGetLigneFourniture(ligne_id)
            ##print("Ligne fourniture {0} recupere ".format(ligne_fourniture.id))
            #Si la quantité demandée est superieure à la somme des quantitées déjà fournies, on ne receptionne pas pcq on n'a pas encore tout reçu
            #if ligne_fourniture.quantite_demande > ligne_fourniture.quantite_fournie + quantite_fournie : est_realisee = False

            # On ajoute la nouvelle quantité reçue
            ligne_fourniture.quantite_fournie = ligne_fourniture.quantite_fournie + quantite_fournie
            ligne_fourniture.save()
            ##print("Ligne fourniture {0} modifie ".format(ligne_fourniture.id))

            # On recuper le stock de l'article de la ligne du bon d'achat (ici l'emplacement d'entrée)
            stock = dao_stock_article.toGetStockArticle(ligne_fourniture.stock_article_id)
            ##print("Stock article {0} recupere ".format(stock.id))

            # AUGMENTATION DE LA QUANTITE DU STOCK CONCERNE (Emplacement d'entrée)
            stock.quantite_disponible = stock.quantite_disponible + quantite_fournie
            loud = dao_stock_article.toUpdateStockArticle(ligne_fourniture.stock_article_id, stock)
            ##print("Stock article {0} recupere ".format(stock.id))

            #ENREGISTRER LE MOUVEMENT
            if quantite_fournie > 0:
                mouvement_stock = dao_mouvement_stock.toCreateMouvementStock(quantite_fournie,"","ACHAT",ligne_fourniture.stock_article_id,None,None,bon_id)
                mouvement_stock = dao_mouvement_stock.toSaveMouvementStock(auteur, mouvement_stock)
                ##print("Mouvement stock {0} cree ".format(mouvement_stock.id))

        bon_reception.est_realisee = est_realisee
        bon_reception.receveur_id = receveur_id
        bon_reception.save()
        ##print("Bon Achat {0} modifie ".format(bon_reception.id))

        # ON CREE LE BON ENTREE STOCK (Model_Bon)
        lignes_fourniture = dao_ligne_fourniture.toListLignesFourniture(bon_reception.id)
        #dao_bon_special.toCreateBonSpecial("",)
        bon_entree = dao_bon_special.toCreateBonSpecial("",  None,bon_reception.id, None, reference_document, bon_reception.devise_id, bon_reception.receveur_id, commentaire)
        bon_entree = dao_bon_special.toSaveBonSpecial(auteur, bon_entree)

        # WORKFLOWS INITIALS
        type_document = "Bon d'entrée depot"
        wkf_task.initializeWorkflow(auteur,bon_entree,type_document)

        #Gref, Bon reception passe d'article
        wkf_task.passingStepWorkflow(auteur,bon_reception)


        ##print("Bon Special {0} cree ".format(bon_entree.id))
        #On enregistre le ligne du bon d'entree
        for item in lignes_fourniture:
            ##print("before ligne", lignes_fourniture)
            ligne_bon_entree = dao_item_bon_special.toCreateItemBonSpecial(bon_entree.id, item.article_id, item.quantite_demande, item.quantite_fournie, item.unite_achat)
            ##print("after ligne")
            ligne_bon_entree = dao_item_bon_special.toSaveItemBonSpecial(auteur,ligne_bon_entree)
            ##print("Ligne bon d'entrée {0} cree ".format(ligne_bon_entree.id))



        transaction.savepoint_commit(sid)
        return HttpResponseRedirect(reverse('module_inventaire_details_bons_entrees', args=(bon_entree.id,)))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        transaction.savepoint_rollback(sid)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_receive_bon_reception', args=(bon_entree.id,)))


@transaction.atomic
def post_workflow_reception(request):
    sid = transaction.savepoint()
    try:
        utilisateur_id = request.user.id
        etape_id = request.POST["etape_id"]
        demande_id = request.POST["doc_id"]

        ##print("print 1 %s %s %s" % (utilisateur_id, etape_id, demande_id))

        employe = dao_employe.toGetEmployeFromUser(utilisateur_id)
        etape = dao_wkf_etape.toGetEtapeWorkflow(etape_id)
        demande_achat = dao_demande_achat.toGetDemande(demande_id)

        ##print("print 2 %s %s %s " % (employe, etape, demande_achat))

        transitions_etapes_suivantes = dao_wkf_etape.toListEtapeSuivante(demande_achat.statut_id)
        for item in transitions_etapes_suivantes:

            # Gestion des transitions dans le document
            demande_achat.statut_id = etape.id
            demande_achat.etat = etape.designation
            demande_achat.save()

        historique = dao_wkf_historique_demande.toCreateHistoriqueWorkflow(employe.id, etape.id, demande_achat.id)
        historique = dao_wkf_historique_demande.toSaveHistoriqueWorkflow(historique)

        if historique != None :
            transaction.savepoint_commit(sid)
            #return HttpResponseRedirect(reverse('module_achat_details_bon_achat', args=(demande.id,)))
            ##print("OKAY")
            return HttpResponseRedirect(reverse('module_achat_detail_demande_achat', args=(demande_id,)))
        else:
            transaction.savepoint_rollback(sid)
            return HttpResponseRedirect(reverse('module_achat_detail_demande_achat', args=(demande_id,)))

    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        transaction.savepoint_rollback(sid)
        return HttpResponseRedirect(reverse('module_achat_add_bon_achat'))

# BON ENTREE DEPOT CONTROLLER
def get_lister_bons_entrees(request):
    permission_number = 71
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
    if response != None:
        return response

    #model = dao_bon_special.toListBonsEntrees()

    # model = dao_bon_special.toListBonsEntrees()
    #*******Filtre sur les règles **********#
    model = dao_model.toListModel(dao_bon_special.toListBonsEntrees(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
    try:
	    view = str(request.GET.get("view","list"))
    except Exception as e:
	    view = "list"

    #Pagination
    model = pagination.toGet(request, model)

    context = {
        'modules':modules,
        'sous_modules':sous_modules,
        'title' : "Liste des bons de reception",
        'model' : model,
        "utilisateur" : utilisateur,
        'view' : view,
        'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
        "modules" : modules,
        "module" : ErpModule.MODULE_INVENTAIRE,
        'menu' : 3
    }
    template = loader.get_template("ErpProject/ModuleInventaire/bons_entrees/list.html")
    return HttpResponse(template.render(context, request))


def get_details_bons_entrees(request, ref):
    permission_number = 71
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
    if response != None:
        return response

    try:
        ref = int(ref)
        bon_entree = dao_bon_special.toGetBonSpecial(ref)
        lignes = dao_item_bon_special.toListItemBons(bon_entree.id)
        historique, transition_etape_suivant, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,bon_entree)
        context = {
            'modules':modules,
            'sous_modules':sous_modules,
            'title' : "Bon de reception N°%s" % bon_entree.numero,
            'model' : bon_entree,
            'lignes' : lignes,
            'signee' : signee,
            'historique':historique,
            'roles':groupe_permissions,
            'content_type_id':content_type_id,
            'documents': documents,
            'etapes_suivantes':transition_etape_suivant,
            "utilisateur" : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
           "module" : ErpModule.MODULE_INVENTAIRE,
            'menu' : 3
        }
        template = loader.get_template("ErpProject/ModuleInventaire/bons_entrees/item.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_bons_entrees'))

####### BON DE SORTIE MATERIEL SMG
def get_lister_bon_sortie_smg(request):
    permission_number = 1008
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
    if response != None:
        return response

    title = "Liste des bons de sortie SMG"
    # model = dao_article.toListArticles()
    #*******Filtre sur les règles **********#
    model = dao_model.toListModel(dao_article.toListArticles(), permission_number, groupe_permissions, identite.utilisateur(request))
    #******* End Regle *******************#

    transfert =  Model_Bon_transfert.objects.filter(emplacement_origine = 7, operation_stock__id=9).order_by("-creation_date")
    # #print("***Transfert", transfert)

    # transferts = dao_bon_transfert.toListBonTransfert()

    # transferts = dao_bon_transfert.toListBonTransfert()() if auth.toCheckAdmin(modules, utilisateur) else dao_bon_transfert.toListBonTransfert()ByAuteur(utilisateur.id)
    try:
        view = str(request.GET.get("view","list"))
    except Exception as e:
        view = "list"

    if "op" in request.GET:
        try:
            """operation_id = int(request.GET["op"])
            operation_stock = dao_operation_stock.toGetOperationStock(operation_id)
            transferts = dao_bon_transfert.toListTransfertsDuType(operation_stock.id)
            title = title + (" - %s" % operation_stock.designation)"""
            reference = str(request.GET["op"])

        except Exception as e:
            #print("ERREUR")
            #print(e)
            pass
    #Pagination
    transfert = pagination.toGet(request, transfert)


    context = {
        'sous_modules':sous_modules,
        'title' : title,
        'emplacements' : dao_emplacement.toListEmplacement(),
        'articles' : model,
        'transfert' : transfert,
        'categories' : dao_categorie_article.toListCategoriesArticle(),
        "utilisateur" : utilisateur,
        'view' : view,
        'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
        "modules" : modules,
        "module" : ErpModule.MODULE_INVENTAIRE,
        'menu': 11
    }
    template = loader.get_template("ErpProject/ModuleInventaire/bon_sortie_smg/list.html")
    return HttpResponse(template.render(context, request))

#creation bon de sortie SMG
def get_creer_bon_sortie_smg(request):
    try:
        permission_number = 1009
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        type_emplacement_entrepot = dao_type_emplacement.toGetTypeEmplacementEntrepot()
        ##print(type_emplacement_entrepot)
        entrepot = dao_emplacement.toGetEmplacement(type_emplacement_entrepot.id)
        ##print(entrepot)
        #etat_besoins = dao_expression_besoin.toListExpressionsNonTraites()

        #services_referents = dao_unite_fonctionnelle.toListUniteFonctionnelleWH()
        services_referents = dao_unite_fonctionnelle.toListUniteFonctionnelleWHNoneService()
        emplacement_internal = dao_emplacement.toGetEmplacementInternalBusiness()

        etat_actuel_id = 0
        etat = ""
        lignes = []

        try:
            etat_actuel_id = request.POST["doc_id"]
            etat = dao_expression_besoin.toGetExpression(etat_actuel_id)
            lignes = dao_ligne_expression.toListLigneOfExpressions(etat.id)
        except Exception as e:
            ##print("Aucun etat de besoin trouvé")
            pass

        if utilisateur.unite_fonctionnelle != None:

            etat_besoins = dao_expression_besoin.toListExpressionsNonTraitesByServiceRef(utilisateur.unite_fonctionnelle.id)
            ##print("etat", etat_besoins)
            service_referent = dao_unite_fonctionnelle.toGetUniteFonctionnelle(utilisateur.unite_fonctionnelle_id)
        else:
            etat_besoins = dao_expression_besoin.toListExpressionsNonTraites()
            service_referent = 0
        context = {
            'sous_modules':sous_modules,
            'title' : "Nouveau bon de sortie SMG ",
            'emplacements':dao_emplacement.toListEmplacementsInEntrepot(entrepot.id),
            'type_emplacement_entre': dao_type_emplacement.toGetTypeEmplacementEntree(),
            'type_emplacement_stock': dao_type_emplacement.toGetTypeEmplacementStock(),
            'etat' : etat,
            'emplacement_internal':emplacement_internal,
            'services_referents':services_referents,
            'lignes_etat'  : lignes,
            'etat_besoins' : etat_besoins,
            'etat_actuel_id' : int(etat_actuel_id),
            'operations' : dao_operation_stock.toListOperationsStock(),
            'categories' : dao_categorie_article.toListCategoriesArticle(),
            "utilisateur" : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		    'organisation': dao_organisation.toGetMainOrganisation(),
            'service_referent':service_referent,
            "departement" : dao_unite_fonctionnelle.toListUniteFonctionnelle(),
            "employes"    : dao_employe.toListEmployes(),
            'articles' : dao_article.toListArticlesStockables(),
            # "numero" : dao_bon_transfert.toGenerateNumeroTransfert(),
            "module" : ErpModule.MODULE_INVENTAIRE,
            "modules" : modules,
            'menu': 11,
            'numero':dao_bon_transfert.toGenerateNumeroBonSortie()
        }
        template = loader.get_template("ErpProject/ModuleInventaire/bon_sortie_smg/add.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        # print("Erreur GEt Transfert interne")
        # print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_sortie_mat_smg'))

#valider bon de srotie SMG
def get_valider_bon_sortie_smg(request):
    try:
        #Test de la validité de la date en fonction de l'activation d'une période dans un module
        if not auth.toPostValidityDate(var_module_id, request.POST["date_prevue"]): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")

        permission_number = 1008
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        operation_stock_id = int(request.POST["operation_stock_id"])
        # print("Testing ***")
        numero_bon = str(request.POST["numero_bon"])
        # demandeur_id =int(request.POST["demandeur_id"])
        # print("Numero Bon ***", numero_bon)
        operation_stock = dao_operation_stock.toGetOperationStock(operation_stock_id)
        emplacement_origine_id = int(request.POST["emplacement_origine_id"])
        emplacement_origine = dao_emplacement.toGetEmplacement(emplacement_origine_id)

        demandeur_id = int(request.POST["demandeur_id"])
        demandeur = dao_employe.toGetEmploye(demandeur_id)

        expression_id = int(request.POST["expression_id"])
        expression = dao_expression_besoin.toGetExpression(expression_id)
        lignes_expression = dao_ligne_expression.toListLigneOfExpressions(expression.id)
        # print('Expression de Besoin trouvé', expression.id)

        emplacement_destination_id = int(request.POST["emplacement_destination_id"])
        emplacement_destination = dao_emplacement.toGetEmplacement(emplacement_destination_id)

        context = {
            'sous_modules':sous_modules,
            'title' : "Valider le bon de sortie SMG",
            "emplacement_origine" : emplacement_origine,
            "emplacement_destination" : emplacement_destination,
            'operation_stock' : operation_stock,
            'expression':expression,
            'demandeur':demandeur,
            "utilisateur" : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		    'organisation': dao_organisation.toGetMainOrganisation(),
            "module" : ErpModule.MODULE_INVENTAIRE,
            "modules": modules,
            'menu' : 11,
            'numero_bon':numero_bon,
            'lignes_expression': lignes_expression,
            'demandeur_id': demandeur_id,
        }
        template = loader.get_template("ErpProject/ModuleInventaire/bon_sortie_smg/validate.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        # print("ERREUR")
        # print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_add_creer_bon_sortie_smg'))

#POST BON SORTIE SMG
@transaction.atomic
def post_valider_bon_sortie_(request):
    ''' Cette fonction crée un objet de type bon de transfert, mets à jour le statut du wkf de la demande d'achat si elle est attachée;
    La realisation effective du transfert des articles se fait dans la fonction post_realiser
    '''
    sid = transaction.savepoint()
    try:
        print('*****POST VALIDER BON SORTIE MAT SMG*******')
        numero_transfert = request.POST['numero']
        date_transfert = request.POST["date_prevue"]
        print('*****VALIDER BON TRANSFERT1*******', date_transfert)
        date_transfert = date_transfert[6:10] + '-' + date_transfert[3:5] + '-' + date_transfert[0:2]
        # date_transfert = timezone.datetime(int(date_transfert[6:10]), int(date_transfert[3:5]), int(date_transfert[0:2]))
        print('*****VALIDER BON TRANSFERT2*******')
        emplacement_origine_id = int(request.POST["emplacement_origine_id"])
        emplacement_destination_id = int(request.POST["emplacement_destination_id"])

        operation_stock_id = int(request.POST["operation_stock_id"])
        print('*****VALIDER BON TRANSFERT3*******')
        reference_document = request.POST["reference_document"]
        expression_id = int(request.POST["expression_id"])
        demandeur_id = int(request.POST["demandeur_id"])
        description = ""
        auteur = identite.utilisateur(request)
        print('*****Auteur*******', auteur)
        employe = auteur

        print("mama")
        bon_transfert = dao_bon_transfert.toCreateBonTransfert(numero_transfert, False, date_transfert, "BON LIVRAISON",operation_stock_id, emplacement_origine_id,emplacement_destination_id,employe.id, reference_document, description)
        bon_transfert = dao_bon_transfert.toSaveBonTransfert(auteur, bon_transfert)
        print('bon_transfert', bon_transfert)
        #Ajout traitement service referent necessaire pour le worflow
        #Recuperation du service referent destinataire
        #Enregistrement du services ref en fonction de l'emplacement destinataire
        service_referent = dao_unite_fonctionnelle.toGetUniteFonctionnelleOfEmplacement(emplacement_origine_id)
        bon_transfert.services_ref = service_referent
        bon_transfert.expression_id = expression_id
        bon_transfert.save()

        est_realisee = True
        #Fin traitement complementaire important pr Worflow

        print("geag")
        ##print(demande_achat_id)

        # if ((demande_achat_id != 0) and (demande_achat_id != "") and (demande_achat_id != None)):
        #     bon_transfert.demande_achat_id = demande_achat_id
        #     bon_transfert.save()
        #     demande_achat = dao_demande_achat.toGetDemande(demande_achat_id)

        #     #Flow de transition
        #     wkf_task.passingStepWorkflow(auteur,demande_achat)
        #     bon_entree = dao_bon_special.toGetBonEntreeOfDemande(demande_achat.id)
        #     wkf_task.passingStepWorkflow(auteur, bon_entree)

            #Mise à jour de la demande d'achat

        if bon_transfert != None :
            
            list_article_id = request.POST.getlist('article_id', None)
            print("list_article_id", list_article_id)
            list_quantite_demandee = request.POST.getlist("quantite_demandee", None)
            list_quantite_fournie = request.POST.getlist("quantite_fournie", None)
            list_description = request.POST.getlist("description", None)
            for i in range(0, len(list_article_id)) :
                print("BEGIN RANG")
                article_id = int(list_article_id[i])
                print("article_id", article_id)
                quantite_demandee = makeFloat(list_quantite_demandee[i])
                quantite_fournie = makeFloat(list_quantite_fournie[i])
                print("quantite_demandee", quantite_demandee)
                description = list_description[i]
                print("quantite_fournie", quantite_fournie)

                article = dao_article.toGetArticle(article_id)
                print("Article", article)
                les_stocks = dao_stock_article.toListStocksOfArticleInEmplacement(article_id, emplacement_origine_id)
                print("les_stocks", les_stocks)
                stock = les_stocks[0]

                ligne_transfert = dao_ligne_transfert.toCreateLigneTransfert(bon_transfert.id, stock.id, quantite_demandee, quantite_fournie,'',description)
                ligne_transfert = dao_ligne_transfert.toSaveLigneTransfert(auteur, ligne_transfert)
                print("Ligne transfert {0} creee ".format(ligne_transfert.id))
                

                #SORTIE
                # On recuper le stock de l'article dans l'emplacement de destination pour transfert
                stock_depart = dao_stock_article.toGetStockArticle(ligne_transfert.stock_article_id)    
                print("stock_depart {0} creee ".format(stock_depart.id))
                # list_stocks_destination = dao_stock_article.toListStocksOfArticleInEmplacement(stock_depart.article_id, emplacement_destination_id)
                # if list_stocks_destination: stock_destination = list_stocks_destination[0]
                # else:
                    # stock_destination = dao_stock_article.toCreateStockArticle(stock_depart.article_id,0,emplacement_destination_id)
                    # stock_destination = dao_stock_article.toSaveStockArticle(stock_destination)

                # DIMINUTION DE LA QUANTITE DU STOCK D'ORIGINE
                stock_depart.quantite_disponible = stock_depart.quantite_disponible - quantite_fournie
                dao_stock_article.toUpdateStockArticle(stock_depart.id, stock_depart)

                stock_destination = 5

                # if quantite_fournie > 0:
                #     mouvement_stock = dao_mouvement_stock.toCreateMouvementStock(quantite_fournie,"","TRANSFERT",stock_depart.id, stock_destination,None,None,None,bon_transfert.id)
                #     mv = dao_mouvement_stock.toSaveMouvementStock(employe, mouvement_stock)
                #     print("Mouvement Stock {0} creee ".format(mv))

            # WORKFLOWS INITIALS
            # type_document = "Bon de transmission"
            # wkf_task.initializeWorkflow(auteur,bon_transfert, type_document)
            bon_transfert.est_realisee = True
            if est_realisee == True :bon_transfert.date_realisation = timezone.now()

            bon_transfert.responsable_id = demandeur_id
            is_done = dao_bon_transfert.toUpdateBonTransfert(bon_transfert.id, bon_transfert)

            if is_done == True :
                transaction.savepoint_commit(sid)
                messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
                # return HttpResponseRedirect(reverse('module_inventaire_detail_bon_transfert', args=(bon_transfert.id,)))
                return HttpResponseRedirect(reverse('module_inventaire_list_sortie_mat_smg'))
            else:
                transaction.savepoint_rollback(sid)
                return HttpResponseRedirect(reverse('module_inventaire_add_creer_bon_sortie_smg'))

    except Exception as e:
        module='ModuleInventaire'
        auteur = identite.utilisateur(request)
        monLog.error("{} :: {}::\nErreur lors de l'enregistrement\n {}".format(auteur.nom_complet, module, e))
        ##print('Erreur lors de l enregistrement')
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_add_creer_bon_sortie_smg'))



####TRANSFERT INTERNAL#####
def get_lister_transfert_internal(request):
    permission_number = 152
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
    if response != None:
        return response

    title = "Liste des bons de sortie de matériel"
    # model = dao_article.toListArticles()
    #*******Filtre sur les règles **********#
    model = dao_model.toListModel(dao_article.toListArticles(), permission_number, groupe_permissions, identite.utilisateur(request))
    #******* End Regle *******************#

    transfert =  Model_Bon_transfert.objects.filter(operation_stock_id = 11).order_by("-creation_date")
    # #print("***Transfert", transfert)

    # transferts = dao_bon_transfert.toListBonTransfert()

    # transferts = dao_bon_transfert.toListBonTransfert()() if auth.toCheckAdmin(modules, utilisateur) else dao_bon_transfert.toListBonTransfert()ByAuteur(utilisateur.id)
    try:
	    view = str(request.GET.get("view","list"))
    except Exception as e:
	    view = "list"

    if "op" in request.GET:
        try:
            """operation_id = int(request.GET["op"])
            operation_stock = dao_operation_stock.toGetOperationStock(operation_id)
            transferts = dao_bon_transfert.toListTransfertsDuType(operation_stock.id)
            title = title + (" - %s" % operation_stock.designation)"""
            reference = str(request.GET["op"])

        except Exception as e:
            #print("ERREUR")
            #print(e)
            pass
    #Pagination
    transfert = pagination.toGet(request, transfert)


    context = {
        'sous_modules':sous_modules,
        'title' : title,
        'emplacements' : dao_emplacement.toListEmplacement(),
        'articles' : model,
        'transfert' : transfert,
        'categories' : dao_categorie_article.toListCategoriesArticle(),
        "utilisateur" : utilisateur,
        'view' : view,
        'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
        "modules" : modules,
        "module" : ErpModule.MODULE_INVENTAIRE,
        'menu': 11
    }
    template = loader.get_template("ErpProject/ModuleInventaire/internal/list.html")
    return HttpResponse(template.render(context, request))

def get_creer_transfert_internal(request):
    try:
        permission_number = 151
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        type_emplacement_entrepot = dao_type_emplacement.toGetTypeEmplacementEntrepot()
        ##print(type_emplacement_entrepot)
        entrepot = dao_emplacement.toGetEmplacement(type_emplacement_entrepot.id)
        ##print(entrepot)
        #etat_besoins = dao_expression_besoin.toListExpressionsNonTraites()

        #services_referents = dao_unite_fonctionnelle.toListUniteFonctionnelleWH()
        services_referents = dao_unite_fonctionnelle.toListUniteFonctionnelleWHNoneService()
        emplacement_internal = dao_emplacement.toGetEmplacementInternalBusiness()

        etat_actuel_id = 0
        etat = ""
        lignes = []

        try:
            etat_actuel_id = request.POST["doc_id"]
            etat = dao_expression_besoin.toGetExpression(etat_actuel_id)
            lignes = dao_ligne_expression.toListLigneOfExpressions(etat.id)
        except Exception as e:
            ##print("Aucun etat de besoin trouvé")
            pass

        if utilisateur.unite_fonctionnelle != None:

            etat_besoins = dao_expression_besoin.toListExpressionsNonTraitesByServiceRef(utilisateur.unite_fonctionnelle.id)
            ##print("etat", etat_besoins)
            service_referent = dao_unite_fonctionnelle.toGetUniteFonctionnelle(utilisateur.unite_fonctionnelle_id)
        else:
            etat_besoins = dao_expression_besoin.toListExpressionsNonTraites()
            service_referent = 0
        context = {
            'sous_modules':sous_modules,
            'title' : "Nouveau bon de sortie de matériel",
            'emplacements':dao_emplacement.toListEmplacementsInEntrepot(entrepot.id),
            'type_emplacement_entre': dao_type_emplacement.toGetTypeEmplacementEntree(),
            'type_emplacement_stock': dao_type_emplacement.toGetTypeEmplacementStock(),
            'etat' : etat,
            'emplacement_internal':emplacement_internal,
            'services_referents':services_referents,
            'lignes_etat'  : lignes,
            'etat_besoins' : etat_besoins,
            'etat_actuel_id' : int(etat_actuel_id),
            'operations' : dao_operation_stock.toListOperationsStock(),
            'categories' : dao_categorie_article.toListCategoriesArticle(),
            "utilisateur" : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		    'organisation': dao_organisation.toGetMainOrganisation(),
            'service_referent':service_referent,
            "departement" : dao_unite_fonctionnelle.toListUniteFonctionnelle(),
            "employes"    : dao_employe.toListEmployes(),
            'articles' : dao_article.toListArticlesStockables(),
            "numero" : dao_bon_transfert.toGenerateNumeroTransfert(),
            "module" : ErpModule.MODULE_INVENTAIRE,
            "modules" : modules,
            'menu': 11,
            'numero':dao_bon_transfert.toGenerateNumeroBonSortie()
        }
        template = loader.get_template("ErpProject/ModuleInventaire/internal/add.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        # print("Erreur GEt Transfert interne")
        # print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_transfert_internal'))




def get_valider_transfert_internal(request):
    try:
        #Test de la validité de la date en fonction de l'activation d'une période dans un module
        if not auth.toPostValidityDate(var_module_id, request.POST["date_prevue"]): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")

        permission_number = 151
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        operation_stock_id = int(request.POST["operation_stock_id"])
        # print("Testing ***")
        numero_bon = str(request.POST["numero_bon"])
        # print("Numero Bon ***", numero_bon)
        operation_stock = dao_operation_stock.toGetOperationStock(operation_stock_id)
        emplacement_origine_id = int(request.POST["emplacement_origine_id"])
        emplacement_origine = dao_emplacement.toGetEmplacement(emplacement_origine_id)

        demandeur_id = int(request.POST["demandeur_id"])
        demandeur = dao_employe.toGetEmploye(demandeur_id)

        expression_id = int(request.POST["expression_id"])
        expression = dao_expression_besoin.toGetExpression(expression_id)
        # print('Expression de Besoin trouvé', expression.id)

        emplacement_destination_id = int(request.POST["emplacement_destination_id"])
        emplacement_destination = dao_emplacement.toGetEmplacement(emplacement_destination_id)

        context = {
            'sous_modules':sous_modules,
            'title' : "Valider le bon de sortie de matériel",
            "emplacement_origine" : emplacement_origine,
            "emplacement_destination" : emplacement_destination,
            'operation_stock' : operation_stock,
            'expression':expression,
            'demandeur':demandeur,
            "utilisateur" : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		    'organisation': dao_organisation.toGetMainOrganisation(),
            "module" : ErpModule.MODULE_INVENTAIRE,
            "modules": modules,
            'menu' : 11,
            'numero_bon':numero_bon,
        }
        template = loader.get_template("ErpProject/ModuleInventaire/internal/validate.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        # print("ERREUR")
        # print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_add_transfert_internal'))

@transaction.atomic
def post_valider_transfert_internal(request):
    sid = transaction.savepoint()
    ##print("SID : %s" % sid)
    try:
        numero_transfert = ""
        numero_transfert = request.POST["numero_bon"]
        ##print("Testing")
        date_transfert = request.POST["date_prevue"]
        date_transfert = timezone.datetime(int(date_transfert[6:10]), int(date_transfert[3:5]), int(date_transfert[0:2]))
        emplacement_origine_id = int(request.POST["emplacement_origine_id"])
        ##print("emplacement_origine_id")



        emplacement_destination_id = int(request.POST["emplacement_destination_id"])
        # print("ZE")
        operation_stock_id = int(request.POST["operation_stock_id"])
        ##print("RE")
        reference_document = request.POST["reference_document"]
        demandeur_id = int(request.POST["demandeur_id"])
        ##print("LO")
        description = ""
        est_partiel = request.POST["est_partiel"]
        ##print(est_partiel)
        expression_id = int(request.POST["expression_id"])
        # print("EXPRESSION", expression_id)
        auteur = identite.utilisateur(request)
        employe_id = auteur.id

        bon_transfert = dao_bon_transfert.toCreateBonTransfert(numero_transfert, False, date_transfert,"SORTIE MATERIEL", operation_stock_id,emplacement_origine_id, emplacement_destination_id, employe_id, reference_document, description, 0.0, 0,"", None, demandeur_id)
        bon_transfert = dao_bon_transfert.toSaveBonTransfert(auteur, bon_transfert)
        # print("Bon", bon_transfert)
        bon_transfert.expression_id = expression_id
        # print("Expression ELEKI")
        service_referent = dao_unite_fonctionnelle.toGetUniteFonctionnelleOfEmplacement(emplacement_origine_id)
        bon_transfert.services_ref = service_referent
        bon_transfert.save()
        ##print("nnn")
        # print(bon_transfert)


        #StopHere
        expression = dao_expression_besoin.toGetExpression(expression_id)


        if est_partiel == "true":
            uneetape = dao_wkf_etape.toGetEtapeByDesignation("Livré partiellement")
            ##print(uneetape)

            ##print('***VALIDER LIVRAISON PARTIELLE**')

            list_QD = request.POST.getlist('quantite_demandee', None)
            list_QF = request.POST.getlist('quantite_fournie', None)
            list_article_id = request.POST.getlist('article_id', None)
            for i in range(0, len(list_article_id)) :
                qd = int(list_QD[i])
                qf = int(list_QF[i])
                articleid = int(list_article_id[i])
                quantite_restant = qd - qf
                rest = dao_ligne_expression.toupdateLigneExpressionLivraisonPartielle(expression_id,articleid,quantite_restant)
                # print('**INSERTION DES NOMBRES D\'ARTICLES RESTANT**')
                # print('**La quantité restante:**',rest)

            wkf_task.passingStepWorkflow(auteur,expression,uneetape.id)

        else:
            uneetape = dao_wkf_etape.toGetEtapeByDesignation("Articles livrés")
            wkf_task.passingStepWorkflow(auteur,expression, uneetape.id)
            ##print('***VALIDER LIVRAISON COMPLETE**')


        if bon_transfert != None :
            ##print("Ligne transfert {0} creee ".format(bon_transfert.id))
            list_article_id = request.POST.getlist('article_id', None)
            ##print(list_article_id)
            list_numero_serie = request.POST.getlist('numero_serie', None)
            ##print(list_numero_serie)
            list_description = request.POST.getlist('description', None)
            ##print(list_description)
            list_quantite_demandee = request.POST.getlist('quantite_demandee', None)
            list_quantite_fournie = request.POST.getlist('quantite_fournie', None)
            #list_quantite_demandee = request.POST.getlist("quantite_demandee", None)
            for i in range(0, len(list_article_id)) :
                # print("in")
                article_id = int(list_article_id[i])
                # print("in1")
                numero_serie = list_numero_serie[i]
                # print("in2")
                description = list_description[i]
                # print("in3")
                quantite_demandee = makeFloat(list_quantite_demandee[i])
                quantite_fournie = makeFloat(list_quantite_fournie[i])

                # quantite_restant = quantite_demandee - quantite_fournie
                # quantite_restant = dao_ligne_expression.toupdateLigneExpressionLivraisonPartielle(expression_id, quantite_restant)
                # ##print('**La quantité restante:**',quantite_restant)

                article = dao_article.toGetArticle(article_id)
                print(article)
                print(emplacement_origine_id)
                print(dao_emplacement.toGetEmplacement(emplacement_origine_id))
                les_stocks = dao_stock_article.toListStocksOfArticleInEmplacement(article_id, emplacement_origine_id)
                # print('**LES STOCKS**', les_stocks)
                stock = les_stocks[0]
                # print("Les Stocks", stock)


                ligne_transfert = dao_ligne_transfert.toCreateLigneTransfert(bon_transfert.id, stock.id, quantite_demandee,quantite_fournie, numero_serie,description)
                ligne_transfert = dao_ligne_transfert.toSaveLigneTransfert(auteur, ligne_transfert)
                # print("Ligne", ligne_transfert)


                #gestion des assets
                '''if int(employe_id) != 0:
                    employe = dao_employe.toGetEmploye(employe_id)
                    unite_fonctionnelle_id = employe.unite_fonctionnelle_id
                else:
                    unite_fonctionnelle_id = int(list_departement_id[i])
                    employe_id = None
                ##print("in")
                asset=dao_asset.toCreateAsset(dao_utils.genererNumeroAsset(),type_asset,article_id,employe_id,unite_fonctionnelle_id, bon_transfert.id)
                asset=dao_asset.toSaveAsset(auteur, asset)'''
            ##print("Ligne transfert {0} creee ".format(ligne_transfert.id))


            # WORKFLOWS INITIALS
            type_document = "Sortie de matériel"
            wkf_task.initializeWorkflow(auteur,bon_transfert,type_document)

            transaction.savepoint_commit(sid)
            return HttpResponseRedirect(reverse('module_inventaire_details_transfert_internal', args=(bon_transfert.id,)))
        else:
            transaction.savepoint_rollback(sid)
            return HttpResponseRedirect(reverse('module_inventaire_list_transfert_internal'))
    except Exception as e:
        # print("ERREUR")
        # print(e)
        transaction.savepoint_rollback(sid)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_add_transfert_internal'))

def get_realiser_transfert_internal(request, ref):
    try:
        permission_number = 151
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        bon_transfert = dao_bon_transfert.toGetBonTransfert(ref)
        service_ref = dao_unite_fonctionnelle.toGetUniteFonctionnelleOfEmplacement(bon_transfert.emplacement_origine.id)
        if service_ref.libelle == "Moyens généraux":
            #employe_role = dao_role.toGetPersonOfRole("Technicien MG")
            employe_role = dao_groupe_permission.toGetPersonOfPermission("Technicien MG")
        else:
            employe_role = dao_groupe_permission.toGetPersonOfPermission("Technicien SI")
            #employe_role = dao_role.toGetPersonOfRole("Technicien SI")

        ref = int(ref)
        bon_transfert = dao_bon_transfert.toGetBonTransfert(ref)
        if bon_transfert.est_realisee == True : return HttpResponseRedirect(reverse('module_inventaire_list_transfert_internal'))
        lignes = dao_ligne_transfert.toListLignesTransfert(bon_transfert.id)
        item = lignes[0]
        stock = dao_stock_article.toGetStockArticle(item.stock_article_id)
        emplacement_origine = dao_emplacement.toGetEmplacement(stock.emplacement_id)
        context = {
            'sous_modules':sous_modules,
            'title' : "Bon de sortie de matériel N°%s" % bon_transfert.numero_transfert,
            'model' : bon_transfert,
            'lignes' : lignes,
            "service_referent_origine" : dao_unite_fonctionnelle.toGetUniteFonctionnelleOfEmplacement(emplacement_origine.id),
            "agents" : employe_role,
            "utilisateur" : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
            "module" : ErpModule.MODULE_INVENTAIRE,
            "modules": modules,
            'menu' : 11
        }
        template = loader.get_template("ErpProject/ModuleInventaire/internal/release.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_transfert_internal'))

@transaction.atomic
def post_realiser_transfert_internal(request):
    sid = transaction.savepoint()
    ##print("On est là")
    ordre_id = int(request.POST["ordre_id"])
    try:
        auteur = identite.utilisateur(request)
        responsable_id = int(request.POST["responsable_id"])
        agent_id = int(request.POST["agent_id"])
        est_realisee = True

        bon_transfert = dao_bon_transfert.toGetBonTransfert(ordre_id)
        operation_stock = dao_operation_stock.toGetOperationStock(bon_transfert.operation_stock_id)
        emplacement_destination = dao_emplacement.toGetEmplacement(bon_transfert.emplacement_destination_id)
        list_ligne_id = request.POST.getlist('ligne_id', None)
        list_quantite_fournie = request.POST.getlist("quantite_fournie", None)
        ##print(len(list_ligne_id))
        ##print(len(list_quantite_fournie))
        for i in range(0, len(list_ligne_id)):
            ligne_id = int(list_ligne_id[i])
            quantite_fournie = makeFloat(list_quantite_fournie[i])

            ligne_transfert = dao_ligne_transfert.toGetLigneTransfert(ligne_id)
            #Si la quantité demandée est superieure à la somme des quantitées déjà fournies, on n'est réalise pas pcq on n'a pas encore tout reçu
            if quantite_fournie > ligne_transfert.quantite_fournie : return HttpResponseRedirect(reverse('module_inventaire_realiser_transfert_internal', args=(ordre_id,)))

            # On ajoute la nouvelle quantité reçue
            ligne_transfert.quantite_fournie = quantite_fournie
            dao_ligne_transfert.toUpdateLigneTransfert(ligne_id, ligne_transfert)

            # On recuper le stock de l'article dans l'emplacement de destination pour transfert
            stock_depart = dao_stock_article.toGetStockArticle(ligne_transfert.stock_article_id)
            list_stocks_destination = dao_stock_article.toListStocksOfArticleInEmplacement(stock_depart.article_id, emplacement_destination.id)
            if list_stocks_destination: stock_destination = list_stocks_destination[0]
            else:
                # Si il ya pas de stock pour cet article dans cet emplacement, on crée un nouveau stock
                stock_destination = dao_stock_article.toCreateStockArticle(0, emplacement_destination.id, stock_depart.article_id)
                stock_destination = dao_stock_article.toSaveStockArticle(auteur, stock_destination)

            # DIMINUTION DE LA QUANTITE DU STOCK D'ORIGINE
            stock_depart.quantite_disponible = stock_depart.quantite_disponible - quantite_fournie
            dao_stock_article.toUpdateStockArticle(stock_depart.id, stock_depart)

            # AUGMENTATION DE LA QUANTITE DU STOCK DE DESTINATION
            stock_destination.quantite_disponible = stock_destination.quantite_disponible + quantite_fournie
            dao_stock_article.toUpdateStockArticle(stock_destination.id, stock_destination)

            #ENREGISTRER LE MOUVEMENT
            if quantite_fournie > 0:
                mouvement_stock = dao_mouvement_stock.toCreateMouvementStock(quantite_fournie,"","TRANSFERT",stock_depart.id, stock_destination.id,None,None,None,ordre_id)
                dao_mouvement_stock.toSaveMouvementStock(auteur, mouvement_stock)

        bon_transfert.est_realisee = est_realisee
        if est_realisee == True :
            bon_transfert.date_realisation = timezone.now()

        bon_transfert.employe_id = responsable_id
        ##print("agent")
        ##print(agent_id)
        if agent_id != 0 :
            bon_transfert.agent_id = agent_id

        is_done = dao_bon_transfert.toUpdateBonTransfert(ordre_id, bon_transfert)


        #Flow
        bon_transfert = dao_bon_transfert.toGetBonTransfert(ordre_id)
        wkf_task.passingStepWorkflow(auteur,bon_transfert)


        if is_done == True :
            transaction.savepoint_commit(sid)
            return HttpResponseRedirect(reverse('module_inventaire_details_transfert_internal', args=(ordre_id,)))
        else:
            transaction.savepoint_rollback(sid)
            return HttpResponseRedirect(reverse('module_inventaire_realiser_transfert_internal', args=(ordre_id,)))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        transaction.savepoint_rollback(sid)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_realiser_transfert_internal', args=(ordre_id,)))


def get_to_asset_of_transfert_internal(request):
    sid = transaction.savepoint()
    ordre_id = int(request.POST["ordre_id"])
    try:
        permission_number = 152
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        responsable_id = int(request.POST["responsable_id"])
        agent_id = int(request.POST["agent_id"])
        ##print(agent_id)
        est_realisee = True
        dico_asset = {}

        bon_transfert = dao_bon_transfert.toGetBonTransfert(ordre_id)
        emplacement_origine = dao_emplacement.toGetEmplacement(bon_transfert.emplacement_origine_id)
        emplacement_destination = dao_emplacement.toGetEmplacement(bon_transfert.emplacement_destination_id)
        list_ligne_id = request.POST.getlist('ligne_id', None)
        list_quantite_fournie = request.POST.getlist("quantite_fournie", None)

        lignes = dao_ligne_transfert.toListLignesTransfert(ordre_id)
        for ligne in lignes:
            dico_asset[ligne.article_identifiant] = dao_asset.toGetAssetByArticleOfEmplacement(ligne.article_identifiant,emplacement_origine.id)

        is_done = True
        if is_done == True :

            lignes = dao_ligne_transfert.toListLignesTransfert(ordre_id)
            bon_transfert = dao_bon_transfert.toGetBonTransfert(ordre_id)
            serv_ref_id = request.POST["service_referent_id"]
            service_referent = dao_unite_fonctionnelle.toGetUniteFonctionnelle(serv_ref_id)

            context = {
                'sous_modules':sous_modules,
                'title' : "Affecter les assets relatifs au bon N°%s" % bon_transfert.numero_transfert,
                'model' : bon_transfert,
                'lignes' : lignes,
                "dico_asset":dico_asset,
                "service_referent" : service_referent,
                "utilisateur" : utilisateur,
                "module" : ErpModule.MODULE_INVENTAIRE,
                'actions':auth.toGetActions(modules,utilisateur),
		        'organisation': dao_organisation.toGetMainOrganisation(),
                "modules": modules,
                'responsable_id':responsable_id,
                'roles':groupe_permissions,
                'agent_id':agent_id,
                'ordre_id':ordre_id,
                'list_quantite_fournie':list_quantite_fournie,
                'menu' : 11
            }

            template = loader.get_template("ErpProject/ModuleInventaire/internal/asset.html")
            return HttpResponse(template.render(context, request))
        else:

            return HttpResponseRedirect(reverse('module_inventaire_realiser_transfert_internal', args=(ordre_id,)))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_realiser_transfert_internal', args=(ordre_id,)))


@transaction.atomic
def post_to_asset_of_transfert_internal(request):
    sid = transaction.savepoint()
    ordre_id = int(request.POST["ordre_id"])
    try:

        auteur = identite.utilisateur(request)
        responsable_id = int(request.POST["responsable_id"])
        agent_id = int(request.POST["agent_id"])
        ##print('agent on POST')
        ##print(agent_id)
        est_realisee = True

        bon_transfert = dao_bon_transfert.toGetBonTransfert(ordre_id)
        operation_stock = dao_operation_stock.toGetOperationStock(bon_transfert.operation_stock_id)
        emplacement_destination = dao_emplacement.toGetEmplacement(bon_transfert.emplacement_destination_id)
        list_ligne_id = request.POST.getlist('ligne_id', None)
        list_quantite_fournie = request.POST.getlist("quantite_fournie", None)
        ##print(list_ligne_id)
        ##print("listes")
        ##print(list_quantite_fournie)
        ##print(len(list_ligne_id))
        ##print(len(list_quantite_fournie))
        for i in range(0, len(list_ligne_id)):
            ligne_id = int(list_ligne_id[i])
            quantite_fournie = makeFloat(list_quantite_fournie[i])

            ligne_transfert = dao_ligne_transfert.toGetLigneTransfert(ligne_id)
            #Si la quantité demandée est superieure à la somme des quantitées déjà fournies, on n'est réalise pas pcq on n'a pas encore tout reçu
            if quantite_fournie > ligne_transfert.quantite_fournie : return HttpResponseRedirect(reverse('module_inventaire_realiser_transfert_internal', args=(ordre_id,)))

            # On ajoute la nouvelle quantité reçue
            ligne_transfert.quantite_fournie = quantite_fournie
            dao_ligne_transfert.toUpdateLigneTransfert(ligne_id, ligne_transfert)

            # On recuper le stock de l'article dans l'emplacement de destination pour transfert
            stock_depart = dao_stock_article.toGetStockArticle(ligne_transfert.stock_article_id)
            list_stocks_destination = dao_stock_article.toListStocksOfArticleInEmplacement(stock_depart.article_id, emplacement_destination.id)
            if list_stocks_destination: stock_destination = list_stocks_destination[0]
            else:
                # Si il ya pas de stock pour cet article dans cet emplacement, on crée un nouveau stock
                stock_destination = dao_stock_article.toCreateStockArticle(0, emplacement_destination.id, stock_depart.article_id)
                stock_destination = dao_stock_article.toCreateStockArticle(stock_depart.article_id,0,emplacement_destination.id)
                stock_destination = dao_stock_article.toSaveStockArticle(stock_destination)

            # DIMINUTION DE LA QUANTITE DU STOCK D'ORIGINE
            stock_depart.quantite_disponible = stock_depart.quantite_disponible - quantite_fournie
            dao_stock_article.toUpdateStockArticle(stock_depart.id, stock_depart)

            # AUGMENTATION DE LA QUANTITE DU STOCK DE DESTINATION
            stock_destination.quantite_disponible = stock_destination.quantite_disponible + quantite_fournie
            dao_stock_article.toUpdateStockArticle(stock_destination.id, stock_destination)

            #ENREGISTRER LE MOUVEMENT
            if quantite_fournie > 0:
                mouvement_stock = dao_mouvement_stock.toCreateMouvementStock(quantite_fournie,"","TRANSFERT",stock_depart.id, stock_destination.id,None,None,None,ordre_id)
                dao_mouvement_stock.toSaveMouvementStock(auteur, mouvement_stock)

        bon_transfert.est_realisee = est_realisee
        if est_realisee == True :
            bon_transfert.date_realisation = timezone.now()

        bon_transfert.employe_id = responsable_id
        if agent_id != 0 :
            ##print("inside")
            bon_transfert.agent_id = agent_id

        is_done = dao_bon_transfert.toUpdateBonTransfert(ordre_id, bon_transfert)


        #Flow
        bon_transfert = dao_bon_transfert.toGetBonTransfert(ordre_id)
        wkf_task.passingStepWorkflow(auteur,bon_transfert)

        #Traitement des assets

        #list_numero_serie = request.POST.getlist('numero_serie', None)
        list_asset_id = request.POST.getlist('asset_id', None)

        #list_description = request.POST.getlist('description', None)
        list_article_id = request.POST.getlist('article_id', None)
        service_ref_id = request.POST["service_referent_id"]
        ##print("responsable")
        ##print(responsable_id)
        for i in range(0, len(list_asset_id)):
            ##print("inside ")
            asset_id = list_asset_id[i]
            ##print(asset_id)
            asset = dao_asset.toUpdateAssetAffectation(asset_id,responsable_id)
            ##print(asset)


        if is_done == True :
            transaction.savepoint_commit(sid)
            return HttpResponseRedirect(reverse('module_inventaire_details_transfert_internal', args=(ordre_id,)))
        else:
            transaction.savepoint_rollback(sid)
            return HttpResponseRedirect(reverse('module_inventaire_realiser_transfert_internal', args=(ordre_id,)))
    except Exception as e:
        transaction.savepoint_rollback(sid)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_realiser_transfert_internal', args=(ordre_id,)))

def get_details_transfert_internal(request, ref):
    try:
        permission_number = 152
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response
        ref = int(ref)

        transfert = dao_bon_transfert.toGetBonTransfert(ref)
        lignes = dao_ligne_transfert.toListLignesTransfert(ref)

        service_ref = dao_unite_fonctionnelle.toGetUniteFonctionnelleOfEmplacement(transfert.emplacement_origine.id)
        est_integrale = True
        #lignes = dao_ligne_transfert.toListLignesTransfert(ref)
        for ligne in lignes:
            if ligne.quantite_demandee > ligne.quantite_fournie:
                est_integrale = False
                break
        item = lignes[0]
        stock = dao_stock_article.toGetStockArticle(item.stock_article_id)
        emplacement_origine = dao_emplacement.toGetEmplacement(stock.emplacement_id)

        historique, transition_etape_suivant, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,transfert)


        context = {
            'title' : transfert.numero_transfert,
            'model' : transfert,
            'lignes' : lignes,
            'historique' : historique,
            'etapes_suivantes' : transition_etape_suivant,
            'est_integrale':est_integrale,
            'roles':groupe_permissions,
            'content_type_id':content_type_id,
            "documents":documents,
            'signee' : signee,
            'service_referent':service_ref,
            'emplacement_origine' : emplacement_origine,
            "utilisateur" : utilisateur,
            'sous_modules':sous_modules,
            'actions':auth.toGetActions(modules,utilisateur),
		    'organisation': dao_organisation.toGetMainOrganisation(),
            "module" : ErpModule.MODULE_INVENTAIRE,
            "modules": modules,
            "menu" : 11
        }
        template = loader.get_template("ErpProject/ModuleInventaire/internal/item.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        ##print("erreur", e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_transfert_internal'))


def get_completer_transfert_internal(request, ref):
    try:
        permission_number = 153
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        ref = int(ref)

        bon_transfert = dao_bon_transfert.toGetBonTransfert(ref)
        est_integrale = True
        lignes = dao_ligne_transfert.toListLignesTransfert(bon_transfert.id)
        for ligne in lignes:
            if ligne.quantite_demandee > ligne.quantite_fournie:
                est_integrale = False
                break
        ##print(bon_transfert)
        if ((bon_transfert.est_realisee == True) and (est_integrale == True)) : return HttpResponseRedirect(reverse('module_inventaire_list_transfert_internal'))

        item = lignes[0]
        stock = dao_stock_article.toGetStockArticle(item.stock_article_id)
        emplacement_origine = dao_emplacement.toGetEmplacement(stock.emplacement_id)
        context = {
            'sous_modules':sous_modules,
            'title' : "Bon de sortie de matériel N°%s" % bon_transfert.numero_transfert,
            'model' : bon_transfert,
            'lignes' : lignes,
            "emplacement_origine" : emplacement_origine,
            "agents" : dao_employe.toListEmployesActifs(),
            "utilisateur" : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		    'organisation': dao_organisation.toGetMainOrganisation(),
            "modules" : modules ,
            "module" : ErpModule.MODULE_INVENTAIRE,
            'menu' : 4
        }
        template = loader.get_template("ErpProject/ModuleInventaire/internal/complete.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_transfert_internal'))


@transaction.atomic
def post_completer_transfert_internal(request):
    sid = transaction.savepoint()
    ordre_id = int(request.POST["ordre_id"])
    try:
        auteur = identite.utilisateur(request)
        responsable_id = int(request.POST["responsable_id"])
        est_realisee = True
        ##print("nakati 2")

        bon_transfert = dao_bon_transfert.toGetBonTransfert(ordre_id)
        operation_stock = dao_operation_stock.toGetOperationStock(bon_transfert.operation_stock_id)
        emplacement_destination = dao_emplacement.toGetEmplacement(bon_transfert.emplacement_destination_id)
        list_ligne_id = request.POST.getlist('ligne_id', None)
        list_quantite_fournie = request.POST.getlist("quantite_fournie", None)
        ##print(len(list_ligne_id))
        ##print(len(list_quantite_fournie))
        for i in range(0, len(list_ligne_id)):
            ligne_id = int(list_ligne_id[i])
            quantite_recue = makeFloat(list_quantite_fournie[i])

            ligne_transfert = dao_ligne_transfert.toGetLigneTransfert(ligne_id)
            #Si la quantité demandée est superieure à la somme des quantitées déjà fournies, on n'est réalise pas pcq on n'a pas encore tout reçu
            if (quantite_recue + ligne_transfert.quantite_fournie) > ligne_transfert.quantite_demandee : return HttpResponseRedirect(reverse('module_inventaire_compleyer_bon_transfert', args=(ordre_id,)))
            #if ligne_transfert.quantite_demandee > ligne_transfert.quantite_fournie + quantite_fournie : est_realisee = False

            # On ajoute la nouvelle quantité reçue
            ##print(ligne_transfert.quantite_fournie)
            ligne_transfert.quantite_fournie = ligne_transfert.quantite_fournie + quantite_recue
            ##print(quantite_recue)
            ##print(ligne_transfert.quantite_fournie)
            #breakpoint
            dao_ligne_transfert.toUpdateLigneTransfert(ligne_id, ligne_transfert)

            # On recuper le stock de l'article dans l'emplacement de destination pour transfert
            stock_depart = dao_stock_article.toGetStockArticle(ligne_transfert.stock_article_id)
            list_stocks_destination = dao_stock_article.toListStocksOfArticleInEmplacement(stock_depart.article_id, emplacement_destination.id)
            if list_stocks_destination: stock_destination = list_stocks_destination[0]
            else:
                # Si il ya pas de stock pour cet article dans cet emplacement, on crée un nouveau stock
                stock_destination = dao_stock_article.toCreateStockArticle(0, emplacement_destination.id, stock_depart.article_id)
                stock_destination = dao_stock_article.toSaveStockArticle(auteur, stock_destination)

            # DIMINUTION DE LA QUANTITE DU STOCK D'ORIGINE
            stock_depart.quantite_disponible = stock_depart.quantite_disponible - quantite_recue
            dao_stock_article.toUpdateStockArticle(stock_depart.id, stock_depart)

            # AUGMENTATION DE LA QUANTITE DU STOCK DE DESTINATION
            stock_destination.quantite_disponible = stock_destination.quantite_disponible + quantite_recue
            dao_stock_article.toUpdateStockArticle(stock_destination.id, stock_destination)

            #ENREGISTRER LE MOUVEMENT
            if quantite_recue > 0:
                mouvement_stock = dao_mouvement_stock.toCreateMouvementStock(quantite_recue,"","TRANSFERT",stock_depart.id, stock_destination.id,None,None,None,ordre_id)
                dao_mouvement_stock.toSaveMouvementStock(auteur, mouvement_stock)

        bon_transfert.est_realisee = est_realisee
        if est_realisee == True :
            bon_transfert.date_realisation = timezone.now()

        bon_transfert.employe_id = responsable_id
        is_done = dao_bon_transfert.toUpdateBonTransfert(ordre_id, bon_transfert)



        if is_done == True :
            transaction.savepoint_commit(sid)
            return HttpResponseRedirect(reverse('module_inventaire_details_transfert_internal', args=(ordre_id,)))
        else:
            transaction.savepoint_rollback(sid)
            return HttpResponseRedirect(reverse('module_inventaire_completer_transfert_internal', args=(ordre_id,)))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        transaction.savepoint_rollback(sid)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_completer_transfert_internal', args=(ordre_id,)))


@transaction.atomic
def post_workflow_affectation(request):
    sid = transaction.savepoint()
    try:
        utilisateur_id = request.user.id
        auteur = identite.utilisateur(request)
        base_dir = settings.BASE_DIR
        media_dir = settings.MEDIA_ROOT
        media_url = settings.MEDIA_URL
        etape_id = request.POST["etape_id"]
        transfert_id = request.POST["doc_id"]

        employe = dao_employe.toGetEmployeFromUser(utilisateur_id)
        etape = dao_wkf_etape.toGetEtapeWorkflow(etape_id)
        bon_transfert = dao_bon_transfert.toGetBonTransfert(transfert_id)

        service_ref = dao_unite_fonctionnelle.toGetUniteFonctionnelleOfEmplacement(bon_transfert.emplacement_origine.id)

        transitions_etapes_suivantes = dao_wkf_etape.toListEtapeSuivante(bon_transfert.statut_id, service_ref.id)
        for item in transitions_etapes_suivantes:

            if item.condition.designation == "Upload":
                if 'file_upload' in request.FILES:
                    nom_fichier = request.FILES['file_upload']
                    doc = dao_document.toUploadDocument(auteur, nom_fichier, bon_transfert)

                    bon_transfert.statut_id = etape.id
                    bon_transfert.etat = etape.designation
                    bon_transfert.save()
                    document = dao_document_bon_transfert.toCreateDocument("Bon de sortie de matériel",doc.url_document, bon_transfert.etat,transfert_id)
                    document = dao_document_bon_transfert.toSaveDocument(auteur, document)
                else:
                    pass

            else:
                # Gestion des transitions dans le document
                bon_transfert.statut_id = etape.id
                bon_transfert.etat = etape.designation
                bon_transfert.save()

        historique = dao_wkf_historique_bon_transfert.toCreateHistoriqueWorkflow(employe.id, etape.id, bon_transfert.id)
        historique = dao_wkf_historique_bon_transfert.toSaveHistoriqueWorkflow(historique)

        if historique != None :
            transaction.savepoint_commit(sid)
            #return HttpResponseRedirect(reverse('module_achat_details_bon_achat', args=(demande.id,)))
            return HttpResponseRedirect(reverse('module_inventaire_details_transfert_internal', args=(transfert_id,)))
        else:
            transaction.savepoint_rollback(sid)
            return HttpResponseRedirect(reverse('module_inventaire_details_transfert_internal', args=(transfert_id,)))

    except Exception as e:
        transaction.savepoint_rollback(sid)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_transfert_internal'))

def get_lister_asset(request):
    # modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(7, request)
    permission_number = 4
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
    if response != None:
        return response

    # model = dao_asset.toListAsset()
    #*******Filtre sur les règles **********#
    model = dao_model.toListModel(dao_asset.toListAsset(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
    context ={'title' : 'Liste d\'assets','model' : model,'utilisateur' : utilisateur,
    'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
        'sous_modules':sous_modules,
    'modules' : modules,"module" : ErpModule.MODULE_INVENTAIRE,'menu' : 1}
    template = loader.get_template('ErpProject/ModuleInventaire/asset/list.html')
    return HttpResponse(template.render(context, request))

def get_creer_asset(request):
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(7, request)
    if response != None:
        return response

    model = dao_employe.toListEmployes()
    model2 = dao_article.toListArticles()
    model3 = dao_unite_fonctionnelle.toListUniteFonctionnelle()
    context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Nouvel asset','model':model,'model2':model2,'model3':model3,'utilisateur' : utilisateur,
    'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
    'modules' : modules,"module" : ErpModule.MODULE_INVENTAIRE,'menu' : 2}
    template = loader.get_template('ErpProject/ModuleInventaire/asset/add.html')
    return HttpResponse(template.render(context, request))

def post_creer_asset(request):

    try:
        numero_identification = dao_utils.genererNumeroAsset()
        article_id = request.POST['article_id']
        employe_id = request.POST['employe_id']
        type = request.POST['type']
        auteur = identite.utilisateur(request)
        if int(employe_id) != 0:
            employe = dao_employe.toGetEmploye(employe_id)
            unite_fonctionnelle_id = employe.unite_fonctionnelle_id
        else:
             employe_id = None
             unite_fonctionnelle_id = request.POST['unite_fonctionnelle_id']

        unite_fonctionnelle = dao_unite_fonctionnelle.toGetUniteFonctionnelle(unite_fonctionnelle_id)
        asset = dao_asset.toCreateAsset(numero_identification,type,article_id,employe_id,unite_fonctionnelle.emplacement_id,"")
        #asset = dao_asset.toCreateAsset(num_serie,"ARTICLES",art_id,None,emplacement.id,descript)
        asset=dao_asset.toSaveAsset(auteur, asset)
        messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
        return HttpResponseRedirect(reverse('module_inventaire_detail_asset', args=(asset.id)))
    except Exception as e:
        ##print('Erreur lors de l enregistrement')
        auteur = identite.utilisateur(request)
        monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER IMMOBILIER \n {}'.format(auteur.nom_complet, module,e))
        #print(e)
        messages.add_message(request, messages.ERROR,e)
        return HttpResponseRedirect(reverse('module_inventaire_add_asset'))


def get_details_asset(request,ref):
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(7, request)
    if response != None:
        return response
    try:
        ref=int(ref)
        asset=dao_asset.toGetAsset(ref)
        historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,asset)

        template = loader.get_template('ErpProject/ModuleInventaire/asset/item.html')
        context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Details d\'un asset','asset' : asset,'utilisateur' : utilisateur,
        'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
        "historique": historique,
        "etapes_suivantes": etapes_suivantes,
        "signee": signee,
        "content_type_id": content_type_id,
        "documents": documents,
        "roles": groupe_permissions,
        'modules' : modules,"module" : ErpModule.MODULE_INVENTAIRE,'menu' : 4}

        return HttpResponse(template.render(context, request))
    except Exception as e:
        auteur = identite.utilisateur(request)
        monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS IMMOBILIER \n {}'.format(auteur.nom_complet, module,e))
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_asset'))
def get_modifier_asset(request,ref):
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(7, request)
    if response != None:
        return response

    ref = int(ref)
    model = dao_asset.toGetAsset(ref)
    context ={'title' : 'Modifier Asset','model':model, 'utilisateur' : utilisateur,
    'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
        'sous_modules':sous_modules,
    'modules' : modules,"module" : ErpModule.MODULE_INVENTAIRE,'menu' : 2}
    template = loader.get_template('ErpProject/ModuleInventaire/asset/update.html')
    return HttpResponse(template.render(context, request))

def post_modifier_asset(request):

    id = int(request.POST['ref'])
    try:
        numero_identification = request.POST['numero_identification']
        article_id = request.POST['article_id']
        employe_id = request.POST['employe_id']
        ##print(employe_id)
        type = request.POST['type']
        if int(employe_id) != 0:
            employe = dao_employe.toGetEmploye(employe_id)
            unite_fonctionnelle_id = employe.unite_fonctionnelle_id
        else:
             employe_id = None
             unite_fonctionnelle_id = request.POST['unite_fonctionnelle_id']
        auteur = identite.utilisateur(request)

        unite_fonctionnelle = dao_unite_fonctionnelle.toGetUniteFonctionnelle(unite_fonctionnelle_id)
        asset=dao_asset.toCreateAsset(numero_identification,type,article_id,employe_id,unite_fonctionnelle.id,"")
        asset=dao_asset.toUpdateAsset(id, asset)
        messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
        return HttpResponseRedirect(reverse('module_inventaire_detail_asset',args=(asset.id)))
    except Exception as e:
        ##print('Erreur lors de l enregistrement')
        auteur = identite.utilisateur(request)
        monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER IMMOBILIER \n {}'.format(auteur.nom_complet, module,e))
        ##print(e)

        messages.add_message(request, messages.ERROR,e)
        return HttpResponseRedirect(reverse('module_inventaire_add_asset'))



@transaction.atomic
def post_workflow_bon_entree_depot(request):
    sid = transaction.savepoint()
    try:
        utilisateur_id = request.user.id
        auteur = identite.utilisateur(request)
        base_dir = settings.BASE_DIR
        media_dir = settings.MEDIA_ROOT
        media_url = settings.MEDIA_URL
        etape_id = request.POST["etape_id"]
        entree_id = request.POST["doc_id"]

        ##print("print 1 %s %s %s" % (utilisateur_id, etape_id, entree_id))

        employe = dao_employe.toGetEmployeFromUser(utilisateur_id)
        etape = dao_wkf_etape.toGetEtapeWorkflow(etape_id)
        bon_entree = dao_bon_special.toGetBonSpecial(entree_id)

        ##print("print 2 %s %s %s " % (employe, etape, bon_entree))

        transitions_etapes_suivantes = dao_wkf_etape.toListEtapeSuivante(bon_entree.statut_id)
        for item in transitions_etapes_suivantes:

            if item.condition.designation == "Upload":
                ##print("Upload")
                if 'file_upload' in request.FILES:
                    nom_fichier = request.FILES['file_upload']
                    doc = dao_document.toUploadDocument(auteur, nom_fichier, bon_entree)

                    bon_entree.statut_id = etape.id
                    bon_entree.etat = etape.designation
                    bon_entree.save()
                    document = dao_document_bon_entree.toCreateDocument("Bon de reception",doc.url_document, bon_entree.etat,entree_id)
                    document = dao_document_bon_entree.toSaveDocument(auteur, document)

                    ##print("docu saved")
                else:
                    pass

            else:
                # Gestion des transitions dans le document
                bon_entree.statut_id = etape.id
                bon_entree.etat = etape.designation
                bon_entree.save()

        historique = dao_wkf_historique_bon_entree_depot.toCreateHistoriqueWorkflow(employe.id, etape.id, bon_entree.id)
        historique = dao_wkf_historique_bon_entree_depot.toSaveHistoriqueWorkflow(historique)

        if historique != None :
            transaction.savepoint_commit(sid)
            #return HttpResponseRedirect(reverse('module_achat_details_bon_achat', args=(demande.id,)))
            ##print("OKAY")
            return HttpResponseRedirect(reverse('module_inventaire_details_bons_entrees', args=(entree_id,)))
        else:
            transaction.savepoint_rollback(sid)
            return HttpResponseRedirect(reverse('module_inventaire_details_bons_entrees', args=(entree_id,)))

    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        transaction.savepoint_rollback(sid)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_bons_entrees'))



def get_to_asset_of_bons_entrees(request):
    sid = transaction.savepoint()
    ordre_id = int(request.POST["doc_id"])
    try:
        permission_number = 71
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response



        #Aux allures de Get
        # modules = dao_module.toListModulesInstalles()
        # utilisateur = identite.utilisateur(request)
        #Fin allure Get

        # auteur = identite.utilisateur(request)
        #responsable_id = int(request.POST["responsable_id"])
        #agent_id = int(request.POST["agent_id"])
        est_realisee = True

        #bon_transfert = dao_bon_transfert.toGetBonTransfert(ordre_id)
        bon_entree = dao_bon_special.toGetBonSpecial(ordre_id)
        #operation_stock = dao_operation_stock.toGetOperationStock(bon_transfert.operation_stock_id)
        #emplacement_destination = dao_emplacement.toGetEmplacement(bon_transfert.emplacement_destination_id)
        list_ligne_id = request.POST.getlist('ligne_id', None)
        list_quantite_fournie = request.POST.getlist("quantite_fournie", None)

        is_done = True
        if is_done == True :

            lignes = dao_item_bon_special.toListItemBons(ordre_id)
            context = {
                'modules':modules,'sous_modules':sous_modules,
                'title' : "Enregistrer les assets relatifs au bon N°%s" % bon_entree.numero,
                'model' : bon_entree,
                'lignes' : lignes,
                "utilisateur" : utilisateur,
                "module" : ErpModule.MODULE_INVENTAIRE,
                'actions':auth.toGetActions(modules,utilisateur),
                'sous_modules':sous_modules,
		        'organisation': dao_organisation.toGetMainOrganisation(),
                "modules": modules,
                'roles':groupe_permissions,
                'menu' : 11
            }

            template = loader.get_template("ErpProject/ModuleInventaire/bons_entrees/asset.html")
            return HttpResponse(template.render(context, request))
        else:

            return HttpResponseRedirect(reverse('module_inventaire_details_bons_entrees', args=(ordre_id,)))
    except Exception as e:
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_details_bons_entrees', args=(ordre_id,)))

@transaction.atomic
def post_to_asset_of_bons_entrees(request):
    sid = transaction.savepoint()
    ordre_id = int(request.POST["ordre_id"])
    try:
        auteur = identite.utilisateur(request)
        est_realisee = True
        document = request.POST["document"]

        bon_entree = dao_bon_special.toGetBonSpecial(ordre_id)

        #Flow
        wkf_task.passingStepWorkflow(auteur,bon_entree)
        #Traitement des assets
        list_numero_serie = request.POST.getlist('numero_serie', None)
        list_description = request.POST.getlist('description', None)
        list_article_id = request.POST.getlist('article_id', None)
        type_emplacement = dao_type_emplacement.toGetTypeEmplacementEntree()
        emplacement = dao_emplacement.toGetEmplacementEntree(type_emplacement)
        for i in range(0, len(list_numero_serie)):
            num_serie = list_numero_serie[i]
            descript = list_description[i]
            art_id = list_article_id[i]
            article = dao_article.toGetArticle(art_id)
            asset = dao_asset.toCreateAsset(num_serie,"ARTICLES",art_id,None,emplacement.id,descript)
            asset = dao_asset.toSaveAsset(auteur,asset)
            asset.bon_entree = bon_entree
            asset.bon_reception = bon_entree.bon_reception
            asset.save()
            asset_historique = dao_asset_historique.toCreateAssetHistorique(bon_entree.numero,document,asset.id,bon_entree,None,True)
            asset_historique = dao_asset_historique.toSaveAssetHistorique(auteur,asset_historique)

        transaction.savepoint_commit(sid)
        return HttpResponseRedirect(reverse('module_inventaire_details_bons_entrees', args=(ordre_id,)))

    except Exception as e:
        transaction.savepoint_rollback(sid)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_details_bons_entrees', args=(ordre_id,)))


def get_lister_immobilisations(request):
    permission_number = 346
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
    if response != None:
        return response
    # model = dao_immobilisation.toList()
    #*******Filtre sur les règles **********#
    model = dao_model.toListModel(dao_immobilisation.toList(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
    try:
        view = str(request.GET.get("view","list"))
    except Exception as e:
        view = "list"

    #Pagination
    model = pagination.toGet(request, model)

    context = {
        'modules':modules,'sous_modules':sous_modules,
		'title' : "Liste des immobilisations",
		'model' : model,
        'view' : view,
		'devise_ref' : dao_devise.toGetDeviseReference(),
		"utilisateur" : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules ,
		"module" : ErpModule.MODULE_INVENTAIRE,
		'menu' : 25
	}
    template = loader.get_template("ErpProject/ModuleInventaire/immobilisation/list.html")
    return HttpResponse(template.render(context, request))


def get_details_immobilisation(request, ref):
	try:
		permission_number = 346
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
		    return response


		ref = int(ref)
		immobilisation = dao_immobilisation.toGet(ref)
		historique, transition_etape_suivant, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,immobilisation)
		##print("trans", transition_etape_suivant)

		lignes_amortissements = dao_immobilisation.toListLigneAmortissement(immobilisation.id)

		context = {
			'title' : "Immobilisation %s" % immobilisation.code,
			'model' : immobilisation,
			'immobilier' : dao_asset.toGetAsset(immobilisation.immobilier_id),
			'devise_ref' : dao_devise.toGetDeviseReference(),
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
		    'organisation': dao_organisation.toGetMainOrganisation(),
			'historique':historique,
			'roles':groupe_permissions,
			'lignes_amortissements':lignes_amortissements,
			'etapes_suivantes':transition_etape_suivant,
			'content_type_id':content_type_id,
			'documents':documents,
            "organisation":dao_organisation.toGetMainOrganisation(),
            'sous_modules': sous_modules,
			"modules" : modules,
            'signee':signee,
			"module" : ErpModule.MODULE_INVENTAIRE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleInventaire/immobilisation/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		##print("ERREUR")
		##print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_inventaire_list_immobilisations'))

def get_lister_traitement_immobilisation(request):
	permission_number = 346
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
	    return response

	# model = dao_traitement_immobilisation.toListTraitement_immobilisation()
    #*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_traitement_immobilisation.toListTraitement_immobilisation(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	try:
	    view = str(request.GET.get("view","list"))
	except Exception as e:
	    view = "list"

    #Pagination
	model = pagination.toGet(request, model)

	context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Liste des traitements d\'immobilisation',
        'actions':auth.toGetActions(modules,utilisateur),
        'view' : view,
		'organisation': dao_organisation.toGetMainOrganisation(),
        'model' : model,'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_INVENTAIRE,'menu' : 1}
	template = loader.get_template('ErpProject/ModuleInventaire/traitement_immobilisation/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_traitement_immobilisation(request):
	permission_number = 345
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
	    return response

	immobilisations = dao_immobilisation.toListImmobilisationAvailableAndComptabilise()
	context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Créer une liste des immobilisations à traiter',
    'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
    'immobilisations':immobilisations,
    'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_INVENTAIRE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleInventaire/traitement_immobilisation/add.html')
	return HttpResponse(template.render(context, request))

@transaction.atomic
def post_creer_traitement_immobilisation(request):
	sid = transaction.savepoint()
	try:
		base_dir = settings.BASE_DIR
		media_dir = settings.MEDIA_ROOT
		media_url = settings.MEDIA_URL

		# numero_traitement = request.POST['numero_traitement']
		numero_traitement = dao_traitement_immobilisation.toGenerateNumeroTraitement_immo()
		description = request.POST['description']
		typeTraitement = int(request.POST['typeTraitement'])
		auteur = identite.utilisateur(request)

		traitement_immobilisation=dao_traitement_immobilisation.toCreateTraitement_immobilisation(numero_traitement,description, typeTraitement, None)
		traitement_immobilisation=dao_traitement_immobilisation.toSaveTraitement_immobilisation(auteur, traitement_immobilisation)
		if traitement_immobilisation != None:
			if 'file_upload' in request.FILES:
				files = request.FILES.getlist("file_upload",None)
				doc = dao_document.toUploadDocument(auteur, files, traitement_immobilisation)


				##print(bzb)

				document = dao_document.toCreateDocument("Rapport d'inventaire " + numero_traitement,doc.url_document, "Rapport d'inventaire",traitement_immobilisation)
				document = dao_document.toSaveDocument(auteur, document)
				traitement_immobilisation.rapport_inventaire_id = document.id
				traitement_immobilisation.save()

			list_immobilisation = request.POST.getlist("immobilisation",None)
			##print("sdjqkjsk")
			list_description = request.POST.getlist("description", None)

			for i in range(0, len(list_immobilisation)) :
				immobilisation_id = int(list_immobilisation[i])
				description = list_description[i]
				ligne_traitement = dao_ligne_traitementimmobilisation.toCreateLigne_traitementimmobilisation(immobilisation_id,description, traitement_immobilisation.id)
				ligne_traitement = dao_ligne_traitementimmobilisation.toSaveLigne_traitementimmobilisation(auteur,ligne_traitement)

			# WORKFLOWS INITIALS
			type_document = "Traitement Immobilisation"
			wkf_task.initializeWorkflow(auteur,traitement_immobilisation)


		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_inventaire_detail_traitement_immobilisation', args=(traitement_immobilisation.id,)))
	except Exception as e:
		##print('Erreur lors de l enregistrement')
		transaction.savepoint_rollback(sid)
		auteur = identite.utilisateur(request)

		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER TRAITEMENT_IMMOBILISATION \n {}'.format(auteur.nom_complet, module,e))
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse('module_inventaire_add_traitement_immobilisation'))

def get_details_traitement_immobilisation(request,ref):

	permission_number = 346
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
	    return response
	try:

		ref=int(ref)
		traitement_immobilisation=dao_traitement_immobilisation.toGetTraitement_immobilisation(ref)
		historique, transition_etape_suivant, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,traitement_immobilisation)
		lignes_traitements = dao_ligne_traitementimmobilisation.toListLigneOfTraitement(ref)

		template = loader.get_template('ErpProject/ModuleInventaire/traitement_immobilisation/item.html')
		context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Details sur un dossier de traitement d\'immobilisation',
        'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
        'historique':historique,
        'lignes_traitements': lignes_traitements,
        'etapes_suivantes':transition_etape_suivant,
        'content_type_id': content_type_id,
        'roles':groupe_permissions,
        'documents':documents,
        'signee':signee,
        'model':traitement_immobilisation,
        'utilisateur' : utilisateur,
        'modules' : modules,'module' : ErpModule.MODULE_INVENTAIRE,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		##print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS TRAITEMENT_IMMOBILISATION \n {}'.format(auteur.nom_complet, module,e))
		##print(e)
		return HttpResponseRedirect(reverse('module_inventaire_list_traitement_immobilisation'))
def get_modifier_traitement_immobilisation(request,ref):
	permission_number = 347
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
	    return response

	ref = int(ref)
	model = dao_traitement_immobilisation.toGetTraitement_immobilisation(ref)
	context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Modifier un dossier de traitement d\'immobilisation',
    'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
    'model':model, 'utilisateur': utilisateur,'modules' : modules,'module' : ErpModule.MODULE_INVENTAIRE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleInventaire/traitement_immobilisation/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_traitement_immobilisation(request):

	id = int(request.POST['ref'])
	try:
		numero_traitement = request.POST['numero_traitement']
		rapport_inventaire_id = request.POST['rapport_inventaire_id']
		description = request.POST['description']
		typeTraitement = request.POST['typeTraitement']
		auteur = identite.utilisateur(request)

		traitement_immobilisation=dao_traitement_immobilisation.toCreateTraitement_immobilisation(numero_traitement,description, typeTraitement, rapport_inventaire_id)
		traitement_immobilisation=dao_traitement_immobilisation.toUpdateTraitement_immobilisation(id, traitement_immobilisation)
		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_inventaire_detail_traitement_immobilisation',args=(traitement_immobilisation.id)))
	except Exception as e:
		##print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER TRAITEMENT_IMMOBILISATION \n {}'.format(auteur.nom_complet, module,e))
		##print(e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse('module_inventaire_add_traitement_immobilisation'))

######RETOUR EN STOCK########

## RETOUR MATERIEL
def get_lister_retour_internal(request):
    permission_number = 980
    # modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request)
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
    if response != None:
        return response

    title = "Liste de Retour Matériel"
    # model = dao_article.toListArticles()
    #*******Filtre sur les règles **********#
    model = dao_model.toListModel(dao_article.toListArticles(), permission_number, groupe_permissions, identite.utilisateur(request))
    #******* End Regle *******************#

    # transfert =  Model_Bon_transfert.objects.filter(is_return_materiel = True).order_by("-creation_date")
    Bon_retour = dao_bon_retour.toListBonRetour()
    # #print(transfert)

    # transferts = dao_bon_transfert.toListBonTransfert()

    # transferts = dao_bon_transfert.toListBonTransfert()() if auth.toCheckAdmin(modules, utilisateur) else dao_bon_transfert.toListBonTransfert()ByAuteur(utilisateur.id)
    try:
	    view = str(request.GET.get("view","list"))
    except Exception as e:
	    view = "list"

    if "op" in request.GET:
        try:
            """operation_id = int(request.GET["op"])
            operation_stock = dao_operation_stock.toGetOperationStock(operation_id)
            transferts = dao_bon_transfert.toListTransfertsDuType(operation_stock.id)
            title = title + (" - %s" % operation_stock.designation)"""
            reference = str(request.GET["op"])

        except Exception as e:
            #print("ERREUR")
            #print(e)
            pass
    #Pagination
    bon_retour = pagination.toGet(request, Bon_retour)


    context = {
        'sous_modules':sous_modules,
        'title' : title,
        'emplacements' : dao_emplacement.toListEmplacement(),
        'articles' : model,
        'bons' : bon_retour,
        'categories' : dao_categorie_article.toListCategoriesArticle(),
        "utilisateur" : utilisateur,
        'view' : view,
        'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
        "modules" : modules,
        "module" : ErpModule.MODULE_INVENTAIRE,
        'menu': 11
    }
    template = loader.get_template("ErpProject/ModuleInventaire/retour_materiel/list.html")
    return HttpResponse(template.render(context, request))

def get_creer_retour_internal(request):
    try:
        permission_number = 981
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        type_emplacement_entrepot = dao_type_emplacement.toGetTypeEmplacementEntrepot()
        ##print(type_emplacement_entrepot)
        entrepot = dao_emplacement.toGetEmplacement(type_emplacement_entrepot.id)
        ##print(entrepot)

        services_referents = dao_unite_fonctionnelle.toListUniteFonctionnelleWHNoneService()
        emplacement_internal = dao_emplacement.toGetEmplacementInternalBusiness()

        etat_actuel_id = 0
        etat = ""
        lignes = []

        try:
            etat_actuel_id = request.POST["doc_id"]
            etat = dao_expression_besoin.toGetExpression(etat_actuel_id)
            lignes = dao_ligne_expression.toListLigneOfExpressions(etat.id)
        except Exception as e:
            ##print("Aucun etat de besoin trouvé")
            pass

        if utilisateur.unite_fonctionnelle != None:
            etat_besoins = dao_expression_besoin.toListExpressionsNonTraitesByServiceRef(utilisateur.unite_fonctionnelle.id)
            ##print("etat", etat_besoins)
            service_referent = dao_unite_fonctionnelle.toGetUniteFonctionnelle(utilisateur.unite_fonctionnelle_id)
        else:
            etat_besoins = dao_expression_besoin.toListExpressionsNonTraites()
            service_referent = 0

        context = {
            'sous_modules':sous_modules,
            'title' : "Nouveau bon de retour de matériel",
            'emplacements':dao_emplacement.toListEmplacementsInEntrepot(entrepot.id),
            'type_emplacement_entre': dao_type_emplacement.toGetTypeEmplacementEntree(),
            'type_emplacement_stock': dao_type_emplacement.toGetTypeEmplacementStock(),
            'etat' : etat,
            'emplacement_internal':emplacement_internal,
            'services_referents':services_referents,
            'lignes_etat'  : lignes,
            'etat_besoins' : etat_besoins,
            'etat_actuel_id' : int(etat_actuel_id),
            'operations' : dao_operation_stock.toListOperationsStock(),
            'categories' : dao_categorie_article.toListCategoriesArticle(),
            "utilisateur" : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		    'organisation': dao_organisation.toGetMainOrganisation(),
            'service_referent':service_referent,
            "departement" : dao_unite_fonctionnelle.toListUniteFonctionnelle(),
            "employes"    : dao_employe.toListEmployes(),
            'articles' : dao_article.toListArticlesStockables(),
            "numero" : dao_bon_retour.toGenerateNumeroBonRetour(),
            "module" : ErpModule.MODULE_INVENTAIRE,
            "modules" : modules,
            'menu': 11
        }
        template = loader.get_template("ErpProject/ModuleInventaire/retour_materiel/add.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        #print("Erreur GEt Bon Retour")
        #print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_retour_internal'))

def get_valider_retour_internal(request):
    try:
        permission_number = 151
        # modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request)
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        operation_stock_id = int(request.POST["operation_stock_id"])
        operation_stock = dao_operation_stock.toGetOperationStock(operation_stock_id)
        emplacement_origine_id = int(request.POST["emplacement_destination_id"])
        emplacement_origine = dao_emplacement.toGetEmplacement(emplacement_origine_id)
        date_prevu = request.POST["date_prevue"]

        demandeur_id = int(request.POST["demandeur_id"])
        demandeur = dao_employe.toGetEmploye(demandeur_id)

        #expression_id = int(request.POST["expression_id"])
        #expression = dao_expression_besoin.toGetExpression(expression_id)

        emplacement_destination_id = int(request.POST["emplacement_origine_id"])
        emplacement_destination = dao_emplacement.toGetEmplacement(emplacement_destination_id)

        context = {
            'sous_modules':sous_modules,
            'title' : "Valider le retour de matériel",
            "emplacement_origine" : emplacement_origine,
            "emplacement_destination" : emplacement_destination,
            'operation_stock' : operation_stock,
            'date_prevu':date_prevu,
            #'expression':expression,
            'demandeur':demandeur,
            "utilisateur" : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
            "module" : ErpModule.MODULE_INVENTAIRE,
            "modules": modules,
            'menu' : 11
        }
        template = loader.get_template("ErpProject/ModuleInventaire/retour_materiel/validate.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_add_retour_internal'))

@transaction.atomic
def post_valider_retour_internal(request):
    sid = transaction.savepoint()
    ##print("SID : %s" % sid)
    try:
        numero_transfert = ""
        ##print("Testing")
        date_transfert = request.POST["date_prevue"]
        date_transfert = timezone.datetime(int(date_transfert[6:10]), int(date_transfert[3:5]), int(date_transfert[0:2]))
        emplacement_origine_id = int(request.POST["emplacement_origine_id"])
        ##print("emplacement_origine_id")



        emplacement_destination_id = int(request.POST["emplacement_destination_id"])
        ##print("ZE")
        operation_stock_id = int(request.POST["operation_stock_id"])
        ##print("RE")
        reference_document = request.POST["reference_document"]
        demandeur_id = int(request.POST["demandeur_id"])
        ##print("LO")
        description = ""
        # est_partiel = request.POST["est_partiel"]
        ##print(est_partiel)
        #expression_id = int(request.POST["expression_id"])
        ##print("LA")
        auteur = identite.utilisateur(request)
        employe_id = auteur.id

        bon_retour = dao_bon_retour.toCreateBonTransfert(numero_transfert, False, date_transfert,"RETOUR MATERIEL", operation_stock_id,emplacement_origine_id, emplacement_destination_id, employe_id, reference_document, description, 0.0, 0,"", None, demandeur_id)
        ##print("ssss")
        bon_retour = dao_bon_retour.toSaveBonTransfert(auteur, bon_retour)
        #bon_transfert.expression_id = expression_id
        service_referent = dao_unite_fonctionnelle.toGetUniteFonctionnelleOfEmplacement(emplacement_destination_id)
        #print('SERVICE REF', service_referent.id)
        bon_retour.services_ref_id = service_referent.id
        bon_retour.save()
        #print("nnn")
        #print(bon_retour)


        #StopHere
        #expression = dao_expression_besoin.toGetExpression(expression_id)

        """
        if est_partiel == "true":
            uneetape = dao_wkf_etape.toGetEtapeByDesignation("Livré partiellement")
            ##print(uneetape)

            ##print('***VALIDER LIVRAISON PARTIELLE**')

            list_QD = request.POST.getlist('quantite_demandee', None)
            list_QF = request.POST.getlist('quantite_fournie', None)
            list_article_id = request.POST.getlist('article_id', None)
            for i in range(0, len(list_article_id)) :
                qd = int(list_QD[i])
                qf = int(list_QF[i])
                articleid = int(list_article_id[i])
                quantite_restant = qd - qf
                rest = dao_ligne_expression.toupdateLigneExpressionLivraisonPartielle(expression_id,articleid,quantite_restant)
                ##print('**INSERTION DES NOMBRES D\'ARTICLES RESTANT**')
                ##print('**La quantité restante:**',rest)

            wkf_task.passingStepWorkflow(auteur,expression,uneetape.id)

        else:
            uneetape = dao_wkf_etape.toGetEtapeByDesignation("Articles livrés")
            wkf_task.passingStepWorkflow(auteur,expression, uneetape.id)
            ##print('***VALIDER LIVRAISON COMPLETE**')
        """

        if bon_retour != None :
            ##print("Ligne transfert {0} creee ".format(bon_transfert.id))
            list_article_id = request.POST.getlist('article_id', None)
            #print(list_article_id)
            list_numero_serie = request.POST.getlist('numero_serie', None)
            ##print(list_numero_serie)
            list_description = request.POST.getlist('description', None)
            ##print(list_description)
            list_quantite_demandee = request.POST.getlist('quantite_demandee', None)
            list_quantite_fournie = request.POST.getlist('quantite_fournie', None)
            #list_quantite_demandee = request.POST.getlist("quantite_demandee", None)
            for i in range(0, len(list_article_id)) :
                ##print("in")
                article_id = int(list_article_id[i])
                ##print("in1")
                numero_serie = list_numero_serie[i]
                ##print("in2")
                description = list_description[i]
                ##print("in3")
                quantite_demandee = makeFloat(list_quantite_demandee[i])
                quantite_fournie = makeFloat(list_quantite_fournie[i])

                # quantite_restant = quantite_demandee - quantite_fournie
                # quantite_restant = dao_ligne_expression.toupdateLigneExpressionLivraisonPartielle(expression_id, quantite_restant)
                # ##print('**La quantité restante:**',quantite_restant)

                article = dao_article.toGetArticle(article_id)
                # #print(article)
                ##print(emplacement_origine_id)
                ##print(dao_emplacement.toGetEmplacement(emplacement_origine_id))
                les_stocks = dao_stock_article.toListStocksOfArticleInEmplacement(article_id, emplacement_destination_id)
                ##print(les_stocks)
                stock = les_stocks[0]
                ##print("in")


                ligne_bon_retour = dao_ligne_bon_retour.toCreateLigneBonRetour(bon_retour.id, stock.id, quantite_demandee,quantite_fournie, numero_serie,description)
                ligne_bon_retour = dao_ligne_bon_retour.toSaveLigneBonRetour(auteur, ligne_bon_retour)
                # #print('***LIGNE CREE', ligne_bon_retour)


                #gestion des assets
                '''if int(employe_id) != 0:
                    employe = dao_employe.toGetEmploye(employe_id)
                    unite_fonctionnelle_id = employe.unite_fonctionnelle_id
                else:
                    unite_fonctionnelle_id = int(list_departement_id[i])
                    employe_id = None
                ##print("in")
                asset=dao_asset.toCreateAsset(dao_utils.genererNumeroAsset(),type_asset,article_id,employe_id,unite_fonctionnelle_id, bon_transfert.id)
                asset=dao_asset.toSaveAsset(auteur, asset)'''
            ##print("Ligne transfert {0} creee ".format(ligne_transfert.id))


            # WORKFLOWS INITIALS
            type_document = "Retour en Stock"
            wkf_task.initializeWorkflow(auteur,bon_retour,type_document)

            transaction.savepoint_commit(sid)
            return HttpResponseRedirect(reverse('module_inventaire_details_retour_internal', args=(bon_retour.id,)))
        else:
            transaction.savepoint_rollback(sid)
            return HttpResponseRedirect(reverse('module_inventaire_list_retour_internal'))
    except Exception as e:
        # #print("ERREUR")
        # #print(e)
        transaction.savepoint_rollback(sid)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_add_retour_internal'))

def get_realiser_retour_internal(request, ref):
    try:
        permission_number = 151
        # modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request)
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        # bon_transfert = dao_bon_transfert.toGetBonTransfert(ref)
        bon_transfert = dao_bon_retour.toGetBonRetour(ref)
        service_ref = dao_unite_fonctionnelle.toGetUniteFonctionnelleOfEmplacement(bon_transfert.emplacement_destination.id)
        if service_ref.libelle == "Moyens généraux":
            #employe_role = dao_role.toGetPersonOfRole("Technicien MG")
            employe_role = dao_groupe_permission.toGetPersonOfPermission("Technicien MG")
        else:
            employe_role = dao_groupe_permission.toGetPersonOfPermission("Technicien SI")
            #employe_role = dao_role.toGetPersonOfRole("Technicien SI")

        ref = int(ref)
        bon_transfert = dao_bon_retour.toGetBonRetour(ref)
        if bon_transfert.est_realisee == True : return HttpResponseRedirect(reverse('module_inventaire_list_retour_internal'))
        # lignes = dao_ligne_transfert.toListLignesTransfert(bon_transfert.id)
        lignes = dao_ligne_bon_retour.toListLignesBonRetour(bon_transfert.id)
        item = lignes[0]
        stock = dao_stock_article.toGetStockArticle(item.stock_article_id)
        emplacement_origine = dao_emplacement.toGetEmplacement(stock.emplacement_id)
        context = {
            'sous_modules':sous_modules,
            'title' : "Bon de Retour Matériel N°%s" % bon_transfert.numero_bon_retour,
            'model' : bon_transfert,
            'lignes' : lignes,
            "service_referent_origine" : dao_unite_fonctionnelle.toGetUniteFonctionnelleOfEmplacement(emplacement_origine),
            "agents" : employe_role,
            "utilisateur" : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
            "module" : ErpModule.MODULE_INVENTAIRE,
            "modules": modules,
            'menu' : 11
        }
        template = loader.get_template("ErpProject/ModuleInventaire/retour_materiel/release.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        ##print("ERREUR REALISER")
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_retour_internal'))

@transaction.atomic
def post_realiser_retour_internal(request):
    sid = transaction.savepoint()
    ###print("On est là")
    ordre_id = int(request.POST["ordre_id"])
    try:
        auteur = identite.utilisateur(request)
        responsable_id = int(request.POST["responsable_id"])
        agent_id = int(request.POST["agent_id"])
        est_realisee = True

        # bon_transfert = dao_bon_transfert.toGetBonTransfert(ordre_id)
        bon_transfert = dao_bon_retour.toGetBonRetour(ordre_id)
        operation_stock = dao_operation_stock.toGetOperationStock(bon_transfert.operation_stock_id)
        emplacement_destination = dao_emplacement.toGetEmplacement(bon_transfert.emplacement_destination_id)
        list_ligne_id = request.POST.getlist('ligne_id', None)
        list_quantite_fournie = request.POST.getlist("quantite_fournie", None)
        ##print(len(list_ligne_id))
        ##print(len(list_quantite_fournie))
        for i in range(0, len(list_ligne_id)):
            ligne_id = int(list_ligne_id[i])
            quantite_fournie = makeFloat(list_quantite_fournie[i])

            # ligne_transfert = dao_ligne_transfert.toGetLigneTransfert(ligne_id)
            ligne_transfert = dao_ligne_bon_retour.toGetLigneBonRetour(ligne_id)
            #Si la quantité demandée est superieure à la somme des quantitées déjà fournies, on n'est réalise pas pcq on n'a pas encore tout reçu
            if quantite_fournie > ligne_transfert.quantite_fournie : return HttpResponseRedirect(reverse('module_inventaire_realiser_retour_internal', args=(ordre_id,)))

            # On ajoute la nouvelle quantité reçue
            ligne_transfert.quantite_fournie = quantite_fournie
            dao_ligne_bon_retour.toUpdateLigneBonRetour(ligne_id, ligne_transfert)

            # On recuper le stock de l'article dans l'emplacement de destination pour transfert
            stock_depart = dao_stock_article.toGetStockArticle(ligne_transfert.stock_article_id)
            list_stocks_destination = dao_stock_article.toListStocksOfArticleInEmplacement(stock_depart.article_id, emplacement_destination.id)
            if list_stocks_destination: stock_destination = list_stocks_destination[0]
            else:
                # Si il ya pas de stock pour cet article dans cet emplacement, on crée un nouveau stock
                stock_destination = dao_stock_article.toCreateStockArticle(0, emplacement_destination.id, stock_depart.article_id)
                stock_destination = dao_stock_article.toSaveStockArticle(auteur, stock_destination)

            # DIMINUTION DE LA QUANTITE DU STOCK D'ORIGINE
            stock_depart.quantite_disponible = stock_depart.quantite_disponible - quantite_fournie
            dao_stock_article.toUpdateStockArticle(stock_depart.id, stock_depart)

            # AUGMENTATION DE LA QUANTITE DU STOCK DE DESTINATION
            stock_destination.quantite_disponible = stock_destination.quantite_disponible + quantite_fournie
            dao_stock_article.toUpdateStockArticle(stock_destination.id, stock_destination)

            #ENREGISTRER LE MOUVEMENT
            if quantite_fournie > 0:
                mouvement_stock = dao_mouvement_stock.toCreateMouvementStock(quantite_fournie,"","TRANSFERT",stock_depart.id, stock_destination.id,None,None,None,None)
                mouvement_stock =dao_mouvement_stock.toSaveMouvementStock(auteur, mouvement_stock)
                mouvement_stock.bon_retour_id = ordre_id
                mouvement_stock.save()

        bon_transfert.est_realisee = est_realisee
        if est_realisee == True :
            bon_transfert.date_realisation = timezone.now()

        bon_transfert.employe_id = responsable_id
        ###print("agent")
        ###print(agent_id)
        if agent_id != 0 :
            bon_transfert.agent_id = agent_id

        is_done = dao_bon_retour.toUpdateBonTransfert(ordre_id, bon_transfert)


        #Flow
        bon_transfert = dao_bon_retour.toGetBonRetour(ordre_id)
        ##print("statut id")
        ##print(bon_transfert.statut_id)
        wkf_task.passingStepWorkflow(auteur,bon_transfert)


        if is_done == True :
            transaction.savepoint_commit(sid)
            return HttpResponseRedirect(reverse('module_inventaire_details_retour_internal', args=(ordre_id,)))
        else:
            transaction.savepoint_rollback(sid)
            return HttpResponseRedirect(reverse('module_inventaire_realiser_retour_internal', args=(ordre_id,)))
    except Exception as e:
        ##print("ERREUR POST REALISER")
        ##print(e)
        transaction.savepoint_rollback(sid)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_realiser_retour_internal', args=(ordre_id,)))


def get_to_asset_of_retour_internal(request):
    sid = transaction.savepoint()
    ordre_id = int(request.POST["ordre_id"])
    try:
        permission_number = 980
        # modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request)
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        responsable_id = int(request.POST["responsable_id"])
        agent_id = int(request.POST["agent_id"])
        ###print(agent_id)
        est_realisee = True
        dico_asset = {}

        # bon_transfert = dao_bon_transfert.toGetBonTransfert(ordre_id)
        bon_transfert = dao_bon_retour.toGetBonRetour(ordre_id)
        emplacement_origine = dao_emplacement.toGetEmplacement(bon_transfert.emplacement_origine_id)
        emplacement_destination = dao_emplacement.toGetEmplacement(bon_transfert.emplacement_destination_id)
        list_ligne_id = request.POST.getlist('ligne_id', None)
        list_quantite_fournie = request.POST.getlist("quantite_fournie", None)

        lignes = dao_ligne_bon_retour.toListLignesBonRetour(ordre_id)
        for ligne in lignes:
            dico_asset[ligne.article_identifiant] = dao_asset.toGetAssetByArticleOfEmplacement(ligne.article_identifiant,emplacement_origine.id)

        is_done = True
        if is_done == True :

            # lignes = dao_ligne_transfert.toListLignesTransfert(ordre_id)
            lignes = dao_ligne_bon_retour.toListLignesBonRetour(ordre_id)
            bon_transfert = dao_bon_retour.toGetBonRetour(ordre_id)
            serv_ref_id = request.POST["service_referent_id"]
            service_referent = dao_unite_fonctionnelle.toGetUniteFonctionnelle(serv_ref_id)

            context = {
                'sous_modules':sous_modules,
                'title' : "Affecter les assets relatifs au bon N°%s" % bon_transfert.numero_bon_retour,
                'model' : bon_transfert,
                'lignes' : lignes,
                "dico_asset":dico_asset,
                "service_referent" : service_referent,
                "utilisateur" : utilisateur,
                "module" : ErpModule.MODULE_INVENTAIRE,
                'actions':auth.toGetActions(modules,utilisateur),
		        'organisation': dao_organisation.toGetMainOrganisation(),
                "modules": modules,
                'responsable_id':responsable_id,
                'roles':groupe_permissions,
                'agent_id':agent_id,
                'ordre_id':ordre_id,
                'list_quantite_fournie':list_quantite_fournie,
                'menu' : 11
            }

            template = loader.get_template("ErpProject/ModuleInventaire/retour_materiel/asset.html")
            return HttpResponse(template.render(context, request))
        else:

            return HttpResponseRedirect(reverse('module_inventaire_realiser_retour_internal', args=(ordre_id,)))
    except Exception as e:
        ###print("ERREUR")
        ###print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_realiser_retour_internal', args=(ordre_id,)))


@transaction.atomic
def post_to_asset_of_retour_internal(request):
    sid = transaction.savepoint()
    ordre_id = int(request.POST["ordre_id"])
    try:

        auteur = identite.utilisateur(request)
        responsable_id = int(request.POST["responsable_id"])
        agent_id = int(request.POST["agent_id"])
        ###print('agent on POST')
        ###print(agent_id)
        est_realisee = True

        # bon_transfert = dao_bon_transfert.toGetBonTransfert(ordre_id)
        bon_transfert = dao_bon_retour.toGetBonRetour(ordre_id)
        operation_stock = dao_operation_stock.toGetOperationStock(bon_transfert.operation_stock_id)
        emplacement_destination = dao_emplacement.toGetEmplacement(bon_transfert.emplacement_destination_id)
        list_ligne_id = request.POST.getlist('ligne_id', None)
        list_quantite_fournie = request.POST.getlist("quantite_fournie", None)
        ##print(list_ligne_id)
        ##print("listes")
        ##print(list_quantite_fournie)
        ##print(len(list_ligne_id))
        ##print(len(list_quantite_fournie))
        for i in range(0, len(list_ligne_id)):
            ligne_id = int(list_ligne_id[i])
            quantite_fournie = makeFloat(list_quantite_fournie[i])

            ligne_transfert = dao_ligne_bon_retour.toGetLigneBonRetour(ligne_id)
            #Si la quantité demandée est superieure à la somme des quantitées déjà fournies, on n'est réalise pas pcq on n'a pas encore tout reçu
            if quantite_fournie > ligne_transfert.quantite_fournie : return HttpResponseRedirect(reverse('module_inventaire_realiser_retour_internal', args=(ordre_id,)))

            # On ajoute la nouvelle quantité reçue
            ligne_transfert.quantite_fournie = quantite_fournie
            dao_ligne_transfert.toUpdateLigneTransfert(ligne_id, ligne_transfert)

            # On recuper le stock de l'article dans l'emplacement de destination pour transfert
            stock_depart = dao_stock_article.toGetStockArticle(ligne_transfert.stock_article_id)
            list_stocks_destination = dao_stock_article.toListStocksOfArticleInEmplacement(stock_depart.article_id, emplacement_destination.id)
            if list_stocks_destination: stock_destination = list_stocks_destination[0]
            else:
                # Si il ya pas de stock pour cet article dans cet emplacement, on crée un nouveau stock
                stock_destination = dao_stock_article.toCreateStockArticle(0, emplacement_destination.id, stock_depart.article_id)
                stock_destination = dao_stock_article.toCreateStockArticle(stock_depart.article_id,0,emplacement_destination.id)
                stock_destination = dao_stock_article.toSaveStockArticle(stock_destination)

            # DIMINUTION DE LA QUANTITE DU STOCK D'ORIGINE
            stock_depart.quantite_disponible = stock_depart.quantite_disponible - quantite_fournie
            dao_stock_article.toUpdateStockArticle(stock_depart.id, stock_depart)

            # AUGMENTATION DE LA QUANTITE DU STOCK DE DESTINATION
            stock_destination.quantite_disponible = stock_destination.quantite_disponible + quantite_fournie
            dao_stock_article.toUpdateStockArticle(stock_destination.id, stock_destination)

            #ENREGISTRER LE MOUVEMENT
            if quantite_fournie > 0:
                mouvement_stock = dao_mouvement_stock.toCreateMouvementStock(quantite_fournie,"","TRANSFERT",stock_depart.id, stock_destination.id,None,None,None,ordre_id)
                dao_mouvement_stock.toSaveMouvementStock(auteur, mouvement_stock)

        bon_transfert.est_realisee = est_realisee
        if est_realisee == True :
            bon_transfert.date_realisation = timezone.now()

        bon_transfert.employe_id = responsable_id
        if agent_id != 0 :
            ##print("inside")
            bon_transfert.agent_id = agent_id

        is_done = dao_bon_retour.toUpdateBonTransfert(ordre_id, bon_transfert)


        #Flow
        bon_transfert = dao_bon_retour.toGetBonRetour(ordre_id)
        wkf_task.passingStepWorkflow(auteur,bon_transfert)

        #Traitement des assets

        #list_numero_serie = request.POST.getlist('numero_serie', None)
        list_asset_id = request.POST.getlist('asset_id', None)

        #list_description = request.POST.getlist('description', None)
        list_article_id = request.POST.getlist('article_id', None)
        service_ref_id = request.POST["service_referent_id"]
        ##print("responsable")
        ##print(responsable_id)
        for i in range(0, len(list_asset_id)):
            ##print("inside ")
            asset_id = list_asset_id[i]
            ##print(asset_id)
            asset = dao_asset.toUpdateAssetAffectation(asset_id,responsable_id)
            ##print(asset)


        if is_done == True :
            transaction.savepoint_commit(sid)
            return HttpResponseRedirect(reverse('module_inventaire_details_retour_internal', args=(ordre_id,)))
        else:
            transaction.savepoint_rollback(sid)
            return HttpResponseRedirect(reverse('module_inventaire_realiser_retour_internal', args=(ordre_id,)))
    except Exception as e:
        transaction.savepoint_rollback(sid)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_realiser_retour_internal', args=(ordre_id,)))


def get_details_retour_internal(request, ref):
    # #print('***DETAIL COMING****')
    try:
        permission_number = 980
        # modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request)
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response
        ref = int(ref)

        # transfert = dao_bon_transfert.toGetBonTransfert(ref)
        bon_retour = dao_bon_retour.toGetBonRetour(ref)
        # #print('***DETAIL COMING BON****', bon_retour)
        # lignes = dao_ligne_transfert.toListLignesTransfert(ref)
        lignes = dao_ligne_bon_retour.toListLignesBonRetour(ref)
        # #print('***DETAIL COMING LIGNES****', lignes)

        # #print('*****EMPLACEMENT ORIGINE****', bon_retour.emplacement_origine.id)
        # #print('*****EMPLACEMENT DESTINATION****', bon_retour.emplacement_destination.id)

        service_ref = dao_unite_fonctionnelle.toGetUniteFonctionnelleOfEmplacement(bon_retour.emplacement_destination.id)
        # #print('***DETAIL COMING service_ref****', service_ref)
        est_integrale = True
        #lignes = dao_ligne_transfert.toListLignesTransfert(ref)
        for ligne in lignes:
            if ligne.quantite_demandee > ligne.quantite_fournie:
                est_integrale = False
                break
        item = lignes[0]
        # #print('***DETAIL COMING item****', item)
        stock = dao_stock_article.toGetStockArticle(item.stock_article_id)
        # #print('***STOCK', stock)
        emplacement_origine = dao_emplacement.toGetEmplacement(stock.emplacement_id)
        # #print('***EMPL ORIGINE', emplacement_origine)

        historique, transition_etape_suivant, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,bon_retour)


        context = {
            'title' : bon_retour.numero_bon_retour,
            'model' : bon_retour,
            'lignes' : lignes,
            'historique' : historique,
            'etapes_suivantes' : transition_etape_suivant,
            'est_integrale':est_integrale,
            'roles':groupe_permissions,
            'content_type_id':content_type_id,
            "documents":documents,
            'service_referent':service_ref,
            'emplacement_origine' : emplacement_origine,
            "utilisateur" : utilisateur,
            'sous_modules':sous_modules,
            'actions':auth.toGetActions(modules,utilisateur),
		    'organisation': dao_organisation.toGetMainOrganisation(),
            "module" : ErpModule.MODULE_INVENTAIRE,
            "modules": modules,
            "menu" : 11
        }
        template = loader.get_template("ErpProject/ModuleInventaire/retour_materiel/item.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        #print("erreur", e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_retour_internal'))


def get_completer_retour_internal(request, ref):
    try:
        permission_number = 980
        # modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request)
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        ref = int(ref)

        # bon_transfert = dao_bon_transfert.toGetBonTransfert(ref)
        bon_retour = dao_bon_retour.toGetBonRetour(ref)
        est_integrale = True
        # lignes = dao_ligne_transfert.toListLignesTransfert(bon_transfert.id)
        lignes = dao_ligne_bon_retour.toListLignesBonRetour(ref)

        for ligne in lignes:
            if ligne.quantite_demandee > ligne.quantite_fournie:
                est_integrale = False
                break
        ##print(bon_transfert)
        if ((bon_retour.est_realisee == True) and (est_integrale == True)) : return HttpResponseRedirect(reverse('module_inventaire_list_retour_internal'))

        item = lignes[0]
        stock = dao_stock_article.toGetStockArticle(item.stock_article_id)
        emplacement_origine = dao_emplacement.toGetEmplacement(stock.emplacement_id)
        context = {
            'sous_modules':sous_modules,
            'title' : "Bon de retour matériel N°%s" % bon_retour.numero_bon_retour,
            'model' : bon_retour,
            'lignes' : lignes,
            "emplacement_origine" : emplacement_origine,
            "agents" : dao_employe.toListEmployesActifs(),
            "utilisateur" : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		    'organisation': dao_organisation.toGetMainOrganisation(),
            "modules" : modules ,
            "module" : ErpModule.MODULE_INVENTAIRE,
            'menu' : 4
        }
        template = loader.get_template("ErpProject/ModuleInventaire/retour_materiel/complete.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_retour_internal'))


@transaction.atomic
def post_completer_retour_internal(request):
    sid = transaction.savepoint()
    ordre_id = int(request.POST["ordre_id"])
    try:
        auteur = identite.utilisateur(request)
        responsable_id = int(request.POST["responsable_id"])
        est_realisee = True
        ##print("nakati 2")

        # bon_transfert = dao_bon_transfert.toGetBonTransfert(ordre_id)
        bon_retour = dao_bon_retour.toGetBonRetour(ordre_id)
        operation_stock = dao_operation_stock.toGetOperationStock(bon_retour.operation_stock_id)
        emplacement_destination = dao_emplacement.toGetEmplacement(bon_retour.emplacement_destination_id)
        list_ligne_id = request.POST.getlist('ligne_id', None)
        list_quantite_fournie = request.POST.getlist("quantite_fournie", None)
        ##print(len(list_ligne_id))
        ##print(len(list_quantite_fournie))
        for i in range(0, len(list_ligne_id)):
            ligne_id = int(list_ligne_id[i])
            quantite_recue = makeFloat(list_quantite_fournie[i])

            # ligne_transfert = dao_ligne_transfert.toGetLigneTransfert(ligne_id)
            ligne_bon_retour = dao_ligne_bon_retour.toGetLigneBonRetour(ligne_id)
            #Si la quantité demandée est superieure à la somme des quantitées déjà fournies, on n'est réalise pas pcq on n'a pas encore tout reçu
            if (quantite_recue + ligne_bon_retour.quantite_fournie) > ligne_bon_retour.quantite_demandee : return HttpResponseRedirect(reverse('module_inventaire_completer_retour_internal', args=(ordre_id,)))
            #if ligne_transfert.quantite_demandee > ligne_transfert.quantite_fournie + quantite_fournie : est_realisee = False

            # On ajoute la nouvelle quantité reçue
            ##print(ligne_transfert.quantite_fournie)
            ligne_bon_retour.quantite_fournie = ligne_bon_retour.quantite_fournie + quantite_recue
            ##print(quantite_recue)
            ##print(ligne_transfert.quantite_fournie)
            #breakpoint
            dao_ligne_bon_retour.toUpdateLigneBonRetour(ligne_id, ligne_bon_retour)

            # On recuper le stock de l'article dans l'emplacement de destination pour transfert
            stock_depart = dao_stock_article.toGetStockArticle(ligne_bon_retour.stock_article_id)
            list_stocks_destination = dao_stock_article.toListStocksOfArticleInEmplacement(stock_depart.article_id, emplacement_destination.id)
            if list_stocks_destination: stock_destination = list_stocks_destination[0]
            else:
                # Si il ya pas de stock pour cet article dans cet emplacement, on crée un nouveau stock
                stock_destination = dao_stock_article.toCreateStockArticle(0, emplacement_destination.id, stock_depart.article_id)
                stock_destination = dao_stock_article.toSaveStockArticle(auteur, stock_destination)

            # DIMINUTION DE LA QUANTITE DU STOCK D'ORIGINE
            stock_depart.quantite_disponible = stock_depart.quantite_disponible - quantite_recue
            dao_stock_article.toUpdateStockArticle(stock_depart.id, stock_depart)

            # AUGMENTATION DE LA QUANTITE DU STOCK DE DESTINATION
            stock_destination.quantite_disponible = stock_destination.quantite_disponible + quantite_recue
            dao_stock_article.toUpdateStockArticle(stock_destination.id, stock_destination)

            #ENREGISTRER LE MOUVEMENT
            if quantite_recue > 0:
                mouvement_stock = dao_mouvement_stock.toCreateMouvementStock(quantite_recue,"","TRANSFERT",stock_depart.id, stock_destination.id,None,None,None,ordre_id)
                dao_mouvement_stock.toSaveMouvementStock(auteur, mouvement_stock)

        bon_retour.est_realisee = est_realisee
        if est_realisee == True :
            bon_retour.date_realisation = timezone.now()

        bon_retour.employe_id = responsable_id
        is_done = dao_bon_retour.toUpdateBonTransfert(ordre_id, bon_retour)



        if is_done == True :
            transaction.savepoint_commit(sid)
            return HttpResponseRedirect(reverse('module_inventaire_details_retour_internal', args=(ordre_id,)))
        else:
            transaction.savepoint_rollback(sid)
            return HttpResponseRedirect(reverse('module_inventaire_completer_retour_internal', args=(ordre_id,)))
    except Exception as e:
        #print("ERREUR")
        #print(e)
        transaction.savepoint_rollback(sid)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_completer_retour_internal', args=(ordre_id,)))


@transaction.atomic
def post_workflow_retour(request):
    sid = transaction.savepoint()
    try:
        utilisateur_id = request.user.id
        auteur = identite.utilisateur(request)
        base_dir = settings.BASE_DIR
        media_dir = settings.MEDIA_ROOT
        media_url = settings.MEDIA_URL
        etape_id = request.POST["etape_id"]
        transfert_id = request.POST["doc_id"]

        employe = dao_employe.toGetEmployeFromUser(utilisateur_id)
        etape = dao_wkf_etape.toGetEtapeWorkflow(etape_id)
        # bon_transfert = dao_bon_transfert.toGetBonTransfert(transfert_id)
        bon_retour = dao_bon_retour.toGetBonRetour(transfert_id)

        service_ref = dao_unite_fonctionnelle.toGetUniteFonctionnelleOfEmplacement(bon_retour.emplacement_origine.id)

        transitions_etapes_suivantes = dao_wkf_etape.toListEtapeSuivante(bon_retour.statut_id, service_ref.id)
        for item in transitions_etapes_suivantes:

            if item.condition.designation == "Upload":
                if 'file_upload' in request.FILES:
                    nom_fichier = request.FILES['file_upload']
                    doc = dao_document.toUploadDocument(auteur, nom_fichier, bon_retour)

                    bon_retour.statut_id = etape.id
                    bon_retour.etat = etape.designation
                    bon_retour.save()
                    document = dao_document_bon_transfert.toCreateDocument("Bon de retour de matériel",doc.url_document, bon_retour.etat,transfert_id)
                    document = dao_document_bon_transfert.toSaveDocument(auteur, document)
                else:
                    pass

            else:
                # Gestion des transitions dans le document
                bon_retour.statut_id = etape.id
                bon_retour.etat = etape.designation
                bon_retour.save()

        historique = dao_wkf_historique_bon_transfert.toCreateHistoriqueWorkflow(employe.id, etape.id, bon_retour.id)
        historique = dao_wkf_historique_bon_transfert.toSaveHistoriqueWorkflow(historique)

        if historique != None :
            transaction.savepoint_commit(sid)
            #return HttpResponseRedirect(reverse('module_achat_details_bon_achat', args=(demande.id,)))
            return HttpResponseRedirect(reverse('module_inventaire_details_retour_internal', args=(transfert_id,)))
        else:
            transaction.savepoint_rollback(sid)
            return HttpResponseRedirect(reverse('module_inventaire_details_retour_internal', args=(transfert_id,)))

    except Exception as e:
        transaction.savepoint_rollback(sid)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_retour_internal'))


def get_to_asset_of_retour_internal(request):
    sid = transaction.savepoint()
    ordre_id = int(request.POST["ordre_id"])
    try:
        permission_number = 980
        # modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request)
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        responsable_id = int(request.POST["responsable_id"])
        agent_id = int(request.POST["agent_id"])
        ##print(agent_id)
        est_realisee = True
        dico_asset = {}

        # bon_transfert = dao_bon_transfert.toGetBonTransfert(ordre_id)
        bon_retour = dao_bon_retour.toGetBonRetour(ordre_id)
        emplacement_origine = dao_emplacement.toGetEmplacement(bon_retour.emplacement_origine_id)
        emplacement_destination = dao_emplacement.toGetEmplacement(bon_retour.emplacement_destination_id)
        list_ligne_id = request.POST.getlist('ligne_id', None)
        list_quantite_fournie = request.POST.getlist("quantite_fournie", None)

        # lignes = dao_ligne_transfert.toListLignesTransfert(ordre_id)
        lignes = dao_ligne_bon_retour.toListLignesBonRetour(ordre_id)
        for ligne in lignes:
            dico_asset[ligne.article_identifiant] = dao_asset.toGetAssetByArticleOfEmplacement(ligne.article_identifiant,emplacement_origine.id)

        is_done = True
        if is_done == True :

            lignes = dao_ligne_bon_retour.toListLignesBonRetour(ordre_id)
            bon_retour = dao_bon_retour.toGetBonRetour(ordre_id)
            serv_ref_id = request.POST["service_referent_id"]
            service_referent = dao_unite_fonctionnelle.toGetUniteFonctionnelle(serv_ref_id)

            context = {
                'sous_modules':sous_modules,
                'title' : "Affecter les assets relatifs au bon N°%s" % bon_retour.numero_bon_retour,
                'model' : bon_retour,
                'lignes' : lignes,
                "dico_asset":dico_asset,
                "service_referent" : service_referent,
                "utilisateur" : utilisateur,
                "module" : ErpModule.MODULE_INVENTAIRE,
                'actions':auth.toGetActions(modules,utilisateur),
		        'organisation': dao_organisation.toGetMainOrganisation(),
                "modules": modules,
                'responsable_id':responsable_id,
                'roles':groupe_permissions,
                'agent_id':agent_id,
                'ordre_id':ordre_id,
                'list_quantite_fournie':list_quantite_fournie,
                'menu' : 11
            }

            template = loader.get_template("ErpProject/ModuleInventaire/retour_materiel/asset.html")
            return HttpResponse(template.render(context, request))
        else:

            return HttpResponseRedirect(reverse('module_inventaire_realiser_retour_internal', args=(ordre_id,)))
    except Exception as e:
        #print("ERREUR")
        #print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_realiser_retour_internal', args=(ordre_id,)))


@transaction.atomic
def post_to_asset_of_retour_internal(request):
    sid = transaction.savepoint()
    ordre_id = int(request.POST["ordre_id"])
    try:

        auteur = identite.utilisateur(request)
        responsable_id = int(request.POST["responsable_id"])
        agent_id = int(request.POST["agent_id"])
        ##print('agent on POST')
        ##print(agent_id)
        est_realisee = True

        # bon_transfert = dao_bon_transfert.toGetBonTransfert(ordre_id)
        bon_retour = dao_bon_retour.toGetBonRetour(ordre_id)
        operation_stock = dao_operation_stock.toGetOperationStock(bon_retour.operation_stock_id)
        emplacement_destination = dao_emplacement.toGetEmplacement(bon_retour.emplacement_destination_id)
        list_ligne_id = request.POST.getlist('ligne_id', None)
        list_quantite_fournie = request.POST.getlist("quantite_fournie", None)
        ##print(list_ligne_id)
        ##print("listes")
        ##print(list_quantite_fournie)
        ##print(len(list_ligne_id))
        ##print(len(list_quantite_fournie))
        for i in range(0, len(list_ligne_id)):
            ligne_id = int(list_ligne_id[i])
            quantite_fournie = makeFloat(list_quantite_fournie[i])

            # ligne_transfert = dao_ligne_transfert.toGetLigneTransfert(ligne_id)
            ligne_transfert = dao_ligne_bon_retour.toGetLigneBonRetour(ligne_id)
            #Si la quantité demandée est superieure à la somme des quantitées déjà fournies, on n'est réalise pas pcq on n'a pas encore tout reçu
            if quantite_fournie > ligne_transfert.quantite_fournie : return HttpResponseRedirect(reverse('module_inventaire_realiser_retour_internal', args=(ordre_id,)))

            # On ajoute la nouvelle quantité reçue
            ligne_transfert.quantite_fournie = quantite_fournie
            dao_ligne_bon_retour.toUpdateLigneBonRetour(ligne_id, ligne_transfert)

            # On recuper le stock de l'article dans l'emplacement de destination pour transfert
            stock_depart = dao_stock_article.toGetStockArticle(ligne_transfert.stock_article_id)
            list_stocks_destination = dao_stock_article.toListStocksOfArticleInEmplacement(stock_depart.article_id, emplacement_destination.id)
            if list_stocks_destination: stock_destination = list_stocks_destination[0]
            else:
                # Si il ya pas de stock pour cet article dans cet emplacement, on crée un nouveau stock
                stock_destination = dao_stock_article.toCreateStockArticle(0, emplacement_destination.id, stock_depart.article_id)
                stock_destination = dao_stock_article.toCreateStockArticle(stock_depart.article_id,0,emplacement_destination.id)
                stock_destination = dao_stock_article.toSaveStockArticle(stock_destination)

            # DIMINUTION DE LA QUANTITE DU STOCK D'ORIGINE
            stock_depart.quantite_disponible = stock_depart.quantite_disponible - quantite_fournie
            dao_stock_article.toUpdateStockArticle(stock_depart.id, stock_depart)

            # AUGMENTATION DE LA QUANTITE DU STOCK DE DESTINATION
            stock_destination.quantite_disponible = stock_destination.quantite_disponible + quantite_fournie
            dao_stock_article.toUpdateStockArticle(stock_destination.id, stock_destination)

            #ENREGISTRER LE MOUVEMENT
            if quantite_fournie > 0:
                mouvement_stock = dao_mouvement_stock.toCreateMouvementStock(quantite_fournie,"","TRANSFERT",stock_depart.id, stock_destination.id,None,None,None,ordre_id)
                dao_mouvement_stock.toSaveMouvementStock(auteur, mouvement_stock)

        bon_retour.est_realisee = est_realisee
        if est_realisee == True :
            bon_retour.date_realisation = timezone.now()

        bon_retour.employe_id = responsable_id
        if agent_id != 0 :
            ##print("inside")
            bon_retour.agent_id = agent_id

        is_done = dao_bon_retour.toUpdateBonTransfert(ordre_id, bon_retour)


        #Flow
        dao_bon_retour = dao_bon_retour.toGetBonRetour(ordre_id)
        wkf_task.passingStepWorkflow(auteur,bon_retour)

        #Traitement des assets

        #list_numero_serie = request.POST.getlist('numero_serie', None)
        list_asset_id = request.POST.getlist('asset_id', None)

        #list_description = request.POST.getlist('description', None)
        list_article_id = request.POST.getlist('article_id', None)
        service_ref_id = request.POST["service_referent_id"]
        ##print("responsable")
        ##print(responsable_id)
        for i in range(0, len(list_asset_id)):
            ##print("inside ")
            asset_id = list_asset_id[i]
            ##print(asset_id)
            asset = dao_asset.toUpdateAssetAffectation(asset_id,responsable_id)
            ##print(asset)


        if is_done == True :
            transaction.savepoint_commit(sid)
            return HttpResponseRedirect(reverse('module_inventaire_details_retour_internal', args=(ordre_id,)))
        else:
            transaction.savepoint_rollback(sid)
            return HttpResponseRedirect(reverse('module_inventaire_realiser_retour_internal', args=(ordre_id,)))
    except Exception as e:
        transaction.savepoint_rollback(sid)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_realiser_retour_internal', args=(ordre_id,)))

#######

#REBUT

def get_lister_rebut(request):
    permission_number = 1005
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
    if response != None:
        return response

    #*******Filtre sur les règles **********#
    model = dao_model.toListModel(dao_rebut.toList(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
    # print('LIST REBUT', model)

    try:
	    view = str(request.GET.get("view","list"))
    except Exception as e:
	    view = "list"

    #Pagination
    model = pagination.toGet(request, model)

    context = {
        'sous_modules':sous_modules,
        'title' : "Liste des rebuts",
        'model' : model,
        "utilisateur" : utilisateur,
        'view' : view,
        'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
        "modules" : modules,
        "module" : ErpModule.MODULE_INVENTAIRE,
        'menu': 9
    }
    template = loader.get_template("ErpProject/ModuleInventaire/rebut/list.html")
    return HttpResponse(template.render(context, request))

def get_creer_rebut(request):
    try:
        permission_number = 1006
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        services_referents = dao_unite_fonctionnelle.toListUniteFonctionnelleWHNoneService()
        emplacements = dao_emplacement.toListAllEmplacementNotRebut()

        context = {
            'sous_modules':sous_modules,
            'title' : "Nouveau rébut",
            'emplacements':emplacements,
            'services_referents':services_referents,
            "utilisateur" : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		    'organisation': dao_organisation.toGetMainOrganisation(),
            'articles' : dao_article.toListArticlesStockables(),
            "numero" : dao_rebut.toGenerateNumero(),
            "module" : ErpModule.MODULE_INVENTAIRE,
            "modules" : modules,
            'menu': 11,
            'operations' : dao_operation_stock.toListOperationsStock(),
        }
        template = loader.get_template("ErpProject/ModuleInventaire/rebut/add.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        # print("Erreur Get Rebut")
        # print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_rebut'))

@transaction.atomic
def post_valider_rebut(request):
    sid = transaction.savepoint()
    try:
        print('*****CREATION REBUT******')
        numero = dao_rebut.toGenerateNumero()
        emplacement = int(request.POST["emplacement_origine_id"])
        article = int(request.POST["article_id"])
        print('****BEFOR LA QUANTITE PREVU')
        # quantite = request.POST["quantite"]
        united = int(request.POST["unite_id"])
        numero_serie = int(request.POST["serie_id"])
        document = request.POST["document"]
        type_op = int(request.POST["operation_stock_id"])

        emplacement_rebut = dao_emplacement.toGetEmplacementByREBUT()
        auteur = identite.utilisateur(request)
        employe_id = auteur.id

        quantite = float(1)

        rebut = dao_rebut.toCreate(numero,article,numero_serie,quantite,united,emplacement,emplacement_rebut.id,document)
        rebut = dao_rebut.toSave(employe_id,rebut)
        # print(rebut)
        rebut.type_operation_id = type_op
        rebut.save()

        if rebut != 0:
            stock_depart = dao_stock_article.toGetStocksOfArticleInEmplacement(article,emplacement)
            list_stocks_destination = dao_stock_article.toGetStocksOfArticleInEmplacement(article,emplacement_rebut.id)
            if list_stocks_destination: stock_destination = list_stocks_destination[0]

            else:
                # Si il ya pas de stock pour cet article dans cet emplacement, on crée un nouveau stock
                stock_destination = dao_stock_article.toCreateStockArticle(article, 0, emplacement_rebut.id, None)
                stock_destination = dao_stock_article.toSaveStockArticle(stock_destination)


            # print('STOCK DEPART', stock_depart)
            # DIMINUTION DE LA QUANTITE DU STOCK D'ORIGINE
            stock_depart.quantite_disponible = stock_depart.quantite_disponible - quantite
            dao_stock_article.toUpdateStockArticle(stock_depart.id, stock_depart)

            # AUGMENTATION DE LA QUANTITE DU STOCK DE DESTINATION
            stock_destination.quantite_disponible = stock_destination.quantite_disponible + quantite
            dao_stock_article.toUpdateStockArticle(stock_destination.id, stock_destination)

            #ENREGISTRER LE MOUVEMENT
            if quantite > 0:
                mouvement_stock = dao_mouvement_stock.toCreateMouvementStock(quantite,"","TRANSFERT",stock_depart.id, stock_destination.id,None,None,None,None)
                dao_mouvement_stock.toSaveMouvementStock(auteur, mouvement_stock)

            #Traitement des assets
            MonAsset = dao_asset.toGetAsset(numero_serie)
            MonAsset.emplacement = emplacement_rebut
            MonAsset.save()

            transaction.savepoint_commit(sid)
            messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
            return HttpResponseRedirect(reverse('module_inventaire_list_rebut'))
        else:
            transaction.savepoint_rollback(sid)
            messages.error(request,messages.ERROR, "Une Erreur est survenue lors du tranfert")
            return HttpResponseRedirect(reverse('module_inventaire_add_rebut'))
    except Exception as e:
        transaction.savepoint_rollback(sid)
        print('ERREUR DE POST VALIDER REBUT')
        print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_add_rebut'))

def get_detail_rebut(request, ref):
    try:
        permission_number = 1005
        # modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request)
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        ref = int(ref)

        model = dao_rebut.toGet(ref)

        context = {
            'sous_modules':sous_modules,
            'title' : "Détail du transfert Rébut N°%s" % model.numero,
            'model' : model,
            "utilisateur" : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		    'organisation': dao_organisation.toGetMainOrganisation(),
            "modules" : modules ,
            "module" : ErpModule.MODULE_INVENTAIRE,
            'menu' : 4
        }
        template = loader.get_template("ErpProject/ModuleInventaire/rebut/item.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_list_rebut'))


#RAPPORT MOUVEMENT DE STOCK
def get_rapport_mvt_stock(request):
    try:
        permission_number = 1007
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response
        services_referents = dao_unite_fonctionnelle.toListUniteFonctionnelleWHNoneService()
        emplacements = dao_emplacement.toListEmplacement()
        articlesInStock = dao_stock_article.toListStocksArticles()
        context = {
            'sous_modules':sous_modules,
            'title' : "Mouvement de Stock",
            'emplacements':emplacements,
            'services_referents':services_referents,
            "utilisateur" : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		    'organisation': dao_organisation.toGetMainOrganisation(),
            'articles' : articlesInStock,
            "numero" : dao_rebut.toGenerateNumero(),
            "module" : ErpModule.MODULE_INVENTAIRE,
            "modules" : modules,
            'menu': 11,
            'operations' : dao_operation_stock.toListOperationsStock(),
        }
        template = loader.get_template("ErpProject/ModuleInventaire/rapports/add.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        # print('ERREUR RAPPORT INVENTAIRE')
        # print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_tableau_de_bord'))

def get_list_categorie_of_article(request):
    data = []
    res_list = []

    try:
        service = int(request.GET["ref"])
        stock = dao_stock_article.toListStocksInEmplacement(service)
        # print("LES CAT", lescat)
        for el in stock:
            item = {"id" : el.article.categorie.id, "designation" :el.article.categorie.designation}
            res_list.append(item)

        # print('BEFORE PASS CONTENT', res_list)
        data = [i for n, i in enumerate(res_list) if i not in res_list[n + 1:]]

        # print('APRES CONTENT', data)
        return JsonResponse(data, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse(data, safe=False)


def get_detail_rapport_mvt_stock(request):
    try:
        permission_number = 1007
        # modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request)
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        filtre = int(request.POST['filtre'])
        emplacement = int(request.POST['emplacement_origine_id'])
        rapport_de = int(request.POST["inventaire_de"])
        article_id = request.POST['article_id']
        categorie_id = request.POST["categorie_id"]

        date_debut = request.POST['date_debut']
        date_fin = request.POST['date_fin']

        date_debut_bcp = request.POST['date_debut']
        date_fin_bcp = request.POST['date_fin']

        checkprint = int(request.POST['print'])

        date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))
        date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]))

        txt_emplacement = "Tous les emplacements"
        # txt_valeur = ""
        txt_filtre  = "ACHAT / TRANSFERT / INVENTAIRE"
        rapport_sur = 'Tous les articles'

        if rapport_de == 0:
            lignes_mvt = Model_Mouvement_stock.objects.filter(creation_date__date__range = [date_debut, date_fin])
            print(' rapport 0 LIGNE MVT', lignes_mvt)

        elif rapport_de == 1:
            categorie = Model_Categorie.objects.get(pk=categorie_id)
            rapport_sur =  categorie.designation

            lignes_mvt = Model_Mouvement_stock.objects.filter(creation_date__date__range = [date_debut, date_fin], stock_article_entrant__article__categorie__id=categorie.id)
            # print(' rapport 1 LIGNE MVT', lignes_mvt)


        elif rapport_de == 2:
            article = Model_Article.objects.filter(pk=article_id).first()
            rapport_sur =  article.designation

            lignes_mvt = Model_Mouvement_stock.objects.filter(creation_date__date__range = [date_debut, date_fin], stock_article_entrant__article__id=article.id)
            # print(' rapport 2 LIGNE MVT', lignes_mvt)

        if emplacement != 0 :
            emplacement = Model_Emplacement.objects.filter(pk=emplacement).first()
            txt_emplacement = emplacement.designation
            # print('EMPLACEMENT ID', emplacement.id)

            #tot = lignes_commandes.filter(commande__session__pos__emplacement__entrepot__shop__id = site.id).aggregate(Sum('montant'))
            #lignes_commandes = lignes_commandes.filter(commande__session__pos__emplacement__entrepot__shop__id = site.id)
            lignes_mvt = lignes_mvt.filter(stock_article_entrant__emplacement__id = emplacement.id)
            print('Emplacement', txt_emplacement, ':', lignes_mvt)

        if filtre == 1:
            lignes_mvt = lignes_mvt.filter(type__contains='ACHAT')
            txt_filtre = "ACHAT"
            # print('Filtre 1 LIGNE MVT', lignes_mvt)


        elif filtre == 2:
            lignes_mvt = lignes_mvt.filter(type__contains='TRANSFERT')
            txt_filtre = "TRANSFERT"
            print('Filtre 2 LIGNE MVT', lignes_mvt)

        elif filtre == 3:
            lignes_mvt = lignes_mvt.filter(type__contains='INVENTAIRE')
            txt_filtre = "INVENTAIRE"
            # print('Filtre 3 LIGNE MVT', lignes_mvt)




        context = {
            'sous_modules':sous_modules,
            'title' : "Rapport des Mouvements de Stock",
            'model' : lignes_mvt,
            "utilisateur" : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		    'organisation': dao_organisation.toGetMainOrganisation(),
            "modules" : modules ,
            "module" : ErpModule.MODULE_INVENTAIRE,
            'menu' : 4,
            'txt_emplacement' : txt_emplacement,
            'txt_filtre' : txt_filtre,
            'dates' : ' Du ' + date_debut_bcp + ' au ' + date_fin_bcp,
            'rapport': rapport_sur,
            'rapport_de' : int(rapport_de),

            'filtre' : filtre,
            'emplacement' : int(request.POST['emplacement_origine_id']),
            'article_id' : article_id,
            'categorie_id' : categorie_id,
            'date_debut' : request.POST['date_debut'],
            'date_fin' : request.POST['date_fin'],
        }
        if checkprint == 0:
            template = loader.get_template("ErpProject/ModuleInventaire/rapports/item.html")
            return HttpResponse(template.render(context, request))
        else :
            return weasy_print("ErpProject/ModuleInventaire/rapports/print.html", "Mouvement_de_stock.pdf", context)
    except Exception as e:
        print("ERREUR")
        # print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_create_rapport_stock'))

#RAPPORT ARTICLE EN STOCK
def get_rapport_article_stock(request):
    try:
        permission_number = 1007
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response
        services_referents = dao_unite_fonctionnelle.toListUniteFonctionnelleWHNoneService()
        emplacements = dao_emplacement.toListEmplacement()
        articlesInStock = dao_stock_article.toListStocksArticles()
        context = {
            'sous_modules':sous_modules,
            'title' : "Article en Stock",
            'emplacements':emplacements,
            'services_referents':services_referents,
            "utilisateur" : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		    'organisation': dao_organisation.toGetMainOrganisation(),
            'articles' : articlesInStock,
            "numero" : dao_rebut.toGenerateNumero(),
            "module" : ErpModule.MODULE_INVENTAIRE,
            "modules" : modules,
            'menu': 11,
        }
        template = loader.get_template("ErpProject/ModuleInventaire/reporting/article_stock/add.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print('ERREUR RAPPORT ARTICLE EN STOCK')
        print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_tableau_de_bord'))

def get_detail_article_stock(request):
    try:
        permission_number = 1007
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response
        emplacement_origine_id = int(request.POST['emplacement_origine_id'])
        inventaire_de = int(request.POST["inventaire_de"])
        checkprint = int(request.POST['print'])
        emplac = None

        if inventaire_de == 0:
            articles = dao_article.toListArticles()
            categorie = None
            article = None
            categories = None
        elif inventaire_de == 1:
            categorie_id = int(request.POST["categorie_id"])
            categorie = Model_Categorie.objects.get(pk=categorie_id)
            articles = Model_Article.objects.filter(categorie_id = categorie_id).order_by('designation')
            article = None
            categories = None

        elif inventaire_de == 2:
            article_id = int(request.POST["article_id"])
            articles = Model_Article.objects.filter(pk=article_id).order_by('designation')
            article = Model_Article.objects.get(pk=article_id)
            categorie = None
            categories = None

        data = []
        valeur_stock = 0
        if emplacement_origine_id == 0:
            for i in articles:
                stockage = Model_StockArticle.objects.filter(article_id = i.id).order_by('emplacement__designation').exclude(quantite_disponible = 0)
                if not stockage:
                    stockage = None
                else :
                    for it in stockage:
                        valeur_stock += it.quantite_disponible * i.prix_unitaire
                item = {
                    'article' : i,
                    'stockage' : stockage,
                }
                data.append(item)
        else:
            emplac = Model_Emplacement.objects.get(pk=emplacement_origine_id)
            for i in articles:
                qte = 0
                val = 0
                stockage = Model_StockArticle.objects.filter(article_id = i.id, emplacement_id = emplacement_origine_id).order_by('emplacement__designation').exclude(quantite_disponible = 0)
                if not stockage:
                    stockage = None
                else:
                    for it in stockage:
                        valeur_stock += it.quantite_disponible * i.prix_unitaire
                        val += it.quantite_disponible * i.prix_unitaire
                        qte = it.quantite_disponible
                item = {
                    'article' : i,
                    'stockage' : stockage,
                    'qte' : qte,
                    'val_inventaire' : val,
                }
                data.append(item)

        context = {
            'sous_modules':sous_modules,
            'title' : "Rapport des Articles en Stock",
            'model' : data,
            "utilisateur" : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		    'organisation': dao_organisation.toGetMainOrganisation(),
            "modules" : modules ,
            "module" : ErpModule.MODULE_INVENTAIRE,
            'menu' : 4,
            'emplacement' : emplacement_origine_id,
            'empl' : emplac,
            'valeur_stock' : valeur_stock,

            'emplacement_origine_id' : request.POST['emplacement_origine_id'],
            'inventaire_de' : request.POST["inventaire_de"],
            'categorie_id' : request.POST["categorie_id"],
            'article_id' : request.POST["article_id"],
        }
        if checkprint == 0:
            template = loader.get_template("ErpProject/ModuleInventaire/reporting/article_stock/item.html")
            return HttpResponse(template.render(context, request))
        else :
            return weasy_print("ErpProject/ModuleInventaire/reporting/article_stock/print.html", "Article_en_stock.pdf", context)
    except Exception as e:
        # print("ERREUR POST RAPPORT ARTICLE EN STOCK")
        # print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_create_rapport_article_stock'))
