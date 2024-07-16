from django.utils import timezone
from ErpBackOffice.models import Model_Temp_Notification, Model_Notification, Model_Role, Model_RoleUtilisateur, Model_Expression, Model_Demande_achat, Model_Bon_reception
from ErpBackOffice.models import  Model_Bon_transfert, Model_Bon,Model_Avis_appel_offre, Model_Conge, Model_Asset,Model_TraitementImmobilisation
from ErpBackOffice.models import Model_Wkf_Etape, Model_Wkf_Transition
from django.db.models.signals import post_save
from ErpBackOffice import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from ErpBackOffice.dao.dao_role import dao_role
#from ErpBackOffice.utils.sending_email import sending_email
from ErpBackOffice.utils.EmailThread import send_async_mail
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


def signal_expression_besoin(sender,instance,created,**kwargs):
    try:
        recipient_list = []
        texte = ""
        if created:
            #print("NOTIFICATION EXPRESSION BESOIN CREEE")
            #Formattage de la notification
            texte = "Expression de besoin N° {0} initiée par {1} en date du {2}".format(instance.numero_expression, instance.demandeur.nom_complet, instance.date_expression)
            #Création occurrence Notification
            
            notif = Model_Notification.objects.create(module_source = "MODULE_ACHAT",text=texte,created_at = timezone.now(), expression = instance)
            role_name=""
            role_users = None
            #Message envoyé à la personne qui a fait la demande
            Model_Temp_Notification.objects.create(user_id=instance.demandeur.id, type_action = 'Link', lien_action = "module_achat_detail_expression", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            #conservation mail
            if instance.demandeur.email != "" and instance.demandeur.email != None:
                recipient_list.append(instance.demandeur.email)

            # si auteur different de la personne qui demande
            if instance.auteur != None:
                if instance.auteur_id != instance.demandeur.id:
                    Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_achat_detail_expression", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if instance.auteur.email != "" and instance.auteur.email != None:
                        recipient_list.append(instance.auteur.email)
                

            '''responsable_service_id = instance.demandeur.unite_fonctionnelle.responsable_id
            find = False
            Model_Temp_Notification.objects.create(user_id=responsable_service_id, type_action = 'Link', lien_action = "module_achat_detail_expression", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())'''

            #Envoi au responsable du service selon le role dans chaque service
            # Cas RH
            '''if instance.demandeur.unite_fonctionnelle.libelle == "Ressources Humaines":
                role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de service RH")'''
            # Envoi au supérieur hierarchique de la personne qui fait la demande
            superieur_hierarchique = instance.demandeur.unite_fonctionnelle.responsable
            Model_Temp_Notification.objects.create(user_id=superieur_hierarchique.id, type_action = 'Link', lien_action = "module_achat_detail_expression", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            if superieur_hierarchique.email != "" and superieur_hierarchique.email != None:
                        recipient_list.append(superieur_hierarchique.email)

            '''if role_users != None:
                for item in role_users:
                    Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_achat_detail_expression", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if item.utilisateur.email != "" and item.utilisateur.email != None:
                        recipient_list.append(item.utilisateur.email)'''
            
            #Envoi des mails au concerné
            send_async_mail('Notification Système ARPCE',texte,recipient_list,False,'Notification Module Achat','')
            recipient_list.clear()
        
        else:
            #On est dans le cas de Mis à jour d'une expression de besoin
            #print("enfoiré tu as compris comment je fonctionne!!!!")
            #print(kwargs)
            role_name=""
            role_users = None
            
            texte = ""
            #Cas Service informatique
            if instance.services_ref.libelle == "Service Informatique":
                #1. Palier 1 : Passage de Créé à Envoyé au service référent
                if instance.etat == "Envoyé au service référent":
                    #Preparation de la notification
                    texte = "L'expression de besoin N° {0} en provenance de {1} vous a été envoyée".format(instance.numero_expression,instance.demandeur.unite_fonctionnelle.libelle)
                    notif = Model_Notification.objects.create(module_source = "MODULE_ACHAT",text=texte,created_at = timezone.now(), expression = instance)
                    #1.1. Cas Service référent is informatique
                    #print("cas Envoyé au service informatique")
                    role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de bureau exploitation SI")
                    for item in role_users:
                        Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_achat_detail_expression", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                        #conservation mail
                        if item.utilisateur.email != "" and item.utilisateur.email != None:
                            recipient_list.append(item.utilisateur.email)
                


                #2. Palier 2: Passage de Envoyé au service référent à Articles livrés/Demande d'achat généré/Livré partiellement
                elif (instance.etat == "Articles livrés") or (instance.etat == "Demande d'achat généré") or (instance.etat == "Livré partiellement") :
                    #Customisation du texte selon le cas
                    if instance.etat == "Articles livrés":
                        texte = "L'expression de besoin N° {0} a été traité avec succès et fait l'objet d'une livraison  d'articles demandés".format(instance.numero_expression)
                    elif instance.etat == "Demande d'achat généré":
                        texte = "L'expression de besoin N° {0} a été traité avec succès et fait l'objet d'une demande d'achat".format(instance.numero_expression)
                    elif instance.etat == "Livré partiellement":
                        texte = "L'expression de besoin N° {0} a été traité et fait l'objet d'une livraison partielle".format(instance.numero_expression)
                    #Preparation de la notification
                    notif = Model_Notification.objects.create(module_source = "MODULE_ACHAT",text=texte,created_at = timezone.now(), expression = instance)
                    #2.1.Envoi à la Personne demanderesse
                    Model_Temp_Notification.objects.create(user_id=instance.demandeur.id, type_action = 'Link', lien_action = "module_achat_detail_expression", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if instance.demandeur.email != "" and instance.demandeur.email != None:
                        recipient_list.append(instance.demandeur.email)
                    # si auteur different de la personne qui demande
                    if instance.auteur != None:
                        if instance.auteur_id != instance.demandeur.id:
                            Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_achat_detail_expression", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                            #conservation mail
                            if instance.auteur.email != "" and instance.auteur.email != None:
                                recipient_list.append(instance.auteur.email)
                    
                    # Envoi au supérieur hierarchique de la personne qui fait la demande
                    superieur_hierarchique = instance.demandeur.unite_fonctionnelle.responsable
                    Model_Temp_Notification.objects.create(user_id=superieur_hierarchique.id, type_action = 'Link', lien_action = "module_achat_detail_expression", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    if superieur_hierarchique.email != "" and superieur_hierarchique.email != None:
                        recipient_list.append(superieur_hierarchique.email)

                elif instance.etat == "Annulé":
                    #print("amamao")
                    texte = "L'expression de besoin N° {0} a été annulé".format(instance.numero_expression)
                    notif = Model_Notification.objects.create(module_source = "MODULE_ACHAT",text=texte,created_at = timezone.now(), expression = instance)
                    Model_Temp_Notification.objects.create(user_id=instance.demandeur.id, type_action = 'Link', lien_action = "module_achat_detail_expression", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if instance.demandeur.email != "" and instance.demandeur.email != None:
                        recipient_list.append(instance.demandeur.email)
                    # si auteur different de la personne qui demande
                    if instance.auteur != None:
                        if instance.auteur_id != instance.demandeur.id:
                            Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_achat_detail_expression", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                            #conservation mail
                            if instance.auteur.email != "" and instance.auteur.email != None:
                                recipient_list.append(instance.auteur.email)
                    
                
            elif instance.services_ref.libelle == "Moyens généraux":
                #1. Palier 1 : Passage de Créé à Envoyé au DAFC
                if instance.etat == "Envoyé au DAFC":
                    #Preparation de la notification
                    texte = "L'expression de besoin N° {0} en provenance de {1} vous a été envoyée pour approbation".format(instance.numero_expression,instance.demandeur.unite_fonctionnelle.libelle)
                    notif = Model_Notification.objects.create(module_source = "MODULE_ACHAT",text=texte,created_at = timezone.now(), expression = instance)
                    #1.1. Cas Service référent is informatique
                    role_users = dao_role.toListRoleUtilisateurByRoleName("Directeur DAFC")
                    for item in role_users:
                        Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_achat_detail_expression", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                        #conservation mail
                        if item.utilisateur.email != "" and item.utilisateur.email != None:
                            recipient_list.append(item.utilisateur.email)
                
                #1. Palier 2 : Passage de Envoyé au DAFC à Approuvé
                elif instance.etat == "Approuvé":
                    #Preparation de la notification
                    texte = "L'expression de besoin N° {0} en provenance de {1} est approuvée et est en attente d'un traitement de votre part".format(instance.numero_expression,instance.demandeur.unite_fonctionnelle.libelle)
                    notif = Model_Notification.objects.create(module_source = "MODULE_ACHAT",text=texte,created_at = timezone.now(), expression = instance)
                    #1.1. Cas Service référent is informatique
                    role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de bureau exploitation MG")
                    for item in role_users:
                        Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_achat_detail_expression", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                        #conservation mail
                        if item.utilisateur.email != "" and item.utilisateur.email != None:
                            recipient_list.append(item.utilisateur.email)

                #2. Palier 3: Passage de Envoyé au service référent à Articles livrés/Demande d'achat généré/Livré partiellement
                elif (instance.etat == "Articles livrés") or (instance.etat == "Demande d'achat généré") or (instance.etat == "Livré partiellement") :
                    #Customisation du texte selon le cas
                    if instance.etat == "Articles livrés":
                        texte = "L'expression de besoin N° {0} a été traité avec succès et fait l'objet d'une livraison  d'articles demandés".format(instance.numero_expression)
                    elif instance.etat == "Demande d'achat généré":
                        texte = "L'expression de besoin N° {0} a été traité avec succès et fait l'objet d'une demande d'achat".format(instance.numero_expression)
                    elif instance.etat == "Livré partiellement":
                        texte = "L'expression de besoin N° {0} a été traité et fait l'objet d'une livraison partielle".format(instance.numero_expression)
                    #Preparation de la notification
                    notif = Model_Notification.objects.create(module_source = "MODULE_ACHAT",text=texte,created_at = timezone.now(), expression = instance)
                    #2.1.Envoi à la Personne demanderesse
                    Model_Temp_Notification.objects.create(user_id=instance.demandeur.id, type_action = 'Link', lien_action = "module_achat_detail_expression", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if instance.demandeur.email != "" and instance.demandeur.email != None:
                        recipient_list.append(instance.demandeur.email)
                    # si auteur different de la personne qui demande
                    if instance.auteur != None:
                        if instance.auteur_id != instance.demandeur.id:
                            Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_achat_detail_expression", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                            #conservation mail
                            if instance.auteur.email != "" and instance.auteur.email != None:
                                recipient_list.append(instance.auteur.email)
                    
                    # Envoi au supérieur hierarchique de la personne qui fait la demande
                    superieur_hierarchique = instance.demandeur.unite_fonctionnelle.responsable
                    Model_Temp_Notification.objects.create(user_id=superieur_hierarchique.id, type_action = 'Link', lien_action = "module_achat_detail_expression", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    if superieur_hierarchique.email != "" and superieur_hierarchique.email != None:
                        recipient_list.append(superieur_hierarchique.email)

                elif instance.etat == "Annulé":
                    #print("amamao")
                    texte = "L'expression de besoin N° {0} a été annulé".format(instance.numero_expression)
                    notif = Model_Notification.objects.create(module_source = "MODULE_ACHAT",text=texte,created_at = timezone.now(), expression = instance)
                    Model_Temp_Notification.objects.create(user_id=instance.demandeur.id, type_action = 'Link', lien_action = "module_achat_detail_expression", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if instance.demandeur.email != "" and instance.demandeur.email != None:
                        recipient_list.append(instance.demandeur.email)
                    # si auteur different de la personne qui demande
                    if instance.auteur != None:
                        if instance.auteur_id != instance.demandeur.id:
                            Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_achat_detail_expression", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                            #conservation mail
                            if instance.auteur.email != "" and instance.auteur.email != None:
                                recipient_list.append(instance.auteur.email)


            elif instance.services_ref.libelle == "Ressources Humaines":
                #1. Palier 1 : Passage de Créé à Envoyé au DAFC
                if instance.etat == "Envoyé au DAFC":
                    #Preparation de la notification
                    texte = "L'expression de besoin N° {0} en provenance de {1} vous a été envoyée pour approbation".format(instance.numero_expression,instance.demandeur.unite_fonctionnelle.libelle)
                    notif = Model_Notification.objects.create(module_source = "MODULE_ACHAT",text=texte,created_at = timezone.now(), expression = instance)
                    #1.1. Cas Service référent is informatique
                    role_users = dao_role.toListRoleUtilisateurByRoleName("Directeur DAFC")
                    for item in role_users:
                        Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_achat_detail_expression", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                        #conservation mail
                        if item.utilisateur.email != "" and item.utilisateur.email != None:
                            recipient_list.append(item.utilisateur.email)
                
                #1. Palier 2 : Passage de Envoyé au DAFC à Approuvé
                elif instance.etat == "Approuvé":
                    #Preparation de la notification
                    texte = "L'expression de besoin N° {0} en provenance de {1} est approuvée et est en attente d'un traitement de votre part".format(instance.numero_expression,instance.demandeur.unite_fonctionnelle.libelle)
                    notif = Model_Notification.objects.create(module_source = "MODULE_ACHAT",text=texte,created_at = timezone.now(), expression = instance)
                    #1.1. Cas Service référent is informatique
                    role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de bureau exploitation RH")
                    for item in role_users:
                        Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_achat_detail_expression", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                        #conservation mail
                        if item.utilisateur.email != "" and item.utilisateur.email != None:
                            recipient_list.append(item.utilisateur.email)

                #2. Palier 3: Passage de Envoyé au service référent à Articles livrés/Demande d'achat généré/Livré partiellement
                elif (instance.etat == "Demande d'achat généré") :
                    #Customisation du texte selon le cas
                    if instance.etat == "Demande d'achat généré":
                        texte = "L'expression de besoin N° {0} a été traité avec succès et fait l'objet d'une demande d'achat".format(instance.numero_expression)
                    #Preparation de la notification
                    notif = Model_Notification.objects.create(module_source = "MODULE_ACHAT",text=texte,created_at = timezone.now(), expression = instance)
                    #2.1.Envoi à la Personne demanderesse
                    Model_Temp_Notification.objects.create(user_id=instance.demandeur.id, type_action = 'Link', lien_action = "module_achat_detail_expression", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if instance.demandeur.email != "" and instance.demandeur.email != None:
                        recipient_list.append(instance.demandeur.email)
                    # si auteur different de la personne qui demande
                    if instance.auteur != None:
                        if instance.auteur_id != instance.demandeur.id:
                            Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_achat_detail_expression", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                            #conservation mail
                            if instance.auteur.email != "" and instance.auteur.email != None:
                                recipient_list.append(instance.auteur.email)
                    
                    # Envoi au supérieur hierarchique de la personne qui fait la demande
                    superieur_hierarchique = instance.demandeur.unite_fonctionnelle.responsable
                    Model_Temp_Notification.objects.create(user_id=superieur_hierarchique.id, type_action = 'Link', lien_action = "module_achat_detail_expression", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    if superieur_hierarchique.email != "" and superieur_hierarchique.email != None:
                        recipient_list.append(superieur_hierarchique.email)

                elif instance.etat == "Annulé":
                    #print("amamao")
                    texte = "L'expression de besoin N° {0} a été annulé".format(instance.numero_expression)
                    notif = Model_Notification.objects.create(module_source = "MODULE_ACHAT",text=texte,created_at = timezone.now(), expression = instance)
                    Model_Temp_Notification.objects.create(user_id=instance.demandeur.id, type_action = 'Link', lien_action = "module_achat_detail_expression", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if instance.demandeur.email != "" and instance.demandeur.email != None:
                        recipient_list.append(instance.demandeur.email)
                    # si auteur different de la personne qui demande
                    if instance.auteur != None:
                        if instance.auteur_id != instance.demandeur.id:
                            Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_achat_detail_expression", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                            #conservation mail
                            if instance.auteur.email != "" and instance.auteur.email != None:
                                recipient_list.append(instance.auteur.email)
            
            

            #Envoi des mails au concerné
            send_async_mail('Notification Système ARPCE',texte,recipient_list,False,'Notification Module Achat','')
    except Exception as e:
        #print("Erreur",e)
#Connection avec le Model
post_save.connect(signal_expression_besoin,sender=Model_Expression)



def signal_demande_achat(sender,instance,created,**kwargs):
    try:
        recipient_list = []
        texte = ""
        if created:
            #print("NOTIFICATION DEMANDE ACHAT CREEE")
            #Formattage de la notification
            texte = "Demande d'achat N° {0} initiée par {1} en date du {2}".format(instance.numero_demande, instance.auteur.nom_complet, instance.date_demande)
            #Création occurrence Notification
            
            notif = Model_Notification.objects.create(module_source = "MODULE_ACHAT",text=texte,created_at = timezone.now(), demande = instance)
            role_name=""
            role_users = None
            #Message envoyé à la personne qui a fait la demande
            #Model_Temp_Notification.objects.create(user_id=instance.demandeur.id, type_action = 'Link', lien_action = "module_achat_detail_demande_achat", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            # SI LE DEMANDEUR DOIT ETRE NOTIFIE

            #Envoi à l'auteur de la demande
            if instance.auteur != None:
                #if instance.auteur_id != instance.demandeur.id:
                Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_achat_detail_demande_achat", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                #conservation mail
                if instance.auteur.email != "" and instance.auteur.email != None:
                    recipient_list.append(instance.auteur.email)

            '''responsable_service_id = instance.demandeur.unite_fonctionnelle.responsable_id
            find = False
            Model_Temp_Notification.objects.create(user_id=responsable_service_id, type_action = 'Link', lien_action = "module_achat_detail_demande_achat", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())'''

            #Envoi au Chef de service du service référent pour Validation
            # Cas SI
            #print("kjkjkj")
            role_users = None
            if instance.services_ref.libelle == "Service Informatique":
                role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de service SI")
            # Cas ... Le reste des services put here
            elif instance.services_ref.libelle == "Moyens généraux":
                role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de service MG")
            elif instance.services_ref.libelle == "Ressources Humaines":
                role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de service RH")
            

            #print("passed")
            #print(role_users)
            

            if role_users != None:
                for item in role_users:
                    Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_achat_detail_demande_achat", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail*
                    if item.utilisateur.email != "" and item.utilisateur.email != None:
                        recipient_list.append(item.utilisateur.email)
            
            #print("Notification sent")
            #Envoi des mails au concerné
            send_async_mail('Notification Système ARPCE',texte,recipient_list,False,'Notification Module Achat','')
            recipient_list.clear()
        
        else:
            role_name=""
            role_users = None
            
            #1. Palier 1 : Passage de Créé à Validée
            if instance.etat == "Validée":
                #Preparation de la notification
                texte = "La demande d'achat N° {0} en provenance de {1} vous a été envoyée pour validation".format(instance.numero_demande,instance.demandeur.unite_fonctionnelle.libelle)
                notif = Model_Notification.objects.create(module_source = "MODULE_ACHAT",text=texte,created_at = timezone.now(), demande = instance)
                #Envoi aux personnes disposant du role S B A
                role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de service SBA")
                for item in role_users:
                    Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_achat_detail_demande_achat", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if item.utilisateur.email != "" and item.utilisateur.email != None:
                        recipient_list.append(item.utilisateur.email)
                    
            
            #2. Palier 2: Passage de Validée à Envoyé au au bureau achat
            elif instance.etat == "Envoyé au Bureau Achats":
                #Preparation de la notification
                texte = "La demande d'achat N° {0} vous a été envoyée pour traitement".format(instance.numero_demande)
                notif = Model_Notification.objects.create(module_source = "MODULE_ACHAT",text=texte,created_at = timezone.now(), demande = instance)
                #Envoi aux personnes disposant du role Assistant S B A
                role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de bureau Achat")
                for item in role_users:
                    Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_achat_detail_demande_achat", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if item.utilisateur.email != "" and item.utilisateur.email != None:
                        recipient_list.append(item.utilisateur.email)
            
            #2. Palier 2: Passage de Validée à Envoyé au au bureau Marché Public
            elif instance.etat == "Envoyé au CGMP":
                #Preparation de la notification
                texte = "La demande d'achat N° {0} vous a été envoyée pour traitement".format(instance.numero_demande)
                notif = Model_Notification.objects.create(module_source = "MODULE_ACHAT",text=texte,created_at = timezone.now(), demande = instance)
                #Envoi aux personnes disposant du role Assistant S B A
                role_users = dao_role.toListRoleUtilisateurByRoleName("Assistant CGMP")
                for item in role_users:
                    Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_achat_detail_demande_achat", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if item.utilisateur.email != "" and item.utilisateur.email != None:
                        recipient_list.append(item.utilisateur.email)
            
            #2. Palier 2: Passage de Marché Public à Avis d'appel d'offre créé
            elif instance.etat == "Avis d'appel d'offre créé":
                #Preparation de la notification
                texte = "La demande d'achat N° {0} a fait l'objet d'un avis d'appel d'offre".format(instance.numero_demande)
                notif = Model_Notification.objects.create(module_source = "MODULE_ACHAT",text=texte,created_at = timezone.now(), demande = instance)
                #2.1.Envoi à la Personne demanderesse
                #Model_Temp_Notification.objects.create(user_id=instance.demandeur.id, type_action = 'Link', lien_action = "module_achat_detail_demande_achat", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                # si auteur different de la personne qui demande
                if instance.auteur != None:
                    #if instance.auteur_id != instance.demandeur.id:
                    Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_achat_detail_demande_achat", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if instance.auteur.email != "" and instance.auteur.email != None:
                        recipient_list.append(instance.auteur.email)
            
            #2. Palier 2: Passage de Validée à Envoyé au au bureau achat
            elif instance.etat == "Dossier complété":
                #Preparation de la notification
                texte = "La demande d'achat N° {0} vous a été envoyée pour approbation".format(instance.numero_demande)
                notif = Model_Notification.objects.create(module_source = "MODULE_ACHAT",text=texte,created_at = timezone.now(), demande = instance)
                #Envoi aux personnes disposant du role Assistant S B A
                role_users = dao_role.toListRoleUtilisateurByRoleName("Directeur DAFC")
                for item in role_users:
                    Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_achat_detail_demande_achat", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if item.utilisateur.email != "" and item.utilisateur.email != None:
                        recipient_list.append(item.utilisateur.email)
            


            #2. Palier 2: Passage de Validée à Approuvée
            elif instance.etat == "Approuvée":
                #Preparation de la notification
                texte = "La demande d'achat N° {0} est en attente de la génération d'un bon de commande".format(instance.numero_demande)
                notif = Model_Notification.objects.create(module_source = "MODULE_ACHAT",text=texte,created_at = timezone.now(), demande = instance)
                #Envoi aux personnes disposant du role Assistant S B A
                role_users = dao_role.toListRoleUtilisateurByRoleName("Assistant SBA")
                for item in role_users:
                    Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_achat_detail_demande_achat", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if item.utilisateur.email != "" and item.utilisateur.email != None:
                        recipient_list.append(item.utilisateur.email)


            elif (instance.etat == "Bon de commande généré") or (instance.etat == "Traitée"):
                #Customisation du texte selon le cas
                if instance.etat == "Bon de commande généré":
                    texte = "La demande d'achat N° {0} a été traitée avec succès et fait l'objet d'un bon de commande".format(instance.numero_demande)
                elif instance.etat == "Traitée":
                    texte = "La demande d'achat N° {0} a été intégralement traitée avec succès".format(instance.numero_demande)
                #Preparation de la notification
                notif = Model_Notification.objects.create(module_source = "MODULE_ACHAT",text=texte,created_at = timezone.now(), demande = instance)
                #2.1.Envoi à la Personne demanderesse
                #Model_Temp_Notification.objects.create(user_id=instance.demandeur.id, type_action = 'Link', lien_action = "module_achat_detail_demande_achat", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                # si auteur different de la personne qui demande
                if instance.auteur != None:
                    #if instance.auteur_id != instance.demandeur.id:
                    Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_achat_detail_demande_achat", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if instance.auteur.email != "" and instance.auteur.email != None:
                        recipient_list.append(instance.auteur.email)

                #2.2.Envoi à son superieur
                #Cas SI : Chef de Service Informatique 
                if instance.services_ref.libelle == "Service Informatique": 
                    role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de service SI")
                
                # Cas ... Le reste des services put here

                if role_users != None:
                    for item in role_users:
                        Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_achat_detail_demande_achat", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                        #conservation mail
                        if item.utilisateur.email != "" and item.utilisateur.email != None:
                            recipient_list.append(item.utilisateur.email)
            
            elif instance.etat == "Annulée":
                texte = "La demande d'achat N° {0} a été annulée".format(instance.numero_demande)
                notif = Model_Notification.objects.create(module_source = "MODULE_ACHAT",text=texte,created_at = timezone.now(), demande = instance)
                #Envoi à la personne ayant effectué la demande
                #Envoi à l'auteur de la demande
                if instance.auteur != None:
                    #if instance.auteur_id != instance.demandeur.id:
                    Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_achat_detail_demande_achat", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if instance.auteur.email != "" and instance.auteur.email != None:
                        recipient_list.append(instance.auteur.email)
            
            #Envoi des mails au concerné
            send_async_mail('Notification Système ARPCE',texte,recipient_list,False,'Notification Module Achat','')
            recipient_list.clear()
    except Exception as e:
        #print("Erreur",e)
            
#Connection avec le Model
post_save.connect(signal_demande_achat,sender=Model_Demande_achat)


def signal_bon_commande(sender,instance,created,**kwargs):
    try:
        recipient_list = []
        texte = ""
        if created:
            #print("NOTIFICATION BOON DE COMMANDE CREEE")
            #Formattage de la notification
            texte = "Le bon de commande N° {0} est validé et est en attente d'une confirmation de la disponibilité de la ligne budgetaire".format(instance.numero_reception)
            #texte = "Bon de commande N° {0} concernant {1} établi date du {2}".format(instance.numero_reception, instance.fournisseur.nom_complet, instance.date_prevue)
            #Création occurrence Notification
            
            notif = Model_Notification.objects.create(module_source = "MODULE_ACHAT",text=texte,created_at = timezone.now(), bon_reception = instance)
            role_name=""
            role_users = None
            #Message envoyé à la personne qui a créé le bon
            Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_achat_detail_bon_reception", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            if instance.auteur != None:
                Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_achat_detail_bon_reception", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                #conservation mail
                if instance.auteur.email != "" and instance.auteur.email != None:
                    recipient_list.append(instance.auteur.email)
                

            '''responsable_service_id = instance.demandeur.unite_fonctionnelle.responsable_id
            find = False
            Model_Temp_Notification.objects.create(user_id=responsable_service_id, type_action = 'Link', lien_action = "module_achat_detail_bon_reception", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())'''

            #Envoi au Chef de service du SBA
            role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de bureau Budget")
            if role_users != None:
                for item in role_users:
                    Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_achat_detail_bon_reception", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if item.utilisateur.email != "" and item.utilisateur.email != None:
                        recipient_list.append(item.utilisateur.email)
            
            #Envoi des mails au concerné
            send_async_mail('Notification Système ARPCE',texte,recipient_list,False,'Notification Module Achat','')
            recipient_list.clear()
                    
        
        else:
            role_name=""
            role_users = None
            
            #1. Palier 1 : Passage de Créé à Validée ou de validé à Bon signé téléchargé 
            if (instance.etat == "Validé") :#or (instance.etat == "Bon signé téléchargé") or (instance.etat == "Envoyé au service courrier") or (instance.etat == "Accusé de reception téléchargé"):
                #Preparation de la notification
                texte = "Le bon de commande N° {0} est validé et est en attente d'une confirmation de la disponibilité de la ligne budgetaire".format(instance.numero_reception)
                '''if instance.etat == "Validé":
                    texte = "Le bon de commande N° {0} est validé et est en attente de la jointe d'un bon de commande signé".format(instance.numero_reception)
                elif instance.etat == "Bon signé téléchargé":
                    texte = "Le bon de commande signé N° {0} a été téléchargé avec succès et est en attente d'une transmission".format(instance.numero_reception)
                elif instance.etat == "Envoyé au service courrier":
                    texte = "Le bon de commande N° {0} est envoyé avec succès au service courrier et est en attente de la jointe d'une accusé de reception".format(instance.numero_reception)
                elif instance.etat == "Accusé de reception téléchargé":
                    texte = "Le bon de commande signé N° {0} fait l'objet d'une livraison d'articles".format(instance.numero_reception)'''

                notif = Model_Notification.objects.create(module_source = "MODULE_ACHAT",text=texte,created_at = timezone.now(), bon_reception = instance)
                #Envoi aux personnes disposant du role Assistant S B A
                role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de bureau Budget")
                for item in role_users:
                    Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_achat_detail_bon_reception", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if item.utilisateur.email != "" and item.utilisateur.email != None:
                        recipient_list.append(item.utilisateur.email)

            
            #1. Palier 1 : Passage de Créé à Validée ou de validé à Bon signé téléchargé 
            if (instance.etat == "Confirmé la disponibilité de la ligne budgétaire") :#or (instance.etat == "Bon signé téléchargé") or (instance.etat == "Envoyé au service courrier") or (instance.etat == "Accusé de reception téléchargé"):
                #Preparation de la notification
                texte = "Le bon de commande N° {0} est confirmé et est en attente d'une approbation de votre part".format(instance.numero_reception)
                notif = Model_Notification.objects.create(module_source = "MODULE_ACHAT",text=texte,created_at = timezone.now(), bon_reception = instance)
                #Envoi aux personnes disposant du role Assistant S B A
                role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de service SBA")
                for item in role_users:
                    Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_achat_detail_bon_reception", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if item.utilisateur.email != "" and item.utilisateur.email != None:
                        recipient_list.append(item.utilisateur.email)
            
            #1. Palier 1 : Passage de Créé à Validée ou de validé à Bon signé téléchargé 
            if (instance.etat == "Approuvé") :#or (instance.etat == "Bon signé téléchargé") or (instance.etat == "Envoyé au service courrier") or (instance.etat == "Accusé de reception téléchargé"):
                #Preparation de la notification
                texte = "Le bon de commande N° {0} est approuvé et est en attente d'un traitement de votre part".format(instance.numero_reception)
                notif = Model_Notification.objects.create(module_source = "MODULE_ACHAT",text=texte,created_at = timezone.now(), bon_reception = instance)
                #Envoi aux personnes disposant du role Assistant S B A
                role_users = dao_role.toListRoleUtilisateurByRoleName("Assistant SBA")
                for item in role_users:
                    Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_achat_detail_bon_reception", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if item.utilisateur.email != "" and item.utilisateur.email != None:
                        recipient_list.append(item.utilisateur.email)
            
            
            #Notification au comptable
            if (instance.etat=="Articles récus"):
                texte = "Le bon de commande N° {0} est en attente de la création d'une facture".format(instance.numero_reception)
                notif = Model_Notification.objects.create(module_source = "MODULE_ACHAT",text=texte,created_at = timezone.now(), bon_reception = instance)
                #Envoi aux personnes disposant du role Assistant S B A
                role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de service SCT")
                for item in role_users:
                    Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_achat_detail_bon_reception", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if item.utilisateur.email != "" and item.utilisateur.email != None:
                        recipient_list.append(item.utilisateur.email)

            #Envoi des mails au concerné
            send_async_mail('Notification Système ARPCE',texte,recipient_list,False,'Notification Module Achat','')
            recipient_list.clear()
    except Exception as e:
        #print("Erreur",e)
            
#Connection avec le Model
post_save.connect(signal_bon_commande,sender=Model_Bon_reception)



def signal_bon_entree_depot(sender,instance,created,**kwargs):
    try:
        recipient_list = []
        texte = ""
        if created:
            #print("NOTIFICATION BON D'ENTREE DEPOT")
            #Formattage de la notification
            texte = "Bon d'entrée en dépôt  N° {0} enregistré en date du {1}".format(instance.numero,instance.creation_date)
            #Création occurrence Notification
            
            notif = Model_Notification.objects.create(module_source = "MODULE_INVENTAIRE",text=texte,created_at = timezone.now(), bon = instance)
            role_name=""
            role_users = None
            #Message envoyé à la personne qui a enregistré le transfert
            Model_Temp_Notification.objects.create(user_id=instance.inventoriste_id, type_action = 'Link', lien_action = "module_inventaire_details_bons_entrees", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            # si auteur different de la personne qui crée le bon
            #print("Lolo")
            if instance.auteur != None:
                if instance.auteur_id != instance.inventoriste_id:
                    Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_inventaire_details_bons_entrees", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if instance.auteur.email != "" and instance.auteur.email != None:
                        recipient_list.append(instance.auteur.email)
                    
                

            '''responsable_service_id = instance.demandeur.unite_fonctionnelle.responsable_id
            find = False
            Model_Temp_Notification.objects.create(user_id=responsable_service_id, type_action = 'Link', lien_action = "module_inventaire_details_bons_entrees", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())'''

            #Envoi au Chef de service du SBA
            role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de service SBA")
            if role_users != None:
                for item in role_users:
                    Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_inventaire_details_bons_entrees", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if item.utilisateur.email != "" and item.utilisateur.email != None:
                        recipient_list.append(item.utilisateur.email)
            
            #Envoi des mails au concerné
            send_async_mail('Notification Système ARPCE',texte,recipient_list,False,'Notification Module Inventaire','')
            recipient_list.clear()
        
        else:
            role_name=""
            role_users = None
            
            texte = ""
            #1. Palier 1 : Passage de Créé à Télechargé le bon de livraison
            #PASS
            #2. Palier 2 : Passage de Télécharger à valider
            if instance.etat == "Bon de livraison téléchargé":
                #Preparation de la notification
                texte = "Le Bon d'entrée en dépôt  N° {0} enregistré en date du {1} est an attente de validation".format(instance.numero,instance.creation_date)
                notif = Model_Notification.objects.create(module_source = "MODULE_INVENTAIRE",text=texte,created_at = timezone.now(), bon = instance)
                role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de service SBA")
                for item in role_users:
                    Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_inventaire_details_bons_entrees", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if item.utilisateur.email != "" and item.utilisateur.email != None:
                        recipient_list.append(item.utilisateur.email)
            
                    #2. Palier 2 : Passage de Télécharger à valider
                
            elif instance.etat == "Envoyé au SMG":
                #Preparation de la notification
                texte = "Le Bon d'entrée en dépôt  N° {0} enregistré en date du {1} est an attente d'un traitement de votre part".format(instance.numero,instance.creation_date)
                notif = Model_Notification.objects.create(module_source = "MODULE_INVENTAIRE",text=texte,created_at = timezone.now(), bon = instance)
                role_users = dao_role.toListRoleUtilisateurByRoleName("Assistant MG")
                for item in role_users:
                    Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_inventaire_details_bons_entrees", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if item.utilisateur.email != "" and item.utilisateur.email != None:
                        recipient_list.append(item.utilisateur.email)
    except Exception as e:
        #print("Erreur",e)
    
           
#Connection avec le Model
post_save.connect(signal_bon_entree_depot,sender=Model_Bon)


def signal_bon_transfert(sender,instance,created,**kwargs):
    try:
        recipient_list = []
        texte = ""
        if created:
            #print("NOTIFICATION BOON TRANSFERT CREEE")
            #Formattage de la notification

            #Cas 1: Bon de sortie de matériel

            if instance.operation_stock.designation == "Affectation interne":

                texte = "Bon de sortie de materiel N° {0} en faveur de {1} établi en date du {2}".format(instance.numero_transfert, instance.employe.nom_complet, instance.date_transfert)
                notif = Model_Notification.objects.create(module_source = "MODULE_INVENTAIRE",text=texte,created_at = timezone.now(), bon_transfert = instance)
                role_name = ""
                role_users = None
                #Message envoyé à la personne initiant l'opération
                Model_Temp_Notification.objects.create(user_id=instance.employe_id, type_action = 'Link', lien_action = "module_inventaire_details_transfert_internal", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                #conservation mail
                if instance.employe.email != "" and instance.employe.email != None:
                    recipient_list.append(instance.employe.email)
                # si auteur different de la personne qui crée le bon
                #print("Lolo")
                if instance.auteur != None:
                    if instance.auteur_id != instance.employe_id:
                        Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_inventaire_details_transfert_internal", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                        #conservation mail
                        if instance.auteur.email != "" and instance.auteur.email != None:
                            recipient_list.append(instance.auteur.email)
                    
                
                #Envoi au personne disposant du role de "Chef de bureau d'exploitation"
                role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de bureau exploitation SI")
                if role_users != None:
                    for item in role_users:
                        Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_inventaire_details_transfert_internal", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                        #conservation mail
                    if item.utilisateur.email != "" and item.utilisateur.email != None:
                        recipient_list.append(item.utilisateur.email)
                        
            
            elif instance.operation_stock.designation == "Transfert d'articles":

                texte = "Bon de transmission N° {0} établi en date du {1}".format(instance.numero_transfert, instance.date_transfert)
                notif = Model_Notification.objects.create(module_source = "MODULE_INVENTAIRE",text=texte,created_at = timezone.now(), bon_transfert = instance)
                role_name = ""
                role_users = None
                #Message envoyé à la personne initiant l'opération
                Model_Temp_Notification.objects.create(user_id=instance.employe_id, type_action = 'Link', lien_action = "module_inventaire_detail_bon_transfert", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                #conservation mail
                if instance.employe.email != "" and instance.employe.email != None:
                    recipient_list.append(instance.employe.email)
                # si auteur different de la personne qui crée le bon
                #print("Lolo")
                if instance.auteur != None:
                    if instance.auteur_id != instance.employe_id:
                        Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_inventaire_detail_bon_transfert", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                        #conservation mail
                        if instance.auteur.email != "" and instance.auteur.email != None:
                            recipient_list.append(instance.auteur.email)
                    
                
                #Envoi au personne disposant du role de "Chef de service SBA"
                role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de service MG")
                if role_users != None:
                    for item in role_users:
                        Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_inventaire_detail_bon_transfert", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                        #conservation mail
                        if item.utilisateur.email != "" and item.utilisateur.email != None:
                            recipient_list.append(item.utilisateur.email)
                
            #Envoi des mails au concerné
            send_async_mail('Notification Système ARPCE',texte,recipient_list,False,'Notification Module Inventaire','')
            recipient_list.clear()       

    
        
        else:
            if instance.operation_stock.designation == "Affectation interne":
                role_name=""
                role_users = None
                
                #1. Palier 1 : Passage de Créé à Ordonné
                if instance.etat == "Créée" :
                    #Preparation de la notification
                    texte = "Le bon de sortie de materiel N° {0} est en attente d'une validation (Ordre)".format(instance.numero_transfert)
                    notif = Model_Notification.objects.create(module_source = "MODULE_INVENTAIRE",text=texte,created_at = timezone.now(), bon_transfert = instance)
                    #Envoi aux personnes disposant du role Chef de bureaux d'exploitation
                    if instance.emplacement_origine.designation == "Stockage IT":
                        role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de bureau exploitation SI")
                        for item in role_users:
                            Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_inventaire_details_transfert_internal", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                            #conservation mail
                            if item.utilisateur.email != "" and item.utilisateur.email != None:
                                recipient_list.append(item.utilisateur.email)
                    
                    elif instance.emplacement_origine.designation == "Stockage Moyens généraux":
                        role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de bureau exploitation MG")
                        for item in role_users:
                            Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_inventaire_details_transfert_internal", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                            #conservation mail
                            if item.utilisateur.email != "" and item.utilisateur.email != None:
                                recipient_list.append(item.utilisateur.email)
                    
                #1. Palier 2 : Passage de  Ordonnée à Autorisée
                elif instance.etat == "Ordonnée" :
                    #Preparation de la notification
                    texte = "Le bon de sortie de materiel N° {0} est en attente d'une autorisation de votre part".format(instance.numero_transfert)
                    notif = Model_Notification.objects.create(module_source = "MODULE_INVENTAIRE",text=texte,created_at = timezone.now(), bon_transfert = instance)
                    #Envoi aux personnes disposant du role Chef de bureaux d'exploitation
                    if instance.emplacement_origine.designation == "Stockage IT":
                        role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de service SI")
                        for item in role_users:
                            Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_inventaire_details_transfert_internal", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                            #conservation mail
                            if item.utilisateur.email != "" and item.utilisateur.email != None:
                                recipient_list.append(item.utilisateur.email)
                    if instance.emplacement_origine.designation == "Stockage Moyens généraux":
                        role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de service MG")
                        for item in role_users:
                            Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_inventaire_details_transfert_internal", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                            #conservation mail
                            if item.utilisateur.email != "" and item.utilisateur.email != None:
                                recipient_list.append(item.utilisateur.email)
                
                #1. Palier 3 : Passage de  Ordonnée à Autorisée
                elif instance.etat == "Autorisée" :
                    #Preparation de la notification
                    texte = "Le bon de sortie de materiel N° {0} est en attente d'un traitement de votre part".format(instance.numero_transfert)
                    notif = Model_Notification.objects.create(module_source = "MODULE_INVENTAIRE",text=texte,created_at = timezone.now(), bon_transfert = instance)
                    #Envoi aux personnes disposant du role S B A
                    if instance.emplacement_origine.designation == "Stockage IT":
                        role_users = dao_role.toListRoleUtilisateurByRoleName("Support Informatique")
                        for item in role_users:
                            Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_inventaire_details_transfert_internal", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                            #conservation mail
                            if item.utilisateur.email != "" and item.utilisateur.email != None:
                                recipient_list.append(item.utilisateur.email)
                    if instance.emplacement_origine.designation == "Stockage Moyens généraux":
                        role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de bureau exploitation MG")
                        for item in role_users:
                            Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_inventaire_details_transfert_internal", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                            #conservation mail
                            if item.utilisateur.email != "" and item.utilisateur.email != None:
                                recipient_list.append(item.utilisateur.email)
                
                #1. Palier 3 : Passage de  Ordonnée à Autorisée
                elif instance.etat == "Traitée" :
                    #Preparation de la notification
                    texte = "Le bon de sortie de materiel N° {0} est effectué avec succès et est en attente d'une finalisation effective".format(instance.numero_transfert)
                    notif = Model_Notification.objects.create(module_source = "MODULE_INVENTAIRE",text=texte,created_at = timezone.now(), bon_transfert = instance)
                    #Envoi à l'agent asigné par le support It
                    Model_Temp_Notification.objects.create(user_id=instance.agent_id, type_action = 'Link', lien_action = "module_inventaire_details_transfert_internal", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    #print("in mail")
                    #print(instance.agent_email)
                    if instance.agent.email != "" and instance.agent.email != None:
                        recipient_list.append(instance.agent.email)
                    #Message envoyé à la personne initiant l'opération
                    Model_Temp_Notification.objects.create(user_id=instance.employe_id, type_action = 'Link', lien_action = "module_inventaire_details_transfert_internal", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if instance.employe.email != "" and instance.employe.email != None:
                        recipient_list.append(instance.employe.email)
                    # si auteur different de la personne qui crée le bon
                    #print("Lolo")
                    if instance.auteur != None:
                        if instance.auteur_id != instance.employe_id:
                            Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_inventaire_details_transfert_internal", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                            #conservation mail
                            if instance.auteur.email != "" and instance.auteur.email != None:
                                recipient_list.append(instance.auteur.email)
                
            elif instance.operation_stock.designation == "Transfert d'articles":
                role_users = None

                #1.Palier 1: Passage de créé à envoyé au servic référent
                if instance.etat == "Envoyé au service référent":
                    #Preparation de la notification
                    texte = "Le bon de transmission N° {0} provenant du Service MG vous a été envoyé et en attente d'une vérification".format(instance.numero_transfert)
                    notif = Model_Notification.objects.create(module_source = "MODULE_INVENTAIRE",text=texte,created_at = timezone.now(), bon_transfert = instance)
                    #choix de l'emplacement
                    if instance.emplacement_destination.designation == "Stockage IT":
                        role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de bureau exploitation SI")
                        for item in role_users:
                            Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_inventaire_detail_bon_transfert", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                            #conservation mail
                            if item.utilisateur.email != "" and item.utilisateur.email != None:
                                recipient_list.append(item.utilisateur.email)
                    elif instance.emplacement_destination.designation == "Stockage Moyens généraux":
                        #print("I'm inside the loop")
                        role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de bureau exploitation MG")
                        for item in role_users:
                            Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_inventaire_detail_bon_transfert", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                            #conservation mail
                            if item.utilisateur.email != "" and item.utilisateur.email != None:
                                recipient_list.append(item.utilisateur.email)                    
                    
                
                #2.Palier 2: Passage de nvoyé au service référent à Vérification du matériel livré
                elif instance.etat == "Vérification du matériel livré":
                    #Preparation de la notification
                    texte = "Le bon de transmission N° {0} a fait l'objet d'une vérification et est en attente d'une validation".format(instance.numero_transfert)
                    notif = Model_Notification.objects.create(module_source = "MODULE_INVENTAIRE",text=texte,created_at = timezone.now(), bon_transfert = instance)

                    if instance.emplacement_destination.designation == "Stockage IT":
                        role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de bureau exploitation SI")
                        for item in role_users:
                            Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_inventaire_detail_bon_transfert", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                            #conservation mail
                            if item.utilisateur.email != "" and item.utilisateur.email != None:
                                recipient_list.append(item.utilisateur.email)
                    
                    elif instance.emplacement_destination.designation == "Stockage Moyens généraux":
                        role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de bureau exploitation MG")
                        for item in role_users:
                            Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_inventaire_detail_bon_transfert", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                            #conservation mail
                            if item.utilisateur.email != "" and item.utilisateur.email != None:
                                recipient_list.append(item.utilisateur.email)
                    
                    
                
                #3.Palier : Passage de Vérification du matériel livré à Bon reception créé
                elif instance.etat == "Bon de reception créé":
                    #Preparation de la notification
                    texte = "Le bon de reception relatif au bon de transmission N° {0} a été crée avec succès et est en attente d'une livraison effective. ".format(instance.numero_transfert)
                    notif = Model_Notification.objects.create(module_source = "MODULE_INVENTAIRE",text=texte,created_at = timezone.now(), bon_transfert = instance)
                    #Envoi aux personnes disposant du role Technicien SI
                    if instance.emplacement_destination.designation == "Stockage IT":
                        role_users = dao_role.toListRoleUtilisateurByRoleName("Technicien SI")
                        for item in role_users:
                            Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_inventaire_detail_bon_transfert", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                            #conservation mail
                            if item.utilisateur.email != "" and item.utilisateur.email != None:
                                recipient_list.append(item.utilisateur.email)
                    
                    elif instance.emplacement_destination.designation == "Stockage Moyens généraux":
                        role_users = dao_role.toListRoleUtilisateurByRoleName("Technicien MG")
                        for item in role_users:
                            Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_inventaire_detail_bon_transfert", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                            #conservation mail
                            if item.utilisateur.email != "" and item.utilisateur.email != None:
                                recipient_list.append(item.utilisateur.email)

                #3.Palier : Passage de Vérification du matériel livré à Bon reception créé
                elif instance.etat == "Articles enregistrés":
                    #Preparation de la notification
                    texte = "Les articles relatifs au bon de transmission N° {0} ont été enregistrés avec succès. ".format(instance.numero_transfert)
                    notif = Model_Notification.objects.create(module_source = "MODULE_INVENTAIRE",text=texte,created_at = timezone.now(), bon_transfert = instance)
                    #Envoi à 
                    if instance.emplacement_destination.designation == "Stockage IT":
                        role_users = dao_role.toListRoleUtilisateurByRoleName("Technicien SI")
                    elif instance.emplacement_destination.designation == "Stockage Moyens généraux":
                        role_users = None
                        role_users = dao_role.toListRoleUtilisateurByRoleName("Technicien MG")
                    #Message envoyé à la personne initiant l'opération
                    Model_Temp_Notification.objects.create(user_id=instance.employe_id, type_action = 'Link', lien_action = "module_inventaire_detail_bon_transfert", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if instance.employe.email != "" and instance.employe.email != None:
                        recipient_list.append(instance.employe.email)
                    # si auteur different de la personne qui crée le bon
                    #print("Lolo")

                    if instance.responsable_id != None:
                        Model_Temp_Notification.objects.create(user_id=instance.responsable_id, type_action = 'Link', lien_action = "module_inventaire_detail_bon_transfert", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                        #conservation mail
                        if instance.responsable.email != "" and instance.responsable.email != None:
                            recipient_list.append(instance.responsable.email)
                    if instance.auteur != None:
                        if instance.auteur_id != instance.employe_id:
                            Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_inventaire_detail_bon_transfert", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                            #conservation mail
                            if instance.auteur.email != "" and instance.auteur.email != None:
                                recipient_list.append(instance.auteur.email)
                
            #Envoi des mails au concerné
            send_async_mail('Notification Système ARPCE',texte,recipient_list,False,'Notification Module Inventaire','')
            recipient_list.clear() 
    except Exception as e:
        #print("Erreur",e) 
                
#Connection avec le Model
post_save.connect(signal_bon_transfert,sender=Model_Bon_transfert)


def signal_avis_appel_offre(sender,instance,created,**kwargs):
    try:
        recipient_list = []
        texte = ""
        if created:
            #print("NOTIFICATION AVIS APPEL OFFRE CREEE")
            #Formattage de la notification
            texte = "Avis d'appel d'offre N° {0} concernant {1} établi date du {2}".format(instance.numero_reference, instance.objet_appel, instance.date_signature)
            #Création occurrence Notification
            
            notif = Model_Notification.objects.create(module_source = "MODULE_ACHAT",text=texte,created_at = timezone.now(), avis_appel_offre = instance)
            role_name=""
            role_users = None
            #Message envoyé à la personne qui a créé l'avis
            Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_achat_detail_avis_appel_offre", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            if instance.auteur != None:
                Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_achat_detail_avis_appel_offre", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                #conservation mail
                if instance.auteur.email != "" and instance.auteur.email != None:
                    recipient_list.append(instance.auteur.email)
                

            #Envoi au Responsable CGMP
            role_users = dao_role.toListRoleUtilisateurByRoleName("Responsable CGMP")
            if role_users != None:
                for item in role_users:
                    Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_achat_detail_avis_appel_offre", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if item.utilisateur.email != "" and item.utilisateur.email != None:
                        recipient_list.append(item.utilisateur.email)
            
            #Envoi des mails au concerné
            send_async_mail('Notification Système ARPCE',texte,recipient_list,False,'Notification Module Achat','')
            recipient_list.clear()
                    
        
        else:
            role_name=""
            role_users = None
            
            #1. Palier 1 : Passage de Créé à Validée ou de validé à Bon signé téléchargé 
            if (instance.etat == "Dossier constitué") or (instance.etat == "Validation externe téléchargée") or (instance.etat == "Contrat établi") :
                #Preparation de la notification
                texte = "Le dossier d'appel d'offre N° {0} est en attente d'un traitement de votre part".format(instance.numero_dossier)
                notif = Model_Notification.objects.create(module_source = "MODULE_ACHAT",text=texte,created_at = timezone.now(), avis_appel_offre = instance)
                #Envoi aux personnes disposant du role Assistant S B A
                role_users = dao_role.toListRoleUtilisateurByRoleName("Responsable CGMP")
                for item in role_users:
                    Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_achat_detail_avis_appel_offre", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if item.utilisateur.email != "" and item.utilisateur.email != None:
                        recipient_list.append(item.utilisateur.email)

            
            #1. Palier 1 : Passage de Créé à Validée ou de validé à Bon signé téléchargé 
            if (instance.etat == "DAO Validé") or (instance.etat == "Approuvé pour publication") :
                #Preparation de la notification
                texte = "Le dossier d'appel d'offre N° {0} est en attente d'un traitement de votre part".format(instance.numero_dossier)
                notif = Model_Notification.objects.create(module_source = "MODULE_ACHAT",text=texte,created_at = timezone.now(), avis_appel_offre = instance)
                #Envoi aux personnes disposant du role Assistant S B A
                role_users = dao_role.toListRoleUtilisateurByRoleName("Assistant CGMP")
                for item in role_users:
                    Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_achat_detail_avis_appel_offre", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if item.utilisateur.email != "" and item.utilisateur.email != None:
                        recipient_list.append(item.utilisateur.email)
            
            #Envoi des mails au concerné
            send_async_mail('Notification Système ARPCE',texte,recipient_list,False,'Notification Module Achat','')
            recipient_list.clear()
    except Exception as e:
        #print("Erreur",e)
            
#Connection avec le Model
post_save.connect(signal_avis_appel_offre,sender=Model_Avis_appel_offre)


def signal_demande_conge(sender,instance,created,**kwargs):
    try:
        recipient_list = []
        texte = ""
        if created:
            #print("NOTIFICATION CONGE")
            #Formattage de la notification
            texte = "Votre demande de congé du type {0} allant de {1} à {2}, soit un total de {3} jours a été reçu avec succès".format(instance.histypeconge, instance.date_from, instance.date_to, instance.nombre_jour)
            notif = Model_Notification.objects.create(module_source = "MODULE_RESSOURCES_HUMAINES",text=texte,created_at = timezone.now(), conge = instance)
            role_name=""
            role_users = None
            #Message envoyé à la personne qui a envoyé la demande de congé
            Model_Temp_Notification.objects.create(user_id=instance.employe_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_conge", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            # si auteur different de la personne qui crée le bon
            #print("Lolo")
            if instance.auteur != None:
                if instance.auteur_id != instance.employe_id:
                    Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_conge", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if instance.auteur.email != "" and instance.auteur.email != None:
                        recipient_list.append(instance.auteur.email)
                    
            #Envoi au Chef de service du RH
            role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de service RH")
            if role_users != None:
                for item in role_users:
                    Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_conge", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if item.utilisateur.email != "" and item.utilisateur.email != None:
                        recipient_list.append(item.utilisateur.email)
            
            #Envoi des mails au concerné
            send_async_mail('Notification Système ARPCE',texte,recipient_list,False,'Notification Module Ressources Humaines','')
            recipient_list.clear()
        
        else:
            role_name=""
            role_users = None
            
            texte = ""
            #1. Palier 1 : Passage de Créé à Télechargé le bon de livraison
            #PASS
            #2. Palier 2 : Passage de Télécharger à valider
            if instance.etat == "Demande de congé validée":
                #Preparation de la notification
                texte = "Votre demande de congé du type {0} allant de {1} à {2}, soit un total de {3} jours est validé".format(instance.histypeconge, instance.date_from, instance.date_to, instance.nombre_jour)
                notif = Model_Notification.objects.create(module_source = "MODULE_RESSOURCES_HUMAINES",text=texte,created_at = timezone.now(), conge = instance)
                Model_Temp_Notification.objects.create(user_id=instance.employe_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_conge", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                #conservation mail
                if instance.employe.email != "" and instance.employe.email != None:
                    recipient_list.append(instance.employe.email)
                # si auteur different de la personne qui demande
                if instance.auteur != None:
                    if instance.auteur_id != instance.employe.id:
                        Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_conge", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                        #conservation mail
                        if instance.auteur.email != "" and instance.auteur.email != None:
                            recipient_list.append(instance.auteur.email)
    except Exception as e:
        #print("Erreur",e)
    
           
#Connection avec le Model
post_save.connect(signal_demande_conge,sender=Model_Conge)

#Connection avec le modèle requête
def signal_expression_besoin_mission(sender, instance, created, **kwargs):
    try:
        recipient_list = []
        texte = ""
        if created:
            #print("NOTIFICATION EXPRESSION DE BESOIN DE MISSION")
            #Formattage de la notification
            texte = "Votre expression de besoin pour mission concernant {0} a été reçu avec succès".format(instance.description)
            notif = Model_Notification.objects.create(module_source = "MODULE_RESSOURCES_HUMAINES",text=texte,created_at = timezone.now(), requete = instance)
            role_name=""
            role_users = None
            #Message envoyé à la personne qui a envoyé la demande de congé
            Model_Temp_Notification.objects.create(user_id=instance.demandeur_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_requete", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            # si auteur different de la personne qui crée le bon

            #print("Lolo")
            if instance.auteur != None:
                if instance.auteur_id != instance.demandeur_id:
                    Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_requete", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if instance.auteur.email != "" and instance.auteur.email != None:
                        recipient_list.append(instance.auteur.email)

            # Envoi au supérieur hierarchique de la personne qui fait la demande
            superieur_hierarchique = instance.demandeur.unite_fonctionnelle.responsable
            Model_Temp_Notification.objects.create(user_id=superieur_hierarchique.id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_requete", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            if superieur_hierarchique.email != "" and superieur_hierarchique.email != None:
                recipient_list.append(superieur_hierarchique.email)

            # #Envoi au Chef de service du RH
            # role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de service RH")
            # if role_users != None:
            #     for item in role_users:
            #         Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_requete", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            #         #conservation mail
            #         if item.utilisateur.email != "" and item.utilisateur.email != None:
            #             recipient_list.append(item.utilisateur.email)
            
            #Envoi des mails au concerné
            send_async_mail('Notification Système ARPCE',texte,recipient_list,False,'Notification Module Ressources Humaines','')
            recipient_list.clear()
        else:
            role_name=""
            role_users = None
            
            texte = ""
            #1. Palier 1 : Passage de Créé à Etat de besoin de mission validé
            #PASS
            #2. Palier 2 : Passage de Etat de besoin de mission validé à Approuver
            if instance.etat == "Etat de besoin de mission validé":
                #Preparation de la notification
                texte = "Votre expression de besoin pour mission concernant {0} a été reçu avec succès".format(instance.description)
                notif = Model_Notification.objects.create(module_source = "MODULE_RESSOURCES_HUMAINES",text=texte,created_at = timezone.now(), requete = instance)
                # Model_Temp_Notification.objects.create(user_id=instance.employe_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_requete", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                #conservation mail
                # if instance.demandeur.email != "" and instance.demandeur.email != None:
                #     recipient_list.append(instance.demandeur.email)
                # # si auteur different de la personne qui demande
                # if instance.auteur != None:
                #     if instance.auteur_id != instance.demandeur.id:
                #         Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_conge", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                #         #conservation mail
                #         if instance.auteur.email != "" and instance.auteur.email != None:
                #             recipient_list.append(instance.auteur.email)
                
                #Envoi au Directeur DAFC
                role_users = dao_role.toListRoleUtilisateurByRoleName("Directeur DAFC")
                if role_users != None:
                    for item in role_users:
                        Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_requete", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                        #conservation mail
                        if item.utilisateur.email != "" and item.utilisateur.email != None:
                            recipient_list.append(item.utilisateur.email)
                
                #Envoi des mails au concerné
                # send_async_mail('Notification Système ARPCE',texte,recipient_list,False,'Notification Module Ressources Humaines','')
                # recipient_list.clear()
            
            #3. Palier 3 : Passage de Approuver à valider
            if instance.etat == "Etat de besoin de mission approuvé":
                #Preparation de la notification
                texte = "Votre expression de besoin pour mission concernant {0} a été reçu avec succès".format(instance.description)
                notif = Model_Notification.objects.create(module_source = "MODULE_RESSOURCES_HUMAINES",text=texte,created_at = timezone.now(), requete = instance)
                # Model_Temp_Notification.objects.create(user_id=instance.employe_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_requete", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                #conservation mail
                # if instance.demandeur.email != "" and instance.demandeur.email != None:
                #     recipient_list.append(instance.demandeur.email)
                # # si auteur different de la personne qui demande
                # if instance.auteur != None:
                #     if instance.auteur_id != instance.demandeur.id:
                #         Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_conge", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                #         #conservation mail
                #         if instance.auteur.email != "" and instance.auteur.email != None:
                #             recipient_list.append(instance.auteur.email)
                
                #Envoi au Chef de service RH
                role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de service RH")
                if role_users != None:
                    for item in role_users:
                        Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_requete", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                        #conservation mail
                        if item.utilisateur.email != "" and item.utilisateur.email != None:
                            recipient_list.append(item.utilisateur.email)

            #4. Palier 4 : Passage de Approuver à valider
            if instance.etat == "Instruction de l'ordre de mission":
                #Preparation de la notification
                texte = "Votre expression de besoin pour mission concernant {0} a été reçu avec succès".format(instance.description)
                notif = Model_Notification.objects.create(module_source = "MODULE_RESSOURCES_HUMAINES",text=texte,created_at = timezone.now(), requete = instance)
                # Model_Temp_Notification.objects.create(user_id=instance.employe_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_requete", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                #conservation mail
                # if instance.demandeur.email != "" and instance.demandeur.email != None:
                #     recipient_list.append(instance.demandeur.email)
                # # si auteur different de la personne qui demande
                # if instance.auteur != None:
                #     if instance.auteur_id != instance.demandeur.id:
                #         Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_conge", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                #         #conservation mail
                #         if instance.auteur.email != "" and instance.auteur.email != None:
                #             recipient_list.append(instance.auteur.email)
                
                #Envoi au Chef de service RH
                role_users = dao_role.toListRoleUtilisateurByRoleName("Assistant RH")
                if role_users != None:
                    for item in role_users:
                        Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_requete", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                        #conservation mail
                        if item.utilisateur.email != "" and item.utilisateur.email != None:
                            recipient_list.append(item.utilisateur.email)

            #Envoi des mails au concerné
            send_async_mail('Notification Système ARPCE',texte,recipient_list,False,'Notification Module Ressources Humaines','')
            recipient_list.clear()


            #5. Palier 5 : Passage de Approuver à valider
            # if instance.etat == "Ordre de Mission créé":
            #     #Preparation de la notification
            #     texte = "Votre expression de besoin pour mission concernant {0} a été reçu avec succès".format(instance.description)
            #     notif = Model_Notification.objects.create(module_source = "MODULE_RESSOURCES_HUMAINES",text=texte,created_at = timezone.now(), requete = instance)
            #     # Model_Temp_Notification.objects.create(user_id=instance.employe_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_requete", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            #     #conservation mail
            #     # if instance.demandeur.email != "" and instance.demandeur.email != None:
            #     #     recipient_list.append(instance.demandeur.email)
            #     # # si auteur different de la personne qui demande
            #     # if instance.auteur != None:
            #     #     if instance.auteur_id != instance.demandeur.id:
            #     #         Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_conge", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            #     #         #conservation mail
            #     #         if instance.auteur.email != "" and instance.auteur.email != None:
            #     #             recipient_list.append(instance.auteur.email)
                
            #     #Envoi au Chef de service RH
            #     role_users = dao_role.toListRoleUtilisateurByRoleName("Assistant RH")
            #     if role_users != None:
            #         for item in role_users:
            #             Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_requete", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            #             #conservation mail
            #             if item.utilisateur.email != "" and item.utilisateur.email != None:
            #                 recipient_list.append(item.utilisateur.email)

            #Envoi des mails au concerné
            send_async_mail('Notification Système ARPCE',texte,recipient_list,False,'Notification Module Ressources Humaines','')
            recipient_list.clear()

    except Exception as e:
        #print("Erreur",e)

post_save.connect(signal_expression_besoin_mission,sender=models.Model_Requete)


#Connection avec le modèle ordre de mission
def signal_ordre_de_mission(sender, instance,created, **kwargs):
    try:
        recipient_list = []
        texte = ""
        if created:
            #print("NOTIFICATION ORDRE DE MISSION")
            #Formattage de la notification
            texte = "Votre ordre de mission en date du {} au {} dont l'objet est {} a été reçu avec succès".format(instance.date_depart, instance.date_retour, instance.objet_mission)
            notif = Model_Notification.objects.create(module_source = "MODULE_RESSOURCES_HUMAINES",text=texte,created_at = timezone.now(), mission = instance)
            role_name=""
            role_users = None
            #Message envoyé à la personne qui a envoyé la demande de congé
            Model_Temp_Notification.objects.create(user_id=instance.demandeur_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_ordre_de_mission", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            # si auteur different de la personne qui crée le bon
            #print("Lolo")
            if instance.auteur != None:
                if instance.auteur_id != instance.demandeur_id:
                    Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_ordre_de_mission", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if instance.auteur.email != "" and instance.auteur.email != None:
                        recipient_list.append(instance.auteur.email)

            # Envoi au supérieur hierarchique de la personne qui fait la demande
            # superieur_hierarchique = instance.demandeur.unite_fonctionnelle.responsable
            # Model_Temp_Notification.objects.create(user_id=superieur_hierarchique.id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_ordre_de_mission", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            # if superieur_hierarchique.email != "" and superieur_hierarchique.email != None:
            #             recipient_list.append(superieur_hierarchique.email)

            # #Envoi au Chef de service du RH
            # role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de service RH")
            # if role_users != None:
            #     for item in role_users:
            #         Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_requete", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            #         #conservation mail
            #         if item.utilisateur.email != "" and item.utilisateur.email != None:
            #             recipient_list.append(item.utilisateur.email)
            
            #Envoi des mails au concerné
            send_async_mail('Notification Système ARPCE',texte,recipient_list,False,'Notification Module Ressources Humaines','')
            recipient_list.clear()
        else:
            role_name=""
            role_users = None
            
            texte = ""
            #1. Palier 1 : Passage de Créé à Etat de besoin de mission validé
            #PASS
            # #2. Palier 2 : Passage de Etat de besoin de mission validé à Approuver
            # if instance.etat == "Ordre de Mission signé par le DAFC":
            #     #Preparation de la notification
            #     texte = "Votre ordre de mission concernant du {} au {} a été reçu avec succès".format(instance.date_depart, instance.date_retour)
            #     notif = Model_Notification.objects.create(module_source = "MODULE_RESSOURCES_HUMAINES",text=texte,created_at = timezone.now(), mission = instance)
            #     Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_ordre_de_mission", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            #     #conservation mail
            #     # if instance.demandeur.email != "" and instance.demandeur.email != None:
            #     #     recipient_list.append(instance.demandeur.email)
            #     # # si auteur different de la personne qui demande
            #     # if instance.auteur != None:
            #     #     if instance.auteur_id != instance.demandeur.id:
            #     #         Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_mission", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            #     #         #conservation mail
            #     #         if instance.auteur.email != "" and instance.auteur.email != None:
            #     #             recipient_list.append(instance.auteur.email)
                
            #     #Envoi au Directeur DAFC
            #     role_users = dao_role.toListRoleUtilisateurByRoleName("Assistant RH")
            #     if role_users != None:
            #         for item in role_users:
            #             Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_ordre_de_mission", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            #             #conservation mail
            #             if item.utilisateur.email != "" and item.utilisateur.email != None:
            #                 recipient_list.append(item.utilisateur.email)
                
                #Envoi des mails au concerné
                # send_async_mail('Notification Système ARPCE',texte,recipient_list,False,'Notification Module Ressources Humaines','')
                # recipient_list.clear()
            
            #3. Palier 3 : Passage de Approuver à valider
            if instance.etat == "Ordre de Mission signé par le DAFC et par le DG":
                #Preparation de la notification
                texte = "Votre ordre de mission en date du {} au {} dont l'objet est {} a été reçu avec succès".format(instance.date_depart, instance.date_retour, instance.objet_mission)


                notif = Model_Notification.objects.create(module_source = "MODULE_RESSOURCES_HUMAINES",text=texte,created_at = timezone.now(), mission = instance)
                Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_ordre_de_mission", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                #conservation mail
                # if instance.demandeur.email != "" and instance.demandeur.email != None:
                #     recipient_list.append(instance.demandeur.email)
                # # si auteur different de la personne qui demande
                # if instance.auteur != None:
                #     if instance.auteur_id != instance.demandeur.id:
                #         Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_mission", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                #         #conservation mail
                #         if instance.auteur.email != "" and instance.auteur.email != None:
                #             recipient_list.append(instance.auteur.email)
                
                #Envoi au Chef de service RH
                role_users = dao_role.toListRoleUtilisateurByRoleName("Assistant RH")
                if role_users != None:
                    for item in role_users:
                        Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_ordre_de_mission", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                        #conservation mail
                        if item.utilisateur.email != "" and item.utilisateur.email != None:
                            recipient_list.append(item.utilisateur.email)


                #3. Palier 3 : Passage de Approuver à valider
            if instance.etat == "Ordre de Mission signé envoyé à la comptabilité":
                #Preparation de la notification
                texte = "Votre ordre de mission en date du {} au {} dont l'objet est {} a été reçu avec succès".format(instance.date_depart, instance.date_retour, instance.objet_mission)


                notif = Model_Notification.objects.create(module_source = "MODULE_RESSOURCES_HUMAINES",text=texte,created_at = timezone.now(), mission = instance)
                Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_ordre_de_mission", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                #conservation mail
                # if instance.demandeur.email != "" and instance.demandeur.email != None:
                #     recipient_list.append(instance.demandeur.email)
                # # si auteur different de la personne qui demande
                # if instance.auteur != None:
                #     if instance.auteur_id != instance.demandeur.id:
                #         Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_mission", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                #         #conservation mail
                #         if instance.auteur.email != "" and instance.auteur.email != None:
                #             recipient_list.append(instance.auteur.email)
                
                #Envoi au Chef de service RH
                role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de service RH")
                if role_users != None:
                    for item in role_users:
                        Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_ordre_de_mission", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                        #conservation mail
                        if item.utilisateur.email != "" and item.utilisateur.email != None:
                            recipient_list.append(item.utilisateur.email)


                # if instance.etat == "Ordre de Mission signé envoyé à la caisse":
                #     #Preparation de la notification
                #     texte = "Votre ordre de mission en date du {} au {} dont l'objet est {} a été reçu avec succès".format(instance.date_depart, instance.date_retour, instance.objet_mission)


                #     notif = Model_Notification.objects.create(module_source = "MODULE_RESSOURCES_HUMAINES",text=texte,created_at = timezone.now(), mission = instance)
                #     Model_Temp_Notification.objects.create(user_id=instance.employe_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_ordre_de_mission", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                #     #conservation mail
                #     # if instance.demandeur.email != "" and instance.demandeur.email != None:
                #     #     recipient_list.append(instance.demandeur.email)
                #     # # si auteur different de la personne qui demande
                #     # if instance.auteur != None:
                #     #     if instance.auteur_id != instance.demandeur.id:
                #     #         Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_mission", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                #     #         #conservation mail
                #     #         if instance.auteur.email != "" and instance.auteur.email != None:
                #     #             recipient_list.append(instance.auteur.email)
                    
                #     #Envoi au Chef de service RH
                #     role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de service RH")
                #     if role_users != None:
                #         for item in role_users:
                #             Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_ordre_de_mission", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                #             #conservation mail
                #             if item.utilisateur.email != "" and item.utilisateur.email != None:
                #                 recipient_list.append(item.utilisateur.email)



            #Envoi des mails au concerné
            send_async_mail('Notification Système ARPCE',texte,recipient_list,False,'Notification Module Ressources Humaines','')
            recipient_list.clear()

    except Exception as e:
        #print("Erreur",e)

post_save.connect(signal_ordre_de_mission,sender=models.Model_Ordre_de_mission)


def signal_dossier_social(sender, instance, created, **kwargs):
    try:
        recipient_list = []
        texte = ""
        if created:
            #print("NOTIFICATION Dossier Social")
            #Formattage de la notification
            texte = "Une plainte de {} concernant {0} a été transmis                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     avec succès".format(instance.employe.nom_complet,instance.sujet_plainte)
            notif = Model_Notification.objects.create(module_source = "MODULE_RESSOURCES_HUMAINES",text=texte,created_at = timezone.now(), dossier_social = instance)
            role_name=""
            role_users = None
            #Message envoyé à la personne qui a envoyé la demande de congé
            Model_Temp_Notification.objects.create(user_id=instance.employe_id, type_action = 'Link', lien_action = "module_ressources_humaines_details_dossier_social", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            # si auteur different de la personne qui crée le bon

            #print("Lolo")
            if instance.auteur != None:
                if instance.auteur_id != instance.employe_id:
                    Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_ressources_humaines_details_dossier_social", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                    #conservation mail
                    if instance.auteur.email != "" and instance.auteur.email != None:
                        recipient_list.append(instance.auteur.email)

            # Envoi au supérieur hierarchique de la personne qui fait la demande
            superieur_hierarchique = instance.responsable
            Model_Temp_Notification.objects.create(user_id=superieur_hierarchique.id, type_action = 'Link', lien_action = "module_ressources_humaines_details_dossier_social", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            if superieur_hierarchique.email != "" and superieur_hierarchique.email != None:
                recipient_list.append(superieur_hierarchique.email)

            # #Envoi au Chef de service du RH
            # role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de service RH")
            # if role_users != None:
            #     for item in role_users:
            #         Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_requete", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            #         #conservation mail
            #         if item.utilisateur.email != "" and item.utilisateur.email != None:
            #             recipient_list.append(item.utilisateur.email)
            
            #Envoi des mails au concerné
            send_async_mail('Notification Système ARPCE',texte,recipient_list,False,'Notification Module Ressources Humaines','')
            recipient_list.clear()
        else:
            pass
            # role_name=""
            # role_users = None
            
            # texte = ""
            # #1. Palier 1 : Passage de Créé à Etat de besoin de mission validé
            # #PASS
            # #2. Palier 2 : Passage de Etat de besoin de mission validé à Approuver
            # if instance.etat == "Plainte validé":
            #     #Preparation de la notification
            #     texte = "Votre expression de besoin pour mission concernant {0} a été reçu avec succès".format(instance.description)
            #     notif = Model_Notification.objects.create(module_source = "MODULE_RESSOURCES_HUMAINES",text=texte,created_at = timezone.now(), requete = instance)
            #     # Model_Temp_Notification.objects.create(user_id=instance.employe_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_requete", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            #     #conservation mail
            #     # if instance.demandeur.email != "" and instance.demandeur.email != None:
            #     #     recipient_list.append(instance.demandeur.email)
            #     # # si auteur different de la personne qui demande
            #     # if instance.auteur != None:
            #     #     if instance.auteur_id != instance.demandeur.id:
            #     #         Model_Temp_Notification.objects.create(user_id=instance.auteur_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_conge", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            #     #         #conservation mail
            #     #         if instance.auteur.email != "" and instance.auteur.email != None:
            #     #             recipient_list.append(instance.auteur.email)
                
            #     #Envoi au Directeur DAFC
            #     role_users = dao_role.toListRoleUtilisateurByRoleName("Directeur DAFC")
            #     if role_users != None:
            #         for item in role_users:
            #             Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_ressourceshumaines_detail_requete", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            #             #conservation mail
            #             if item.utilisateur.email != "" and item.utilisateur.email != None:
            #                 recipient_list.append(item.utilisateur.email)
                
            #     #Envoi des mails au concerné
            #     # send_async_mail('Notification Système ARPCE',texte,recipient_list,False,'Notification Module Ressources Humaines','')
            #     # recipient_list.clear()
            
           
            #Envoi des mails au concerné
            send_async_mail('Notification Système ARPCE',texte,recipient_list,False,'Notification Module Ressources Humaines','')
            recipient_list.clear()

    except Exception as e:
        #print("Erreur",e)

post_save.connect(signal_dossier_social,sender=models.Model_Dossier_Social)




def signal_asset(sender,instance,created,**kwargs):
    try:
        recipient_list = []
        texte = ""
        if created:
            pass
        else:
            #print("NOTIFICATION ASSET CREEE")
            #Formattage de la notification
            texte = "Nouvel Asset enregistré {0}  N° {1}, en attente d'immobilisation".format(instance.article.designation,instance.numero_identification)
            notif = Model_Notification.objects.create(module_source = "MODULE_COMPTABILITE",text=texte,created_at = timezone.now())
            #Envoi aux personnes disposant du role Assistant S C T
            role_users = dao_role.toListRoleUtilisateurByRoleName("Chef de service SCT")
            for item in role_users:
                Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Adding', lien_action = "module_comptabilite_add_immobilisation", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                #conservation mail
                if item.utilisateur.email != "" and item.utilisateur.email != None:
                    recipient_list.append(item.utilisateur.email)
            
            #Envoi des mails au concerné
            send_async_mail('Notification Système ARPCE',texte,recipient_list,False,'Notification Module Comptabilité','')
            recipient_list.clear()
    except Exception as e:
        #print("Erreur",e)
#Connection avec le Model
post_save.connect(signal_asset,sender=Model_Asset)


def signal_traitement_immobilisation(sender,instance,created,**kwargs):
    try:
        texte = "Le dossier d'immobilisation N° {0} vous a été envoyé pour traitement".format(instance.numero_traitement)
        lien_action = 'module_inventaire_detail_traitement_immobilisation'
        sending_notification(instance,"MODULE_INVENTAIRE",texte,lien_action)        
    except Exception as e:
        #print("il y a erreur ########################################")
        #print("Erreur",e)

#Connection avec le Model
post_save.connect(signal_traitement_immobilisation,sender=Model_TraitementImmobilisation)


############################ CODE D'ENVOI DES NOTIFICATION #################################
def sending_notification(instance,module_source,texte,lien_action):
    
    recipient_list = []
    #recuperation des transitions
    transitions_concernees = Model_Wkf_Transition.objects.filter(etape_source = instance.statut)

    #création de la notification
    notif = Model_Notification.objects.create(module_source = module_source,text=texte,created_at = timezone.now())
    
    #Constitution du role utilisateur des etapes concernées
    role_users = []
    for transition in transitions_concernees:
        if transition.role_utilisateur:
            list_roles = dao_role.toListRoleUtilisateurByRoleName(transition.role_utilisateur.nom_role)
            for un_role in list_roles:
                role_users.append(un_role)

    #Envoi des notifications aux utilisateurs concernées
    for item in role_users:
        Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = "module_inventaire_detail_traitement_immobilisation", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
        #conservation mail
        if item.utilisateur.email != "" and item.utilisateur.email != None:
            recipient_list.append(item.utilisateur.email)
    
    #Envoi des mails au concerné
    send_async_mail('Notification Système ARPCE',texte,recipient_list,False,'Notification Module Inventaire','')
    recipient_list.clear()