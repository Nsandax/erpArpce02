from django.utils import timezone
import random
import string
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
import urllib	

class utils(object):
		
	@staticmethod
	def remove_duplicate_in_list(the_list):
		new_list = []
		for i in the_list:
			if i not in new_list:
				new_list.append(i)
		return new_list
	
