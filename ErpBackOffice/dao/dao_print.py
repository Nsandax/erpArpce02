from __future__ import unicode_literals
from django.utils import timezone
import ErpBackOffice
from ErpBackOffice.models import Model_Place, PlaceType
from ErpBackOffice.models import Model_Avis_appel_offre
from ErpBackOffice.models import Model_Bon, Model_ItemBon
from ErpBackOffice.models import Model_Bon_transfert, Model_Ligne_transfert, Model_Unite_fonctionnelle
from ErpBackOffice.models import Model_Immobilisation, Model_Ligne_Immobilisation
from ErpBackOffice.models import Model_TraitementImmobilisation, Model_LigneTraitementImmobilisation
from ErpBackOffice.models import Model_Bon_reception, Model_Ligne_reception
from ErpBackOffice.models import Model_Ordre_paiement, Model_Ligne_ordre_paiement
from ErpBackOffice.models import Model_Dossier_Social
from ErpBackOffice.models import Model_Requete, Model_Ligne_requete

#### Structure de base du model à retourner
model = {
        'title':'', #Titre à donner au rapport
        'reference':'', #Sous-titre ou Référence
        'date_creation':'', #Date de création de l'objet
        'date_now':timezone.now(), #Date d'impression,
        'etat': '',
        'details':[], #Tableau contenant une liste des dictionnaires Champs - Valeurs, gérant l'affichage dans le fichier print.html
        #Dans le cas où le rapport contient des lignes de tableau relatif à l'objet 
        'tabEntete':[], #Tableau des entêtes souhaitées dans le tableau
        'tabLignes':[], #Tableau contenant les lignes relatifs aux données en fontion des entêtes prealablement défini
}
#### Fin de la structure

#********** Code Outils aidant à l'éxécution ************#


#creation d'une fonction qui renvoit "" dans le cas où la valeur recherchée par jointure est inexistante 
def get_value_of_attribute(attribut, objet):
    try:
        attribut = my_exec_objet(attribut, objet)
        return attribut
    except Exception as e:
        #print("errerur her",e)
        return ""
def my_exec_objet(code, objet):
    exec('global i; i = %s' % code)
    global i
    return i
#********** Fin Code Outils aidant à l'éxécution ************#
    

def print_avis_appel_offre(id):
    try:
        model={}
        model['date_now'] = timezone.now()
        #recuperation de l'objet
        avis = Model_Avis_appel_offre.objects.get(pk = id)
        #print("first check", model)

        #Affectation du titre et de la valeur de référence
        model['title'] = "Avis d'appel d'offre"
        model['reference'] = avis.numero_reference
        model['etat'] = avis.etat
        model['date_creation'] = avis.created_at

        #Définition des détails de champ et valeur à afficher sous le format suivant
        list_detail = []
        detail = {'champ':'','valeur':''} #Format à completer

        list_detail = [
            {'champ': 'Commission',                                 'valeur':get_value_of_attribute('objet.designation_commission', avis)},
            {'champ': 'Financement',                                'valeur':get_value_of_attribute('objet.financement', avis)},
            {'champ': 'Objet de l\'appel',                          'valeur':get_value_of_attribute('objet.objet_appel', avis)},
            {'champ': 'Type d\'appel d\'offre',                     'valeur':get_value_of_attribute('objet.type_appel_offre', avis)},
            {'champ': 'Montant de la caution de soumission',        'valeur':get_value_of_attribute('objet.montant_commission', avis)},
            {'champ': 'Lieu(x) de consultation',                    'valeur':get_value_of_attribute('objet.lieu_consultation', avis)},
            {'champ': 'Lieu(x) de dépôt',                           'valeur':get_value_of_attribute('objet.lieu_depot', avis)},
            {'champ': 'Qualification',                              'valeur':get_value_of_attribute('objet.qualification', avis)},

        ]
        model['details'] = list_detail
        #print("that that", model)
        
        return model
    except Exception as e:
        #print("erreur on printing avis appel offre ", e)
        return model 

