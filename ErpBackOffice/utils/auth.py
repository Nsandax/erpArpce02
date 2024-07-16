from __future__ import unicode_literals
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.template import loader
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils import timezone
from django.core import serializers
from random import randint
from django.core.mail import send_mail
import datetime
import json

from ErpBackOffice.dao.dao_droit import dao_droit
from ErpBackOffice.dao.dao_module import dao_module
from ErpBackOffice.dao.dao_role import dao_role

from ErpBackOffice.utils.identite import identite
from ErpBackOffice.dao.dao_sous_module import dao_sous_module
from ErpBackOffice.dao.dao_groupe_permission import dao_groupe_permission
from ErpBackOffice.dao.dao_groupe_menu import dao_groupe_menu
from ErpBackOffice.dao.dao_permission import dao_permission
from ErpBackOffice.dao.dao_operationnalisation_module import dao_operationnalisation_module
from ErpBackOffice.utils.utils import utils
from ErpBackOffice.models import Model_Permission, Model_ActionUtilisateur
#POUR LOGGING
import logging, inspect
monLog = logging.getLogger('logger')

class auth(object):

    @staticmethod
    def toPostValidityDate(module_id, date):
        #Test if a module Controle de Gestion exist and it is activate!
        if dao_module.toTestModuleInstalledByCode("CTRL"):        
            return dao_operationnalisation_module.toCheckValidity(module_id, date)
        else:
            return True

    @staticmethod
    def toReturnFailed(request, function, module = "", exception = "", redirect = None, msg = "Une erreur est survenue pendant l'exécution"):
        monLog.error("{} :: {} :: ERREUR EFFECTUEE DANS LA FONCTION {} :: {}".format(identite.utilisateur(request), module, function.upper(), exception))
        monLog.debug("Info")
        print("ERREUR FONCTION {}() : {}".format(function, exception))
        messages.add_message(request, messages.ERROR, msg)
        if redirect == None: redirect = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(redirect)
    
    @staticmethod
    def toReturnApiFailed(request, function, module = "", exception = "", msg = "Une erreur est survenue pendant l'exécution"):
        monLog.error("{} :: {} :: ERREUR EFFECTUEE DANS LA FONCTION API {} :: {}".format("USER API", module, function.upper(), exception))
        monLog.debug("Info")
        print("ERREUR FONCTION API {}() : {}".format(function, exception))
        context = { "error" : True, "message" : msg}
        return JsonResponse(context, safe=False)

    @staticmethod
    def toGetAuth(requete):
        is_connect = identite.est_connecte(requete)
        if is_connect == False: return None, None, HttpResponseRedirect(reverse("backoffice_connexion"))
        #modules = []
        modules = dao_module.toListModulesInstalles()

        utilisateur = identite.utilisateur(requete)

        if utilisateur.nom_complet != "SYSTEM":
            #role = dao_role.toGetRoleDeLaPersonne(utilisateur.id)
            roles = dao_role.toListRoleDeLaPersonne(utilisateur.id)
            #print(roles)
            modules = []
            if roles == []: return None, None, HttpResponseRedirect(reverse("backoffice_erreur_role"))
            else :
                for role in roles:
                    list_modules = dao_module.toListModulesAttachesAuRole(role.id)
                    for module in list_modules:
                        modules.append(module)
        modules = set(modules)
        modules = list(modules)

        return modules,utilisateur,None

    @staticmethod
    def toGetAuthDroit(droit,requete):
        is_connect = identite.est_connecte(requete)
        if is_connect == False: return None, None, None, HttpResponseRedirect(reverse('backoffice_connexion'))
        utilisateur = identite.utilisateur(requete)
        roles = dao_role.toListRoleDeLaPersonne(utilisateur.id)
        modules = []
        allow_droit = False

        if droit == '': utilisateur.nom_complet = "SYSTEM"


        if utilisateur.nom_complet != "SYSTEM":
            if roles == []: return None, None,None, HttpResponseRedirect(reverse("backoffice_erreur_role"))
            else:
                for role in roles:
                    list_modules = dao_module.toListModulesAttachesAuRole(role.id)
                    nom_role = role.nom_role
                    #print("sjsjdsjsh")
                    for module in list_modules:
                        modules.append(module)
                    #print("ksdsdksj")
                    if allow_droit == False:
                        #print("je suis false")
                        allow_droit = dao_droit.toGetDroitRole(droit, nom_role, utilisateur.nom_complet)
                if allow_droit == False: return None, None,None, HttpResponseRedirect(reverse("backoffice_erreur_autorisation"))
            modules = set(modules)
            modules = list(modules)
        else:
            modules = dao_module.toListModulesInstalles()
            modules = set(modules)
            modules = list(modules)


        return modules,utilisateur,roles, None


    @staticmethod
    def toGetActions(modules,utilisateur):
        sous_modules = []
        actions = []

        roles = dao_role.toListRoleDeLaPersonne(utilisateur.id)

        if utilisateur.nom_complet == "SYSTEM":
            modules = dao_module.toListModulesInstalles()
            actions.extend(dao_droit.toListDroits())
            return actions


        for role in roles:
            for item in modules:
                sous_modules.extend(dao_sous_module.toListSousModulesOfAttachesAuRole(role.id, item.id))

        for role in roles:
            for item in sous_modules:
                actions.extend(dao_droit.toListDroitAutroses(item.id,role.nom_role))

        return actions


    @staticmethod
    def toCheckAdmin(module_name,utilisateur):
        if utilisateur.nom_complet == "SYSTEM": return True
        module = dao_module.toGetModuleByName(module_name)
        groupe_permissions = dao_groupe_permission.toListGroupePermissionDeLaPersonne(utilisateur.id)
        permission = dao_permission.toGetPermissionOfAdmin(module.id)
        for groupe_permission in groupe_permissions:
            if dao_permission.toCheckPermission(groupe_permission.id, permission.id):
                return True
        return False



    @staticmethod
    def toGetAuthentification(permission_number, requete, function_name=""):
        try:
            from django.urls import resolve
            current_func = resolve(requete.path_info).func
            module_name = current_func.__module__.split(".")[0]
            module = dao_module.toGetModuleByAppName(module_name)
            auth.toCreateActionIfNotExist(permission_number, function_name, module.id)
            is_connect = identite.est_connecte(requete)
            if is_connect == False: return None, None, None, None, HttpResponseRedirect(reverse("backoffice_connexion"))
            utilisateur = identite.utilisateur(requete)
            groupe_permissions = dao_groupe_permission.toListGroupePermissionDeLaPersonne(utilisateur.id)
            #les cas avec les mêmes noms de fonction dans des modules différents sont gerés maintenant
            action = Model_ActionUtilisateur.objects.filter(nom_action = function_name, permission__sous_module__module_id = module.id).first() 
            #action = Model_ActionUtilisateur.objects.filter(nom_action = function_name).first()
            permission = action.permission
            sous_modules = []
            modules = []
            is_permissioned = False

            if function_name == "": utilisateur.nom_complet = "SYSTEM"

            if utilisateur.nom_complet != "SYSTEM":
                for groupe_permission in groupe_permissions:
                    sous_modules.extend(dao_sous_module.toListSousModulesByPermission(permission, groupe_permission))
                    modules.extend(dao_module.toListModulesByPermission(groupe_permission))

                    if dao_permission.toCheckPermission(groupe_permission.id, permission.id) == True:
                        is_permissioned = True
                if not is_permissioned:
                    return  None, None, None, groupe_permissions, HttpResponseRedirect(reverse("backoffice_erreur_autorisation"))
            else:
                modules = dao_module.toListModulesInstalles()
                sous_modules = dao_sous_module.toListSousModulesByOfModuleByPermissionForAdmin(permission)

            modules = list(set(modules))
            modules = sorted(modules, key=lambda module: module.numero_ordre, reverse=False) 

            sous_modules = utils.remove_duplicate_in_list(sous_modules)
            sous_modules = sorted(sous_modules, key=lambda sous_module: 0 if sous_module.groupe_menu is None else sous_module.groupe_menu.id, reverse=False)  
            return  modules,sous_modules, utilisateur, groupe_permissions, None
        except Exception as e:
            print("ERREUR toGetDashboardAuthentification()")
            print(e)
            return  None, None, None, [], HttpResponseRedirect(reverse("backoffice_erreur_autorisation"))

    @staticmethod
    def toGetDashboardAuthentification(module_id, requete):
        try:
            is_connect = identite.est_connecte(requete)
            if is_connect == False: return None, None, None, None, HttpResponseRedirect(reverse("backoffice_connexion"))

            utilisateur = identite.utilisateur(requete)
            groupe_permissions = dao_groupe_permission.toListGroupePermissionDeLaPersonne(utilisateur.id)
            if module_id != 0: #erpbackoffice
                module = dao_module.toGetModule(module_id)
            sous_modules = []
            modules = []
            is_permissioned = False

            
            if utilisateur.nom_complet != "SYSTEM":
                for groupe_permission in groupe_permissions:
                    modules.extend(dao_module.toListModulesByPermission(groupe_permission))
                    if module_id != 0:
                        sous_modules.extend(dao_sous_module.toListSousModulesByGroupePermission(module, groupe_permission))
                        if module in modules:
                            is_permissioned = True
                if not is_permissioned:
                    if module_id != 0:      
                        return  None, None, None, groupe_permissions, HttpResponseRedirect(reverse("backoffice_erreur_autorisation"))
                    
            else:
                modules = dao_module.toListModulesInstalles()
                groupe_permission = dao_groupe_permission.toListGroupePermissions()
                if module_id != 0:
                    module = dao_module.toGetModule(module_id)
                    sous_modules = dao_sous_module.toListSousModulesByGroupePermissionForAdmin(module)
                    
            modules = list(set(modules))
            modules = sorted(modules, key=lambda module: module.numero_ordre, reverse=False) 
            
            sous_modules = utils.remove_duplicate_in_list(sous_modules)
            sous_modules = sorted(sous_modules, key=lambda sous_module: 0 if sous_module.groupe_menu is None else sous_module.groupe_menu.id, reverse=False)             
            return  modules,sous_modules, utilisateur, groupe_permissions, None
        except Exception as e:
            #print("ERREUR toGetDashboardAuthentification()")
            #print(e)
            return  None, None, None, [], HttpResponseRedirect(reverse("backoffice_erreur_autorisation"))
    
    @staticmethod
    def toCreateActionIfNotExist(permission_number, function_name, module_id):
        try:
            if permission_number == 0: return False
            
            action = None
            permission = dao_permission.toGetPermissionByNumber(permission_number)
            if permission != None: action = Model_ActionUtilisateur.objects.filter(nom_action = function_name, permission_id = permission.id, permission__sous_module__module_id = module_id).first()

            if action == None and permission != None:
                action = Model_ActionUtilisateur()
                action.nom_action = function_name
                action.permission_id = permission.id
                action.save()
                #print("Nouvelle action creee")
            return True
        except Exception as e:
            return False