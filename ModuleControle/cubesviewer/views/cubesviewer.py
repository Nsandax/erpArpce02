from django.views.generic.base import TemplateView
from django.conf import settings

#Normalement l'url proposé se presentait de la sorte url(r'^$', login_required( CubesViewerView.as_view() ) ), et pointait vers ici
#Cette partie du code a été redirigé vers ModuleControle.views.get_cubeviewer()
class CubesViewerView(TemplateView):

    template_name = "ErpProject/ModuleControle/Cube/index.html"
    exclude = ()

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        context["cubesviewer_cubes_url"] = settings.CUBESVIEWER_CUBES_URL
        context["cubesviewer_backend_url"] = settings.CUBESVIEWER_BACKEND_URL
        return context