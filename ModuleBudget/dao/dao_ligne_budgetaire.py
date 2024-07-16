from __future__ import unicode_literals
from ErpBackOffice.models import Model_LigneBudgetaire, Model_Transactionbudgetaire
from django.db.models import Max, Sum
from django.utils import timezone
from ModuleBudget.dao.dao_exercicebudgetaire import dao_exercicebudgetaire


def verify_id(value):
    if value == 0 or value == "0":
        return None
    else:
        return value

class dao_ligne_budgetaire(object):
    id = 0
    code = ""
    responsable_id 	= None
    designation = ""
    entite = ""
    compte_id = None
    nature_activite = 0
    centre_cout_id = None
    activite_id = None
    nature_charge = ""
    localite = ""
    budget_id = None
    pourcentage_alert = 0.0
    message_alert = ""
    correspondant_id = None
    type = ""
    is_bloqued = False


    @staticmethod
    def toCreateLigneBudgetaire(code, designation, budget_id, responsable_id = None, entite = "1", compte_id = None, nature_activite = 0, centre_cout_id = "", activite_id = None, nature_charge = 0, localite = 0, pourcentage_alert = 0.0, message_alert = "", type = "", is_bloqued = False):
        try:
            ligne = dao_ligne_budgetaire()
            ligne.code = code
            ligne.entite = entite
            ligne.compte_id = verify_id(compte_id)
            ligne.nature_activite = nature_activite
            ligne.centre_cout_id = verify_id(centre_cout_id)
            ligne.activite_id = verify_id(activite_id)
            ligne.nature_charge = nature_charge
            ligne.localite = localite
            ligne.designation = designation
            ligne.budget_id = verify_id(budget_id)
            ligne.responsable_id = verify_id(responsable_id)
            ligne.pourcentage_alert = pourcentage_alert
            ligne.message_alert = message_alert
            ligne.is_bloqued = is_bloqued
            ligne.type = type

            return ligne
        except Exception as e:
            # print("ERREUR LORS DE LA CREATION DE LA LIGNE BUDGETAIRE")
            # print(e)
            return None

    @staticmethod
    def toSaveLigneBudgetaire(auteur, objet_dao_ligne_budgetaire):
        try :
            ligne = Model_LigneBudgetaire()
            ligne.code = objet_dao_ligne_budgetaire.code
            ligne.designation = objet_dao_ligne_budgetaire.designation
            ligne.entite = objet_dao_ligne_budgetaire.entite
            ligne.compte_id = objet_dao_ligne_budgetaire.compte_id
            ligne.nature_activite = objet_dao_ligne_budgetaire.nature_activite
            ligne.centre_cout_id = objet_dao_ligne_budgetaire.centre_cout_id
            ligne.activite_id = objet_dao_ligne_budgetaire.activite_id
            ligne.localite = objet_dao_ligne_budgetaire.localite
            ligne.budget_id = objet_dao_ligne_budgetaire.budget_id
            ligne.responsable_id = objet_dao_ligne_budgetaire.responsable_id
            ligne.pourcentage_alert = objet_dao_ligne_budgetaire.pourcentage_alert
            ligne.message_alert = objet_dao_ligne_budgetaire.message_alert
            ligne.type = objet_dao_ligne_budgetaire.type
            ligne.is_bloqued = objet_dao_ligne_budgetaire.is_bloqued
            ligne.auteur_id = auteur.id

            ligne.save()
            return ligne
        except Exception as e:
            # print("ERREUR SAVE LIGNE BUDGETAIRE")
            # print(e)
            return None

    @staticmethod
    def toUpdateLigneBudgetaire(id, objet_dao_ligne_budgetaire):
        try:
            ligne = Model_LigneBudgetaire.objects.get(pk = id)
            ligne.code = objet_dao_ligne_budgetaire.code
            ligne.designation = objet_dao_ligne_budgetaire.designation
            ligne.budget_id = objet_dao_ligne_budgetaire.budget_id
            ligne.responsable_id = objet_dao_ligne_budgetaire.responsable_id
            ligne.auteur = objet_dao_ligne_budgetaire.auteur

            ligne.save()
            return True
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return False

    @staticmethod
    def toGetLigneBudgetaire(id):
        try:
            return Model_LigneBudgetaire.objects.get(pk = id)
        except Exception as e:
            return None

    @staticmethod
    def toGetLigneBudgetaireBudgetDepense():
        try:
            exercice = dao_exercicebudgetaire.toGetActiveExercicebudgetaire()
            ligne = Model_LigneBudgetaire.objects.filter(budget__categoriebudget__type = 2,exericebudgetaires__id=exercice.id)
            return ligne
        except Exception as e:
            return None

    @staticmethod
    def toGetLigneBudgetaireBudgetRecette():
        try:
            exercice = dao_exercicebudgetaire.toGetActiveExercicebudgetaire()
            ligne = Model_LigneBudgetaire.objects.filter(budget__categoriebudget__type = 1, exericebudgetaires__id=exercice.id)
            return ligne
        except Exception as e:
            return None

    @staticmethod
    def toGetLigneBudgetaireByCombinaison(code):
        try:
            return Model_LigneBudgetaire.objects.filter(code = code).first()

        except Exception as e:
            return []


    @staticmethod
    def toDeleteLigneBudgetaire(id):
        try:
            ligne = Model_LigneBudgetaire.objects.get(pk = id)
            ligne.delete()
            return True
        except Exception as e:
            return False

    @staticmethod
    def toListLigneBudgetaires():
        try:
            lignes = Model_LigneBudgetaire.objects.all().order_by('-id')
            return lignes
        except Exception as e:
            return []

    @staticmethod
    def toListLigneBudgetairesExerciceON():
        try:
            exercice = dao_exercicebudgetaire.toGetActiveExercicebudgetaire()
            if exercice:
                lignes = Model_LigneBudgetaire.objects.filter(exericebudgetaires__id = exercice.id).order_by('-id')
                return lignes
            else: return []
        except Exception as e:
            return []

    @staticmethod
    def toListLigneBudgetairesofExeciceEncours():
        try:
            Combine = []
            LignesBudgetaire = []
            exercice = dao_exercicebudgetaire.toGetActiveExercicebudgetaire()
            exeid = exercice.id
            lignes = Model_LigneBudgetaire.objects.all()
            for item in lignes:
                transactions = Model_Transactionbudgetaire.objects.filter(exercice_budgetaire__id=exeid,ligne_budgetaire=item)
                for ele in transactions:
                    if ele.ligne_budgetaire.id not in Combine:
                        Combine.append(ele.ligne_budgetaire.id)

            # print('**Montre moi la combine', Combine)
            for item in Combine:
                laligne = dao_ligne_budgetaire.toGetLigneBudgetaire(item)
                LignesBudgetaire.append(laligne)

            # print('**Montre moi la combinaison', LignesBudgetaire)
            return LignesBudgetaire
        except Exception as e:
            # print(e)
            return []

    @staticmethod
    def toSendTransactionB(exercice, ligne):
        try:
            transactions = Model_Transactionbudgetaire.objects.filter(exercice_budgetaire__id=exercice,ligne_budgetaire=ligne)
            return transactions
        except Exception as e:
            return None

    @staticmethod
    def toListLigneBudgetaireReport():
        try:
            lignes = Model_LigneBudgetaire.objects.filter(is_reportable = True).order_by('-id')
            return lignes
        except Exception as e:
            return None

    @staticmethod
    def toListLigneOfBudgets(id):
        try:
            exercice = dao_exercicebudgetaire.toGetActiveExercicebudgetaire()
            lignes = Model_LigneBudgetaire.objects.filter(budget = id, exericebudgetaires__id=exercice.id)
            return lignes
        except Exception as e:
            return None

    @staticmethod
    def toListLigneBudgetsProjets():
        try:
            lignes = Model_LigneBudgetaire.objects.filter(type = 2)
            return lignes
        except Exception as e:
            return None

    @staticmethod
    def toGetLigneOfCode(code):
        try:
            ligne = Model_LigneBudgetaire.objects.filter(code = code).first()
            return ligne
        except Exception as e:
            return None

    @staticmethod
    def toListPropositionByCompteComptable(numero_compte):
        try:
            result = []

            lignes = Model_LigneBudgetaire.objects.all()
            for ligne in lignes:
                item = {}
                # print(ligne.compte.numero, numero_compte)
                if numero_compte[:3] in ligne.compte.numero:
                    item = {'id': ligne.id, 'code': ligne.code, 'intitule': ligne.designation, 'budget':ligne.budget.designation, 'compte_comptable': ligne.compte.numero}
                    result.append(item)
            return result
        except Exception as e:
            # print(e)
            return []



    @staticmethod
    def toComputeValueOfLigneBudgetaireForExerciceBudgetaire(id, exercice_budgetaire_id):
        ligne = Model_LigneBudgetaire.objects.get(pk = id)
        resultat = {
                'id': ligne.id,
				'code':ligne.code,
				'designation': ligne.designation,
				# 'budget':ligne.budget.designation,
                'dotation':0,
                'rallonge':0,
                'diminution':0,
				'normal':0,
				'solde':0,
                'is_reportable':ligne.is_reportable,
                }
        try:
            dotation = 0
            rallonge = 0
            diminution = 0
            normal = 0

            transactions = Model_Transactionbudgetaire.objects.filter(exercice_budgetaire_id = exercice_budgetaire_id).filter(ligne_budgetaire = ligne)

            for transaction in transactions:
                #print(transaction.montant)
                if transaction.typetransactionbudgetaire == 1:
                    #print("un")
                    normal += transaction.montant
                elif transaction.typetransactionbudgetaire == 2:
                    #print("deux")
                    rallonge += transaction.montant
                elif transaction.typetransactionbudgetaire == 3:
                    #print("trois")
                    diminution += transaction.montant
                elif transaction.typetransactionbudgetaire == 4:
                    #print("quatre")
                    dotation += transaction.montant


            resultat['dotation'] = dotation
            resultat['rallonge'] = rallonge
            resultat['diminution'] = diminution
            resultat['normal'] = normal
            resultat['solde'] = dotation + rallonge - diminution - normal

            return  resultat
        except Exception as e:
            #print("Erreur lors du calcul")
            #print(e)
            return resultat


    @staticmethod
    def toComputeValeur(ligne_budgetaire_id):
        montant = 0
        try:
            #print("likolo")
            transactions = Model_Transactionbudgetaire.objects.filter(ligne_budgetaire_id = ligne_budgetaire_id ).filter(status=2).exclude(typetransactionbudgetaire=2).filter(exercice_budgetaire__is_active = True).exclude(typetransactionbudgetaire=4).aggregate(reel=Sum('montant'))
            print("transaction", transactions)
            if transactions["reel"] != None:
                return transactions["reel"]
            return 0
        except Exception as e:
            # print('Erreur valeur_reel(): {}'.format(e))
            return 0

    @staticmethod
    def toSetUserConfirmationOfBlocusLigneBudgetaire(ligne_id, employe_id):
        try:
            ligne = dao_ligne_budgetaire.toGetLigneBudgetaire(ligne_id)
            ligne.user_confirmation_id = employe_id
            ligne.is_waiting_confirmation = True
            ligne.save()
            return ligne
        except Exception as e:
            return None



    @staticmethod
    def toCheckCompteComptable(compte_id):
        try:
            find = False
            lignes = Model_LigneBudgetaire.objects.all().order_by('-id')
            for ligne in lignes:
                if ligne.compte_id == compte_id:
                    find = True
            return find
        except Exception as e:
            return False

    @staticmethod
    def toGetReportLignebudgetaire(id):
        try:
            Ligne = Model_LigneBudgetaire.objects.get(pk = id)
            Ligne.is_reportable = True
            Ligne.save()
            return Ligne
        except Exception as e:
			#print(e)
            return None

    @staticmethod
    def toDesactiveReportLignebudgetaire(id):
        try:
            Ligne = Model_LigneBudgetaire.objects.get(pk = id)
            Ligne.is_reportable = False
            Ligne.save()
            return Ligne
        except Exception as e:
			#print(e)
            return None
