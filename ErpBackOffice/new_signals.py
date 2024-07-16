from django.utils import timezone
from ErpBackOffice.models import Model_Temp_Notification, Model_Notification, Model_Role, Model_RoleUtilisateur, Model_Expression, Model_Demande_achat, Model_Bon_reception
from ErpBackOffice.models import  Model_Bon_transfert, Model_Bon,Model_Avis_appel_offre, Model_Conge, Model_Asset,Model_TraitementImmobilisation
from ErpBackOffice.models import Model_Bon_retour, Model_Wkf_Etape, Model_Wkf_Transition, Model_Wkf_Workflow
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from ErpBackOffice import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from ErpBackOffice.dao.dao_role import dao_role
#from ErpBackOffice.utils.sending_email import sending_email
from ErpBackOffice.utils.EmailThread import send_async_mail
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


#VERIFIED
def signal_expression_besoin(sender,instance,created,**kwargs):

    #si superieur hierarchique, nécessaire:
    try:
        superieur_hierarchique = instance.demandeur.unite_fonctionnelle.responsable
    except Exception as e:
        superieur_hierarchique = None

    texte = "L'expression de besoin N° {0} initiée par {1} en date du {2} vous a été envoyé pour traitement".format(instance.numero_expression, instance.demandeur.nom_complet, instance.date_expression)
    lien_action = 'module_achat_detail_expression'
    sending_notification(instance,"MODULE_ACHAT",texte,lien_action, superieur_hierarchique)

#Connection avec le Model
post_save.connect(signal_expression_besoin,sender=Model_Expression)


#VERIFIED
def signal_demande_achat(sender,instance,created,**kwargs):

    texte = "Demande d'achat N° {0} initiée par {1} en date du {2} vous est envoyé pour traitement".format(instance.numero_demande, instance.auteur.nom_complet, instance.date_demande)
    lien_action = 'module_achat_detail_demande_achat'
    sending_notification(instance,"MODULE_ACHAT",texte,lien_action)

#Connection avec le Model
post_save.connect(signal_demande_achat,sender=Model_Demande_achat)

#VERIFIED (Trop de notif en mm temps pr Buitys)
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

    texte = "Le bon de sortie de materiel N° {0} en faveur de {1} établi en date du {2} vous est envoyé pour traitement".format(instance.numero_transfert, instance.employe.nom_complet, instance.date_transfert)
    lien_action = 'module_inventaire_details_transfert_internal'
    sending_notification(instance,"MODULE_INVENTAIRE",texte,lien_action)

#Connection avec le Model
post_save.connect(signal_bon_transfert,sender=Model_Bon_transfert)

#RETOUR MATERIEL
#VERIFIED
def signal_bon_retour(sender,instance,created,**kwargs):

    texte = "Le bon de retour materiel N° {0} en faveur de {1} établi en date du {2} vous est envoyé pour traitement".format(instance.numero_bon_retour, instance.employe.nom_complet, instance.date_retour)
    lien_action = 'module_inventaire_details_retour_internal'
    sending_notification(instance,"MODULE_INVENTAIRE",texte,lien_action)

#Connection avec le Model
post_save.connect(signal_bon_retour,sender=Model_Bon_retour)



def signal_avis_appel_offre(sender,instance,created,**kwargs):

    texte = "L'avis d'appel d'offre N° {0} concernant {1} établi en date du {2} vous est envoyé pour traitement".format(instance.numero_reference, instance.intitule, instance.date_signature)
    lien_action = 'module_achat_detail_avis_appel_offre'
    sending_notification(instance,"MODULE_ACHAT",texte,lien_action)

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
        superieur_hierarchique = instance.demandeur.unite_fonctionnelle.responsable
    except Exception as e:
        superieur_hierarchique = None

    texte = "L'expression de besoin pour mission concernant {0} vous est envoyé pour traitement".format(instance.description)
    lien_action = 'module_ressourceshumaines_detail_requete'
    sending_notification(instance,"MODULE_RESSOURCES_HUMAINES",texte,lien_action, superieur_hierarchique)

post_save.connect(signal_expression_besoin_mission,sender=models.Model_Requete)


