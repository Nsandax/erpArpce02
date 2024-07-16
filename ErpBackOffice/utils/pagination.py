from __future__ import unicode_literals
from ErpBackOffice.dao.dao_utilisateur import dao_utilisateur, Model_Employe
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

class pagination(object):
    
    @staticmethod
    def toGet(request, model):
        try:
            page = int(request.GET.get("page",1))
        except Exception as e:
            page = 1  
        try:			
            count = int(request.GET.get("count",10))
        except Exception as e:
            count = 10
        try:
            view = str(request.GET.get("view","list"))
        except Exception as e:
            view = "list"

        paginator = []

        if view == "list" or view == "kanban":	
            paginator = Paginator(model, count)
            try:
                model = paginator.page(page)
            except PageNotAnInteger:
                model = paginator.page(1)
            except EmptyPage:
                model = paginator.page(paginator.num_pages)
            model.num_items = count
        return model