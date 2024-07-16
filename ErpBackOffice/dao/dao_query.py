from __future__ import unicode_literals
from ErpBackOffice.models import Model_Query
from django.utils import timezone

class dao_query(object):
	id = 0
	title = ""
	query_string = ''
	query_graphic  = ''
	query_card  = ''
	select = ''
	filter = ''
	main_model = None
	is_chart = False
	is_card = False
	model_chart = 0
	measure_function = ''
	measure_attribute = ''
	card_function = ''
	card_attribute = ''
	dimension = ''
	is_success = False

	@staticmethod
	def toListQuery():
		return Model_Query.objects.all()

	@staticmethod
	def toCreateQuery(title,query_string,select,filter,main_model_id,is_chart = False, \
					model_chart = 0, measure_function = None,measure_attribute = None, \
						dimension = None, query_graphic = '', is_card = False, card_function = "",  \
						card_attribute = "", query_card = "", is_success = True,):
		try:
			query = dao_query()
			query.title = title
			query.query_string = query_string
			query.select = select
			query.filter = filter
			query.main_model_id = main_model_id
			query.is_chart = is_chart
			query.model_chart = model_chart
			query.measure_function = measure_function
			query.measure_attribute = measure_attribute
			query.dimension = dimension
			query.query_graphic = query_graphic
			query.is_card = is_card
			query.card_function = card_function
			query.card_attribute = card_attribute
			query.query_card = query_card
			query.is_success = is_success
			return query
		except Exception as e:
			print('ERREUR LORS DE LA CREATION DE LA QUERY')
			print(e)
			return None

	@staticmethod
	def toSaveQuery(auteur, objet_dao_Query):
		try:
			query  = Model_Query()
			query.title = objet_dao_Query.title
			query.query_string = objet_dao_Query.query_string
			query.select = objet_dao_Query.select
			query.filter = objet_dao_Query.filter
			query.main_model_id = objet_dao_Query.main_model_id
			query.is_chart = objet_dao_Query.is_chart
			query.model_chart = objet_dao_Query.model_chart
			query.measure_function = objet_dao_Query.measure_function
			query.measure_attribute = objet_dao_Query.measure_attribute
			query.dimension = objet_dao_Query.dimension
			query.query_graphic = objet_dao_Query.query_graphic
			query.is_card = objet_dao_Query.is_card
			query.card_function = objet_dao_Query.card_function
			query.card_attribute = objet_dao_Query.card_attribute
			query.query_card = objet_dao_Query.query_card
			query.is_success = objet_dao_Query.is_success
			query.auteur_id = auteur.id
			query.created_at = timezone.now()
			query.updated_at = timezone.now()
			query.save()
			return query
		except Exception as e:
			print('ERREUR LORS DE L ENREGISTREMENT DE LA QUERY')
			print(e)
			return None

	@staticmethod
	def toUpdateQuery(id, objet_dao_Query):
		try:
			query = Model_Query.objects.get(pk = id)
			query.title = objet_dao_Query.title
			query.query_string =objet_dao_Query.query_string
			query.select =objet_dao_Query.select
			query.filter =objet_dao_Query.filter
			query.main_model_id =objet_dao_Query.main_model_id
			query.is_chart = objet_dao_Query.is_chart
			query.model_chart = objet_dao_Query.model_chart
			query.measure_function =objet_dao_Query.measure_function
			query.measure_attribute =objet_dao_Query.measure_attribute
			query.dimension =objet_dao_Query.dimension
			query.query_graphic = objet_dao_Query.query_graphic
			query.is_card = objet_dao_Query.is_card
			query.card_function = objet_dao_Query.card_function
			query.card_attribute = objet_dao_Query.card_attribute
			query.query_card = objet_dao_Query.query_card
			query.is_success =objet_dao_Query.is_success
			query.updated_at = timezone.now()
			query.save()
			return query
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA QUERY')
			#print(e)
			return None

	@staticmethod
	def toGetQuery(id):
		try:
			return Model_Query.objects.get(pk = id)
		except Exception as e:
			return None
	
	

	@staticmethod
	def toDeleteQuery(id):
		try:
			query = Model_Query.objects.get(pk = id)
			query.delete()
			return True
		except Exception as e:
			return False