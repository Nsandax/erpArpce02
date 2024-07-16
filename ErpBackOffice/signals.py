from django.utils import timezone
from ErpBackOffice.models import Model_Temp_Notification, Model_Notification, Model_Role, Model_RoleUtilisateur, Model_Expression, Model_Demande_achat, Model_Bon_reception, Model_Transactionbudgetaire
from ErpBackOffice.models import  Model_Bon_transfert, Model_Bon,Model_Avis_appel_offre, Model_Conge, Model_Asset,Model_TraitementImmobilisation, Model_Requete_competence
from ErpBackOffice.models import Model_Wkf_Etape, Model_Wkf_Transition, Model_Wkf_Workflow, Model_Wkf_Stakeholder
from ErpBackOffice.models import Model_Annee_fiscale
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from ErpBackOffice import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from ErpBackOffice.dao.dao_role import dao_role
from ErpBackOffice.dao.dao_groupe_permission import dao_groupe_permission
#from ErpBackOffice.utils.sending_email import sending_email
from ErpBackOffice.utils.EmailThread import send_async_mail
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


def newsignal(sender,instance,created,**kwargs):
    if instance.statut: #C'est pour ne pas envoyer 2 notifications après l'etape initiale       
        auteur = "Admin"
        if instance.auteur: auteur = instance.auteur.nom_complet
        texte = "Le Bon d'Engagement N° {0} initié par {1} en date du {2} vous est envoyé pour traitement".format(instance.numero, auteur, instance.creation_date)
        lien_action = 'module_comptabilites_detail_engagements'
        sending_notification(instance,"MODULE_COMPTABILITES",texte,lien_action)

#VERIFIED
def signal_expression_besoin(sender,instance,created,**kwargs):

    #si superieur hierarchique, nécessaire:
    try: 
        superieur_hierarchique = instance.demandeur.superieur_hierarchique
    except Exception as e:
        superieur_hierarchique = instance.demandeur

    texte = "L'expression de besoin N° {0} initiée par {1} en date du {2} vous a été envoyé pour traitement".format(instance.numero_expression, instance.demandeur.nom_complet, instance.date_expression)
    lien_action = 'module_achat_detail_expression'
    sending_notification(instance,"MODULE_ACHAT",texte,lien_action, superieur_hierarchique)

#Connection avec le Model
post_save.connect(signal_expression_besoin,sender=Model_Expression)


#VERIFIED
def signal_demande_achat(sender,instance,created,**kwargs):

    if instance.auteur:
        texte = "Demande d'achat N° {0} initiée par {1} en date du {2} vous est envoyé pour traitement".format(instance.numero_demande, instance.auteur.nom_complet, instance.date_demande)
    else:
        texte = "Demande d'achat N° {0} initiée par {1} en date du {2} vous est envoyé pour traitement".format(instance.numero_demande, "Admin", instance.date_demande)
    lien_action = 'module_achat_detail_demande_achat'
    sending_notification(instance,"MODULE_ACHAT",texte,lien_action)
            
#Connection avec le Model
post_save.connect(signal_demande_achat,sender=Model_Demande_achat)

#VERIFIED (Buitys, 3 notifs de suite)
def signal_bon_commande(sender,instance,created,**kwargs):
    
    texte = "Le bon de commande N° {0} vous est envoyé pour traitement".format(instance.numero_reception)
    lien_action = 'module_achat_detail_bon_reception'
    sending_notification(instance,"MODULE_ACHAT",texte,lien_action)
            
#Connection avec le Model
post_save.connect(signal_bon_commande,sender=Model_Bon_reception)


#VERIFIED
def signal_bon_entree_depot(sender,instance,created,**kwargs):
    
    texte = "Le bon d'entrée en dépôt  N° {0} enregistré en date du {1} vous est envoyé pour traitement".format(instance.numero,instance.creation_date)
    lien_action = 'module_inventaire_details_bons_entrees'
    sending_notification(instance,"MODULE_INVENTAIRE",texte,lien_action)
           
