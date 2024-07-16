from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db import connection
from .dao_query import dao_query

class dao_query_builder():

    def toListContentTypes():
        return ContentType.objects.filter(app_label = "ErpBackOffice")
    
    def toListRelatedOfModel(model_id):
        #refaire
        result = []
        objet_modele = ContentType.objects.get(pk = model_id).model_class()
        for f in objet_modele._meta.get_fields():
            print(f)
            modele = objet_modele._meta.get_field(f.name).related_model
            if f.model:
                try:
                    model_content_type = ContentType.objects.get_for_model(modele)
                    result.append(model_content_type)        
                except Exception as e:
                    pass
            
        return result

    def toListFieldOfModel(model_id):
        '''Fonction qui retourne les champs propres à un modèle. Cette fonction retourne un
        tuple comprenant le verbose name et le name du champ '''
        fields = []
        objet_modele = ContentType.objects.get(pk = model_id).model_class()
        for f in objet_modele._meta.fields:
            #if not(isinstance(f,models.ForeignKey) or isinstance(f, models.ManyToManyField)):
            fields.append((f.name, f.verbose_name))
        return fields
    
    def toPerformRawQuery(auteur, title, is_chart, list_modele_id, list_select, list_filter, \
                          list_operator, list_value, list_logique = None, model_chart = 0, \
                              measure_function = "", measure_attribute = "", dimension = "", \
                                is_card = False, card_function = "", card_attribute = "" ):
        '''Fonction qui se charge de creer la requete en fonction des valeurs saisies et
        creer un objet Query qu'il enregistre dans la BD. 
        Il s'agit d'une création manuelle flexible d'un script SQL.
        Notions à noter: 
        1. Chaque type de rapport souhaité (DataTable, Graphique et Card) font appels à des requetes 
        SQL spécifiques. Cette fonction construit donc 3 requetes SQL en fonction du type de rapport
        souhaités.
        2. Pour le cas de "Graphique", Si la dimension choisie est de type "DateTime", un traitement 
        spécifique est effectué au niveau de la requete. un decoupage en année, mois et jour

        
        '''
        try:
            main_modele_id = list_modele_id[0]
            #recuperation du modele de l'objet à partir de l'identifiant du content type
            model_content_ref = ContentType.objects.get(pk = main_modele_id)
            main_model_name = f"{model_content_ref.app_label}_{model_content_ref.model}"
            main_model = model_content_ref.model_class()
            query_sql = "SELECT "
            query_graphic = ""
            query_card = ""
            select = ""
            filter = ""
            if list_select:
                for obj in list_select:
                    select += f"{obj},"
                select = select[:-1] #On enleve la dernière virgule
            else:
                select += " * "
            query_sql += select
            
            query_sql += f" FROM {main_model_name} "        
            print("liste logique", list_logique)    

            if list_filter:
                filter += " WHERE "
                for i in range(len(list_filter)):
                    if list_logique: #On sarrete pr l'instant à une ligne (on doit gerer après les AND OR xx)
                        if i > 0: #On saute la premiere iteration pour equilibrer les tailles 
                            filter += f' {list_logique[i-1]} '    
                    filter += f"{list_filter[i]} {list_operator[i]} '{list_value[i]}'"
                          
            
            print("filter.....", filter)
            query_sql += filter

            date_filter  = ["date", "creat", "updat"]
            
            if is_chart:#si c'est un graphique
                if any(map(dimension.__contains__, date_filter)) :#test si c'est une dimension de date , c'est pareil que #any(substring in dimension for substring in date_filter): 
                    query_graphic = f"SELECT YEAR({dimension}), MONTH({dimension}), {measure_function}({measure_attribute})"
                    query_graphic += f" FROM {main_model_name} "
                    query_graphic += filter
                    query_graphic += f" GROUP BY YEAR({dimension}), MONTH({dimension}) "
                    query_graphic += f" ORDER BY YEAR({dimension}), MONTH({dimension}) "
                else:
                    query_graphic = f"SELECT {dimension}, {measure_function}({measure_attribute}) "
                    query_graphic += f" FROM {main_model_name} "
                    query_graphic += filter
                    query_graphic += f" GROUP BY {dimension}"
                    #query_graphic += f" ORDER BY {dimension} "
            
            if is_card:
                query_card = f"SELECT {card_function}({card_attribute}) "
                query_card += f" FROM {main_model_name} "
                query_card += filter
            
            print(query_sql)
            result_row = dao_query_builder.my_custom_sql(query_sql) if query_sql else [] #Si requete non vide, then run
            result_graphic = dao_query_builder.my_custom_sql(query_graphic) if query_graphic else [] #Si requete non vide, then run
            result_card = dao_query_builder.my_custom_sql(query_card) if query_card else [] #Si requete non vide, then run
            #Creating query Object
            query = dao_query.toCreateQuery(title, query_sql,select, filter,main_modele_id, \
                    is_chart, model_chart, measure_function, measure_attribute, dimension, \
                        query_graphic, is_card, card_function, card_attribute, query_card)
            query = dao_query.toSaveQuery(auteur, query)
            #Traitement des données graphiques dans le cas ou la valeur is_chart est True
            result_graphic = dao_query_builder.processing_data_graphic(dimension,result_graphic) if is_chart else None
            return query, result_row, result_card, result_graphic
        except Exception as e:
            print("Error on toPerformRawQuery", e)
        
    
    

    def my_custom_sql(query):
        "Fonction qui execute une requete sql et retour le resultat sous forme de liste de tuples"
        try: 
            with connection.cursor() as cursor:
                cursor.execute(query)
                row = cursor.fetchall()
            return row
        except Exception as e:
            print("Error on my_custom_sql", e)
            return []
    
    def processing_data_graphic(dimension, result_graphic):
        try:
            category_list = []
            dataset_list = []
            date_filter  = ["date", "creat", "updat"]
            for result in result_graphic:
                if any(map(dimension.__contains__, date_filter)) :
                    category_list.append(f"{result[1]}/{result[0]}")
                    dataset_list.append(result[2])
                else:
                    print("on est ici", result)
                    category_list.append(result[0])
                    dataset_list.append(result[1])

            return {"categories":category_list, "datasets": dataset_list}
        except Exception as e:
            print("Error on processing_data_graphic", e)
            return None
        
    
    def testIfFieldIsFK(thefield, model_content_type):
        #refaire
        result = []
        objet_modele = model_content_type.model_class()
        for f in objet_modele._meta.get_fields():
            if f.name == thefield:
                if f.model:
                    try:
                        modele = objet_modele._meta.get_field(f.name).related_model                
                        model_content_ref = ContentType.objects.get_for_model(modele)
                        ref_model_name = f"{model_content_ref.app_label}_{model_content_ref.model}"

                        return ref_model_name      
                    except Exception as e:
                        return None
        return None
    
    def checkSelectFieldFK(list_select, model_content_type):
        list_join = []

            





