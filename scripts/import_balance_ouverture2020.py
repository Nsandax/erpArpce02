from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import os
from datetime import time, timedelta, datetime
from django.utils import timezone
import json
from django.db import transaction
from django.db.models import Q
import pandas as pd
import requests
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np
import time
from requests.auth import HTTPBasicAuth,HTTPDigestAuth
from ErpBackOffice.utils.separateur import makeFloat
from ErpBackOffice.utils.auth import auth

#-----------------------------------------------
from ErpBackOffice.utils.separateur import AfficheEntier
#-----------------------------------------------


from ErpBackOffice.models import Model_Unite_fonctionnelle, Model_Budget, Model_Employe, Model_Image, Model_Taux, Model_PieceComptable , Model_Compte, Model_EcritureComptable,Model_Annee_fiscale #Model_PlanComptable Model_PieceComptable_attente,

# Import ErpBackOffice.dao
from ErpBackOffice.dao.dao_personne import dao_personne
from ErpBackOffice.dao.dao_place import dao_place
from ErpBackOffice.dao.dao_module import dao_module
from ErpBackOffice.dao.dao_role import dao_role
from ErpBackOffice.dao.dao_devise import dao_devise
from ErpBackOffice.dao.dao_droit import dao_droit
from ErpBackOffice.dao.dao_facture_fournisseur import dao_facture_fournisseur
from ErpBackOffice.dao.dao_facture_client import dao_facture_client
from ErpBackOffice.dao.dao_facture import dao_facture
from ErpBackOffice.dao.dao_paiement import dao_paiement
from ErpBackOffice.dao.dao_transaction import dao_transaction
from ErpBackOffice.dao.dao_payloads import dao_payloads
from ErpBackOffice.dao.dao_statut_transaction import dao_statut_transaction
from ErpBackOffice.dao.dao_moyen_paiement import dao_moyen_paiement
from ErpBackOffice.dao.dao_article import dao_article

# Import from ModuleAchat et ModuleVente

from ModuleAchat.dao.dao_bon_reception import dao_bon_reception
from ModuleAchat.dao.dao_ligne_reception import dao_ligne_reception
from ModuleAchat.dao.dao_fournisseur import dao_fournisseur
from ModuleVente.dao.dao_client import dao_client
from ModuleVente.dao.dao_bon_commande import dao_bon_commande
from ModuleVente.dao.dao_ligne_commande import dao_ligne_commande
from ModuleInventaire.dao.dao_stock_article import dao_stock_article

# Import from ModuleRessourcesHumaines
from ModuleRessourcesHumaines.dao.dao_employe import dao_employe
from ModuleRessourcesHumaines.dao.dao_unite_fonctionnelle import dao_unite_fonctionnelle

# Import from ModuleComptabilite
from ModuleComptabilite.dao.dao_annee_fiscale import dao_annee_fiscale
from ModuleComptabilite.dao.dao_journal import dao_journal
from ModuleComptabilite.dao.dao_capture_compte import dao_capture_compte
from ModuleComptabilite.dao.dao_compte import dao_compte
from ModuleComptabilite.dao.dao_immobilisation import dao_immobilisation
from ModuleComptabilite.dao.dao_portee_taxe import dao_portee_taxe
from ModuleComptabilite.dao.dao_type_compte import dao_type_compte
from ModuleComptabilite.dao.dao_type_journal import dao_type_journal
from ModuleComptabilite.dao.dao_type_of_typecompte import dao_type_of_typecompte
from ModuleComptabilite.dao.dao_piece_comptable import dao_piece_comptable
from ModuleComptabilite.dao.dao_ecriture_comptable import dao_ecriture_comptable
from ModuleComptabilite.dao.dao_budget import dao_budget
from ModuleComptabilite.dao.dao_ligne_budgetaire import dao_ligne_budgetaire
from ModuleComptabilite.dao.dao_taux_change import dao_taux_change
# from ModuleCaisse_urgente.dao.dao_quittance_caisse import dao_quittance_caisse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# from ModuleComptabilite.dao.dao_acte import dao_acte
from ModuleComptabilite.dao.dao_config_comptabilite import dao_config_comptabilite
from ModuleComptabilite.utils.balance import balanceArray
from ModuleComptabilite.utils.bilan import bilanArray
from ModuleComptabilite.utils.compte_resultat import compteResultatArray

# LANCER LE FICHIER SCRIPT : python manage.py runscript ModuleComptabilite.import

def run():
    print("---Execution script IMPORT COMPTA---")
    # importBalance("Balance_globale_ouverture", 0)
    # importBalance("Balance_Cloture", 0)
    importBalance("Bg2020", 0)



