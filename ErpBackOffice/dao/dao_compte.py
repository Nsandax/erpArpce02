from __future__ import unicode_literals
from ErpBackOffice.models import Model_Compte, Model_TypeCompte
from django.utils import timezone


class dao_compte(object):
    id = 0
    numero_compte = ""
    designation = ""
    type_compte_id = None
    devise_id = None
    permet_reconciliation = False
    description = ""
    auteur_id = None

    @staticmethod
    def toCreateCompte(numero_compte, designation, type_compte_id, permet_reconciliation = False, description = "", devise_id = 0):
        try:
            compte = dao_compte()
            compte.numero_compte = numero_compte
            compte.designation = designation
            compte.permet_reconciliation = permet_reconciliation
            compte.type_compte_id = type_compte_id
            if devise_id != 0 :
                compte.devise_id = devise_id
            compte.description = description
            return compte
        except Exception as e:
	        #print("ERREUR LORS DE LA CREATION DU COMPTE")
	        #print(e)
	        return None

    @staticmethod
    def toSaveCompte(auteur, objet_dao_compte):
        try:
            compte = Model_Compte()
            compte.numero_compte = objet_dao_compte.numero_compte	
            compte.designation = objet_dao_compte.designation
            compte.permet_reconciliation = objet_dao_compte.permet_reconciliation
            compte.type_compte_id = objet_dao_compte.type_compte_id
            compte.devise_id = objet_dao_compte.devise_id
            compte.description = objet_dao_compte.description
            compte.auteur_id = auteur.id
            compte.creation_date = timezone.now()
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
            compte.numero_compte = objet_dao_compte.numero_compte	
            compte.designation =	objet_dao_compte.designation
            compte.permet_reconciliation = objet_dao_compte.permet_reconciliation
            compte.type_compte_id	= objet_dao_compte.type_compte_id
            compte.devise_id = objet_dao_compte.devise_id
            compte.description = objet_dao_compte.description
            compte.save()
            return compte
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
    def toGetCompteDuNumero(numero_compte):
        try:
            return Model_Compte.objects.get(numero_compte = numero_compte)
        except Exception as e:
            #print(e)
            return None

    @staticmethod
    def toGetCompteVente():
        try:
            return Model_Compte.objects.get(vente_par_defaut = True)
        except Exception as e:
            return None

    @staticmethod
    def toSetCompteVente(id):
        try:
            compte = dao_compte.toGetCompteVente()
            if compte != None:
                compte.vente_par_defaut = False
                compte.save()

            compte = dao_compte.toGetCompte(id)
            compte.vente_par_defaut = True
            compte.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU UPDATE")
            #print(e)
            return False

    @staticmethod
    def toGetCompteAchat():
        try:
            return Model_Compte.objects.get(achat_par_defaut = True)
        except Exception as e:
            return None

    @staticmethod
    def toSetCompteAchat(id):
        try:
            compte = dao_compte.toGetCompteAchat()
            if compte != None:
                compte.achat_par_defaut = False
                compte.save()

            compte = dao_compte.toGetCompte(id)
            compte.achat_par_defaut = True
            compte.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU UPDATE")
            #print(e)
            return False

    @staticmethod
    def toGetCompteFournisseur():
        try:
            return Model_Compte.objects.get(fournisseur_par_defaut = True)
        except Exception as e:
            return None

    @staticmethod
    def toSetCompteFournisseur(id):
        try:
            compte = dao_compte.toGetCompteFournisseur()
            if compte != None:
                compte.fournisseur_par_defaut = False
                compte.save()

            compte = dao_compte.toGetCompte(id)
            compte.fournisseur_par_defaut = True
            compte.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU UPDATE")
            #print(e)
            return False

    @staticmethod
    def toGetCompteClient():
        try:
            return Model_Compte.objects.get(client_par_defaut = True)
        except Exception as e:
            return None

    @staticmethod
    def toSetCompteClient(id):
        try:
            compte = dao_compte.toGetCompteClient()
            if compte != None:
                compte.client_par_defaut = False
                compte.save()

            compte = dao_compte.toGetCompte(id)
            compte.client_par_defaut = True
            compte.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU UPDATE")
            #print(e)
            return False

    @staticmethod
    def toGetCompteTaxe():
        try:
            return Model_Compte.objects.get(taxe_par_defaut = True)
        except Exception as e:
            return None

    @staticmethod
    def toSetCompteTaxe(id):
        try:
            compte = dao_compte.toGetCompteTaxe()
            if compte != None:
                compte.taxe_par_defaut = False
                compte.save()

            compte = dao_compte.toGetCompte(id)
            compte.taxe_par_defaut = True
            compte.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU UPDATE")
            #print(e)
            return False

    @staticmethod
    def toGetCompteCaisse():
        try:
            return Model_Compte.objects.get(caisse_par_defaut = True)
        except Exception as e:
            return None

    @staticmethod
    def toSetCompteCaisse(id):
        try:
            compte = dao_compte.toGetCompteCaisse()
            if compte != None:
                compte.caisse_par_defaut = False
                compte.save()

            compte = dao_compte.toGetCompte(id)
            compte.caisse_par_defaut = True
            compte.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU UPDATE")
            #print(e)
            return False

    @staticmethod
    def toGetCompteBanque():
        try:
            return Model_Compte.objects.get(banque_par_defaut = True)
        except Exception as e:
            return None

    @staticmethod
    def toSetCompteBanque(id):
        try:
            compte = dao_compte.toGetCompteBanque()
            if compte != None:
                compte.banque_par_defaut = False
                compte.save()

            compte = dao_compte.toGetCompte(id)
            compte.banque_par_defaut = True
            compte.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU UPDATE")
            #print(e)
            return False

    @staticmethod
    def toGetCompteMarchandise():
        try:
            return Model_Compte.objects.get(marchandise_par_defaut = True)
        except Exception as e:
            return None

    @staticmethod
    def toSetCompteMarchandise(id):
        try:
            compte = dao_compte.toGetCompteMarchandise()
            if compte != None:
                compte.marchandise_par_defaut = False
                compte.save()

            compte = dao_compte.toGetCompte(id)
            compte.marchandise_par_defaut = True
            compte.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU UPDATE")
            #print(e)
            return False

    @staticmethod
    def toGetCompteLiaison():
        try:
            return Model_Compte.objects.get(liaison_par_defaut = True)
        except Exception as e:
            return None

    @staticmethod
    def toSetCompteLiaison(id):
        try:
            compte = dao_compte.toGetCompteLiaison()
            if compte != None:
                compte.liaison_par_defaut = False
                compte.save()

            compte = dao_compte.toGetCompte(id)
            compte.liaison_par_defaut = True
            compte.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU UPDATE")
            #print(e)
            return False

    @staticmethod
    def toGetComptePersonnel():
        try:
            return Model_Compte.objects.get(personnel_par_defaut = True)
        except Exception as e:
            return None

    @staticmethod
    def toSetComptePersonnel(id):
        try:
            compte = dao_compte.toGetComptePersonnel()
            if compte != None:
                compte.personnel_par_defaut = False
                compte.save()

            compte = dao_compte.toGetCompte(id)
            compte.personnel_par_defaut = True
            compte.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU UPDATE")
            #print(e)
            return False

    @staticmethod
    def toGetCompteSalaire():
        try:
            return Model_Compte.objects.get(salaire_par_defaut = True)
        except Exception as e:
            return None

    @staticmethod
    def toSetCompteSalaire(id):
        try:
            compte = dao_compte.toGetCompteSalaire()
            if compte != None:
                compte.salaire_par_defaut = False
                compte.save()

            compte = dao_compte.toGetCompte(id)
            compte.salaire_par_defaut = True
            compte.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU UPDATE")
            #print(e)
            return False

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
            comptes = Model_Compte.objects.all().order_by("numero_compte")
            for item in comptes:
                if len(item.numero_compte) == 6: list.append(item)
            return list
        except Exception as e:
            #print("ERREUR LORS DE LA LECTURE DES COMPTES POUR ECRITURES")
            #print(e)
            return []
        
    @staticmethod
    def toListComptesAffichage():
        try:
            return Model_Compte.objects.all().order_by("numero_compte")
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
            comptes = Model_Compte.objects.all().order_by("numero_compte")
            for item in comptes:
                if len(item.numero_compte) == int_longueur: list.append(item)
            #print(list)
            return list
        except Exception as e:
            #print("ERREUR LORS DE LA LECTURE DES COMPTES DE NUMERO DE LA TAILLE %s" % int_longueur)
            return []
        
    @staticmethod
    def toListComptesOf(type_compte_id):
        try:
            return Model_Compte.objects.filter(type_compte_id = type_compte_id).order_by("numero_compte")
        except Exception as e:
            #print("ERREUR LORS DE LA LECTURE DES COMPTES DU TYPE")
            return []