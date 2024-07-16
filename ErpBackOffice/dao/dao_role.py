from __future__ import unicode_literals

from ErpBackOffice.models import Model_Role, Model_RoleModule, Model_RoleSousModule, Model_RoleUtilisateur, Model_RoleAction
from django.utils import timezone

class dao_role(object):
    id = 0
    nom_role = ""
    auteur_id = 0

    @staticmethod
    def toListRoles():
        return Model_Role.objects.all()

    @staticmethod
    def toListRolesCreesPar(auteur_id):
        return Model_Role.objects.filter(auteur_id = auteur_id).order_by("nom_role")

    @staticmethod
    def toListRolesLiesAuModule(module_id):
        try:
            list = []
            roles_modules = Model_RoleModule.objects.filter(module_id = module_id)
            for item in roles_modules:
                role = Model_Role.objects.get(pk = item.role_id)
                list.append(role)
            return list
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return []

    @staticmethod
    def toListRolesModules():
        try:
            return Model_RoleModule.objects.all()
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return []

    @staticmethod
    def toListRolesLiesAuSousModule(sous_module_id):
        try:
            list = []
            roles_sous_modules = Model_RoleSousModule.objects.filter(sous_module_id = sous_module_id)
            for item in roles_sous_modules:
                role = Model_Role.objects.get(pk = item.role_id)
                list.append(role)
            return list
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return []

    @staticmethod
    def toGetRoleDeLaPersonne(personne_id):
        try:
            role_utilisateur = Model_RoleUtilisateur.objects.get(utilisateur_id = personne_id)
            role = Model_Role.objects.get(pk = role_utilisateur.role_id)
            return role
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return None
    

    @staticmethod
    def toListRoleDeLaPersonne(personne_id):
        try:
            liste = []
            role_utilisateur = Model_RoleUtilisateur.objects.filter(utilisateur_id = personne_id)
            for item in role_utilisateur:
                role = Model_Role.objects.get(pk = item.role_id)
                liste.append(role)
            return liste
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return None


    @staticmethod
    def toListRolesRefusesTo(personne_id):
        try:
            list = []
            roles = Model_Role.objects.all().order_by("nom_role")
            for item in roles:
                nombre_roles_utilisateurs = Model_RoleUtilisateur.objects.filter(role_id = item.id).count()
                if nombre_roles_utilisateurs != 0:
                    roles_utilisateurs = Model_RoleUtilisateur.objects.filter(role_id = item.id)
                    for r_user in roles_utilisateurs:
                        if r_user.utilisateur_id != personne_id: list.append(item)
                else: list.append(item)
            return list
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return []

    @staticmethod
    def toListRolesLiesAction(action_id):
        try:
            list = []
            roles_actions = Model_RoleAction.objects.filter(action_id = action_id)
            for item in roles_actions:
                role = Model_Role.objects.get(pk = item.role_id)
                list.append(role)
            return list
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return []

    @staticmethod
    def toCreateRole(nom_role):
        try:
            role = dao_role()
            role.nom_role = nom_role
            return role
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DU ROLE")
            #print(e)
            return None

    @staticmethod
    def toSaveRole(auteur, object_dao_role):
        try:
            role = Model_Role()
            role.auteur_id = auteur.id
            role.nom_role = object_dao_role.nom_role
            role.creation_date = timezone.now()
            role.save()
            return role
        except Exception as e:
            #print("ERREUR LORS DU SAVE DU ROLE")
            #print(e)
            return None        

    @staticmethod
    def toUpdateRole(id, object_dao_role):
        try:
            role = Model_Role.objects.get(pk = id)
            role.nom_role = object_dao_role.nom_role
            role.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA MISE A JOUR DU ROLE")
            #print(e)
            return False        

    @staticmethod
    def toDeleteRole(id):
        try:
            role = Model_Role.objects.get(pk = id)
            role.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION DU ROLE")
            #print(e)
            return False
  
    @staticmethod
    def toGetRole(id):
        try:
            return Model_Role.objects.get(pk = id)
        except Exception as e:
            return None

    @staticmethod
    def toAddModuleInRole(auteur, module_id, role_id):
        try:
            role_module = Model_RoleModule()
            role_module.auteur_id = auteur.id
            role_module.module_id = module_id
            role_module.role_id = role_id
            role_module.creation_date = timezone.now()
            role_module.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU INSERT")
            #print(e)
            return False

    @staticmethod
    def toDeleteModuleInRole(module_id, role_id):
        try:
            role_module = Model_RoleModule.objects.filter(role_id= role_id).get(module_id = module_id)
            role_module.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DU DELETE")
            #print(e)
            return False

    @staticmethod
    def toAddSousModuleInRole(auteur, sous_module_id, role_id):
        try:
            role_sous_module = Model_RoleSousModule()
            role_sous_module.auteur_id = auteur.id
            role_sous_module.sous_module_id = sous_module_id
            role_sous_module.role_id = role_id
            role_sous_module.creation_date = timezone.now()
            role_sous_module.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU INSERT")
            #print(e)
            return False

    @staticmethod
    def toDeleteSousModuleInRole(sous_module_id, role_id):
        try:
            role_sous_module = Model_RoleSousModule.objects.filter(role_id= role_id).get(sous_module_id = sous_module_id)
            role_sous_module.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DU DELETE")
            #print(e)
            return False

    @staticmethod
    def toAddActionSousModuleInRole(auteur, action_sous_module_id, role_id):
        try:
            role_action_sous_module = Model_RoleAction()
            role_action_sous_module.auteur_id = auteur.id
            role_action_sous_module.action_id = action_sous_module_id
            role_action_sous_module.role_id = role_id
            role_action_sous_module.creation_date = timezone.now()
            role_action_sous_module.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU INSERT")
            #print(e)
            return False

    @staticmethod
    def toDeleteActionSousModuleInRole(action_sous_module_id, role_id):
        try:
            role_action_sous_module = Model_RoleAction.objects.filter(role_id = role_id).get(action_id = action_sous_module_id)
            role_action_sous_module.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DU DELETE DE L'ACTION")
            #print(e)
            return False

    @staticmethod
    def toAttributeRole(auteur, utilisateur_id, role_id):
        try:
            role_utilisateur = Model_RoleUtilisateur()
            role_utilisateur.auteur_id = auteur.id
            role_utilisateur.utilisateur_id = utilisateur_id
            role_utilisateur.role_id = role_id
            role_utilisateur.creation_date = timezone.now()
            role_utilisateur.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU INSERT")
            #print(e)
            return False

    @staticmethod
    def toRetireRole(utilisateur_id, role_id):
        try:
            role_utilisateur = Model_RoleUtilisateur.objects.filter(role_id= role_id).get(utilisateur_id = utilisateur_id)
            role_utilisateur.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DU DELETE")
            #print(e)
            return False

    @staticmethod
    def isActionSousModuleAttacheAuRole(action_sous_module_id, role_id):
        try:
            roles_actions = Model_RoleAction.objects.filter(action_id = action_sous_module_id)
            for item in roles_actions:
                if item.role_id == role_id: return True
            return False
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return False

    @staticmethod
    def isSousModuleAttacheAuRole(sous_module_id, role_id):
        try:
            roles_sous_modules = Model_RoleSousModule.objects.filter(sous_module_id = sous_module_id)
            for item in roles_sous_modules:
                if item.role_id == role_id: return True
            return False
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return False

    @staticmethod
    def isModuleAttacheAuRole(module_id, role_id):
        try:
            roles_modules = Model_RoleModule.objects.filter(module_id = module_id)
            for item in roles_modules:
                if item.role_id == role_id: return True
            return False
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return False
    
    @staticmethod
    def toGetPersonOfRole(role_name):
        try:
            role_utilisateur = Model_RoleUtilisateur.objects.filter(role__nom_role = role_name).select_related()
            return role_utilisateur
        except Exception as e:
            #print("ERREUR LORS DU DELETE")
            #print(e)
            return False
    

    @staticmethod
    def toListRoleUtilisateurByRoleName(role_name):
        try:
            role = Model_Role.objects.get(nom_role = role_name)
            role_users = Model_RoleUtilisateur.objects.filter(role_id = role.id)
            return role_users
        except Exception as e:
            #print("ERREUR LORS DE LA REQUETE")
            #print(e)
            return False
    

    

            