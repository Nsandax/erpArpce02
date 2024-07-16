# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_TrancheBareme
from django.utils import timezone

class dao_tranche_bareme(object):
    id = 0
    designation = ""
    bareme_id = 0
    devise_id = 0
    montant_net_impot = 0.0
    tranche_debut = 0.0
    tranche_fin = 0.0
    pourcentage_net_impot = 0.0
    sequence = 0
    auteur_id = 0

    @staticmethod
    def toList():
        return Model_TrancheBareme.objects.all().order_by("sequence")
    
    @staticmethod
    def toCreate(auteur_id, designation, bareme_id, devise_id, montant_net_impot, tranche_debut, tranche_fin, pourcentage_net_impot, sequence = 1):
        try:
            tranche_bareme = dao_tranche_bareme()
            tranche_bareme.auteur_id = auteur_id
            tranche_bareme.designation = designation
            tranche_bareme.bareme_id = bareme_id
            tranche_bareme.devise_id = devise_id
            tranche_bareme.montant_net_impot = montant_net_impot
            tranche_bareme.tranche_debut = tranche_debut
            tranche_bareme.tranche_fin = tranche_fin
            tranche_bareme.pourcentage_net_impot = pourcentage_net_impot
            tranche_bareme.sequence = sequence
            return tranche_bareme
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION")
            #print(e)
            return None

    @staticmethod
    def toSave(dao_tranche_bareme_object):
        try:
            tranche_bareme = Model_TrancheBareme()
            tranche_bareme.designation = dao_tranche_bareme_object.designation
            tranche_bareme.auteur_id = dao_tranche_bareme_object.auteur_id
            tranche_bareme.bareme_id = dao_tranche_bareme_object.bareme_id
            tranche_bareme.devise_id = dao_tranche_bareme_object.devise_id
            tranche_bareme.montant_net_impot = dao_tranche_bareme_object.montant_net_impot
            tranche_bareme.tranche_debut = dao_tranche_bareme_object.tranche_debut
            tranche_bareme.tranche_fin = dao_tranche_bareme_object.tranche_fin
            tranche_bareme.pourcentage_net_impot = dao_tranche_bareme_object.pourcentage_net_impot
            tranche_bareme.sequence = dao_tranche_bareme_object.sequence
            tranche_bareme.creation_date = timezone.now()
            tranche_bareme.save()
            return tranche_bareme
        except Exception as e:
            #print("ERREUR LORS DU SAVE")
            #print(e)
            return None

    
    @staticmethod
    def toUpdate(id, dao_tranche_bareme_object):
        try:
            tranche_bareme = Model_TrancheBareme.objects.get(pk = id)
            tranche_bareme.designation = dao_tranche_bareme_object.designation
            tranche_bareme.bareme_id = dao_tranche_bareme_object.bareme_id
            tranche_bareme.devise_id = dao_tranche_bareme_object.devise_id
            tranche_bareme.montant_net_impot = dao_tranche_bareme_object.montant_net_impot
            tranche_bareme.tranche_debut = dao_tranche_bareme_object.tranche_debut
            tranche_bareme.tranche_fin = dao_tranche_bareme_object.tranche_fin
            tranche_bareme.pourcentage_net_impot = dao_tranche_bareme_object.pourcentage_net_impot
            tranche_bareme.sequence = dao_tranche_bareme_object.sequence
            tranche_bareme.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR")
            #print(e)
            return False

    
    @staticmethod
    def toDelete(dao_tranche_bareme_object):
        try:
            tranche_bareme = Model_TrancheBareme.objects.get(pk = dao_tranche_bareme_object.id)
            tranche_bareme.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION")
            #print(e)
            return False

    
    @staticmethod
    def toGet(id):
        try:
            tranche_bareme = Model_TrancheBareme.objects.get(pk = id)
            return tranche_bareme
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE")
            #print(e)
            return None

    @staticmethod
    def toGetDuBareme(id):
        try:
            tranche_bareme = Model_TrancheBareme.objects.filter(bareme_id = id).order_by("sequence")
            return tranche_bareme
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE")
            #print(e)
            return None