def print_bon_entree(id):
    try:
        model={}
        model['date_now'] = timezone.now()
        #recuperation de l'objet
        bon = Model_Bon.objects.get(pk = id)
        #print("first check", model)

        #Affectation du titre et de la valeur de référence
        model['title'] = "Bon d'entrée dépôt"
        model['reference'] = bon.numero
        model['etat'] = bon.etat
        model['date_creation'] = bon.creation_date

        #Définition des détails de champ et valeur à afficher sous le format suivant
        list_detail = []
        detail = {'champ':'','valeur':''} #Format à completer

        list_detail = [
            {'champ': 'Nom du fournisseur',                         'valeur':get_value_of_attribute('objet.bon_reception.fournisseur.nom_complet', bon)},
            {'champ': 'Email',                                      'valeur':get_value_of_attribute('objet.bon_reception.fournisseur.email', bon)},
            {'champ': 'Pays',                                       'valeur':get_value_of_attribute('objet.bon_reception.fournisseur.adresse_complete', bon)},
            {'champ': 'Réf. du fournisseur',                        'valeur':get_value_of_attribute('objet.bon_reception.fournisseur.id', bon)},
            {'champ': 'Référence externe',                          'valeur':get_value_of_attribute('objet.reference_document', bon)},
            {'champ': 'Agent receveur',                             'valeur':get_value_of_attribute('objet.inventoriste.nom_complet', bon)}

        ]
        model['details'] = list_detail

        #---------- Cas existence d'un tableau --------------

        lignes = Model_ItemBon.objects.filter(bon_id = id)
        model['tabEntete']= ["Article", "Quantité demandée", "Quantité fournie"] #Entête souhaitée : Respecter la proportion entête et lignes des données à contenir
        tabLignes = [] #Le resultat sera un tableau contenant un sous-tableau
        
        for ligne in lignes:
            tabSousLignes = []
            #Remplissage du sous tableau (Nombre d'élément dans un sous-tableau =  Nombre d'élément du tabEntete)
            tabSousLignes.append(ligne.nom_article)
            tabSousLignes.append(str(ligne.quantite_demandee) + ' ' + str(ligne.unite_article))
            tabSousLignes.append(str(ligne.quantite_fournie) + ' ' + str(ligne.unite_article))
            #Enregistrement du sous tableau dans la liste des lignes préparée à cet effet
            tabLignes.append(tabSousLignes)
        
        model['tabLignes'] = tabLignes
        #print("that that", model)
        
        return model
    except Exception as e:
        #print("erreur on printing bon entrée", e)
        return model

def print_bon_transfert(id):
    try:
        model={}
        model['date_now'] = timezone.now()
        #recuperation de l'objet
        bon_transfert = Model_Bon_transfert.objects.get(pk = id)
        #print("first check", model)

        #Affectation du titre et de la valeur de référence
        model['title'] = "Bon de reception"
        model['reference'] = bon_transfert.numero_transfert
        model['etat'] = bon_transfert.etat
        model['date_creation'] = bon_transfert.creation_date

        #Définition des détails de champ et valeur à afficher sous le format suivant
        list_detail = []
        detail = {'champ':'','valeur':''} #Format à completer

        service_referent_origine = Model_Unite_fonctionnelle.objects.filter(emplacement_id = bon_transfert.emplacement_origine.id).first()
        service_referent_destination = Model_Unite_fonctionnelle.objects.filter(emplacement_id = bon_transfert.emplacement_destination.id).first()

        list_detail = [
            {'champ': 'Demande d\'achat ',                          'valeur':get_value_of_attribute('objet.demande_achat.numero_demande',bon_transfert )},
            {'champ': 'Document externe',                           'valeur':get_value_of_attribute('objet.reference_document',bon_transfert)},
            {'champ': 'Date prévue',                                'valeur':get_value_of_attribute('objet.date_transfert',bon_transfert)},
            {'champ': 'Service référent d\'origine',                'valeur':get_value_of_attribute('objet.libelle', service_referent_origine)},
            {'champ': 'Service référent bénéficiaire',              'valeur':get_value_of_attribute('objet.libelle',service_referent_destination)},
            {'champ': 'Opération',                                  'valeur':get_value_of_attribute('objet.operation_stock.designation',bon_transfert)},
            {'champ': 'Agent recepteur',                            'valeur':get_value_of_attribute('objet.employe.nom_complet',bon_transfert)}

        ]
        model['details'] = list_detail

        #---------- Cas existence d'un tableau --------------

        lignes = Model_Ligne_transfert.objects.filter(bon_transfert_id = id)
        model['tabEntete']= ["Article", "Quantité à transférer", "Quantité transférée"] #Entête souhaitée : Respecter la proportion entête et lignes des données à contenir
        tabLignes = [] #Le resultat sera un tableau contenant un sous-tableau
        
        for ligne in lignes:
            tabSousLignes = []
            #Remplissage du sous tableau (Nombre d'élément dans un sous-tableau =  Nombre d'élément du tabEntete)
            tabSousLignes.append(ligne.nom_article)
            tabSousLignes.append(str(ligne.quantite_demandee) + ' ' + str(ligne.unite_article))
            tabSousLignes.append(str(ligne.quantite_fournie) + ' ' + str(ligne.unite_article))
            #Enregistrement du sous tableau dans la liste des lignes préparée à cet effet
            tabLignes.append(tabSousLignes)
        
        model['tabLignes'] = tabLignes
        #print("that that", model)
        
        return model
    except Exception as e:
        #print("erreur on printing transfert", e)
        return model

