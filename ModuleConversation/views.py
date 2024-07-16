# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ErpBackOffice.utils.auth import auth
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.template import loader
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils import timezone
from django.core import serializers
from random import randint
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from ErpBackOffice.utils.identite import identite
from ErpBackOffice.utils.tools import ErpModule
import datetime
import json
from django.db import transaction
from ErpBackOffice.dao.dao_personne import dao_personne
from ErpBackOffice.dao.dao_place import dao_place
from ErpBackOffice.dao.dao_compte import dao_compte
from ErpBackOffice.dao.dao_module import dao_module
from ErpBackOffice.dao.dao_devise import dao_devise
from ModuleConversation.dao.dao_notification import dao_notification
from ModuleRessourcesHumaines.dao.dao_employe import dao_employe
from ErpBackOffice.dao.dao_document import dao_document
from ErpBackOffice.models import Model_Message
from ErpBackOffice.models import Model_Notification
from ModuleConversation.dao.dao_message import dao_message
from ModuleConversation.dao.dao_notification import dao_notification


#LOGGING
import logging, inspect
monLog = logging.getLogger("logger")
module= "ModuleConversation"


def get_index(request):
	context = {"title" : "Gestion des envois et lectures des messages","utilisateur" : identite.utilisateur(request),"modules" : dao_module.toListModulesInstalles(),"module" : ErpModule.MODULE_CONVERSATION,"msg_count":dao_notification.toCountNotificationUnread(identite.utilisateur(request).id),"msg_list":dao_notification.toGetListNotificationHeader(identite.utilisateur(request).id),"notif_count":dao_notification.toCountSystemNotificationUnread(identite.utilisateur(request).id),"notif_list":dao_notification.toGetListSystemNotificationHeader(identite.utilisateur(request).id),"menu" : 1}
	template = loader.get_template("ErpProject/ModuleConversation/index.html")
	return HttpResponse(template.render(context, request))

def get_lister_msg_sent(request):
	modules, utilisateur = auth.toGetAuth(request)
	#print("Holla")
	auteur = identite.utilisateur(request)
	model = dao_message.toListMessageSentByUserFull(auteur.id)
	count_unread = dao_notification.toCountNotificationUnread(auteur.id)
	
	context ={'title' : 'Liste de messages','count_unread':count_unread, 'model' : model,'utilisateur' : identite.utilisateur(request),'modules' : modules,"module" : ErpModule.MODULE_CONVERSATION,"msg_count":dao_notification.toCountNotificationUnread(identite.utilisateur(request).id),"msg_list":dao_notification.toGetListNotificationHeader(identite.utilisateur(request).id),"notif_count":dao_notification.toCountSystemNotificationUnread(identite.utilisateur(request).id),"notif_list":dao_notification.toGetListSystemNotificationHeader(identite.utilisateur(request).id),'menu' : 1}
	template = loader.get_template('ErpProject/ModuleConversation/message/list_send.html')
	return HttpResponse(template.render(context, request))

def get_lister_message(request):
	modules, utilisateur = auth.toGetAuth(request)

	auteur = identite.utilisateur(request)
	model = dao_message.toListMessageByUserFull(auteur.id)
	count_unread = dao_notification.toCountNotificationUnread(auteur.id)
	#print(model)
	#print("Jo")
	
	context ={'title' : 'Liste de messages','count_unread':count_unread, 'model' : model,'utilisateur' : identite.utilisateur(request),'modules' : modules,"module" : ErpModule.MODULE_CONVERSATION,"msg_count":dao_notification.toCountNotificationUnread(identite.utilisateur(request).id),"msg_list":dao_notification.toGetListNotificationHeader(identite.utilisateur(request).id),"notif_count":dao_notification.toCountSystemNotificationUnread(identite.utilisateur(request).id),"notif_list":dao_notification.toGetListSystemNotificationHeader(identite.utilisateur(request).id),'menu' : 1}
	template = loader.get_template('ErpProject/ModuleConversation/message/list.html')
	return HttpResponse(template.render(context, request))



