# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_Wkf_Historique
from django.utils import timezone

class dao_wkf_historique_bon_transfert(object):
    id = 0
    employe_id = None
    etape_id = None
    bon_transfert_id = None

    @staticmethod
    def toListHistoriqueWorkflows():
        return Model_Wkf_Historique.objects.all()

    @staticmethod
    def toListHistoriqueOfBonTransfert(bon_transfert_id):
        return Model_Wkf_Historique.objects.filter(bon_transfert_id = bon_transfert_id)

    @staticmethod
    def toCreateHistoriqueWorkflow(employe_id , etape_id , bon_transfert_id = None):        
        try:
            historique_workflow = dao_wkf_historique_bon_transfert()
            historique_workflow.employe_id = employe_id
            historique_workflow.etape_id = etape_id
            historique_workflow.bon_transfert_id = bon_transfert_id
            return historique_workflow
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE HISTORIQUE WORKFLOW")
            #print(e)
            return None

    @staticmethod
    def toSaveHistoriqueWorkflow(object_dao_wkf_historique):
        try:
            historique_workflow = Model_Wkf_Historique()
            historique_workflow.employe_id = object_dao_wkf_historique.employe_id
            historique_workflow.etape_id = object_dao_wkf_historique.etape_id
            historique_workflow.bon_transfert_id = object_dao_wkf_historique.bon_transfert_id
            historique_workflow.save()
            return historique_workflow
        except Exception as e:
            #print("ERREUR LORS DE L'ENREGISTREMENT DE HISTORIQUE WORKFLOW")
            #print(e)
            return None
    
    @staticmethod
    def toUpdateHistoriqueWorkflow(id, object_dao_wkf_historique):
        try:
            historique_workflow = Model_Wkf_Historique.objects.get(pk = id)
            historique_workflow.employe_id = object_dao_wkf_historique.employe_id
            historique_workflow.etape_id = object_dao_wkf_historique.etape_id
            historique_workflow.bon_transfert_id = object_dao_wkf_historique.bon_transfert_id
            historique_workflow.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA MISE A JOUR DE HISTORIQUE WORKFLOW")
            #print(e)
            return False
  
    @staticmethod
    def toGetHistoriqueWorkflow(id):
        try:
            return Model_Wkf_Historique.objects.get(pk = id)
        except Exception as e:
            return None

    @staticmethod
    def toDeleteHistoriqueWorkflow(id):
        try:
            historique_workflow = Model_Wkf_Historique.objects.get(pk = id)
            historique_workflow.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION DE HISTORIQUE WORKFLOW")
            #print(e)
            return False

    @staticmethod
    def getCountSignatures(etape_id, bon_transfert_id):
        try:
            historique_workflow = Model_Wkf_Historique.objects.filter(etape_id = etape_id, bon_transfert_id = bon_transfert_id)            
            return historique_workflow.count()
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION DU WORKFLOW")
            #print(e)
            return 0

    @staticmethod
    def toGetIfSigned(etape_id, bon_transfert_id, employe_id):
        try:
            historique_workflow = Model_Wkf_Historique.objects.filter(etape_id = etape_id, bon_transfert_id = bon_transfert_id, employe_id = employe_id) 
            if historique_workflow:
                return True
            else: return False           
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION DU WORKFLOW")
            #print(e)
            return False 
            
        					
            