def print_bon_sortie_materiel(id):
    try:
        model={}
        model['date_now'] = timezone.now()
        #recuperation de l'objet
        bon_transfert = Model_Bon_transfert.objects.get(pk = id)
        #print("first check", model)

        #Affectation du titre et de la valeur de référence
        model['title'] = "Bon de sortie de matériel"
        model['reference'] = bon_transfert.numero_transfert
        model['etat'] = bon_transfert.etat
        model['date_creation'] = bon_transfert.creation_date

        #Définition des détails de champ et valeur à afficher sous le format suivant
        list_detail = []
        detail = {'champ':'','valeur':''} #Format à completer

        #

        list_detail = [
            {'champ': 'Document externe',                           'valeur':get_value_of_attribute('objet.reference_document', bon_transfert)},
            {'champ': 'Date prévue',                                'valeur':get_value_of_attribute('objet.date_transfert', bon_transfert)},
            {'champ': 'Emplacement d\'origine',                     'valeur':get_value_of_attribute('objet.emplacement_origine', bon_transfert)},
            {'champ': 'Emplacement de destination',                 'valeur':get_value_of_attribute('objet.emplacement_destination', bon_transfert)},
            {'champ': 'Opération',                                  'valeur':get_value_of_attribute('objet.operation_stock.designation', bon_transfert)},
            {'champ': 'Département',                                'valeur':get_value_of_attribute('objet.expression.demandeur.unite_fonctionnelle.designation', bon_transfert)},
            {'champ': 'Alloué à',                                   'valeur':get_value_of_attribute('objet.expression.demandeur.unite_fonctionnelle.designation', bon_transfert)},
            {'champ': 'Responsable du transfert',                   'valeur':get_value_of_attribute('objet.employe.nom_complet', bon_transfert)},
            {'champ': 'Agent ayant traité le transfert',            'valeur':get_value_of_attribute('objet.agent.nom_complet', bon_transfert)},
            {'champ': 'Expression de besoin',                       'valeur':get_value_of_attribute('objet.expression.numero_expression', bon_transfert)},


        ]
        model['details'] = list_detail

        #---------- Cas existence d'un tableau --------------

        lignes = Model_Ligne_transfert.objects.filter(bon_transfert_id = id)
        model['tabEntete']= ["Article", "Quantité à transférer", "Quantité transférée"] #Entête souhaitée : Respecter la proportion entête et lignes des données à contenir
        tabLignes = [] #Le resultat sera un tableau contenant un sous-tableau
        
        for ligne in lignes:
            tabSousLignes = []
            #Remplissage du sous tableau (Nombre d'élément dans un sous-tableau =  Nombre d'élément du tabEntete)
            tabSousLignes.append(ligne.nom_article)
            tabSousLignes.append(str(ligne.quantite_demandee) + ' ' + str(ligne.unite_article))
            tabSousLignes.append(str(ligne.quantite_fournie) + ' ' + str(ligne.unite_article))
            #Enregistrement du sous tableau dans la liste des lignes préparée à cet effet
            tabLignes.append(tabSousLignes)
        
        model['tabLignes'] = tabLignes
        #print("that that", model)
        
        return model
    except Exception as e:
        #print("erreur on printing bon sortie matériel", e)
        return model

