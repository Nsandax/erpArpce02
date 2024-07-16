<<<<<<< HEAD
# -*- coding: utf-8 -*-

def calcul_paie(employee_id,code_element_paie,type_calcul,base_de_calcul,pourcentage):
    #print('fonction calcul paie')
    #print('parametre de la fonction')
    #print( "%s %s  %s  %s %s"  %( employee_id,code_element_paie,type_calcul,base_de_calcul,pourcentage))
    #print('========================')
    if code_element_paie == 'BASE':
        #print('Salaire 	A payer 	imposable:') 
        #print('BASE')
    elif code_element_paie == 'CIRC':
        #print('Congé de circonstance 	A payer imposable')
        #print('BASE')
    elif code_element_paie == 'ANC':
        #print('Ancienneté A payer imposable') 
        #print('CIRC')
    elif code_element_paie == 'ALFAMLEG':
        #print('Alloc. Familliale Légales 	A payer 	Non imposable') 
        #print('ALFAMLEG')
    elif(code_element_paie == 'INDTR'):
        #print('Indemnité Transport 	A payer 	Non imposable') 
        #print('INDTR')
    elif(code_element_paie == 'INDLOG'):
        #print('Indemnité Logement 	A payer 	Non imposable')
        #print('INDLOG')	
    elif (code_element_paie == 'IMP'):
        #print('Impôt 	A retenir 	Non imposable') 
        #print('IMP')
    elif (code_element_paie == 'INSS'):
        #print('Impôt 	INSS') 
        #print('INSS')
    else:
        #print('erreur')
    
=======
# -*- coding: utf-8 -*-

def calcul_paie(employee_id,code_element_paie,type_calcul,base_de_calcul,pourcentage):
    #print('fonction calcul paie')
    #print('parametre de la fonction')
    #print( "%s %s  %s  %s %s"  %( employee_id,code_element_paie,type_calcul,base_de_calcul,pourcentage))
    #print('========================')
    if code_element_paie == 'BASE':
        #print('Salaire 	A payer 	imposable:') 
        #print('BASE')
    elif code_element_paie == 'CIRC':
        #print('Congé de circonstance 	A payer imposable')
        #print('BASE')
    elif code_element_paie == 'ANC':
        #print('Ancienneté A payer imposable') 
        #print('CIRC')
    elif code_element_paie == 'ALFAMLEG':
        #print('Alloc. Familliale Légales 	A payer 	Non imposable') 
        #print('ALFAMLEG')
    elif(code_element_paie == 'INDTR'):
        #print('Indemnité Transport 	A payer 	Non imposable') 
        #print('INDTR')
    elif(code_element_paie == 'INDLOG'):
        #print('Indemnité Logement 	A payer 	Non imposable')
        #print('INDLOG')	
    elif (code_element_paie == 'IMP'):
        #print('Impôt 	A retenir 	Non imposable') 
        #print('IMP')
    elif (code_element_paie == 'INSS'):
        #print('Impôt 	INSS') 
        #print('INSS')
    else:
        #print('erreur')
    
>>>>>>> SionMaster