def get_creer_message(request):
	modules, utilisateur = auth.toGetAuth(request)
	model = dao_employe.toListEmployes()
	model2 = dao_document.toListDocuments()
	context ={'title' : 'Nouveau message','model':model,'model2':model2, 'utilisateur' : identite.utilisateur(request),'modules' : modules,"module" : ErpModule.MODULE_CONVERSATION,"msg_count":dao_notification.toCountNotificationUnread(identite.utilisateur(request).id),"msg_list":dao_notification.toGetListNotificationHeader(identite.utilisateur(request).id),"notif_count":dao_notification.toCountSystemNotificationUnread(identite.utilisateur(request).id),"notif_list":dao_notification.toGetListSystemNotificationHeader(identite.utilisateur(request).id),'menu' : 2}
	template = loader.get_template('ErpProject/ModuleConversation/message/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_message(request):

	try:
		#print('la ou')
		auteur = identite.utilisateur(request)
		objet = request.POST['objet']
		corps = request.POST['corps']
		type = request.POST['type']
		#destinataire_id = request.POST['destinataire_id']
		expediteur_id = auteur.id
		status = "sent"
		document_id = request.POST['document_id']
		auteur = identite.utilisateur(request)
		#print(request.POST.getlist)
		list_destinataire_id = request.POST.getlist("destinataire_id",None)
		#print(list_destinataire_id)
		#list_document_id = request.POST.getlist("document_id",None)

		message = Model_Message.objects.create(objet=objet,corps=corps,type=type,expediteur_id=auteur.id,status=status,created_at=timezone.now(),auteur_id=auteur.id)
		#message = message.save()
		#print(message)
		#print(message.id)
		
		for i in range(0,len(list_destinataire_id)):
			destinataire_id = list_destinataire_id[i]
			#print(destinataire_id)
			notification = Model_Notification.objects.create(user_id=destinataire_id,est_lu=False,text=corps[:90],created_at=timezone.now(),auteur_id=auteur.id)
			#notification.save()
			#print("un")
			notification.message.add(message)
			#print("deux")
			
		messages.add_message(request, messages.SUCCESS, "Votre message a bien été envoyé !")
		return HttpResponseRedirect(reverse('module_conversation_list_message'))
	except Exception as e:
		messages.add_message(request, messages.SUCCESS, "Votre message n'a pas été envoyé, réessayez! !")
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER MESSAGE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_conversation_add_message'))

def get_details_msg_sent(request,ref):
	modules, utilisateur = auth.toGetAuth(request)
	try:
		#print("here")
		ref=int(ref)
		message=dao_message.toGetMessage(ref)
		receivers = dao_notification.toListAllReceiverOfAMessage(ref)

		auteur = identite.utilisateur(request)
		#message_read = dao_notification.toUpdateMessageRead(auteur.id,ref)
		template = loader.get_template('ErpProject/ModuleConversation/message/item_sent.html')
		context ={'title' : 'Details d\'un message','message' : message,'receivers':receivers,'utilisateur' : identite.utilisateur(request),'modules' : modules,"module" : ErpModule.MODULE_CONVERSATION,"msg_count":dao_notification.toCountNotificationUnread(identite.utilisateur(request).id),"msg_list":dao_notification.toGetListNotificationHeader(identite.utilisateur(request).id),"notif_count":dao_notification.toCountSystemNotificationUnread(identite.utilisateur(request).id),"notif_list":dao_notification.toGetListSystemNotificationHeader(identite.utilisateur(request).id),'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS MESSAGE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_conversation_list_message'))

def get_details_message(request,ref):
	modules, utilisateur = auth.toGetAuth(request)
	try:
		ref=int(ref)
		message=dao_message.toGetMessage(ref)
		auteur = identite.utilisateur(request)
		message_read = dao_notification.toUpdateMessageRead(auteur.id,ref)
		template = loader.get_template('ErpProject/ModuleConversation/message/item.html')
		context ={'title' : 'Details d\'un message','message' : message,'utilisateur' : identite.utilisateur(request),'modules' : modules,"module" : ErpModule.MODULE_CONVERSATION,"msg_count":dao_notification.toCountNotificationUnread(identite.utilisateur(request).id),"msg_list":dao_notification.toGetListNotificationHeader(identite.utilisateur(request).id),"notif_count":dao_notification.toCountSystemNotificationUnread(identite.utilisateur(request).id),"notif_list":dao_notification.toGetListSystemNotificationHeader(identite.utilisateur(request).id),'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS MESSAGE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_conversation_list_message'))
