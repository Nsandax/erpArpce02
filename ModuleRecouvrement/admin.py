from django.contrib import admin
from . import models

admin.site.register(models.Model_Scenario_relance)
admin.site.register(models.Model_Action_scenario)
admin.site.register(models.Model_Dossier_recouvrement)
admin.site.register(models.Model_Action_relance)