from __future__ import unicode_literals
from ErpBackOffice.models import Model_Etat_Facturation, Model_Facture
from django.utils import timezone

class dao_etat_facturation(object):
    id = 0
    numero_etat_facturation = ""
    description = ""
    date_etat = ""
    document_id = None
    etat = ""
    statut_id = None
    auteur_id = None

    @staticmethod
    def toListEtatFacturation():
        return Model_Etat_Facturation.objects.all().order_by('-id')

    @staticmethod
    def togetNombreEtatFacturation():
        temps= timezone.now().month
        return Model_Etat_Facturation.objects.filter(date_etat__month=temps).count()

    @staticmethod
    def toListEtatFacturationValides():
        return Model_Etat_Facturation.objects.filter(etat = "Envoyé à la comptabilité", est_facture = False)

    @staticmethod
    def toCreateEtatFacturation(numero_etat_facturation,description, date_etat, document_id, etat = "", statut_id = ""):
        try:
            etat_facturation = dao_etat_facturation()
            etat_facturation.description = description
            etat_facturation.numero_etat_facturation = numero_etat_facturation
            etat_facturation.date_etat = date_etat
            etat_facturation.document_id = document_id
            etat_facturation.etat = etat
            etat_facturation.statut_id = statut_id

            return etat_facturation
        except Exception as e:
            #print('ERREUR LORS DE LA CREATION DE LA BON_COMMANDE')
            #print(e)
            return None



    @staticmethod
    def toSaveEtatFacturation(auteur,objet_dao_Etat_Facturation):
        try:
            etat_facturation  = Model_Etat_Facturation()
            etat_facturation.numero_etat_facturation = objet_dao_Etat_Facturation.numero_etat_facturation
            etat_facturation.description = objet_dao_Etat_Facturation.description
            etat_facturation.date_etat = objet_dao_Etat_Facturation.date_etat
            etat_facturation.document_id = objet_dao_Etat_Facturation.document_id
            etat_facturation.etat = objet_dao_Etat_Facturation.etat
            etat_facturation.statut_id = objet_dao_Etat_Facturation.statut_id
            etat_facturation.auteur_id = auteur.id
            etat_facturation.save()
            return etat_facturation
        except Exception as e:
            #print('ERREUR LORS DE L ENREGISTREMENT DE LA BON_COMMANDE')
            #print(e)
            return None

    @staticmethod
    def toUpdateEtatFacturation(id, objet_dao_Etat_Facturation):
        try:
            etat_facturation = Model_Etat_Facturation.objects.get(pk = id)
            etat_facturation.numero_etat_facturation = objet_dao_Etat_Facturation.numero_etat_facturation
            etat_facturation.description = objet_dao_Etat_Facturation.description
            etat_facturation.date_etat = objet_dao_Etat_Facturation.date_etat
            etat_facturation.document_id = objet_dao_Etat_Facturation.document_id
            etat_facturation.etat = objet_dao_Etat_Facturation.etat
            etat_facturation.statut_id = objet_dao_Etat_Facturation.statut_id
            etat_facturation.save()
            return etat_facturation
        except Exception as e:
            #print('ERREUR LORS DE LA MODIFICATION DE LA BON_COMMANDE')
            #print(e)
            return None

    @staticmethod
    def toGetEtatFacturation(id):
        try:
            return Model_Etat_Facturation.objects.get(pk = id)
        except Exception as e:
            return None


    @staticmethod
    def toDeleteEtatFacturation(id):
        try:
            etat_facturation = Model_Etat_Facturation.objects.get(pk = id)
            etat_facturation.delete()
            return True
        except Exception as e:
            return False

    @staticmethod
    def toGenerateNumeroEtatFacturation():
        total_etats = dao_etat_facturation.toListEtatFacturation().count()
        total_etats = total_etats + 1
        temp_numero = str(total_etats)

        for i in range(len(str(total_etats)), 5):
            temp_numero = "0" + temp_numero

        mois = timezone.now().month
        if mois < 10: mois = "0%s" % mois

        temp_numero = "EF-%s%s%s" % (str(timezone.now().year)[:2], "31", temp_numero)
        return temp_numero

    @staticmethod
    def toGetOrderMax():
        try:
            #return Model_Order.objects.all().aggregate(Max('rating'))
            max = Model_Etat_Facturation.objects.all().count()
            max = max + 1
            return max
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return None

    @staticmethod
    def toSetUpBilledEtatFacturation(etat_facturation_id):
        try:
            etat = Model_Etat_Facturation.objects.get(pk = etat_facturation_id)
            if Model_Facture.objects.filter(etat_facturation = etat_facturation_id, type_facture_client = "Agence"):
                #print("OK")
                if Model_Facture.objects.filter(etat_facturation = etat_facturation_id, type_facture_client = "Trésor publique"):
                    #print("OK")
                    etat.est_facture = True
                    etat.save()
                    return True

            return False
        except Exception as e:
            #print("Erreur Get Type Facture")
            #print(e)
            pass
