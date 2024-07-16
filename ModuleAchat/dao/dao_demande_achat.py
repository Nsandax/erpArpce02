from __future__ import unicode_literals
from ErpBackOffice.models import Model_Demande_achat
from django.db.models import Max
from django.utils import timezone
from django.db.models import Q


class dao_demande_achat(object):
    id = 0
    numero_demande = ""
    expression_id = 0
    date_demande = ""
    description = ""
    demandeur_id = None
    #requete_id = None
    ligne_budgetaire_id = None
    services_ref_id = None
    statut_id = None
    auteur_id = None
    document = ""
    etat = ""
    est_groupe =False
    centre_cout_id = None

    @staticmethod
    def toCreateDemande(numero_demande, date_demande, description, statut_id, demandeur_id, document, etat, est_groupe, expression_id = None, ligne_budgetaire_id = None, services_ref_id = None, centre_cout_id = None):
        try:
            demande = dao_demande_achat()
            demande.numero_demande = numero_demande
            demande.date_demande = date_demande
            demande.description = description
            demande.statut_id = statut_id
            demande.demandeur_id = demandeur_id
            demande.est_groupe = est_groupe
            if demande.expression_id =="":
                demande.expression_id = None
            else:
                demande.expression_id = expression_id
            if ligne_budgetaire_id == '':
                demande.ligne_budgetaire_id = None    
            demande.ligne_budgetaire_id = ligne_budgetaire_id
            demande.services_ref_id = services_ref_id
            demande.document = document
            demande.etat = etat
            demande.centre_cout_id = centre_cout_id
            return demande
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE ORDRE")
            #print(e)
            return None
    
    @staticmethod
    def toSaveDemande(auteur, objet_dao_demande_achat):
        try :
            demande = Model_Demande_achat()
            demande.numero_demande = objet_dao_demande_achat.numero_demande
            demande.date_demande = objet_dao_demande_achat.date_demande
            demande.description = objet_dao_demande_achat.description
            demande.statut_id = objet_dao_demande_achat.statut_id
            demande.demandeur_id = objet_dao_demande_achat.demandeur_id
            demande.est_groupe = objet_dao_demande_achat.est_groupe
            demande.expression_id = objet_dao_demande_achat.expression_id
            demande.services_ref_id = objet_dao_demande_achat.services_ref_id
            demande.ligne_budgetaire_id = objet_dao_demande_achat.ligne_budgetaire_id
            demande.etat = objet_dao_demande_achat.etat
            demande.centre_cout_id = objet_dao_demande_achat.centre_cout_id
            demande.auteur_id = auteur.id
            demande.save()

            return demande
        except Exception as e:
            #print("ERREUR SAVE ORDER")
            #print(e)
            return None

    @staticmethod
    def toUpdateDemande(id, objet_dao_demande_achat):
        try:
            demande = Model_Demande_achat.objects.get(pk = id)
            demande.date_demande = objet_dao_demande_achat.date_demande
            demande.description = objet_dao_demande_achat.description
            demande.expression_id = objet_dao_demande_achat.expression_id
            demande.statut_id = objet_dao_demande_achat.statut_id
            demande.demandeur_id = objet_dao_demande_achat.demandeur_id
            demande.est_groupe = objet_dao_demande_achat.est_groupe
            demande.ligne_budgetaire_id = objet_dao_demande_achat.ligne_budgetaire_id
            demande.services_ref_id = objet_dao_demande_achat.services_ref_id
            demande.etat = objet_dao_demande_achat.etat
            demande.centre_cout_id = objet_dao_demande_achat.centre_cout_id
            demande.save()
            return True
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return False

    @staticmethod
    def toChangeStatusDemande(id, status):
        try:
            demande = Model_Demande_achat.objects.get(pk = id)
            demande.status = status
            demande.save()
            return True
        except Exception as e:
            return False

    @staticmethod
    def toGetDemande(id):
        try:
            return Model_Demande_achat.objects.get(pk = id)
        except Exception as e:
            return None


    @staticmethod
    def toGetDemandeMax():
        try:
            #return Model_Demande_achat.objects.all().aggregate(Max('rating'))
            max = Model_Demande_achat.objects.all().count()
            max = max + 1
            return max
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return None


    @staticmethod
    def toDeleteDemande(id):
        try:
            demande = Model_Demande_achat.objects.get(pk = id)
            demande.delete()
            return True
        except Exception as e:
            return False

    @staticmethod
    def toListDemandes():
        try:
            demandes = Model_Demande_achat.objects.all().order_by('-numero_demande')
            return demandes
        except Exception as e:
            return None

    @staticmethod
    def toListDemandesByAuteur(user_id):
        try:
            demandes = Model_Demande_achat.objects.filter(auteur_id=user_id).order_by('-numero_demande')
            return demandes
        except Exception as e:
            return None

    @staticmethod
    def toListDemandesOfBonTransmission():
        try:
            demandes = Model_Demande_achat.objects.filter(Q(from_demande_bon_reception__bons_reception_of_bon__etat="Asset enregistré")|Q(model_bon_reception__bons_reception_of_bon__etat="Asset enregistré")).filter(etat="Bon de commande généré")
            return demandes
        except Exception as e:
            #print(e)
            return None

    @staticmethod
    def toListDemandesOfBonTransmissionByAuteur(user_id):
        try:
            demandes = Model_Demande_achat.objects.filter(Q(from_demande_bon_reception__bons_reception_of_bon__etat="Asset enregistré")|Q(model_bon_reception__bons_reception_of_bon__etat="Asset enregistré")).filter(etat="Bon de commande généré").filter(auteur_id=user_id)
            return demandes
        except Exception as e:
            #print(e)
            return None

    @staticmethod
    def toListDemandeOfBonEntree(bon_entree_id):
        try:
            demandes = Model_Demande_achat.objects.filter(Q(from_demande_bon_reception__bons_reception_of_bon__id=bon_entree_id)|Q(model_bon_reception__bons_reception_of_bon__id=bon_entree_id)).filter(etat="Bon de commande généré")
            return demandes
        except Exception as e:
            #print(e)
            return None

    @staticmethod
    def toListDemandeOfBonEntreeByAuteur(bon_entree_id, user_id):
        try:
            demandes = Model_Demande_achat.objects.filter(Q(from_demande_bon_reception__bons_reception_of_bon__id=bon_entree_id)|Q(model_bon_reception__bons_reception_of_bon__id=bon_entree_id)).filter(etat="Bon de commande généré").filter(auteur_id=user_id)
            return demandes
        except Exception as e:
            #print(e)
            return None

    @staticmethod
    def toListDemandesServiceReferent():
        try:
            demandes = Model_Demande_achat.objects.filter(etat = 'Envoyé au service référent')
            return demandes
        except Exception as e:
            return None

    
    @staticmethod
    def toListDemandesServiceReferentByAuteur(user_id):
        try:
            demandes = Model_Demande_achat.objects.filter(etat = 'Envoyé au service référent').filter(auteur_id=user_id)
            return demandes
        except Exception as e:
            return None
    
    @staticmethod
    def toListDemandesPourBonCommande():
        try:
            demandes = Model_Demande_achat.objects.filter(etat = 'Approuvée')
            return demandes
        except Exception as e:
            return None

    @staticmethod
    def toListDemandesPourBonCommandeByAuteur(user_id):
        try:
            demandes = Model_Demande_achat.objects.filter(etat = 'Approuvée').filter(auteur_id=user_id)
            return demandes
        except Exception as e:
            return None
    
    @staticmethod
    def toListDemandesPourAvisAppelOffre():
        try:
            demandes = Model_Demande_achat.objects.filter(etat = 'Envoyé au CGMP')
            return demandes
        except Exception as e:
            return None

    @staticmethod
    def toListDemandesPourAvisAppelOffreByAuteur(user_id):
        try:
            demandes = Model_Demande_achat.objects.filter(etat = 'Envoyé au CGMP').filter(auteur_id=user_id)
            return demandes
        except Exception as e:
            return None

    @staticmethod
    def toListDemandesRecentes():
        try:
            demandes = Model_Demande_achat.objects.all().order_by('-id')[:5]   
            return demandes
        except Exception as e:
            return None

    @staticmethod
    def toListDemandesRecentesByAuteur(user_id):
        try:
            demandes = Model_Demande_achat.objects.filter(auteur_id=user_id).order_by('-id')[:5]   
            return demandes
        except Exception as e:
            return None


    @staticmethod
    def toGenerateNumeroDemande():
        total_damandes = dao_demande_achat.toListDemandes().count()
        total_damandes = total_damandes + 1
        temp_numero = str(total_damandes)
        
        for i in range(len(str(total_damandes)), 4):
            temp_numero = "0" + temp_numero

        mois = timezone.now().month
        if mois < 10: mois = "0%s" % mois
        
        temp_numero = "DEM%s%s%s" % (timezone.now().year, mois, temp_numero)
        return temp_numero
    
    @staticmethod
    def toIntializeDemandeAchat():
        return Model_Demande_achat
    
