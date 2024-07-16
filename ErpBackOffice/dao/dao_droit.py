# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_Droit
from django.utils import timezone
from ErpBackOffice.dao.dao_sous_module import dao_sous_module
from ErpBackOffice.dao.dao_role import dao_role

class dao_droit(object):
    id = 0
    droit	= ""
    roles = ""
    

    @staticmethod
    def toListDroits():
        return Model_Droit.objects.all()

    @staticmethod
    def toListRoleDroit(id):
        try:
            droit = Model_Droit.objects.get(id = id)

            droits = []

            if droit.roles != None:
                itm = droit.roles.split(',')
                itm = filter(None, itm)
                droits = itm
            return droits
        except Exception as e:
            #print("ERREUR LORS DU LISTE DU DROIT")
            #print(e)
            return None

    

    @staticmethod
    def toCreateDroit(droit, roles):        
        try:
            droit = dao_droit()
            droit.droit = droit
            droit.roles = roles
            return droit
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DU DROIT")
            #print(e)
            return None

    @staticmethod
    def toSaveDroit(object_dao_droit):
        try:
            droit = Model_Droit()
            droit.droit = object_dao_droit.droit
            droit.image = object_dao_droit.droit
            droit.save()
            return droit
        except Exception as e:
            #print("ERREUR LORS DE L'ENREGISTREMENT DU DROIT")
            #print(e)
            return None
    
    @staticmethod
    def toUpdateDroit(id, object_dao_droit):
        try:
            droit = Model_Droit.objects.get(pk = id)
            droit.droit = object_dao_droit.droit
            droit.roles = object_dao_droit.roles
            droit.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA MISE A JOUR DU DROIT")
            #print(e)
            return False
  
    @staticmethod
    def toGetDroit(id):
        try:
            return Model_Droit.objects.get(pk = id)
        except Exception as e:
            return None

    @staticmethod
    def toGetDroitRole(droit, nom_role, nom_utilisateur):
    
        try:

            #print("DROIT = %s , NOM_ROLE = %s , NOM USER = %s" % (droit, nom_role, nom_utilisateur))

            if nom_utilisateur == "SYSTEM":
                return True
            else:
                droit = Model_Droit.objects.get(droit = droit)
                droit = droit.roles.find(nom_role+',')
                if droit == -1:
                    return False
                else:
                    return True

        except Exception as e:
            #print('ERREUR GET ROLE')
            #print(e)
            return False
        


    
    @staticmethod
    def toListDroitNonAutroses(sous_module,nom_role):
        
        try:
            droits = Model_Droit.objects.filter(sous_module_id = sous_module).order_by('droit')
            droit = []
            for item in droits:
                if item.roles != None:
                    itm = item.roles.find(nom_role+',')
                    if itm == -1:
                        droit.append(item)
                else:
                    droit.append(item)

            return droit
        except Exception as e:
            #print("ERREUR LORS DU LISTE DU DROIT")
            #print(e)
            return None
                

    @staticmethod
    def toListDroitAutroses(sous_module,nom_role):
        
        try:
            droits = Model_Droit.objects.filter(sous_module_id = sous_module).order_by('droit')

            droit = []

            for item in droits:
                if item.roles != None:
                    itm = item.roles.find(nom_role + ',')
                    if itm != -1:
                        droit.append(item)
                    
            #print(droit)
            return droit
        except Exception as e:
            #print("ERREUR LORS DU LISTE DU DROIT")
            #print(e)
            return None

    @staticmethod
    def toAddDroit(droit_id,role_id):
        try:
            droit = Model_Droit.objects.get(pk = droit_id)
            role = dao_role.toGetRole(role_id)

            if droit.roles == None or droit.roles == '':
                droit.roles = ',' + role.nom_role + ','
            else:
                droit.roles = droit.roles + role.nom_role + ','
            droit.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU INSERT DU DROIT")
            #print(e)
            return False

    
    @staticmethod
    def toRemoveDroit(droit_id,role_id):
        try:
            droit = Model_Droit.objects.get(pk = droit_id)
            role = dao_role.toGetRole(role_id)
            nom_role = ','+role.nom_role + ','
            droit_role = droit.roles.replace(nom_role,',')
            if droit_role == ',':
                droit_role = ''
            else:
                droit_role = droit_role
            
            #print("DROIIIIIIIIIIIIIIIIIIIT")
            #print(droit_role)

            droit.roles = droit_role
            droit.save()
            return True

        except Exception as e:
            #print("ERREUR LORS DU SUPPRESSION DU DROIT")
            #print(e)
            return False

    @staticmethod
    def toDeleteDroit(id):
        try:
            droit = Model_Droit.objects.get(pk = id)
            droit.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION DU DROIT")
            #print(e)
            return False

    @staticmethod
    def toChangeRoleDroit(nom_role,ancien_nom_role):
        try:
            droits = Model_Droit.objects.all()
            nom_role_old = ancien_nom_role
            #print("OLD ROLE NAME %s" % nom_role_old)
            #print("ACTUAL ROLE NAME %s" % nom_role)

            for item in droits:
                if item.roles != None or item.roles != '':
                    itm = item.roles.find(nom_role_old + ',')
                    #print("ITM %s" % itm)
                    if itm != -1:
                        roles = item.roles.replace(nom_role_old,nom_role)
                        droit = Model_Droit.objects.get(pk = item.id)
                        #print("ROLE %s" % roles)
                        
                        droit.roles = roles
                        droit.save()
            
            return True
        except Exception as e:
            #print("ERREUR LORS DU CHANGEMENT DU DROIT")
            #print(e)
            return False
                            
            