#Connection avec le Model
post_save.connect(signal_bon_entree_depot,sender=Model_Bon)

#VERIFIED
def signal_bon_transfert(sender,instance,created,**kwargs):
    
    if instance.operation_stock.designation == "Affectation interne":
        texte = "Le bon de sortie de materiel N° {0} en faveur de {1} établi en date du {2} vous est envoyé pour traitement".format(instance.numero_transfert, instance.employe.nom_complet, instance.date_transfert)
        lien_action = 'module_inventaire_details_transfert_internal'
        sending_notification(instance,"MODULE_INVENTAIRE",texte,lien_action)
    else:
        texte = "Le bon de transfert N° {0} établi en date du {1} vous est envoyé pour traitement".format(instance.numero_transfert, instance.date_transfert)
        lien_action = 'module_inventaire_detail_bon_transfert'
        sending_notification(instance,"MODULE_INVENTAIRE",texte,lien_action)
                
#Connection avec le Model
post_save.connect(signal_bon_transfert,sender=Model_Bon_transfert)


def signal_avis_appel_offre(sender,instance,created,**kwargs):

    texte = "L'avis d'appel d'offre N° {0} concernant {1} établi en date du {2} vous est envoyé pour traitement".format(instance.numero_reference, instance.intitule, instance.date_signature)
    lien_action = 'module_contrat_detail_avis_appel_offre'
    sending_notification(instance,"MODULE_CONTRAT",texte,lien_action)
            
#Connection avec le Model
post_save.connect(signal_avis_appel_offre,sender=Model_Avis_appel_offre)


#Traitement spécifique
def signal_demande_conge(sender,instance,created,**kwargs):

    texte = "Une demande de congé du type {0} allant de {1} à {2}, soit un total de {3} jours vous est envoyé pour traitement".format(instance.histypeconge, instance.date_from, instance.date_to, instance.nombre_jour)
    lien_action = 'module_ressourceshumaines_detail_conge'
    sending_notification(instance,"MODULE_RESSOURCES_HUMAINES",texte,lien_action)
    
           
#Connection avec le Model
post_save.connect(signal_demande_conge,sender=Model_Conge)

#Connection avec le modèle requête
def signal_expression_besoin_mission(sender, instance, created, **kwargs):

    #si superieur hierarchique, nécessaire:
    try: 
        superieur_hierarchique = instance.demandeur.superieur_hierarchique
    except Exception as e:
        superieur_hierarchique = instance.demandeur
    
    texte = "L'expression de besoin pour mission concernant {0} vous est envoyé pour traitement".format(instance.description)
    lien_action = 'module_ressourceshumaines_detail_requete'
    sending_notification(instance,"MODULE_RESSOURCES_HUMAINES",texte,lien_action, superieur_hierarchique)

post_save.connect(signal_expression_besoin_mission,sender=models.Model_Requete)


#Connection avec le modèle ordre de mission
def signal_ordre_de_mission(sender, instance,created, **kwargs):

    #si superieur hierarchique, nécessaire:
    try: 
        superieur_hierarchique = instance.demandeur.superieur_hierarchique
    except Exception as e:
        superieur_hierarchique = instance.demandeur

    texte = "L'ordre de mission en date du {} au {} vous est envoyé pour traitement".format(instance.date_depart, instance.date_retour)
    lien_action = 'module_ressourceshumaines_detail_ordre_de_mission'
    sending_notification(instance,"MODULE_RESSOURCES_HUMAINES",texte,lien_action, superieur_hierarchique)

post_save.connect(signal_ordre_de_mission,sender=models.Model_Ordre_de_mission)


