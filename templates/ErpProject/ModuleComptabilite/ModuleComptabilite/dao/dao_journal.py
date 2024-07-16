from __future__ import unicode_literals
from ErpBackOffice.models import Model_Journal
from django.utils import timezone


class dao_journal(object):
    id = 0
    code = ""
    designation = ""
    type_journal = 0
    devise_id = None
    est_affiche = False
    compte_debit_id = None
    compte_credit_id = None
    auteur_id = None

    @staticmethod
    def toCreateJournal(code, designation, type_journal, est_affiche = False, compte_debit_id = 0, compte_credit_id = 0, devise_id = 0):
        try:
            journal = dao_journal()
            journal.code = code
            journal.designation = designation
            journal.est_affiche = est_affiche
            journal.type_journal = type_journal
            if devise_id != 0 :
                journal.devise_id = devise_id
            if compte_debit_id != 0:
                journal.compte_debit_id = compte_debit_id
            if compte_credit_id != 0:
                journal.compte_credit_id = compte_credit_id
            return journal
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DU JOURNAL")
            #print(e)
            return None

    @staticmethod
    def toSaveJournal(auteur, objet_dao_journal):
        try:
            journal = Model_Journal()
            journal.code = objet_dao_journal.code	
            journal.designation = objet_dao_journal.designation
            journal.est_affiche = objet_dao_journal.est_affiche
            journal.type_journal = objet_dao_journal.type_journal
            journal.devise_id = objet_dao_journal.devise_id
            journal.compte_debit_id = objet_dao_journal.compte_debit_id
            journal.compte_credit_id = objet_dao_journal.compte_credit_id
            journal.auteur_id = auteur.id
            journal.date_creation = timezone.now()
            journal.save()
            return journal
        except Exception as e:
            #print("ERREUR LORS DU SAVE DU JOURNAL")
            #print(e)
            return None

    @staticmethod
    def toUpdateJournal(id, objet_dao_journal):
        try:
            journal = Model_Journal.objects.get(pk = id)
            journal.code = objet_dao_journal.code	
            journal.designation =	objet_dao_journal.designation
            journal.est_affiche = objet_dao_journal.est_affiche
            journal.type_journal	= objet_dao_journal.type_journal
            journal.devise_id = objet_dao_journal.devise_id
            journal.compte_debit_id = objet_dao_journal.compte_debit_id
            journal.compte_credit_id = objet_dao_journal.compte_credit_id
            journal.save()
            return journal
        except Exception as e:
            #print("ERREUR LORS DU UPDATE DU JOURNAL")
            #print(e)
            return None
        
    @staticmethod
    def toGetJournal(id):
        try:
            return Model_Journal.objects.get(pk = id)
        except Exception as e:
            return None

    @staticmethod
    def toGetJournalDefautOf(type_journal):
        try:
            return Model_Journal.objects.filter(type_journal = type_journal).get(est_journal_par_defaut = True)
        except Exception as e:
            #print("ERREUR LORS DU SELECT")
            #print(e)
            return None

    @staticmethod
    def toSetJournalDefaut(id, type_journal):
        try:
            journal = dao_journal.toGetJournalDefautOf(type_journal)
            if journal != None:
                journal.est_journal_par_defaut = False
                journal.save()
            
            journal = dao_journal.toGetJournal(id)
            journal.type_journal = type_journal
            journal.est_journal_par_defaut = True
            journal.save()
            return True
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return False

    @staticmethod
    def toDeleteJournal(id):
        try:
            journal = Model_Journal.objects.get(pk = id)
            journal.delete()
            return True
        except Exception as e:
            return False
        
    @staticmethod
    def toListJournauxPaie():
        try:
            data = []

            journaux = Model_Journal.objects.filter(type_journal = 3)
            for item in journaux :
                data.append(item)

            journaux = Model_Journal.objects.filter(type_journal = 4)
            for item in journaux :
                data.append(item)

            return data
        except Exception as e:
            #print("ERREUR LORS DE LA LECTURE DES JOURNAUX")
            return []

    @staticmethod
    def toListJournaux():
        try:
            return Model_Journal.objects.all().order_by("designation")
        except Exception as e:
            #print("ERREUR LORS DE LA LECTURE DES JOURNAUX")
            return []
        
    @staticmethod
    def toListJournauxOf(type_journal):
        try:
            return Model_Journal.objects.filter(type_journal = type_journal).order_by("designation")
        except Exception as e:
            #print("ERREUR LORS DE LA LECTURE DES JOURNAUX DU TYPE")
            return []
        
    @staticmethod
    def toListJournauxDuDashboard():
        try:
            return Model_Journal.objects.filter(est_affiche = True).order_by("sequence")
        except Exception as e:
            #print("ERREUR LORS DE LA LECTURE DES JOURNAUX DU DASHBOARD")
            return []

    @staticmethod
    def toGetJournalVentes():
        try:
            journal = Model_Journal.objects.filter(type_journal = 1).order_by("designation").first()
            #print("journal ID {} recupere ".format(journal.id))
            return journal
        except Exception as e:
            #print("ERREUR LORS DE LA LECTURE DES JOURNAUX DU TYPE DIVERS")
            return None
        
    @staticmethod
    def toGetJournalAchats():
        try:
            journal = Model_Journal.objects.filter(type_journal = 2).order_by("designation").first()
            #print("journal ID {} recupere ".format(journal.id))
            return journal
        except Exception as e:
            #print("ERREUR LORS DE LA LECTURE DES JOURNAUX DU TYPE DIVERS")
            return None
        
    @staticmethod
    def toGetJournalBanque():
        try:
            journal = Model_Journal.objects.filter(type_journal = 3).order_by("designation").first()
            #print("journal ID {} recupere ".format(journal.id))
            return journal
        except Exception as e:
            #print("ERREUR LORS DE LA LECTURE DES JOURNAUX DU TYPE DIVERS")
            return None
        
    @staticmethod
    def toGetJournalCaisse():
        try:
            journal = Model_Journal.objects.filter(type_journal = 4).order_by("designation").first()
            #print("journal ID {} recupere ".format(journal.id))
            return journal
        except Exception as e:
            #print("ERREUR LORS DE LA LECTURE DES JOURNAUX DU TYPE DIVERS")
            return None
        
    @staticmethod
    def toGetJournalDivers():
        try:
            journal = Model_Journal.objects.filter(type_journal = 5).order_by("designation").first()
            #print("journal ID {} recupere ".format(journal.id))
            return journal
        except Exception as e:
            #print("ERREUR LORS DE LA LECTURE DES JOURNAUX DU TYPE DIVERS")
            return None