def print_immobilisation(id):
    try:
        model={}
        model['date_now'] = timezone.now()
        #recuperation de l'objet
        immobilisation = Model_Immobilisation.objects.get(pk = id)
        #print("first check", model)

        #Affectation du titre et de la valeur de référence
        model['title'] = "Rapport d'immobilisation"
        model['reference'] = immobilisation.code
        model['etat'] = immobilisation.etat
        model['date_creation'] = immobilisation.date_creation

        #Définition des détails de champ et valeur à afficher sous le format suivant
        list_detail = []
        detail = {'champ':'','valeur':''} #Format à completer

        #

        list_detail = [
            {'champ': 'Article',                                'valeur':get_value_of_attribute('objet.immobilier.article.designation', immobilisation)},
            {'champ': 'N° Immobilier',                          'valeur':get_value_of_attribute('objet.immobilier.numero_identification', immobilisation)},
            {'champ': 'Taux d\'amortissement',                  'valeur':get_value_of_attribute('objet.valeur_taux_amortissement', immobilisation)},
            {'champ': 'Durée de vie',                           'valeur':get_value_of_attribute('objet.emplacement_destination', immobilisation)},
            {'champ': 'Valeur de la dotation',                  'valeur':get_value_of_attribute('objet.operation_stock.designation', immobilisation)},
            {'champ': 'Cumul des amortissements',               'valeur':get_value_of_attribute('objet.employe.Model_Unite_fonctionnelle.designation', immobilisation)},
            {'champ': 'Valeur residuelle',                      'valeur':get_value_of_attribute('objet.valeur_residuelle', immobilisation)},
            {'champ': 'Date d\'acquisition de l\'immobilier',   'valeur':get_value_of_attribute('objet.date_acquisition', immobilisation)},
            {'champ': 'Type d\'amortissement',                  'valeur':get_value_of_attribute('objet.value_type_amortissement', immobilisation)},
            {'champ': 'Enregistrée par',                        'valeur':get_value_of_attribute('objet.auteur.nom_complet', immobilisation)},


        ]
        model['details'] = list_detail

        #---------- Cas existence d'un tableau --------------

        lignes = Model_Ligne_Immobilisation.objects.filter(immobilisation_id = id)
        model['tabEntete']= ["Année", "Base d'amortissement", "Dotation", "Cumul", "Valeur résiduelle"] #Entête souhaitée : Respecter la proportion entête et lignes des données à contenir
        tabLignes = [] #Le resultat sera un tableau contenant un sous-tableau
        
        for ligne in lignes:
            tabSousLignes = []
            #Remplissage du sous tableau (Nombre d'élément dans un sous-tableau =  Nombre d'élément du tabEntete)
            tabSousLignes.append(ligne.annee)
            tabSousLignes.append(ligne.base_amortissement)
            tabSousLignes.append(ligne.dotation)
            tabSousLignes.append(ligne.cumul)
            tabSousLignes.append(ligne.valeur_residuelle)

            #Enregistrement du sous tableau dans la liste des lignes préparée à cet effet
            tabLignes.append(tabSousLignes)
        
        model['tabLignes'] = tabLignes
        #print("that that", model)
        
        return model
    except Exception as e:
        #print("erreur on printing immobilisation", e)
        return model


def print_traitement_immobilisation(id):
    try:
        model={}
        model['date_now'] = timezone.now()
        #recuperation de l'objet
        traitement_immobilisation = Model_TraitementImmobilisation.objects.get(pk = id)
        #print("first check", model)

        #Affectation du titre et de la valeur de référence
        model['title'] = "Rapport de traitement d'immobilisation"
        model['reference'] = traitement_immobilisation.numero_traitement
        model['etat'] = traitement_immobilisation.etat
        model['date_creation'] = traitement_immobilisation.created_at

        #Définition des détails de champ et valeur à afficher sous le format suivant
        list_detail = []
        detail = {'champ':'','valeur':''} #Format à completer

        #

        list_detail = [
            {'champ': 'Type de traitement',                                'valeur':get_value_of_attribute('objet.value_type_traitement', traitement_immobilisation)},
            {'champ': 'Description',                                       'valeur':get_value_of_attribute('objet.description', traitement_immobilisation)},
            

        ]
        model['details'] = list_detail

        #---------- Cas existence d'un tableau --------------

        lignes = Model_LigneTraitementImmobilisation.objects.filter(traitement_immobilisation_id = id)
        model['tabEntete']= ["Immobilisation", "Immobilier", "Article"] #Entête souhaitée : Respecter la proportion entête et lignes des données à contenir
        tabLignes = [] #Le resultat sera un tableau contenant un sous-tableau
        
        for ligne in lignes:
            tabSousLignes = []
            #Remplissage du sous tableau (Nombre d'élément dans un sous-tableau =  Nombre d'élément du tabEntete)
            tabSousLignes.append(get_value_of_attribute('objet.immobilisation.code', ligne))
            tabSousLignes.append(get_value_of_attribute('objet.immobilisation.immobilier.numero_identification', ligne))
            tabSousLignes.append(get_value_of_attribute('objet.immobilisation.immobilier.article.designation', ligne))
            
            
            #Enregistrement du sous tableau dans la liste des lignes préparée à cet effet
            tabLignes.append(tabSousLignes)
        
        model['tabLignes'] = tabLignes
        #print("that that", model)
        
        return model
    except Exception as e:
        #print("erreur on printing traitement immobilisation", e)
        return model