#Connection avec le modèle ordre de mission
def signal_ordre_de_mission(sender, instance,created, **kwargs):

    #si superieur hierarchique, nécessaire:
    try:
        superieur_hierarchique = instance.demandeur.unite_fonctionnelle.responsable
    except Exception as e:
        superieur_hierarchique = None

    texte = "L'ordre de mission en date du {} au {} vous est envoyé pour traitement".format(instance.date_depart, instance.date_retour)
    lien_action = 'module_ressourceshumaines_detail_ordre_de_mission'
    sending_notification(instance,"MODULE_RESSOURCES_HUMAINES",texte,lien_action, superieur_hierarchique)

post_save.connect(signal_ordre_de_mission,sender=models.Model_Ordre_de_mission)


def signal_dossier_social(sender, instance, created, **kwargs):

    texte = "Un dossier social vous est envoyé pour traitement"
    lien_action = 'module_ressources_humaines_details_dossier_social'
    sending_notification(instance,"MODULE_RESSOURCES_HUMAINES",texte,lien_action)

post_save.connect(signal_dossier_social,sender=models.Model_Dossier_Social)




def signal_asset(sender,instance,created,**kwargs):

    texte = "Nouvel Asset enregistré {0}  N° {1}, vous est envoyé pour traitement".format(instance.article.designation,instance.numero_identification)
    lien_action = 'module_inventaire_detail_traitement_immobilisation'
    sending_notification(instance,"MODULE_INVENTAIRE",texte,lien_action)
#Connection avec le Model
post_save.connect(signal_asset,sender=Model_Asset)


def signal_traitement_immobilisation(sender,instance,created,**kwargs):

    texte = "Le dossier d'immobilisation N° {0} vous a été envoyé pour traitement".format(instance.numero_traitement)
    lien_action = 'module_inventaire_detail_traitement_immobilisation'
    sending_notification(instance,"MODULE_INVENTAIRE",texte,lien_action)

#Connection avec le Model
post_save.connect(signal_traitement_immobilisation,sender=Model_TraitementImmobilisation)


############################ CODE D'ENVOI DES NOTIFICATION #################################
def sending_notification(instance,module_source,texte,lien_action, superieur_hierarchique = None):
    try:
        #print("im inside bitch")
        recipient_list = []
        #recuperation des transitions
        transitions_concernees = Model_Wkf_Transition.objects.filter(etape_source = instance.statut)
        #print("inst", instance.statut)

        #Si premier enregistrement
        if not instance.statut:
            etape_initial = retrieving_etape_initiale(instance)
            transitions_concernees = Model_Wkf_Transition.objects.filter(etape_source = etape_initial)
            if transitions_concernees.count() > 1:
                transitions_concernees = Model_Wkf_Transition.objects.filter(etape_source = etape_initial).filter(unite_fonctionnelle = instance.services_ref)



        #création de la notification
        notif = Model_Notification.objects.create(module_source = module_source,text=texte,created_at = timezone.now())

        #Constitution du role utilisateur des etapes concernées
        role_users = []
        for transition in transitions_concernees:
            if transition.role_utilisateur:
                list_roles = dao_role.toListRoleUtilisateurByRoleName(transition.role_utilisateur.nom_role)
                for un_role in list_roles:
                    role_users.append(un_role)

        #Elimination des doublons
        role_users = set(role_users)
        role_users = list(role_users)




        #Envoi des notifications aux utilisateurs concernées
        #print(role_users)
        for item in role_users:
            Model_Temp_Notification.objects.create(user_id=item.utilisateur_id, type_action = 'Link', lien_action = lien_action, source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            #conservation mail
            if item.utilisateur.email != "" and item.utilisateur.email != None:
                recipient_list.append(item.utilisateur.email)

        #Envoi au superieur hierarchique
        if not role_users and superieur_hierarchique:
            Model_Temp_Notification.objects.create(user_id=superieur_hierarchique.id, type_action = 'Link', lien_action = lien_action, source_identifiant=instance.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
            if superieur_hierarchique.email != "" and superieur_hierarchique.email != None:
                recipient_list.append(superieur_hierarchique.email)


        #Envoi des mails au concerné
        send_async_mail('Notification Système ARPCE',texte,recipient_list,False,module_source,'')
        recipient_list.clear()
    except Exception as e:
        #print("Erreur on sub function")
        #print("Erreur",e)


def retrieving_etape_initiale(objet_modele):
    content_type = ContentType.objects.get_for_model(objet_modele)
    workflow = Model_Wkf_Workflow.objects.filter(content_type_id= content_type.id).first()
    return Model_Wkf_Etape.objects.get(workflow_id = workflow.id , est_initiale = True)

