from django import template
from ErpBackOffice.models import Model_Bon_transfert,Model_Article, Model_Emplacement, Model_TypeEmplacement
from ModuleInventaire.dao.dao_stock_article import dao_stock_article
register = template.Library()
from django.template.defaultfilters import stringfilter

@register.filter(name='qte_stock_of_empl')
def qte_stock_of_empl(value, arg):
	obj_article = value
	empl_id = arg
	#qte_stock = obj_article.quantite_stock_of_emplacement(empl_id)
	qte_stock = dao_stock_article.toGetQuantiteStockOfEmplacement(obj_article, empl_id)
	return qte_stock

@register.filter(name='count_todo_transfert')
def count_todo_transfert(value, arg):
	count = 0
	obj_operation = value
	argument = arg

	try:
		type_emplacement = Model_TypeEmplacement.objects.get(designation = obj_operation.reference)
		emplacements = Model_Emplacement.objects.filter(type_emplacement_id = type_emplacement.id)
		for emplacement in emplacements:
			nbre_transfert = Model_Bon_transfert.objects.filter(est_realisee = False).filter(emplacement_destination_id = emplacement.id).count()
			count = count + nbre_transfert
		return count
	except Exception as e:
		#print("ERREUR FILTER COUNT TODO")
		#print(e)
		return count


@register.filter
# stringfilter est utilisé quand la function de contient pas d'argument, rien que la valeur
@stringfilter
def sep_float(valeur):
    try:
        if valeur == "None":
            return 0
        elif valeur == "":
            return ""
        else:
            valeur = float(valeur)
            v = f"{valeur:0,.2f}"
            #v = "{:,.2f}".format(abs(valeur))
            return v.replace(',',' ').replace('.',',')

    except Exception as e:
        pass
