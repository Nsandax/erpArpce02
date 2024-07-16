from __future__ import unicode_literals
from ErpBackOffice.models import Model_Client
from django.utils import timezone

class dao_client(object):
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
    est_particulier = ""
    compte_id = None
    auteur_id = None
    date_de_naissance = ""
    lieu_de_naissance = ""
    sexe = ''
    civilite_id = None


    @staticmethod
    def toCreateClient(prenom,nom, postnom, nom_complet, image,email, phone, adresse, commune_quartier_id , langue = "", est_actif=True, lieu_de_naissance="", date_de_naissance=None, sexe="", compte_id=None, est_particulier= True, civilite_id=None):
        try:
            client = dao_client()
            client.nom_complet = nom_complet
            client.image = image
            client.est_particulier = est_particulier
            client.adresse = adresse
            client.commune_quartier_id = commune_quartier_id
            client.est_actif = True
            client.sexe = sexe
            client.phone = phone
            client.langue = langue
            client.date_de_naissance = date_de_naissance
            client.lieu_de_naissance = lieu_de_naissance
            client.date_de_naissance = date_de_naissance
            client.nom = nom
            client.email = email
            client.compte_id = compte_id
            client.postnom = postnom
            client.prenom = prenom
            client.civilite_id = civilite_id            
            return client
        except Exception as e:
            #print("ERREUR CREATION CLIENT")
            #print(e)
            return None

    @staticmethod
    def toSaveClient(auteur,objet_dao_client):
        try:
            #print("lieu de nais", objet_dao_client.lieu_de_naissance)
            client  = Model_Client()
            client.nom = objet_dao_client.nom
            client.date_de_naissance = objet_dao_client.date_de_naissance
            client.prenom = objet_dao_client.prenom
            client.postnom = objet_dao_client.postnom            
            client.nom_complet = objet_dao_client.nom_complet
            client.image = objet_dao_client.image
            client.est_particulier = objet_dao_client.est_particulier
            client.adresse = objet_dao_client.adresse
            client.commune_quartier_id = objet_dao_client.commune_quartier_id
            
            client.est_actif = True
            client.phone = objet_dao_client.phone
            client.email = objet_dao_client.email
            client.langue= objet_dao_client.langue
            client.lieu_de_naissance = objet_dao_client.lieu_de_naissance
            client.date_de_naissance = objet_dao_client.date_de_naissance
            client.sexe=objet_dao_client.sexe
            
            client.auteur_id = auteur.id
            client.compte_id = objet_dao_client.compte_id
            client.civilite_id = objet_dao_client.civilite_id
            client.creation_date = timezone.now()
            client.save()
                        
            return client
        except Exception as e:
            #print("ERREUR ENREGISTREMENT CLIENT")
            #print(e)
            return None

    @staticmethod
    def toUpdateClient(id,objet_dao_client):
        try:
            client = Model_Client.objects.get(pk = id)
            client.nom = objet_dao_client.nom
            client.prenom = objet_dao_client.prenom
            client.postnom = objet_dao_client.postnom
            
            client.nom_complet = objet_dao_client.nom_complet
            client.image = objet_dao_client.image
            client.est_particulier = objet_dao_client.est_particulier
            client.adresse = objet_dao_client.adresse
            client.commune_quartier_id = objet_dao_client.commune_quartier_id
            
            client.est_actif = True
            client.phone = objet_dao_client.phone
            client.email = objet_dao_client.email
            client.langue = objet_dao_client.langue
            client.lieu_de_naissance = objet_dao_client.lieu_de_naissance
            client.compte_id = objet_dao_client.compte_id
            client.est_particulier = objet_dao_client.est_particulier
            client.sexe=objet_dao_client.sexe
            client.save()
            return True
        except Exception as e:
            #print("ERREUR UPDATE CLIENT")
            #print(e)
            return False

    @staticmethod
    def toActiveClient(id, est_actif):
        try:
            client = Model_Client.objects.get(pk = id)
            client.est_actif = est_actif
            client.save()
            return True
        except Exception as e:
            return False

    @staticmethod
    def toGetClient(id):
        try:
            return Model_Client.objects.get(pk = id)
        except Exception as e:
            return None

    @staticmethod
    def toDeleteClient(id):
        try:
            client = Model_Client.objects.get(pk = id)
            client.delete()
            return True
        except Exception as e:
            return False

    @staticmethod
    def toListClients():
        try:
            return Model_Client.objects.all()
        except Exception as e:
            #print("ERREUR LORS DE LA SELECT")
            #print(e)
            return []
    
    @staticmethod
    def toListClientsParticuliers():
        try:
            return Model_Client.objects.filter(est_particulier = True)
        except Exception as e:
            #print("ERREUR LORS DE LA SELECT")
            #print(e)
            return []
    @staticmethod
    def toListClientsEntreprises():
        try:
            return Model_Client.objects.exclude(est_particulier = True)
        except Exception as e:
            #print("ERREUR LORS DE LA SELECT")
            #print(e)
            return []

    @staticmethod
    def toListClientsActifs():
        try:
            return Model_Client.objects.filter(est_actif = True).order_by("nom_complet")
        except Exception as e:
            #print("ERREUR LORS DU SELECT")
            #print(e)
            return []