from __future__ import unicode_literals
from ErpBackOffice.models import Model_Evaluation
from django.utils import timezone

class dao_evaluation(object):
	id = 0
	description = ''
	instructions = ''
	echelle_notation = ''
	echelle_performance = ''
	echelle_coefficient = ''
	appreciation = ''
	date_appreciation = '2010-01-01'
	employe_id = None

	@staticmethod
	def toListEvaluation():
		return Model_Evaluation.objects.all().order_by('-id')

	@staticmethod
	def toListEvaluationByAuteur(user_id):
		return Model_Evaluation.objects.filter(auteur_id=user_id)

	@staticmethod
	def toCreateEvaluation(description,instructions,echelle_notation,echelle_performance,echelle_coefficient,appreciation,date_appreciation, employe_id = None):
		try:
			evaluation = dao_evaluation()
			evaluation.description = description
			evaluation.instructions = instructions
			evaluation.echelle_notation = echelle_notation
			evaluation.echelle_performance = echelle_performance
			evaluation.echelle_coefficient = echelle_coefficient
			evaluation.appreciation = appreciation
			evaluation.date_appreciation = date_appreciation
			evaluation.employe_id = employe_id
			return evaluation
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA EVALUATION')
			#print(e)
			return None

	@staticmethod
	def toSaveEvaluation(auteur, objet_dao_Evaluation):
		try:
			evaluation  = Model_Evaluation()
			evaluation.description = objet_dao_Evaluation.description
			evaluation.instructions = objet_dao_Evaluation.instructions
			evaluation.echelle_notation = objet_dao_Evaluation.echelle_notation
			evaluation.echelle_performance = objet_dao_Evaluation.echelle_performance
			evaluation.echelle_coefficient = objet_dao_Evaluation.echelle_coefficient
			evaluation.appreciation = objet_dao_Evaluation.appreciation
			evaluation.date_appreciation = objet_dao_Evaluation.date_appreciation
			evaluation.employe_id = objet_dao_Evaluation.employe_id
			evaluation.created_at = timezone.now()
			evaluation.updated_at = timezone.now()
			evaluation.auteur_id = auteur.id

			evaluation.save()
			return evaluation
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA EVALUATION')
			#print(e)
			return None

	@staticmethod
	def toUpdateEvaluation(id, objet_dao_Evaluation):
		try:
			evaluation = Model_Evaluation.objects.get(pk = id)
			evaluation.description =objet_dao_Evaluation.description
			evaluation.instructions =objet_dao_Evaluation.instructions
			evaluation.echelle_notation =objet_dao_Evaluation.echelle_notation
			evaluation.echelle_performance =objet_dao_Evaluation.echelle_performance
			evaluation.echelle_coefficient =objet_dao_Evaluation.echelle_coefficient
			evaluation.appreciation =objet_dao_Evaluation.appreciation
			evaluation.date_appreciation =objet_dao_Evaluation.date_appreciation
			evaluation.employe_id = objet_dao_Evaluation.employe_id
			evaluation.updated_at = timezone.now()
			evaluation.save()
			return evaluation
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA EVALUATION')
			#print(e)
			return None
	@staticmethod
	def toGetEvaluation(id):
		try:
			return Model_Evaluation.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteEvaluation(id):
		try:
			evaluation = Model_Evaluation.objects.get(pk = id)
			evaluation.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toGetEvaluationByEmploye(employe_id):
		try:
			evaluation = Model_Evaluation.objects.filter(employe_id = employe_id)
			return evaluation
		except:
			return None