from __future__ import unicode_literals
from ErpBackOffice.models import Model_Fournisseur
from django.utils import timezone

class dao_fournisseur(object):
    id = 0
    prenom=""
    nom=""
    postnom=""
    nom_complet	= ""
    image	= ""
    email = ""
    phone = ""
    adresse	= ""
    commune_quartier_id	= None
    langue = ""
    est_actif = True
    compte_id = None
    auteur_id = None
    date_de_naissance = ""
    lieu_de_naissance = ""
    denomination = ""
    domaine = ''
    categorie = ''
    civilite=''
    date_fondation = None
    est_particulier = False


    @staticmethod
    def toCreateFournisseur(prenom,nom, postnom, nom_complet, image,email, phone, adresse, commune_quartier_id, langue,civilite,est_actif=True,lieu_de_naissance="",date_de_naissance="2000-01-01",denomination="",domaine="",categorie="",date_fondation='2000-01-01',compte_id=None, est_particulier= False):
        try:
            fournisseur = dao_fournisseur()

            fournisseur.nom_complet = nom_complet

            fournisseur.image = image
            fournisseur.est_particulier = est_particulier
            fournisseur.adresse = adresse
            fournisseur.commune_quartier_id = commune_quartier_id
            fournisseur.est_actif = True
            fournisseur.denomination = denomination
            fournisseur.domaine = domaine
            fournisseur.categorie=categorie
            #fournisseur.civilite=civilite
            fournisseur.date_fondation=date_fondation
            fournisseur.langue = langue

            if phone != None :
                fournisseur.phone = phone
            #if date_de_naissance != None :
                #fournisseur.date_de_naissance = date_de_naissance
            if nom != None :
                fournisseur.nom = nom
            if email != None :
                fournisseur.email = email

            fournisseur.compte_id = None
            fournisseur.postnom = postnom
            fournisseur.prenom = prenom


            return fournisseur
        except Exception as e:
            # print("ERREUR LORS DE LA CREATION DE LA PERSONNE")
            # print(e)
            return None

    @staticmethod
    def toSaveFournisseur(auteur,objet_dao_fournisseur):
        try:
            fournisseur  = Model_Fournisseur()
            fournisseur.nom = objet_dao_fournisseur.nom
            #fournisseur.date_de_naissance = objet_dao_fournisseur.date_de_naissance
            fournisseur.prenom = objet_dao_fournisseur.prenom
            fournisseur.postnom = objet_dao_fournisseur.postnom
            fournisseur.langue = objet_dao_fournisseur.langue

            fournisseur.nom_complet = objet_dao_fournisseur.nom_complet

            fournisseur.image = objet_dao_fournisseur.image
            fournisseur.est_particulier = objet_dao_fournisseur.est_particulier
            fournisseur.adresse = objet_dao_fournisseur.adresse
            fournisseur.commune_quartier_id = objet_dao_fournisseur.commune_quartier_id

            fournisseur.est_actif = objet_dao_fournisseur.est_actif
            fournisseur.phone = objet_dao_fournisseur.phone
            fournisseur.email = objet_dao_fournisseur.email
            fournisseur.langue= objet_dao_fournisseur.langue
            fournisseur.lieu_de_naissance = objet_dao_fournisseur.lieu_de_naissance
            #fournisseur.denomination=objet_dao_fournisseur.denomination
            fournisseur.domaine =objet_dao_fournisseur.domaine
            fournisseur.categorie=objet_dao_fournisseur.categorie
            #fournisseur.civilite=objet_dao_fournisseur.civilite
            #fournisseur.date_fondation=objet_dao_fournisseur.date_fondation

            fournisseur.auteur_id = auteur.id
            fournisseur.compte_id = objet_dao_fournisseur.compte_id

            fournisseur.creation_date = timezone.now()
            fournisseur.save()


            return fournisseur
        except Exception as e:
            # print("ERREUR LORS DE L'ENREGISTREMENT")
            # print(e)
            return None

    @staticmethod
    def toListFournisseursActifs():
        try:
            return Model_Fournisseur.objects.filter(est_actif = True).order_by("nom_complet")
        except Exception as e:
            #print("ERREUR LORS DU SELECT")
            #print(e)
            return []

    @staticmethod
    def toUpdateCompteofFournisseur(id, compte_id):
        try:
            fournisseur = Model_Fournisseur.objects.get(pk = id)
            fournisseur.compte_id = compte_id
            fournisseur.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA MISE A JOUR Du fournisseur")
            #print(e)
            return False


    @staticmethod
    def toUpdateFournisseur(id,objet_dao_fournisseur):
        try:
            fournisseur = Model_Fournisseur.objects.get(pk = id)
            fournisseur.nom = objet_dao_fournisseur.nom
            #fournisseur.date_de_naissance = objet_dao_fournisseur.date_de_naissance
            fournisseur.prenom = objet_dao_fournisseur.prenom
            fournisseur.postnom = objet_dao_fournisseur.postnom

            fournisseur.nom_complet = objet_dao_fournisseur.nom_complet

            fournisseur.image = objet_dao_fournisseur.image
            fournisseur.est_particulier = objet_dao_fournisseur.est_particulier
            fournisseur.adresse = objet_dao_fournisseur.adresse
            fournisseur.commune_quartier_id = objet_dao_fournisseur.commune_quartier_id

            fournisseur.est_actif = objet_dao_fournisseur.est_actif
            fournisseur.phone = objet_dao_fournisseur.phone
            fournisseur.email = objet_dao_fournisseur.email
            fournisseur.langue= objet_dao_fournisseur.langue
            #fournisseur.lieu_de_naissance = objet_dao_fournisseur.lieu_de_naissance
            #fournisseur.denomination=objet_dao_fournisseur.denomination
            #fournisseur.domaine =objet_dao_fournisseur.domaine
            #fournisseur.categorie=objet_dao_fournisseur.categorie
            #fournisseur.civilite=objet_dao_fournisseur.civilite
            #fournisseur.date_fondation=objet_dao_fournisseur.date_fondation

            #fournisseur.auteur_id = auteur.id
            fournisseur.compte_id = objet_dao_fournisseur.compte_id

            fournisseur.creation_date = timezone.now()
            fournisseur.save()
            return True
        except Exception as e:
            #print("ERREUR UPDATE")
            #print(e)
            return False

    @staticmethod
    def toActiveFournisseur(id, est_actif):
        try:
            fournisseur = Model_Fournisseur.objects.get(pk = id)
            fournisseur.est_actif = est_actif
            fournisseur.save()
            return True
        except Exception as e:
            return False

    @staticmethod
    def toGetFournisseur(id):
        try:
            return Model_Fournisseur.objects.get(pk = id)
        except Exception as e:
            return None

    @staticmethod
    def toDeleteFournisseur(id):
        try:
            fournisseur = Model_Fournisseur.objects.get(pk = id)
            fournisseur.delete()
            return True
        except Exception as e:
            return False

    @staticmethod
    def toListFournisseurs():
        try:
            return Model_Fournisseur.objects.all().order_by('-id')
        except Exception as e:
            #print("ERREUR LORS DE LA SELECT")
            #print(e)
            return []
