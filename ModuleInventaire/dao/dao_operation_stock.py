# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ErpBackOffice.models import Model_OperationStock

class dao_operation_stock(object):
    id = 0
    designation = ""
    reference = ""
    type = "TRANSFERT"
    sequence = 100

    @staticmethod
    def toListOperationsStock():
        return Model_OperationStock.objects.all().order_by("designation")
        

    @staticmethod
    def toListOperationsStockOfInventaire():
        return Model_OperationStock.objects.filter(type = "TRANSFERT").order_by("sequence")

    @staticmethod
    def toListOperationsStockByAuteur(user_id):
        return Model_OperationStock.objects.filter(auteur_id=user_id).order_by("designation")
        

    @staticmethod
    def toListOperationsStockOfInventaireByAuteur(user_id):
        return Model_OperationStock.objects.filter(type = "TRANSFERT").filter(auteur_id=user_id).order_by("sequence")
		
    @staticmethod
    def toCreateOperationStock(designation, reference = "", type = "", sequence = 100):
        try:
            operation = dao_operation_stock()
            operation.designation = designation
            operation.reference = reference
            operation.type = type
            operation.sequence = sequence
            return operation
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION")
            #print(e)
            return None
    
    @staticmethod
    def toGetOperationReceptionArticles():
        try:
            operation = Model_OperationStock.objects.get(reference = "IN")
            return operation
        except Exception as e:
            #print("ERREUR LORS DU LA LECTURE")
            #print(e)
            return None

    @staticmethod
    def toGetOperationFabrication():
        try:
            operation = Model_OperationStock.objects.get(type = "FABRICATION")
            return operation
        except Exception as e:
            #print("ERREUR LORS DU LECTURE")
            #print(e)
            return None
    
    @staticmethod
    def toGetOperationTransmission():
        try:
            operation = Model_OperationStock.objects.filter(designation = "Transfert d'articles").first()
            return operation
        except Exception as e:
            #print("ERREUR LORS DU LECTURE")
            #print(e)
            return None

    @staticmethod
    def toGetOperationStock(id):
        try:
            operation = Model_OperationStock.objects.get(pk = id)
            return operation
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE")
            #print(e)
            return None
    
    @staticmethod
    def toSaveOperationStock(dao_operation_stock_object):
        try:
            operation = Model_OperationStock()
            operation.designation = dao_operation_stock_object.designation
            operation.reference = dao_operation_stock_object.reference
            operation.type = dao_operation_stock_object.type
            operation.sequence = dao_operation_stock_object.sequence
            operation.save()
            return operation
        except Exception as e:
            #print("ERREUR LORS DU SAVE")
            #print(e)
            return None
    
    @staticmethod
    def toUpdateOperationStock(id, dao_operation_stock_object):
        try:			
            operation = Model_OperationStock.objects.get(pk = id)
            operation.designation = dao_operation_stock_object.designation
            operation.reference = dao_operation_stock_object.reference
            operation.type = dao_operation_stock_object.type
            operation.sequence = dao_operation_stock_object.sequence		    
            operation.save()			
            return True
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR")
            #print(e)
            return False

    @staticmethod
    def toDeleteOperationStock(id):
        try:
            operation = Model_OperationStock.objects.get(pk = id)
            operation.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION")
            #print(e)
            return False
    @staticmethod
    def toGetAffectionInterne():
        return Model_OperationStock.objects.filter(designation = "Affectation interne").first()

    @staticmethod
    def toGetAffectionInterneByAuteur(user_id):
        return Model_OperationStock.objects.filter(designation = "Affectation interne").filter(auteur_id=user_id).first()

    

    
    
    
    
    
    

    