# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_ItemProfilPaye
from django.utils import timezone

class dao_item_profil_paie(object):
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
        return Model_ItemProfilPaye.objects.all().order_by("sequence")
    
    @staticmethod
    def toCreate(auteur_id, designation, bareme_id, devise_id, montant_net_impot, tranche_debut, tranche_fin, pourcentage_net_impot, sequence = 1):
        try:
            item_profil_paie = dao_item_profil_paie()
            item_profil_paie.auteur_id = auteur_id
            item_profil_paie.designation = designation
            item_profil_paie.bareme_id = bareme_id
            item_profil_paie.devise_id = devise_id
            item_profil_paie.montant_net_impot = montant_net_impot
            item_profil_paie.tranche_debut = tranche_debut
            item_profil_paie.tranche_fin = tranche_fin
            item_profil_paie.pourcentage_net_impot = pourcentage_net_impot
            item_profil_paie.sequence = sequence
            return item_profil_paie
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION")
            #print(e)
            return None

    @staticmethod
    def toSave(dao_item_profil_paie_object):
        try:
            item_profil_paie = Model_ItemProfilPaye()
            item_profil_paie.designation = dao_item_profil_paie_object.designation
            item_profil_paie.auteur_id = dao_item_profil_paie_object.auteur_id
            item_profil_paie.bareme_id = dao_item_profil_paie_object.bareme_id
            item_profil_paie.devise_id = dao_item_profil_paie_object.devise_id
            item_profil_paie.montant_net_impot = dao_item_profil_paie_object.montant_net_impot
            item_profil_paie.tranche_debut = dao_item_profil_paie_object.tranche_debut
            item_profil_paie.tranche_fin = dao_item_profil_paie_object.tranche_fin
            item_profil_paie.pourcentage_net_impot = dao_item_profil_paie_object.pourcentage_net_impot
            item_profil_paie.sequence = dao_item_profil_paie_object.sequence
            item_profil_paie.creation_date = timezone.now()
            item_profil_paie.save()
            return item_profil_paie
        except Exception as e:
            #print("ERREUR LORS DU SAVE")
            #print(e)
            return None

    
    @staticmethod
    def toUpdate(id, dao_item_profil_paie_object):
        try:
            item_profil_paie = Model_ItemProfilPaye.objects.get(pk = id)
            item_profil_paie.designation = dao_item_profil_paie_object.designation
            item_profil_paie.bareme_id = dao_item_profil_paie_object.bareme_id
            item_profil_paie.devise_id = dao_item_profil_paie_object.devise_id
            item_profil_paie.montant_net_impot = dao_item_profil_paie_object.montant_net_impot
            item_profil_paie.tranche_debut = dao_item_profil_paie_object.tranche_debut
            item_profil_paie.tranche_fin = dao_item_profil_paie_object.tranche_fin
            item_profil_paie.pourcentage_net_impot = dao_item_profil_paie_object.pourcentage_net_impot
            item_profil_paie.sequence = dao_item_profil_paie_object.sequence
            item_profil_paie.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR")
            #print(e)
            return False

    
    @staticmethod
    def toDelete(dao_item_profil_paie_object):
        try:
            item_profil_paie = Model_ItemProfilPaye.objects.get(pk = dao_item_profil_paie_object.id)
            item_profil_paie.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION")
            #print(e)
            return False

    
    @staticmethod
    def toGet(id):
        try:
            item_profil_paie = Model_ItemProfilPaye.objects.get(pk = id)
            return item_profil_paie
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE")
            #print(e)
            return None

    @staticmethod
    def toGetItemOfProfil(id):
        try:
            item_profil_paie = Model_ItemProfilPaye.objects.filter(profil_paie_id = id).order_by("sequence")
            return item_profil_paie
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE")
            #print(e)
            return None