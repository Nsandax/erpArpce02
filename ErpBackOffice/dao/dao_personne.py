from __future__ import unicode_literals
from ErpBackOffice.models import Model_Personne
from django.utils import timezone

class dao_personne(object):
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
    est_particulier = False
    est_actif = True
    compte_id = None
    auteur_id = None
    date_de_naissance = ""
    lieu_de_naissance = ""

    @staticmethod
    def toCreatePersonne(prenom,nom, postnom, nom_complet, image,email, phone, adresse, commune_quartier_id, langue,est_actif,lieu_de_naissance,date_de_naissance,compte_id=0, est_particulier = False):
        try:
            personne = dao_personne()
            personne.nom_complet = nom_complet
            personne.image = image
            personne.est_particulier = True
            personne.adresse = adresse
            personne.commune_quartier_id = commune_quartier_id
            personne.est_actif = True
            personne.langue = langue

            if phone != None :
                personne.phone = phone
            if date_de_naissance != None :
                personne.date_de_naissance = date_de_naissance
            if nom != None :
                personne.nom = nom
            if email != None :
                personne.email = email
            if compte_id != 0:
                personne.compte_id = compte_id
            personne.postnom = postnom
            personne.prenom = prenom
            personne.est_particulier = est_particulier


            return personne
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE LA PERSONNE")
            #print(e)
            return None

    @staticmethod
    def toSavePersonne(auteur,objet_dao_personne):
        try:
            personne  = Model_Personne()
            personne.nom = objet_dao_personne.nom
            personne.date_de_naissance = objet_dao_personne.date_de_naissance
            personne.prenom = objet_dao_personne.prenom
            personne.postnom = objet_dao_personne.postnom

            personne.nom_complet = objet_dao_personne.nom_complet
            personne.image = objet_dao_personne.image
            personne.est_particulier = objet_dao_personne.est_particulier
            personne.adresse = objet_dao_personne.adresse
            personne.commune_quartier_id = objet_dao_personne.commune_quartier_id

            personne.est_actif = False
            personne.phone = objet_dao_personne.phone
            personne.email = objet_dao_personne.email
            personne.langue= objet_dao_personne.langue
            personne.est_particulier = objet_dao_personne.est_particulier
            personne.lieu_de_naissance = objet_dao_personne.lieu_de_naissance

            personne.auteur_id = auteur.id
            personne.compte_id = objet_dao_personne.compte_id

            personne.creation_date = timezone.now()
            personne.save()


            return personne
        except Exception as e:
            #print("ERREUR LORS DE L'ENREGISTREMENT")
            #print(e)
            return None

    @staticmethod
    def toUpdatePersonne(objet_dao_personne):
        try:
            personne = Model_Personne.objects.get(pk = objet_dao_personne.id)
            personne.nom = objet_dao_personne.nom
            personne.date_de_naissance = objet_dao_personne.date_de_naissance
            personne.prenom = objet_dao_personne.prenom
            personne.postnom = objet_dao_personne.postnom

            personne.nom_complet = objet_dao_personne.nom_complet
            personne.image = objet_dao_personne.image
            personne.est_particulier = objet_dao_personne.est_particulier
            personne.adresse = objet_dao_personne.adresse
            personne.commune_quartier_id = objet_dao_personne.commune_quartier_id

            personne.est_actif = False
            personne.phone = objet_dao_personne.phone
            personne.email = objet_dao_personne.email
            personne.langue= objet_dao_personne.langue
            personne.lieu_de_naissance = objet_dao_personne.lieu_de_naissance
            personne.compte_id = objet_dao_personne.compte_id
            personne.save()
            return True
        except Exception as e:
            #print("ERREUR UPDATE")
            #print(e)
            return False

    @staticmethod
    def toActivePersonne(id, est_actif):
        try:
            personne = Model_Personne.objects.get(pk = id)
            personne.est_actif = est_actif
            personne.save()
            return True
        except Exception as e:
            return False

    @staticmethod
    def toGetPersonne(id):
        try:
            return Model_Personne.objects.get(pk = id)
        except Exception as e:
            return None

    @staticmethod
    def toDeletePersonne(id):
        try:
            personne = Model_Personne.objects.get(pk = id)
            personne.delete()
            return True
        except Exception as e:
            return False

    @staticmethod
    def toListPersonnes():
        try:
            return Model_Personne.objects.all()
        except Exception as e:
            #print("ERREUR LORS DE LA SELECT")
            #print(e)
            return []

    @staticmethod
    def toListPersonnesActif():
        try:
            return Model_Personne.objects.filter(est_actif=True)
        except Exception as e:
            #print("ERREUR LORS DE LA SELECT")
            #print(e)
            return []