def signal_dossier_social(sender, instance, created, **kwargs):

    texte = "Un dossier social vous est envoyé pour traitement"
    lien_action = 'module_ressources_humaines_details_dossier_social'
    sending_notification(instance,"MODULE_RESSOURCES_HUMAINES",texte,lien_action)

post_save.connect(signal_dossier_social,sender=models.Model_Dossier_Social)


#VERIFIED
#TRAITEMENT PARTICULIER, MAINTENU
def signal_asset(sender,instance,created,**kwargs):
    try:
        recipient_list = []
        texte = ""
        if created:
            pass
        else:
            #print("NOTIFICATION ASSET CREEE")
            annee_fiscale = Model_Annee_fiscale.objects.filter(est_active = True).first()

            if instance.article.est_amortissable:
                if instance.article.prix_unitaire > annee_fiscale.seuil_immobilisation:
                    #Formattage de la notification
                    texte = "Nouvel Asset enregistré {0}  N° {1}, en attente d'immobilisation".format(instance.article.designation,instance.numero_identification)
                    notif = Model_Notification.objects.create(module_source = "MODULE_COMPTABILITE",text=texte,created_at = timezone.now())
                    #Envoi aux personnes disposant du role Assistant S C T
                    role_users = dao_groupe_permission.toListGroupePermissionByDesignation("Chef de service SCT")
                    for item in role_users:
                        Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Adding', lien_action = "module_comptabilite_add_immobilisation", source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
                        #conservation mail
                        if item.utilisateur.email != "" and item.utilisateur.email != None:
                            recipient_list.append(item.utilisateur.email)
            
            #Envoi des mails au concerné
            send_async_mail('Notification Système ARPCE',texte,recipient_list,False,'Notification Module Comptabilité','')
            recipient_list.clear()
    except Exception as e:
        pass
        #print("Erreur",e)
#Connection avec le Model
post_save.connect(signal_asset,sender=Model_Asset)


def signal_traitement_immobilisation(sender,instance,created,**kwargs):

    texte = "Le dossier d'immobilisation N° {0} vous a été envoyé pour traitement".format(instance.numero_traitement)
    lien_action = 'module_inventaire_detail_traitement_immobilisation'
    sending_notification(instance,"MODULE_INVENTAIRE",texte,lien_action)        
    
#Connection avec le Model
post_save.connect(signal_traitement_immobilisation,sender=Model_TraitementImmobilisation)


def signal_transaction_budgetaire(sender,instance,created,**kwargs):

    try:
        if instance.typetransactionbudgetaire == 2 or instance.typetransactionbudgetaire == 3:
            texte = "Un reajustement budgétaire a été initié et est en attente de traitement "
            lien_action = 'module_budget_detail_transactionbudgetaire'
            sending_notification(instance,"MODULE_BUDGET",texte,lien_action)      
    except Exception as e:
        print("signal_transaction_budgetaire", e)

      
    
#Connection avec le Model
post_save.connect(signal_transaction_budgetaire,sender=Model_Transactionbudgetaire)

def signal_requete_competence(sender,instance,created,**kwargs):

    texte = "La requête de compétence N° {0} vous a été envoyé pour traitement".format(instance.numero_requete)
    lien_action = 'module_ressourceshumaines_detail_requete_competence'
    sending_notification(instance,"MODULE_RESSOURCES_HUMAINES",texte,lien_action)        
    
#Connection avec le Model
post_save.connect(signal_requete_competence,sender=Model_Requete_competence)


def signal_stakeholder(sender,instance,created,**kwargs):
    try:
        if instance.est_delegation:
            texte = f'Un traitement de {instance.content_type} vous a été soumis avec le message suivant : {instance.comments}' 
            if instance.url_detail and instance.module_source:
                sending_stakeholder_notification(instance,texte)
    except Exception as e:
        print("signal_stakeholder", e)

post_save.connect(signal_stakeholder,sender=Model_Wkf_Stakeholder)