@transaction.atomic
def importBalance(file_name, type=0):
    """
    Fonction qui exécute le script qui import la balance des comptes
    :param file_name: (string) une chaine de caractère,le nom du fichier à importer
    :param type: (int) un entier, si 1 les comptes importés sont ceux du PC OHADA Révisé; si 0 les comptes importés sont ceux de l'ancien PC OHADA
    :return : (void)  renvoie rien juste affiche le deroulement
    """
    print("importBalance() ...")
    sid = transaction.savepoint()
    try:
        import_dir = settings.MEDIA_ROOT
        file_dir = 'excel/'
        import_dir = import_dir + '/' + file_dir
        file_path = os.path.join(import_dir, str(file_name) + ".xlsx")
        if default_storage.exists(file_path):
            filename = default_storage.generate_filename(file_path)
            sheet = "Ouverture"
            print("Sheet : {} file: {}".format(sheet, filename))
            df = pd.read_excel(io=filename, sheet_name=sheet)

            auteur = Model_Employe()
            auteur.nom_complet = "SYSTEM"
            auteur.id = None

            devise = dao_devise.toGetDeviseByCodeIso("XAF")
            # annee_fiscale = Model_Annee_fiscale.objects.get(designation = "Fisc 2021")
            annee_fiscale = Model_Annee_fiscale.objects.get(est_active = True)
            taux = dao_taux_change.toGetTauxCourantDeLaDeviseArrive(devise.id)
            print("Devise: {} ---- Periode: {} ---- Taux: {}".format(devise.designation, annee_fiscale, taux))
            for i in df.index:
                desig = str(df['desc'][i])

            designation = "Balance {} {}".format(desig, annee_fiscale.date_fin.strftime('%Y'))
            #  designation = "Mouvement Balance_JAN_DEC_2021"
            reference = 'REP00' + annee_fiscale.date_fin.strftime('%Y')

            partenaire_id = None
            montant = 0
            description = ""
            journal_id = None
            date_piece = annee_fiscale.date_debut


            piece_comptable = dao_piece_comptable.toCreatePieceComptable(designation, reference, montant, journal_id, date_piece, partenaire_id, None, None, None, "", devise.id)
            if taux != None: piece_comptable.taux_id = taux.id
            piece_comptable = dao_piece_comptable.toSavePieceComptable(auteur, piece_comptable)

            for i in df.index:
                date_piece = str(df['periode'][i])

            #SAVE ANNEE FISCALE EN COURS
            piece_comptable.fisc_id = annee_fiscale.id
            piece_comptable.date_piece = date_piece
            piece_comptable.save()
            print(piece_comptable)

            montant_test_debit = 0
            montant_test_credit = 0

            for i in df.index:
                print("montant_debit: {}".format(df['montant_debit'][i]))
                print("montant_credit: {}".format(df['montant_credit'][i]))
                montant_debit = makeFloat(df['montant_debit'][i])
                montant_credit = makeFloat(df['montant_credit'][i])
                print("montant_debit (makeFloat): {}".format(montant_debit))
                print("montant_credit (makeFloat): {}".format(montant_credit))
                montant_test_debit += montant_debit
                montant_test_credit += montant_credit

            print("montant_test_debit: {}".format(montant_test_debit))
            print("montant_test_credit: {}".format(montant_test_credit))
            #raise Exception("Surprise! C etait juste un test")

            if montant_test_credit != montant_test_debit:
                raise Exception('Les écritures saisies ne sont pas équilibrées!')


            for i in df.index:
                compte_id = int(i)
                numero = str(df['numero'][i])
                numero = dao_compte.toGetNumeroCompteArrondi(numero)
                designation = str(df['designation'][i])
                desc = str(df['desc'][i])
                #check si le numéro
                compte = dao_compte.toGetCompteDuNumero(numero)
                if compte == None:
                    #On crée un nouveau compte comme le compte n'existe pas
                    type_compte = dao_type_compte.toGetTypeCompteRecevable()
                    permet_reconciliation = False

                    compte = dao_compte.toCreateCompte(numero, designation, type_compte.id, permet_reconciliation, "", None, 0)
                    compte = dao_compte.toSaveCompte(auteur, compte)
                compte_id = compte.id

                libelle = "Balance {} {}".format(desc, annee_fiscale.date_fin.strftime('%Y'))
                montant_debit = makeFloat(df['montant_debit'][i])
                montant_credit = makeFloat(df['montant_credit'][i])
                solde = montant_debit - montant_credit

                print("Compte Numero {}".format(numero))
                print("Compte ID {}".format(compte_id))
                print("Piece comptable {}".format(piece_comptable))

                if solde != 0:
                    ecriture_comptable = dao_ecriture_comptable.toCreateEcritureComptable(libelle, montant_debit, montant_credit, compte_id, piece_comptable.id, None, None, annee_fiscale.id)
                    ecriture_comptable = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_comptable)
                    print("Ecriture comptable ID {} || debit: {} || credit: {} cree".format(ecriture_comptable.id, ecriture_comptable.montant_debit, ecriture_comptable.montant_credit))

                    #if ecriture_comptable.montant_debit != montant_debit or ecriture_comptable.montant_credit != montant_credit:
                        #raise Exception("Les montant enregistres ne correspond pas avec ceux du fichier Excel {} / {}".format(montant_debit, montant_credit))
                elif solde == 0 and (montant_debit > 0 or montant_credit > 0):
                    ecriture_comptable = dao_ecriture_comptable.toCreateEcritureComptable(libelle, montant_debit, 0, compte_id, piece_comptable.id, None, None, annee_fiscale.id)
                    ecriture_comptable = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_comptable)
                    print("Ecriture comptable ID {} || debit: {} || credit: {} cree".format(ecriture_comptable.id, ecriture_comptable.montant_debit, ecriture_comptable.montant_credit))

                    ecriture_comptable = dao_ecriture_comptable.toCreateEcritureComptable(libelle, 0, montant_credit, compte_id, piece_comptable.id, None, None, annee_fiscale.id)
                    ecriture_comptable = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_comptable)
                    print("Ecriture comptable ID {} || debit: {} || credit: {} cree".format(ecriture_comptable.id, ecriture_comptable.montant_debit, ecriture_comptable.montant_credit))

                    #if ecriture_comptable.montant_debit != montant_debit or ecriture_comptable.montant_credit != montant_credit:
                        #raise Exception("Les montant enregistres ne correspond pas avec ceux du fichier Excel {} / {}".format(montant_debit, montant_credit))
            transaction.savepoint_commit(sid)
        else: print("Fichier Excel non trouvé")
    except Exception as e:
        print("ERREUR IMPORT COMPTES COMPTABLE")
        print(e)
        transaction.savepoint_rollback(sid)