def print_reception_facture(id):
    try:
        model={}
        model['date_now'] = timezone.now()
        #recuperation de l'objet
        bon_reception = Model_Bon_reception.objects.get(pk = id)
        #print("first check", model)

        #Affectation du titre et de la valeur de référence
        model['title'] = "Reception de bon de commande"
        model['reference'] = bon_reception.numero_reception
        model['etat'] = bon_reception.etat
        model['date_creation'] = bon_reception.creation_date

        #Définition des détails de champ et valeur à afficher sous le format suivant
        list_detail = []
        detail = {'champ':'','valeur':''} #Format à completer

        list_detail = [
            {'champ': 'Nom du fournisseur',                         'valeur':get_value_of_attribute('objet.fournisseur.nom_complet', bon_reception)},
            {'champ': 'Email',                                      'valeur':get_value_of_attribute('objet.fournisseur.email', bon_reception)},
            {'champ': 'Pays',                                       'valeur':get_value_of_attribute('objet.fournisseur.adresse_complete', bon_reception)},
            {'champ': 'Réf. du fournisseur',                        'valeur':get_value_of_attribute('objet.fournisseur.id', bon_reception)},
            {'champ': 'Référence externe',                          'valeur':get_value_of_attribute('objet.reference_document', bon_reception)},
            {'champ': 'Ligne budgetaire',                           'valeur':get_value_of_attribute('objet.ligne_budgetaire.designation', bon_reception)},
            {'champ': 'Modalité de réglement',                      'valeur':get_value_of_attribute('objet.condition_reglement.designation', bon_reception)}

        ]
        model['details'] = list_detail

        #---------- Cas existence d'un tableau --------------

        lignes = Model_Ligne_reception.objects.filter(bon_reception_id = id)
        model['tabEntete']= ["Article", "Quantité demandée", "Quantité fournie", "Prix unitaire", "Prix total"] #Entête souhaitée : Respecter la proportion entête et lignes des données à contenir
        tabLignes = [] #Le resultat sera un tableau contenant un sous-tableau
        
        for ligne in lignes:
            tabSousLignes = []
            #Remplissage du sous tableau (Nombre d'élément dans un sous-tableau =  Nombre d'élément du tabEntete)
            tabSousLignes.append(ligne.nom_article)
            tabSousLignes.append(str(ligne.quantite_demande) + ' ' + str(ligne.unite_article))
            tabSousLignes.append(str(ligne.quantite_fournie) + ' ' + str(ligne.unite_article))
            tabSousLignes.append(str(ligne.separateur_prix_unitaire) + ' ' + get_value_of_attribute('objet.devise.symbole_devise', bon_reception))
            tabSousLignes.append(str(ligne.separateur_total) + ' ' + get_value_of_attribute('objet.devise.symbole_devise', bon_reception))
            #Enregistrement du sous tableau dans la liste des lignes préparée à cet effet
            tabLignes.append(tabSousLignes)
        
        model['tabLignes'] = tabLignes
        #print("that that", model)
        
        return model
    except Exception as e:
        #print("erreur on printing bon entrée", e)
        return model