############################ CODE D'ENVOI DES NOTIFICATION #################################
def sending_notification(instance,module_source,texte,lien_action, superieur_hierarchique = None):
    try:
        #print("im inside bitch")
        #print("##################################################################")
        recipient_list = []
        #recuperation des transitions
        transitions_concernees = Model_Wkf_Transition.objects.filter(etape_source = instance.statut)
        #print("inst", instance.statut)

        #Si premier enregistrement
        if not instance.statut:
            etape_initial = retrieving_etape_initiale(instance)
            transitions_concernees = Model_Wkf_Transition.objects.filter(etape_source = etape_initial)
            #print("trans", transitions_concernees)
            if transitions_concernees.count() > 1:
                transitions_concernees = Model_Wkf_Transition.objects.filter(etape_source = etape_initial).filter(unite_fonctionnelle = instance.services_ref)
                #print("trans2", transitions_concernees)
                
        

        #création de la notification
        notif = Model_Notification.objects.create(module_source = module_source,text=texte,created_at = timezone.now())
        
        #Constitution du role utilisateur des etapes concernées
        role_users = []
        for transition in transitions_concernees:
            if transition.groupe_permission:
                list_roles = dao_groupe_permission.toListGroupePermissionByDesignation(transition.groupe_permission.designation)
                for un_role in list_roles:
                    role_users.append(un_role)
        
        #Elimination des doublons
        role_users = set(role_users)
        role_users = list(role_users)

        
       

        #Envoi des notifications aux utilisateurs concernées
        #print("role",role_users)
        for item in role_users:
            Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = lien_action, source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            #conservation mail
            if item.utilisateur.email != "" and item.utilisateur.email != None:
                recipient_list.append(item.utilisateur.email)
        
        #Envoi au superieur hierarchique
        if not role_users and superieur_hierarchique:
            #print("in role users")
            Model_Temp_Notification.objects.create(user_id=superieur_hierarchique.id, type_action = 'Link', lien_action = lien_action, source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            if superieur_hierarchique.email != "" and superieur_hierarchique.email != None:
                recipient_list.append(superieur_hierarchique.email)
        
        
        #Envoi des mails au concerné
        send_async_mail('Notification Système ARPCE',texte,recipient_list,False,module_source,'')
        recipient_list.clear()
    except Exception as e:
        print("Erreur on sub function")
        print("Erreur",e)
        pass


############################ CODE D'ENVOI DES NOTIFICATION #################################
def sending_stakeholder_notification(instance,texte):
    try:
        recipient_list = []
        module_source = instance.module_source
        lien_action = instance.url_detail
        users = instance.employes
        Cc = instance.carbon_copies
        
        #création de la notification
        notif = Model_Notification.objects.create(module_source = module_source,text=texte,created_at = timezone.now())
        
        #Envoi des notifications aux utilisateurs concernées
        #print("role",role_users)
        for item in users.all():
            Model_Temp_Notification.objects.create(user_id=item.id, type_action = 'Link', lien_action = lien_action, source_identifiant=instance.document_id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            #conservation mail
            if item.email != "" and item.email != None:
                recipient_list.append(item.email)
        
        for item in Cc.all():
            #Model_Temp_Notification.objects.create(user_id=item.id, type_action = 'Link', lien_action = lien_action, source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            #conservation mail
            if item.email != "" and item.email != None:
                recipient_list.append(item.email)
        
        #Envoi des mails au concerné
        send_async_mail('Notification Système ARPCE',texte,recipient_list,False,module_source,'')
        recipient_list.clear()
    except Exception as e:
        #print("Erreur on sub function")
        #print("Erreur",e)
        pass





def retrieving_etape_initiale(objet_modele):
    content_type = ContentType.objects.get_for_model(objet_modele)
    workflow = Model_Wkf_Workflow.objects.filter(content_type_id= content_type.id).first()
    return Model_Wkf_Etape.objects.get(workflow_id = workflow.id , est_initiale = True)