def get_modifier_message(request,ref):
	modules, utilisateur = auth.toGetAuth(request)

	ref = int(ref)
	model = dao_message.toGetMessage(ref)
	context ={'title' : 'Modifier Message','model':model, 'utilisateur' : identite.utilisateur(request),'modules' : modules,"module" : ErpModule.MODULE_CONVERSATION,"msg_count":dao_notification.toCountNotificationUnread(identite.utilisateur(request).id),"msg_list":dao_notification.toGetListNotificationHeader(identite.utilisateur(request).id),"notif_count":dao_notification.toCountSystemNotificationUnread(identite.utilisateur(request).id),"notif_list":dao_notification.toGetListSystemNotificationHeader(identite.utilisateur(request).id),'menu' : 2}
	template = loader.get_template('ErpProject/ModuleConversation/message/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_message(request):

	id = int(request.POST['ref'])
	try:
		objet = request.POST['objet']
		corps = request.POST['corps']
		type = request.POST['type']
		destinataire_id = request.POST['destinataire_id']
		expediteur_id = request.POST['expediteur_id']
		status = request.POST['status']
		document_id = request.POST['document_id']
		auteur = identite.utilisateur(request)

		message=dao_message.toCreateMessage(objet,corps,type,destinataire_id,expediteur_id,status,document_id)
		message=dao_message.toUpdateMessage(id, message)
		return HttpResponseRedirect(reverse('module_conversation_list_message'))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER MESSAGE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_conversation_add_message'))


def get_lister_notification(request):
	modules, utilisateur = auth.toGetAuth(request)

	auteur = identite.utilisateur(request)
	model = dao_notification.toListNotificationByUser(auteur.id)
	context ={'title' : 'Liste de notifications','model' : model,'utilisateur' : identite.utilisateur(request),'modules' : modules,"module" : ErpModule.MODULE_CONVERSATION,"msg_count":dao_notification.toCountNotificationUnread(identite.utilisateur(request).id),"msg_list":dao_notification.toGetListNotificationHeader(identite.utilisateur(request).id),"notif_count":dao_notification.toCountSystemNotificationUnread(identite.utilisateur(request).id),"notif_list":dao_notification.toGetListSystemNotificationHeader(identite.utilisateur(request).id),'menu' : 1}
	template = loader.get_template('ErpProject/ModuleConversation/notification/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_notification(request):
	modules, utilisateur = auth.toGetAuth(request)

	context ={'title' : 'Nouvelle notification','utilisateur' : identite.utilisateur(request),'modules' : modules,"module" : ErpModule.MODULE_CONVERSATION,"msg_count":dao_notification.toCountNotificationUnread(identite.utilisateur(request).id),"msg_list":dao_notification.toGetListNotificationHeader(identite.utilisateur(request).id),"notif_count":dao_notification.toCountSystemNotificationUnread(identite.utilisateur(request).id),"notif_list":dao_notification.toGetListSystemNotificationHeader(identite.utilisateur(request).id),'menu' : 2}
	template = loader.get_template('ErpProject/ModuleConversation/notification/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_notification(request):

	try:
		user_id = request.POST['user_id']
		est_lu = request.POST['est_lu']
		message_id = request.POST['message_id']
		text = request.POST['text']
		url_piece_concernee = request.POST['url_piece_concernee']
		auteur = identite.utilisateur(request)

		notification=dao_notification.toCreateNotification(user_id,est_lu,message_id,text,url_piece_concernee)
		notification=dao_notification.toSaveNotification(auteur, notification)
		return HttpResponseRedirect(reverse('module_conversation_list_notification'))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER NOTIFICATION \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_conversation_add_notification'))


def get_details_notification(request,ref):
	modules, utilisateur = auth.toGetAuth(request)
	try:
		ref=int(ref)
		notification=dao_notification.toGetNotification(ref)
		template = loader.get_template('ErpProject/ModuleConversation/notification/item.html')
		context ={'title' : 'Details d\'une notification','notification' : notification,'utilisateur' : identite.utilisateur(request),'modules' : modules,"module" : ErpModule.MODULE_CONVERSATION,"msg_count":dao_notification.toCountNotificationUnread(identite.utilisateur(request).id),"msg_list":dao_notification.toGetListNotificationHeader(identite.utilisateur(request).id),"notif_count":dao_notification.toCountSystemNotificationUnread(identite.utilisateur(request).id),"notif_list":dao_notification.toGetListSystemNotificationHeader(identite.utilisateur(request).id),'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS NOTIFICATION \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_conversation_list_notification'))
def get_modifier_notification(request,ref):
	modules, utilisateur = auth.toGetAuth(request)

	ref = int(ref)
	model = dao_notification.toGetNotification(ref)
	context ={'title' : 'Modifier Notification','model':model, 'utilisateur' : identite.utilisateur(request),'modules' : modules,"module" : ErpModule.MODULE_CONVERSATION,"msg_count":dao_notification.toCountNotificationUnread(identite.utilisateur(request).id),"msg_list":dao_notification.toGetListNotificationHeader(identite.utilisateur(request).id),"notif_count":dao_notification.toCountSystemNotificationUnread(identite.utilisateur(request).id),"notif_list":dao_notification.toGetListSystemNotificationHeader(identite.utilisateur(request).id),'menu' : 2}
	template = loader.get_template('ErpProject/ModuleConversation/notification/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_notification(request):

	id = int(request.POST['ref'])
	try:
		user_id = request.POST['user_id']
		est_lu = request.POST['est_lu']
		message_id = request.POST['message_id']
		text = request.POST['text']
		url_piece_concernee = request.POST['url_piece_concernee']
		auteur = identite.utilisateur(request)

		notification=dao_notification.toCreateNotification(user_id,est_lu,message_id,text,url_piece_concernee)
		notification=dao_notification.toUpdateNotification(id, notification)
		return HttpResponseRedirect(reverse('module_conversation_list_notification'))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER NOTIFICATION \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_conversation_add_notification'))