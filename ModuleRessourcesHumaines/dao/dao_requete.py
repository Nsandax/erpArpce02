from __future__ import unicode_literals
from ErpBackOffice.models import Model_Requete
from django.utils import timezone

class dao_requete(object):
	id = 0
	numero_reference = ''
	demandeur_id = None
	date_depart = '2010-01-01'
	date_retour = '2010-01-01'
	description = ''
	service_ref_id = None
	centre_cout_id = None
	document = ''
	statut_id = None
	etat = ''
	auteur_id = None
	url = ''

	@staticmethod
	def toListRequete():
		return Model_Requete.objects.all().order_by('-id')

	@staticmethod
	def toListRequeteByUser(user_id):
		return Model_Requete.objects.filter(auteur_id=user_id)

	@staticmethod
	def toCreateRequete(numero_reference,demandeur_id,date_depart,date_retour,description,service_ref_id,centre_cout_id,document,statut_id,etat):
		try:
			requete = dao_requete()
			requete.numero_reference = numero_reference
			requete.demandeur_id = demandeur_id
			requete.date_depart = date_depart
			requete.date_retour = date_retour
			requete.description = description
			requete.service_ref_id = service_ref_id
			requete.centre_cout_id = centre_cout_id
			requete.document = document
			requete.statut_id = statut_id
			requete.etat = etat
			return requete
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA REQUETE')
			#print(e)
			return None

	@staticmethod
	def toSaveRequete(auteur, objet_dao_Requete):
		try:
			requete  = Model_Requete()
			requete.numero_reference = objet_dao_Requete.numero_reference
			requete.demandeur_id = objet_dao_Requete.demandeur_id
			requete.date_depart = objet_dao_Requete.date_depart
			requete.date_retour = objet_dao_Requete.date_retour
			requete.description = objet_dao_Requete.description
			requete.service_ref_id = objet_dao_Requete.service_ref_id
			requete.centre_cout_id = objet_dao_Requete.centre_cout_id
			requete.document = objet_dao_Requete.document
			requete.statut_id = objet_dao_Requete.statut_id
			requete.etat = objet_dao_Requete.etat
			requete.created_at = timezone.now()
			requete.updated_at = timezone.now()
			requete.auteur = auteur

			requete.save()
			return requete
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA REQUETE')
			#print(e)
			return None

	@staticmethod
	def toUpdateRequete(id, objet_dao_Requete):
		try:
			requete = Model_Requete.objects.get(pk = id)
			requete.numero_reference =objet_dao_Requete.numero_reference
			requete.demandeur_id =objet_dao_Requete.demandeur_id
			requete.date_depart =objet_dao_Requete.date_depart
			requete.date_retour =objet_dao_Requete.date_retour
			requete.description =objet_dao_Requete.description
			requete.service_ref_id =objet_dao_Requete.service_ref_id
			requete.centre_cout_id =objet_dao_Requete.centre_cout_id
			requete.document =objet_dao_Requete.document
			requete.statut_id =objet_dao_Requete.statut_id
			requete.etat =objet_dao_Requete.etat
			requete.updated_at = timezone.now()
			requete.save()
			return requete
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA REQUETE')
			#print(e)
			return None
	@staticmethod
	def toGetRequete(id):
		try:
			return Model_Requete.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteRequete(id):
		try:
			requete = Model_Requete.objects.get(pk = id)
			requete.delete()
			return True
		except:
			return False

	@staticmethod
	def toGenerateNumeroRequete():
		total_damandes = dao_requete.toListRequete().count()
		total_damandes = total_damandes + 1
		temp_numero = str(total_damandes)

		for i in range(len(str(total_damandes)), 4):
			temp_numero = "0" + temp_numero

		mois = timezone.now().month
		if mois < 10: mois = "0%s" % mois

		temp_numero = "EXPM%s%s%s" % (timezone.now().year, mois, temp_numero)
		return temp_numero