def print_ordre_paiement(id):
    try:
        model={}
        model['date_now'] = timezone.now()
        #recuperation de l'objet
        ordre_paiement = Model_Ordre_paiement.objects.get(pk = id)
        #print("first check", model)

        #Affectation du titre et de la valeur de référence
        model['title'] = "Ordre de paiement"
        model['reference'] = ordre_paiement.reference
        model['etat'] = ordre_paiement.etat
        model['date_creation'] = ordre_paiement.created_at

        #Définition des détails de champ et valeur à afficher sous le format suivant
        list_detail = []
        detail = {'champ':'','valeur':''} #Format à completer

        #Test si compte banque et caisse
        devise_entite = ""
        title_entite = ""
        reference_entite = ""
        name_entite = ""
        if ordre_paiement.compte_banque:
            devise_entite = get_value_of_attribute('objet.compte_banque.journal.devise', ordre_paiement)
            title_entite = "Compte bancaire"
            reference_entite = get_value_of_attribute('objet.compte_banque.numero_compte', ordre_paiement)
            name_entite = get_value_of_attribute('objet.compte_banque.banque.designation', ordre_paiement)
        elif ordre_paiement.caisse:
            devise_entite = get_value_of_attribute('objet.compte_banque.journal.devise', ordre_paiement)
            title_entite = "Caisse"
            reference_entite = "Caisse"
            name_entite = get_value_of_attribute('objet.caisse.designation', ordre_paiement)




        list_detail = [
            {'champ': 'Initié par',                                 'valeur':get_value_of_attribute('objet.auteur.nom_complet', ordre_paiement)},
            {'champ': 'Type de paiement',                           'valeur':get_value_of_attribute('objet.value_type_paiement', ordre_paiement)},
            {'champ': 'Devise',                                     'valeur':devise_entite},
            {'champ': title_entite,                                 'valeur':name_entite + " " + reference_entite},
            
        ]
        model['details'] = list_detail

        #---------- Cas existence d'un tableau --------------

        lignes = Model_Ligne_ordre_paiement.objects.filter(ordre_paiement_id = id)
        model['tabEntete']= ["Partenaire", "Libelle", "Facture", "Montant", "Observation"] #Entête souhaitée : Respecter la proportion entête et lignes des données à contenir
        tabLignes = [] #Le resultat sera un tableau contenant un sous-tableau
        
        for ligne in lignes:
            #print("lign",ligne)
            tabSousLignes = []
            #Remplissage du sous tableau (Nombre d'élément dans un sous-tableau =  Nombre d'élément du tabEntete)
            tabSousLignes.append(ligne.partenaire)
            tabSousLignes.append(ligne.libelle)
            tabSousLignes.append("-")
            tabSousLignes.append(ligne.montant)
            tabSousLignes.append(ligne.observation)
            #Enregistrement du sous tableau dans la liste des lignes préparée à cet effet
            tabLignes.append(tabSousLignes)
        
        model['tabLignes'] = tabLignes
        #print("that that", model)
        
        return model
    except Exception as e:
        #print("erreur on printing bon entrée", e)
        return model



def print_tableau_amortissement(id):
    try:
        model={}
        model['date_now'] = timezone.now()
        #recuperation de l'objet
        lignes = Model_Immobilisation.objects.filter(is_available = True).filter(est_comptabilise = True).order_by("date_acquisition")
        #print("first check", model)

        #Affectation du titre et de la valeur de référence
        model['title'] = "Tableau d'immobilisation"
        model['reference'] = ""
        model['etat'] = ""
        model['date_creation'] = ""

        #Définition des détails de champ et valeur à afficher sous le format suivant
        list_detail = []
        detail = {'champ':'','valeur':''} #Format à completer

        

        #---------- Cas existence d'un tableau --------------

        model['tabEntete']= ["Immobilisation", "Asset", "Article", "Type", "Valeur d'acquisition", "Dotation", "Valeur résiduelle"] #Entête souhaitée : Respecter la proportion entête et lignes des données à contenir
        tabLignes = [] #Le resultat sera un tableau contenant un sous-tableau
        
        for ligne in lignes:
            tabSousLignes = []
            #Remplissage du sous tableau (Nombre d'élément dans un sous-tableau =  Nombre d'élément du tabEntete)
            tabSousLignes.append(get_value_of_attribute('objet.code', ligne))
            tabSousLignes.append(get_value_of_attribute('objet.immobilier.numero_identification', ligne))
            tabSousLignes.append(get_value_of_attribute('objet.immobilier.article.designation', ligne))
            tabSousLignes.append(get_value_of_attribute('objet.value_type_amortissement', ligne))
            tabSousLignes.append(get_value_of_attribute('objet.valeur_immobilier', ligne))
            tabSousLignes.append(get_value_of_attribute('objet.valeur_dotation', ligne))
            #tabSousLignes.append(get_value_of_attribute('objet.valeur_cumul_amortissement', ligne))
            tabSousLignes.append(get_value_of_attribute('objet.valeur_residuelle', ligne))
            
            
            #Enregistrement du sous tableau dans la liste des lignes préparée à cet effet
            tabLignes.append(tabSousLignes)
        
        model['tabLignes'] = tabLignes
        #print("that that", model)
        
        return model
    except Exception as e:
        #print("erreur on printing traitement tableau immo", e)
        return model



