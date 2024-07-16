from django.utils import timezone
import random
import string

		

class dao_utils(object):
	@staticmethod
	def genererNumero(prefixe, suffixe, nombre):
		temp_numero = int(str(nombre)) + 1
		for i in range(len(str(nombre)), 3):
			temp_numero = "0" + str(temp_numero)
		return f'{prefixe}-{suffixe}-{temp_numero}-ARPCE-DG-CGMP-{str(timezone.now().year)[2:]}'
		