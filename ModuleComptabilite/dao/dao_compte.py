from __future__ import unicode_literals
from ErpBackOffice.models import Model_Compte
from ModuleComptabilite.dao.dao_config_comptabilite import dao_config_comptabilite
from django.utils import timezone


class dao_compte(object):
    id = 0
    numero = ""
    designation = ""
    type_compte_id = None
    devise_id = None
    permet_reconciliation = False
    description = ""
    balance = 0
    est_obsolete = False
    origine = 1
    auteur_id = None

    @staticmethod
    def toCreateCompte(numero, designation, type_compte_id, permet_reconciliation = False, description = "", devise_id = 0, balance = 0):
        try:
            compte = dao_compte()
            compte.numero = numero
            compte.designation = designation
            compte.permet_reconciliation = permet_reconciliation
            compte.type_compte_id = type_compte_id
            if devise_id != 0 :
                compte.devise_id = devise_id
            compte.description = description
            compte.balance = balance
            return compte
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DU COMPTE")
            #print(e)
            return None

    @staticmethod
    def toSaveCompte(auteur, objet_dao_compte):
        try:
            compte = Model_Compte()
            if len(objet_dao_compte.numero) > 3:
                numero_compte = str(objet_dao_compte.numero)
                #Pour les entreprises qui utilisent les comptes de mouvement à plus de 6 chiffres
                digit = dao_config_comptabilite.toGetDigitCompte()
                if len(numero_compte) < digit: 
                    nbre_zero = int(digit) - int(len(numero_compte))
                    for i in range(0, nbre_zero): numero_compte += "0"  
                compte.numero = numero_compte                          
            else: compte.numero = objet_dao_compte.numero	
            compte.designation = objet_dao_compte.designation
            compte.permet_reconciliation = objet_dao_compte.permet_reconciliation
            compte.type_compte_id = objet_dao_compte.type_compte_id
            compte.devise_id = objet_dao_compte.devise_id
            compte.description = objet_dao_compte.description
            compte.auteur_id = auteur.id
            compte.balance = objet_dao_compte.balance
            compte.origine = 2
            compte.save()
            return compte
        except Exception as e:
            #print("ERREUR LORS DU SAVE DU COMPTE")
            #print(e)
            return None

    @staticmethod
    def toUpdateCompte(id, objet_dao_compte):
        try:
            compte = Model_Compte.objects.get(pk = id)
            #print('je suis id dao compte %s'%(id))
            compte.numero = objet_dao_compte.numero	
            compte.designation =	objet_dao_compte.designation
            #print('designation %s' % (compte.designation))
            compte.permet_reconciliation = objet_dao_compte.permet_reconciliation
            compte.type_compte_id	= objet_dao_compte.type_compte_id
            compte.devise_id = objet_dao_compte.devise_id
            compte.description = objet_dao_compte.description
            compte.balance = objet_dao_compte.balance
            #print('save')
            compte.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU UPDATE DU COMPTE")
            #print(e)
            return None
        
    @staticmethod
    def toGetCompte(id):
        try:
            return Model_Compte.objects.get(pk = id)
        except Exception as e:
            return None

    @staticmethod
    def toGetCompteDuNumero(numero):
        try:
            return Model_Compte.objects.get(numero = numero)
        except Exception as e:
            #print(e)
            return None

    @staticmethod
    def toDeleteCompte(id):
        try:
            compte = Model_Compte.objects.get(pk = id)
            compte.delete()
            return True
        except Exception as e:
            return False
        
    @staticmethod
    def toListComptes():
        try:
            list = []
            comptes = Model_Compte.objects.all().order_by("numero")
            #Pour les entreprises qui utilisent les comptes de mouvement à plus de 6 chiffres
            digit = dao_config_comptabilite.toGetDigitCompte()
            for item in comptes:
                if len(item.numero) == digit: list.append(item)
            return list
        except Exception as e:
            #print("ERREUR LORS DE LA LECTURE DES COMPTES POUR ECRITURES")
            return []
        
    @staticmethod
    def toListComptesClient():
        try:
            list = []
            comptes = Model_Compte.objects.all().order_by("numero")
            #Pour les entreprises qui utilisent les comptes de mouvement à plus de 6 chiffres
            digit = dao_config_comptabilite.toGetDigitCompte()
            for item in comptes:
                if len(item.numero) == digit and item.numero[0:3] == "411": list.append(item)
            return list
        except Exception as e:
            #print("ERREUR LORS DE LA LECTURE DES COMPTES CLIENTS")
            return []
        
    @staticmethod
    def toListComptesFournisseur():
        try:
            list = []
            comptes = Model_Compte.objects.all().order_by("numero")
            #Pour les entreprises qui utilisent les comptes de mouvement à plus de 6 chiffres
            digit = dao_config_comptabilite.toGetDigitCompte()
            for item in comptes:
                if len(item.numero) == digit and item.numero[0:3] == "401": list.append(item)
            return list
        except Exception as e:
            #print("ERREUR LORS DE LA LECTURE DES COMPTES FOURNISSEURS")
            return []
        
    @staticmethod
    def toListComptesAffichage():
        try:
            return Model_Compte.objects.all().order_by("numero")
        except Exception as e:
            #print("ERREUR LORS DE LA LECTURE DES COMPTES POUR AFFICHAGE")
            return []
        
    @staticmethod
    def toListComptesDeClasse(int_classe):
        try:
            list = []
            if int_classe <= 5: comptes = Model_Compte.objects.all().order_by("numero")
            else: comptes = Model_Compte.objects.all().order_by("-numero")
            
            for item in comptes:
                if len(item.numero) == 6 and int(item.numero[0]) == int_classe: list.append(item)
            return list
        except Exception as e:
            #print("ERREUR LORS DE LA LECTURE DES COMPTES DE LA CLASSE %s" % int_classe)
            return []

    @staticmethod
    def toListComptesAvecLongueurDuNumero(int_longueur):
        try:
            list = []
            comptes = Model_Compte.objects.all().order_by("numero")
            for item in comptes:
                if len(item.numero) == int_longueur: list.append(item)
            #print(list)
            return list
        except Exception as e:
            #print("ERREUR LORS DE LA LECTURE DES COMPTES DE NUMERO DE LA TAILLE %s" % int_longueur)
            return []
        
    @staticmethod
    def toListComptesOf(type_compte_id):
        try:
            return Model_Compte.objects.filter(type_compte_id = type_compte_id).order_by("numero")
        except Exception as e:
            #print("ERREUR LORS DE LA LECTURE DES COMPTES DU TYPE")
            return []


    @staticmethod
    def toSetCompteAchat(id):
        try:
            Model_Compte.objects.all().update(achat_par_defaut = False)

            compte = dao_compte.toGetCompte(id)
            compte.achat_par_defaut = True
            compte.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU UPDATE")
            #print(e)
            return False


    @staticmethod
    def toSetCompteVente(id):
        try:
            Model_Compte.objects.all().update(vente_par_defaut = False)

            compte = dao_compte.toGetCompte(id)
            compte.vente_par_defaut = True
            compte.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU UPDATE")
            #print(e)
            return False

    @staticmethod
    def toSetCompteFournisseur(id):
        try:
            Model_Compte.objects.all().update(fournisseur_par_defaut = False)

            compte = dao_compte.toGetCompte(id)
            compte.fournisseur_par_defaut = True
            compte.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU UPDATE")
            #print(e)
            return False

    @staticmethod
    def toSetCompteClient(id):
        try:
            Model_Compte.objects.all().update(client_par_defaut = False)

            compte = dao_compte.toGetCompte(id)
            compte.client_par_defaut = True
            compte.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU UPDATE")
            #print(e)
            return False

    @staticmethod
    def toSetCompteTaxe(id):
        try:
            Model_Compte.objects.all().update(taxe_par_defaut = False)

            compte = dao_compte.toGetCompte(id)
            compte.taxe_par_defaut = True
            compte.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU UPDATE")
            #print(e)
            return False

    @staticmethod
    def toSetCompteCaisse(id):
        try:
            Model_Compte.objects.all().update(caisse_par_defaut = False)

            compte = dao_compte.toGetCompte(id)
            compte.caisse_par_defaut = True
            compte.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU UPDATE")
            #print(e)
            return False

    @staticmethod
    def toSetCompteBanque(id):
        try:
            Model_Compte.objects.all().update(banque_par_defaut = False)

            compte = dao_compte.toGetCompte(id)
            compte.banque_par_defaut = True
            compte.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU UPDATE")
            #print(e)
            return False

            
    @staticmethod
    def toSetCompteMarchandise(id):
        try:
            Model_Compte.objects.all().update(marchandise_par_defaut = False)

            compte = dao_compte.toGetCompte(id)
            compte.marchandise_par_defaut = True
            compte.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU UPDATE")
            #print(e)
            return False

    @staticmethod
    def toSetCompteLiaison(id):
        try:
            Model_Compte.objects.all().update(liaison_par_defaut = False)

            compte = dao_compte.toGetCompte(id)
            compte.liaison_par_defaut = True
            compte.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU UPDATE")
            #print(e)
            return False

    @staticmethod
    def toSetComptePersonnel(id):
        try:
            Model_Compte.objects.all().update(personnel_par_defaut = False)

            compte = dao_compte.toGetCompte(id)
            compte.personnel_par_defaut = True
            compte.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU UPDATE")
            #print(e)
            return False

    @staticmethod
    def toSetCompteSalaire(id):
        try:
            Model_Compte.objects.all().update(salaire_par_defaut = False)

            compte = dao_compte.toGetCompte(id)
            compte.salaire_par_defaut = True
            compte.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU UPDATE")
            #print(e)
            return False

    @staticmethod
    def toGetCompteVente():
        try:
            return Model_Compte.objects.get(vente_par_defaut = True)
        except Exception as e:
            return None

    @staticmethod
    def toGetCompteAchat():
        try:
            return Model_Compte.objects.get(achat_par_defaut = True)
        except Exception as e:
            return None

    @staticmethod
    def toGetCompteFournisseur():
        #print("DEBUT COMPTE PAR DEFAULT")
        try:
            #print("DEBUT TRY COMPTE PAR DEFAULT")
             
            compte = Model_Compte.objects.get(fournisseur_par_defaut = True)
            #print("COMPTE = %s" % compte)
            return compte
        except Exception as e:
            #print("ERREUR COMPTE PAR DEFAULT")
            #print(e)
            return None

    @staticmethod
    def toGetCompteClient():
        try:
            return Model_Compte.objects.get(client_par_defaut = True)
        except Exception as e:
            return None

    @staticmethod
    def toGetCompteTaxe():
        try:
            return Model_Compte.objects.get(taxe_par_defaut = True)
        except Exception as e:
            return None

    @staticmethod
    def toGetCompteCaisse():
        try:
            return Model_Compte.objects.get(caisse_par_defaut = True)
        except Exception as e:
            return None

    @staticmethod
    def toGetCompteBanque():
        try:
            return Model_Compte.objects.get(banque_par_defaut = True)
        except Exception as e:
            return None

    @staticmethod
    def toGetCompteMarchandise():
        try:
            return Model_Compte.objects.get(marchandise_par_defaut = True)
        except Exception as e:
            return None

    @staticmethod
    def toGetCompteLiaison():
        try:
            return Model_Compte.objects.get(liaison_par_defaut = True)
        except Exception as e:
            return None

    @staticmethod
    def toGetComptePersonnel():
        try:
            return Model_Compte.objects.get(personnel_par_defaut = True)
        except Exception as e:
            return None

    @staticmethod
    def toGetCompteSalaire():
        try:
            return Model_Compte.objects.get(salaire_par_defaut = True)
        except Exception as e:
            return None
        
    def toGetNumeroCompteArrondi(numero):
        try:
            numero_compte = str(numero)
            if len(numero_compte) > 3:
                #Pour les entreprises qui utilisent les comptes de mouvement à plus de 6 chiffres
                digit = dao_config_comptabilite.toGetDigitCompte()
                if len(numero_compte) < digit: 
                    nbre_zero = int(digit) - int(len(numero_compte))
                    for i in range(0, nbre_zero): numero_compte += "0"  
            return numero_compte
        except Exception as e:
            return numero
