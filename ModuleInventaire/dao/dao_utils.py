from django.utils import timezone
import random
import string

		

class dao_utils(object):
	@staticmethod
	def genererNumeroAsset():
		uid = ''.join(random.choices(string.digits, k=8))
		uid = 'ASS-'+""+uid
		return uid