"""ErpARPCE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
#from django.urls import path
from django.conf.urls import include, url
from ModuleAchat import views

# admin.autodiscover()
# admin.site.enable_nav_sidebar = False

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('ErpBackOffice.urls')),
    url(r'^configuration/', include('ModuleConfiguration.urls')),
    url(r'^achat/', include('ModuleAchat.urls')),
    url(r'^vente/', include('ModuleVente.urls')),
    url(r'^inventaire/', include('ModuleInventaire.urls')),
    url(r'^comptabilite/', include('ModuleComptabilite.urls')),
    url(r'^ressourceshumaines/', include('ModuleRessourcesHumaines.urls')),
    url(r'^application/', include('ModuleApplication.urls')),
    url(r'^budget/', include('ModuleBudget.urls')),
    url(r'^archivage/', include('ModuleArchivage.urls')),
    url(r'^calendrier/', include('ModuleCalendrier.urls')),
]


urlpatterns.append(url(r'^conversation/', include('ModuleConversation.urls')))
urlpatterns.append(url(r'^payroll/', include('ModulePayroll.urls')))
urlpatterns.append(url(r'^controle/', include('ModuleControle.urls')))
urlpatterns.append(url(r'^contrat/', include('ModuleContrat.urls')))
urlpatterns.append(url(r'^stock/', include('ModuleStock.urls')))