def print_dossier_appel_offre(id):
    try:
        model={}
        model['date_now'] = timezone.now()
        #recuperation de l'objet
        dossier_social = Model_Dossier_Social.objects.get(pk = id)
        #print("first check", model)

        #Affectation du titre et de la valeur de référence
        model['title'] = "Dossier social"
        model['reference'] = dossier_social.numero_dossier_social
        model['etat'] = dossier_social.etat
        model['date_creation'] = dossier_social.creation_date

        #Définition des détails de champ et valeur à afficher sous le format suivant
        list_detail = []
        detail = {'champ':'','valeur':''} #Format à completer

        list_detail = [
            {'champ': 'Sujet',                                      'valeur':get_value_of_attribute('objet.sujet_plainte', dossier_social)},
            {'champ': 'Description',                                'valeur':get_value_of_attribute('objet.description', dossier_social)},
            {'champ': 'Dossier concernant l\'établissement',        'valeur':get_value_of_attribute('objet.structure', dossier_social)},
            {'champ': 'Situé sur l\'adresse',                       'valeur':get_value_of_attribute('objet.lieu', dossier_social)},
            {'champ': 'Responsable',                                'valeur':get_value_of_attribute('objet.responsable.nom_complet', dossier_social)},
        ]
        model['details'] = list_detail
        #print("that that", model)
        
        return model
    except Exception as e:
        #print("erreur on printing avis appel offre ", e)
        return model 


def print_requete_mission(id):
    try:
        model={}
        model['date_now'] = timezone.now()
        #recuperation de l'objet
        requete = Model_Requete.objects.get(pk = id)
        #print("first check", model)

        #Affectation du titre et de la valeur de référence
        model['title'] = "Requête de mission"
        model['reference'] = requete.numero_reference
        model['etat'] = requete.etat
        model['date_creation'] = requete.created_at

        #Définition des détails de champ et valeur à afficher sous le format suivant
        list_detail = []
        detail = {'champ':'','valeur':''} #Format à completer

        list_detail = [
            {'champ': 'Demandé par:',                         'valeur':get_value_of_attribute('objet.demandeur.nom_complet', requete)},
            {'champ': 'Centre de coût',                       'valeur':get_value_of_attribute('objet.centre_cout.designation', requete)},
            {'champ': 'Description de la mission',             'valeur':get_value_of_attribute('objet.description', requete)},
            {'champ': 'Date de départ',                        'valeur':get_value_of_attribute('objet.date_depart', requete)},
            {'champ': 'Date de retour',                        'valeur':get_value_of_attribute('objet.date_retour', requete)}

        ]
        model['details'] = list_detail

        #---------- Cas existence d'un tableau --------------

        lignes = Model_Ligne_requete.objects.filter(requete_id = id)
        model['tabEntete']= ["Employé concerné", "Status"] #Entête souhaitée : Respecter la proportion entête et lignes des données à contenir
        tabLignes = [] #Le resultat sera un tableau contenant un sous-tableau
        
        for ligne in lignes:
            tabSousLignes = []
            #Remplissage du sous tableau (Nombre d'élément dans un sous-tableau =  Nombre d'élément du tabEntete)
            tabSousLignes.append(get_value_of_attribute('objet.employe.nom_complet', ligne))
            tabSousLignes.append(get_value_of_attribute('objet.status', ligne))
            tabLignes.append(tabSousLignes)
        
        model['tabLignes'] = tabLignes
        #print("that that", model)
        
        return model
    except Exception as e:
        #print("erreur on printing bon entrée", e)
        return model