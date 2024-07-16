# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ModuleRessourcesHumaines.dao.dao_employe import dao_employe
from django.contrib.auth.models import User, Group
from django.contrib.sessions.models import Session
from ErpBackOffice.models import Model_Employe, Model_RoleUtilisateur, Model_UserSessions
from django.utils import timezone
from django.db.models.functions import TruncMonth
from django.db.models import Count

class dao_utilisateur(dao_employe):

    
    @staticmethod
    def toListUtilisateur():
        return Model_Employe.objects.order_by("-id")
    
    
    @staticmethod
    def toListSessionOfUtilisateur(user_id):
        return Model_UserSessions.objects.filter(user_id = user_id).order_by("-logout_date")
        


    @staticmethod
    def toListUtilisateursActifs():
        return Model_Employe.objects.filter(est_actif = True).order_by("-nom_complet")

    @staticmethod
    def toListUtilisateursDuRole(role_id):
        try:
            list = []
            collection = Model_RoleUtilisateur.objects.filter(role_id = role_id)
            for item in collection :
                list.append(dao_utilisateur.toGetUtilisateur(item.utilisateur_id))
            return list
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return []
       
    @staticmethod
    def toSaveUtilisateur(auteur, objet_dao_employe):
        try:
            #print(objet_dao_employe.email)
            user = User.objects.create_user(
                username = objet_dao_employe.email,
				password = "password",
				email = objet_dao_employe.email
			)
            objet_dao_employe.user_id = user.id
            objet_dao_employe.type = "UTILISATEUR"
            return dao_employe.toSaveEmploye(auteur, objet_dao_employe)
        except Exception as e:
            #print("ERREUR LORS DE L'INSERT DU USER")
            #print(e)
            return None

    @staticmethod
    def toUpdateUtilisateur(id, objet_dao_employe):
        objet_dao_employe.id = id
        objet_dao_employe.type = "UTILISATEUR"
        return dao_employe.toUpdateEmploye(objet_dao_employe)
	
    @staticmethod
    def toActiveUtilisateur(id, est_actif):
        return dao_employe.toActiveEmploye(id, est_actif)
    
    @staticmethod
    def toGetUtilisateur(id):
        return dao_employe.toGetEmploye(id)
    
    @staticmethod
    def toGetUtilisateurDuProfil(user_id):
        try:
            return Model_Employe.objects.get(user_id = user_id)
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return None

    @staticmethod
    def toDeleteUtilisateur(id):
        return dao_employe.toDeleteEmploye(id) 

    @staticmethod
    def toListnombreEmployéConnecteRecement(today=timezone.now().year):
        try:

            # ListeExpression = Model_Expression.objects.annotate(month=TruncMonth('date_expression')).values('month').annotate(total=Count('demandeur'))
            ListSol = [0,0,0,0,0,0,0,0,0,0,0,0]
            ListeQuery =Model_Employe.objects.annotate(month=TruncMonth('user__last_login')).values('month').annotate(total=Count('user__last_login')).filter(user__last_login__year = today)
            #print("Pour 2020 : {}".format(Model_Expression.objects.annotate(month=TruncMonth('date_expression')).values('month').annotate(total=Count('demandeur')).filter(date_expression__year = 2019)))
            for item in ListeQuery:

                if item["month"].month==1:

                    #ListSol.remove()
                    if item["total"] == 0:
                        ListSol[0] = 0
                    else:
                        ListSol[0] = item["total"]
                    continue
                elif item["month"].month==2:
                    if item["total"] == 0:
                        ListSol[1] = 0
                    else:
                        ListSol[1] = item["total"]
                    continue
                elif item["month"].month==3:
                    if item["total"] == 0:
                        ListSol[2] = 0
                    else:
                        ListSol[2] = item["total"]
                    continue
                elif item["month"].month==4:
                    if item["total"] == 0:
                        ListSol[3] = 0
                    else:
                        ListSol[3] = item["total"]
                    continue
                elif item["month"].month==5:
                    if item["total"] == 0:
                        ListSol[4] = 0
                    else:
                        ListSol[4] = item["total"]
                    continue
                elif item["month"].month==6:
                    if item["total"] == 0:
                        ListSol[5] = 0
                    else:
                        ListSol[5] = item["total"]
                    continue
                elif item["month"].month==7:
                    if item["total"] == 0:
                        ListSol[6] = 0
                    else:
                        ListSol[6] = item["total"]
                    continue
                elif item["month"].month==8:
                    if item["total"] == 0:
                        ListSol[7] = 0
                    else:
                        ListSol[7] = item["total"]
                    continue
                elif item["month"].month==9:
                    if item["total"] == 0:
                        ListSol[8] = 0
                    else:
                        ListSol[8] = item["total"]
                    continue
                elif item["month"].month==10:
                    if item["total"] == 0:
                        ListSol[9] = 0
                    else:
                        ListSol[9] = item["total"]
                    continue
                elif item["month"].month==11:
                    if item["total"] == 0:
                        ListSol[10] = 0
                    else:
                        ListSol[10] = item["total"]
                    continue
                elif item["month"].month==12:
                    if item["total"] == 0:
                        ListSol[11] = 0
                    else:
                        ListSol[11] = item["total"]
                    continue
                else:
                    pass

            #print('Liste des expression %s' %(ListSol))
            return ListSol
        except Exception as e:
            #print("ERRER LISTEEXPRESSION BY MONTH WITHOUT USER ID")
            #print(e)
            pass



