
from __future__ import unicode_literals

from ErpBackOffice.models import Model_EcritureComptable
from ModuleComptabilite.dao.dao_annee_fiscale import dao_annee_fiscale
from django.utils import timezone

class dao_ecriture_comptable(object):
    id = 0
    designation = ""
    montant_debit = 0		
    montant_credit = 0		
    compte_id = 0
    piece_comptable_id = None
    lettrage_id = None
    annee_fiscale_id = None
    date_echeance = None

    @staticmethod
    def toListEcrituresComptables():
        return Model_EcritureComptable.objects.all().order_by("-date_creation")

    @staticmethod
    def toListEcrituresComptablesInPeriode(date_debut, date_fin):
        try:
            return Model_EcritureComptable.objects.filter(piece_comptable__date_piece__range = [date_debut, date_fin], annee_fiscale__est_active = True).order_by("-date_creation")
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return []

    @staticmethod
    def toListEcrituresComptablesOfPieceComptable(piece_comptable_id):
        try:
            return Model_EcritureComptable.objects.filter(piece_comptable_id = piece_comptable_id).order_by("-date_creation")
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return []

    @staticmethod
    def toListEcrituresComptablesOfPieceComptableInPeriode(piece_comptable_id, date_debut, date_fin):
        try:
            return Model_EcritureComptable.objects.filter(piece_comptable_id = piece_comptable_id, piece_comptable__date_piece__range = [date_debut, date_fin]).order_by("-date_creation")
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return []

    @staticmethod
    def toListEcrituresComptablesDuCompte(compte_id):
        try:
            return Model_EcritureComptable.objects.filter(compte_id = compte_id, annee_fiscale__est_active = True).order_by("-date_creation")
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return []

    @staticmethod
    def toListEcrituresComptablesDuCompteInPeriode(compte_id, date_debut, date_fin):
        try:
            return Model_EcritureComptable.objects.filter(compte_id = compte_id, annee_fiscale__est_active = True, piece_comptable__date_piece__range = [date_debut, date_fin]).order_by("-date_creation")
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return []
        
    @staticmethod
    def toListEcrituresDuCompteInPeriode(compte_id, date_debut, date_fin):
        try:
            date_debut = date_debut.replace(hour=23, minute=59, second=59)
            return Model_EcritureComptable.objects.filter(compte_id = compte_id, piece_comptable__date_piece__range = [date_debut, date_fin]).order_by("-date_creation")
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return []
        
    @staticmethod
    def toListEcrituresDuCompteBeforePeriode(compte_id, date_debut):
        try:
            date_debut = date_debut.replace(hour=23, minute=59, second=59)
            return Model_EcritureComptable.objects.filter(compte_id = compte_id, annee_fiscale__est_active = True, piece_comptable__date_piece__lte = date_debut).order_by("-date_creation")
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return []

    @staticmethod
    def toCreateEcritureComptable(designation, montant_debit, montant_credit, compte_id, piece_comptable_id, lettrage_id=None, date_echeance = None, annee_fiscale_id=None):        
        try:
            ecriture_comptable = dao_ecriture_comptable()
            ecriture_comptable.designation = designation
            ecriture_comptable.montant_debit = montant_debit
            ecriture_comptable.montant_credit = montant_credit
            ecriture_comptable.compte_id = compte_id
            ecriture_comptable.piece_comptable_id = piece_comptable_id
            ecriture_comptable.lettrage_id = lettrage_id
            ecriture_comptable.date_echeance = date_echeance
            ecriture_comptable.annee_fiscale_id = annee_fiscale_id
            return ecriture_comptable
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE L'ECRITURE")
            #print(e)
            return None

    @staticmethod
    def toSaveEcritureComptable(object_dao_ecriture_comptable):
        try:
            ecriture_comptable = Model_EcritureComptable()
            ecriture_comptable.designation = object_dao_ecriture_comptable.designation
            ecriture_comptable.montant_debit = object_dao_ecriture_comptable.montant_debit
            ecriture_comptable.montant_credit = object_dao_ecriture_comptable.montant_credit
            ecriture_comptable.compte_id = object_dao_ecriture_comptable.compte_id
            ecriture_comptable.lettrage_id = object_dao_ecriture_comptable.lettrage_id
            ecriture_comptable.date_creation = timezone.now()
            ecriture_comptable.piece_comptable_id = object_dao_ecriture_comptable.piece_comptable_id
            if object_dao_ecriture_comptable.date_echeance != None:
                ecriture_comptable.date_echeance = object_dao_ecriture_comptable.date_echeance
            #Année fiscale
            if object_dao_ecriture_comptable.annee_fiscale_id == None:
                ecriture_comptable.annee_fiscale = dao_annee_fiscale.toGetAnneeFiscaleActive()
            else: ecriture_comptable.annee_fiscale_id = object_dao_ecriture_comptable.annee_fiscale_id

            ecriture_comptable.save()
            return ecriture_comptable
        except Exception as e:
            #print("ERREUR LORS DE L'ENREGISTREMENT DE L'ECRITURE")
            #print(e)
            return None

    @staticmethod
    def toUpdateEcritureComptable(id, object_dao_ecriture_comptable):
        try:
            ecriture_comptable = Model_EcritureComptable.objects.get(pk = id)
            ecriture_comptable.designation = object_dao_ecriture_comptable.designation
            ecriture_comptable.montant_debit = object_dao_ecriture_comptable.montant_debit
            ecriture_comptable.montant_credit = object_dao_ecriture_comptable.montant_credit
            ecriture_comptable.compte_id = object_dao_ecriture_comptable.compte_id
            ecriture_comptable.lettrage_id = object_dao_ecriture_comptable.lettrage_id
            ecriture_comptable.piece_comptable_id = object_dao_ecriture_comptable.piece_comptable_id
            ecriture_comptable.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU UPDATE DE L'ECRITURE")
            #print(e)
            return False

    @staticmethod
    def toDeleteEcritureComptable(id):
        try:
            ecriture_comptable = Model_EcritureComptable.objects.get(pk = id)
            ecriture_comptable.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION")
            #print(e)
            return False

    @staticmethod
    def toGetEcritureComptable(id):
        try:
            return Model_EcritureComptable.objects.get(pk = id)
        except Exception as e:
            return None
    

    @staticmethod
    def toAgregateEcritureComptable(list_ecriture_comptable):
        
        solved_list = []
        for i in range (0, len(list_ecriture_comptable)):
            for j in range (i+1, len(list_ecriture_comptable)):
                if list_ecriture_comptable[i]['id'] == list_ecriture_comptable[j]['id']:
                    list_ecriture_comptable[i]['montant']+= list_ecriture_comptable[j]['montant']
            find = False
            for a in solved_list:
                if a['id'] == list_ecriture_comptable[i]['id']:
                    find = True
            if not find:
                solved_list.append(list_ecriture_comptable[i])

        return solved_list
    
    @staticmethod
    def toListEcrituresComptablesOfAccount(compte_id, date_debut, date_fin):
        try:
            ecritures = []
            montant_debit = 0
            montant_credit = 0
            ecriture = Model_EcritureComptable.objects.filter(compte_id = compte_id).filter(date_creation__lte = date_debut, date_creation__gte = date_fin).order_by("-date_creation")
            for unecriture in ecriture:
                montant_debit += unecriture.montant_debit
                montant_credit += unecriture.montant_credit
                ecritures.append(unecriture)
                

            return ecritures, montant_debit, montant_credit
        except Exception as e:
            print("ERREUR")
            print(e)
            return [],0,0
    
    @staticmethod
    def toListEcrituresComptablesOfAccountPosteBudgetaire(lignes_poste_budgetaire, date_debut, date_fin):
        try:
            ecritures = []
            montant_debit = 0
            montant_credit = 0
            for ligne in lignes_poste_budgetaire:
                ecriture = Model_EcritureComptable.objects.filter(compte_id = ligne.compte_id).filter(date_creation__lte = date_debut, date_creation__gte = date_fin).order_by("-date_creation")
                for unecriture in ecriture:
                    print("ecr",unecriture)
                    montant_debit += unecriture.montant_debit
                    montant_credit += unecriture.montant_credit
                    ecritures.append(unecriture)
                

            return ecritures, montant_debit, montant_credit
        except Exception as e:
            print("ERREUR")
            print(e)
            return [],0,0