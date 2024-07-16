import math, unidecode, codecs, os, inspect
from django.contrib.contenttypes import models
from django.contrib.contenttypes.models import ContentType
from ErpBackOffice.dao.dao_module import dao_module
from ErpBackOffice.utils.identite import identite
from ErpBackOffice.dao.dao_droit import dao_droit
from ErpBackOffice.utils.tools import ErpModule
from ErpBackOffice.models import *
from ErpBackOffice.dao.dao_sous_module import dao_sous_module
from ErpBackOffice.dao.dao_groupe_permission import dao_groupe_permission
from ErpBackOffice.dao.dao_groupe_menu import dao_groupe_menu
from ErpBackOffice.dao.dao_model import dao_model
from ErpBackOffice.dao.dao_regle import dao_regle
from ModuleConfiguration.dao.dao_permission import dao_permission
from ModuleConfiguration.dao.dao_actionutilisateur import dao_actionutilisateur
from ModuleConversation.dao.dao_notification import dao_notification
from ModuleRessourcesHumaines.dao.dao_organisation import dao_organisation
from ModuleConfiguration.dao.dao_sousmodule import dao_sousmodule
from ModuleConfiguration.dao.dao_groupemenu import dao_groupemenu

def genLayoutHtmlOfModule():
    texte_a_ajouter = u'''
{% extends "ErpProject/ErpBackOffice/shared/layout.html" %} {% block content %} {%load static %}
{% if not isPopup %}
<!-- Suite Menu Nav -->
<!-- Menu lateral -->
<div class="sidebar" role="navigation">
    <div class="contenair-profil only-on-large-screen" style="background-color: transparent;">
        {% if utilisateur.image != None and utilisateur.image != '' %}
        <img src="{% static utilisateur.image %}"  class="profil">
        {% else %}
            <img src="/static/ErpProject/image/icone_profile.png" class="profil">
        {% endif %}
        <label class="nom-admin">{{ utilisateur.nom_complet }}</label>
        <p class="fonction">{% if utilisateur.poste == None %} {{"Administrateur"}} {% else %}{{ utilisateur.poste.designation }}{% endif %}</p>
        <div class="divider" style="background-color: transparent;"></div>
    </div>
    <div class="sidebar-nav navbar-collapse" style="background-color: transparent;">
        <ul class=" nav" id="side-menu" style="background-color: transparent;">
            {% include 'ErpProject/ErpBackOffice/widget/menu.html' %}
        </ul>
    </div>
    <!-- /.sidebar-collapse -->
</div>
<!-- /.Menu lateral -->
</nav>
<!-- /.Menu Navbar -->

<!-- Corps de la page (A définir dans chaque fonction du module) -->
<div id="page-wrapper" style="background-color:#f9f9f9;">
{% else %}
<div id="page-wrapper"  style="background-color:#f9f9f9;margin:0!important">
{% endif %}
    {% block page %}{% endblock %}
</div>
<!-- Fin Corps de la page -->
{% endblock %}

'''
    return texte_a_ajouter

def genDashBoardTemplate1(nomModule):
    texte_a_ajouter = u'''
{{% extends "ErpProject/{0}/shared/layout.html" %}}
{{% block page %}}{{%load static %}}{{% load account_filters %}}

<style type="text/css">
   body {{background-color: grey!important;}}
   .btSh{{border-radius: 0px;margin-right: 10px;margin-bottom: 0px;margin-bottom: 3%;}}
   .f{{margin:2%;}}
   .block_f{{margin-left: 0%;}}
   .fond{{background-color: rgba(240, 240, 240, 0.3);border-radius: 50px;height: 50px;width: 50px;opacity:3.5;float: right;display: flex;justify-content: center;align-items: center;}}
</style>

<!-- Design Admin -->
<div id="vue_Admin" class="row" style="padding-top:30px;">
	<div class="col-lg-12">
	<h2>{{{{title}}}}</h2>
	<strong style="float: right;color: grey;opacity: 0.4;margin-top: -30px;">{{% now "jS F Y H:i" %}}</strong>
	<div class="separ" style="background-color: grey;opacity: 0.2"></div>
		<div class="Menu_Inventaire">
			<div class="row">
				<div class="col-md-3">
					<div class="panel panel-success" style="border-radius: 0px;border-bottom: none;background-color:#FF6A22;">
						<div class="panel-heading" style="background-color: transparent;color: white;">
							<div class="row">
								<div class="col-xs-7 text-left">
									<div class="header_vente_stat" style="">Élément 1</div>
									<p style="font-weight: 800;font-size: 22px;font-family: 'Poppins Bold'">15</p>
								</div>
								<div class="col-xs-3 text-right fond">
									<span class="mif-stack" style="float: left;font-size:25px"></span>
								</div>
								<div>
									<p style="float: left;font-size:80%;color:#fff;">Éléments nouvellement inscrits ou sympatisant</p>
								</div>
							</div>
						</div>
					</div>
				</div>
				<div class="col-md-3">
					<div class="panel panel-success p2" style="border-radius: 0px;border-bottom: none;">
						<div class="panel-heading" style="background-color: transparent;color: white;">
							<div class="row">
								<div class="col-md-7 text-left">
									<div class="header_vente_stat" style="">Élément 2</div>
									<p style="font-weight: 800;font-size: 22px;font-family: 'Poppins Bold'">8</p>
								</div>
								<div class="col-md-3 text-right fond">
									<span class="mif-calendar" style="float: left;font-size:25px"></span>
								</div>
								<div>
									<p style="float: left;font-size:80%;color:#fff;">Nombre de éléments actifs au sein du groupe</p>
								</div>
							</div>
						</div>
					</div>
				</div>
				<div class="col-md-3">
					<div class="panel panel-success p3" style="border-radius: 0px;border-bottom: none;">
						<div class="panel-heading" style="background-color: transparent;color: white;">
							<div class="row">
								<div class="col-xs-7 text-left">
									<div class="header_vente_stat" style="">Élément 3</div>
									<p style="font-weight: 800;font-size: 22px;font-family: 'Poppins Bold'">10</p>
								</div>
								<div class="col-xs-3 text-right fond">
									<span class="mif-exit" style="float: left;font-size:25px"></span>
								</div>
								<div>
									<p style="float: left;font-size:80%;color:#fff;">Nombre total d'Éléments officiels du groupe</p>
								</div>
							</div>
						</div>
					</div>
				</div>
				<div class="col-md-3">
					<div class="panel panel-success p4" style="border-radius: 0px;border-bottom: none;">
						<div class="panel-heading" style="background-color: transparent;color: white;">
							<div class="row">
								<div class="col-xs-7 text-left">
									<div class="header_vente_stat" style="">Élément 4</div>
									<p style="font-weight: 800;font-size: 22px;font-family: 'Poppins Bold'">5</p>
								</div>
								<div class="col-xs-3 text-right fond">
									<span class="mif-database" style="font-size:25px"></span>
								</div>
								<div>
									<p style="float: left;font-size:80%;color:#fff;">Le nombre total de cellules officielles du parti</p>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>

			<div class="row">
				<div class="col-md-12">
					<div class="mb-4">
						<!-- Card Body -->
						<div class="card-body" style="padding: 0;">
						<div class="chart-area item-dash" style="padding: 15px;background-color: white;">
							<center> <p>Evolution des éléments par province</p></center>
							<canvas id="bar-chart" width="400" height="100"></canvas>
						</div>
						</div>
					</div>
				</div>
			</div><br>

			<div class="row">
				<div class="col-md-4" style="padding: 10px;">
					<div class="mb-4">
						<div class="card-body shadow" style="padding: 0px;background-color: white;">
							<div  style="width: 100%;background-color: white;/*padding: 10px;">
								<div style="padding: 10px;">
									<strong class="sub-header" style="margin: 10px;font-weight: 900;">Indicateur 1</strong>
								</div>
								<div class="separ" style="background-color: grey;opacity: 0.2;height: 1px;margin-bottom: 10px;"></div>
							</div>
							<div class="pt-4" style="padding: 15px;background-color: white;padding-top: 0px;padding-bottom: 0px;">
								<h3 style="color: gray;font-weight: bold;">100 USD</h3>
								<div class="" style="margin:2% 0 2% 0;font-style:normal;font-size:85%;">
									<span class="fg-red"><i class="fa fa-arrow-down"></i> <i>En diminution</i></span>
									<span class="fg-green" style="margin-left:20px"><i class="fa fa-arrow-up"></i> <i>En hausse</i></span>
								</div>
							</div>
							<div class="separ" style="background-color: grey;opacity: 0.2;height: 1px;margin-bottom: 10px;"></div>
							<div style="padding: 15px;padding-top: 0px;"     >
								<button  onclick="javascript:window.location.assign('')" class="btn rounded primary_color_{{{{module.name|lower}}}}">Voir plus</button>
								<button  onclick="javascript:window.location.assign('')" class="button rounded btn btn-default ">Annuler</button>
							</div>
							<div class="primary_color_{{{{module.name|lower}}}}" style="height: 5px;"></div>
						</div>
					</div>
				</div>

				<div class="col-md-4" style="padding: 10px;">
					<div class="mb-4 ">
						<div class="card-body shadow" style="padding: 0px;background-color: white;">
							<div  style="width: 100%;background-color: white;/*padding: 10px;">
								<div style="padding: 10px;">
									<strong class="sub-header" style="margin: 10px;font-weight: 900;">Indicateur 2</strong>
								</div>
								<div class="separ" style="background-color: grey;opacity: 0.2;height: 1px;margin-bottom: 10px;"></div>
							</div>
							<div class="pt-4" style="padding: 15px;background-color: white;padding-top: 0px;padding-bottom: 0px;">
								<h3 style="color: gray;font-weight: bold;">550 USD</h3>
								<div class="" style="margin:2% 0 2% 0;font-style:normal;font-size:85%;">
									<span class="fg-red"><i class="fa fa-arrow-down"></i> <i>En diminution</i></span>
									<span class="fg-green" style="margin-left:20px"><i class="fa fa-arrow-up"></i> <i>En hausse</i></span>
								</div>
							</div>
							<div class="separ" style="background-color: grey;opacity: 0.2;height: 1px;margin-bottom: 10px;"></div>
							<div style="padding: 15px;padding-top: 0px;"     >
								<button  class="btn rounded primary_color_{{{{module.name|lower}}}}" onclick="javascript:window.location.assign('')">Voir plus</button>
								<button  class="button rounded btn btn-default" onclick="javascript:window.location.assign('')">Annuler</button>
							</div>
							<div class="primary_color_{{{{module.name|lower}}}}" style="height: 5px;"></div>
						</div>
					</div>
				</div>

				<div class="col-md-4" style="padding: 10px;">
					<div class="mb-4 ">
						<div class="card-body shadow" style="padding: 0px;background-color: white;">
							<div  style="width: 100%;background-color: white;/*padding: 10px;">
								<div style="padding: 10px;">
									<strong class="sub-header" style="margin: 10px;font-weight: 900;">Indicateur 3</strong>
								</div>
								<div class="separ" style="background-color: grey;opacity: 0.2;height: 1px;margin-bottom: 10px;"></div>
							</div>
							<div class="pt-4" style="padding: 15px;background-color: white;padding-top: 0px;padding-bottom: 0px;">
								<h3 style="color: gray;font-weight: bold;">200 USD</h3>
								<div class="" style="margin:2% 0 2% 0;font-style:normal;font-size:85%;">
									<span class="fg-red"><i class="fa fa-arrow-down"></i> <i>En diminution</i></span>
									<span class="fg-green" style="margin-left:20px"><i class="fa fa-arrow-up"></i> <i>En hausse</i></span>
								</div>
							</div>
							<div class="separ" style="background-color: grey;opacity: 0.2;height: 1px;margin-bottom: 10px;"></div>
							<div style="padding: 15px;padding-top: 0px;">
								<button  onclick="javascript:window.location.assign('')" class="btn rounded primary_color_{{{{module.name|lower}}}}">Voir plus</button>
								<button  onclick="javascript:window.location.assign('')" class="button rounded btn btn-default ">Annuler</button>
							</div>
							<div class="primary_color_{{{{module.name|lower}}}}" style="height: 5px;"></div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
<!-- End Design Admin -->

<script src="{{% static 'ErpProject/js/Chart.min.js' %}}"></script>
<script>
	// Bar chart
	new Chart(document.getElementById("bar-chart"), {{
		type: 'bar',
		data: {{
		labels: ["Kinshasa", "Kongo Centrale", "Kwango", "Kwilu", "Lomami", "Lualaba", "Mai-Ndombe", "Maniema", "Mongala", "Nord-Kivu", "Nord-Ubangi", "Sankuru", "Sud-Kivu", "Sud-Ubangi", "Tanganyika", "Tshopo", "Tshuapa", "Kasaï oriental", "Kasaï central", "Kasaï", "Ituri", "Haut-Katanga", "Haut-Lomami", "Bas-Uele", "Haut-Uele", "Équateur"],
		datasets: [
			{{
			label: "Elément au niveau national",
			backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850","#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850","#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850","#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850","#c45850","#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
			data: [2478,5267,734,784,433,2478,5267,734,784,433,2478,5267,734,784,433,2478,5267,734,784,433,433,2478,5267,734,784,433]
			}}
		]}},
		options: {{
			legend: {{ display: false }},
			title: {{
				display: true,
				text: "Courbe d'évolution de nouveaux éléments en 2021"
			}},
			font: {{
				family: 'Poppins'
			}}
		}}
	}});
</script>
{{% endblock %}}
    '''.format(nomModule)
    return texte_a_ajouter

def genDashBoardTemplate2(nomModule):
    texte_a_ajouter = u'''
{{% extends "ErpProject/{0}/shared/layout.html" %}}
{{% block page %}}{{%load static %}}{{% load account_filters %}}

<style type="text/css">
    body {{background-color: grey!important;}}
</style>

<div class="row" style="padding-top: 30px;">
    <div class="col-lg-12">
        <h2>{{{{title}}}}</h2>
        <strong style="float: right;color: grey;opacity: 0.4;margin-top: -30px;">{{% now "jS F Y H:i" %}}</strong>
        <div class="separ" style="background-color: grey;opacity: 0.2"></div>
        <div class="panel panel-default" style="border: none;">
            <div class="panel" style="background-color:#f5f5f5;border: none;">
                <div class="col-md-8" style="padding: 10px;">
                    <div>
                        <div class="mb-4">
                            <!-- Card Body -->
                            <div class="card-body">
                                <div class="chart-area item-dash" style="padding: 15px;background-color: white;">
                                    <canvas id="myAreaChart"></canvas>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-4" style="padding: 10px;">
                    <div style="">
                        <div class="mb-4 ">
                            <!-- Card Body -->
                            <div class="card-body">
                                <div class="chart-pie pt-4 item-dash" style="padding: 15px;background-color: white;">
                                    <canvas id="myPieChart"></canvas>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="panel panel-success p1" style="border-radius: 10px;border-bottom: none;">
                    <div class="panel-heading" style="background-color: transparent;color: white;">
                        <div class="row">
                            <div class="col-xs-7 text-left">
                                <div style="font-weight: 500;">Documents</div>
                                <p style="font-size: 20px;font-family: gotham">260</p>
                            </div>
                            <div class="col-xs-5 text-right">
                                <i class="fa fa-bank fa-3x" style="float: left;opacity: 0.3"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="panel panel-success p2" style="border-radius: 10px;border-bottom: none;">
                    <div class="panel-heading" style="background-color: transparent;color: white;">
                        <div class="row">
                            <div class="col-xs-7 text-left">
                                <div style="font-weight: 500;">Dossiers</div>
                                <p style="font-size: 20px;font-family: gotham">260</p>
                            </div>
                            <div class="col-xs-5 text-right">
                                <i class="fa fa-bank fa-3x" style="float: left;opacity: 0.3"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="panel panel-success p3" style="border-radius: 10px;border-bottom: none;">
                    <div class="panel-heading" style="background-color: transparent;color: white;">
                        <div class="row">
                            <div class="col-xs-7 text-left">
                                <div style="font-weight: 500;">Documents</div>
                                <p style="font-size: 20px;font-family: gotham">260</p>
                            </div>
                            <div class="col-xs-5 text-right">
                                <i class="fa fa-bank fa-3x" style="float: left;opacity: 0.3"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="panel panel-success p4" style="border-radius: 10px;border-bottom: none;">
                    <div class="panel-heading" style="background-color: transparent;color: white;">
                        <div class="row">
                            <div class="col-xs-7 text-left">
                                <div style="font-weight: 500;">Dossiers</div>
                                <p style="font-size: 20px;font-family: gotham">260</p>
                            </div>
                            <div class="col-xs-5 text-right">
                                <i class="fa fa-bank fa-3x" style="float: left;opacity: 0.3"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-4" style="padding: 10px;">
                <div class="item-dash col-md-12" style="background-color: white;height: 300px;padding: 20px;padding-top: 25px;">
                    <label style="font-weight: 900;">Documents Recents</label>

                    <ul style="width: 100%;padding: 10px;">
                        <li><strong style="font-weight: 600;">Bon d'achat BA001</strong>
                            <p style="float: right;font-size: 12px;color: grey;">Mardi 01 2017
                            </p>
                            <p style="font-size: 13px;color: grey;">Approuve</p>
                        </li>
                        <li><label style="font-">Bon d'achat BA001</label>
                            <p style="float: right;font-size: 12px;color: grey;">Mardi 01 2017
                            </p>
                            <p style="font-size: 13px;color: grey;">Approuve</p>
                        </li>
                        <li><label style="font-">Bon d'achat BA001</label>
                            <p style="float: right;font-size: 12px;color: grey;">Mardi 01 2017
                            </p>
                            <p style="font-size: 13px;color: grey;">Approuve</p>
                        </li>
                        <li><label style="font-">Bon d'achat BA001</label>
                            <p style="float: right;font-size: 12px;color: grey;">Mardi 01 2017
                            </p>
                            <p style="font-size: 13px;color: grey;">Approuve</p>
                        </li>

                    </ul>
                </div>
            </div>
            <div class="col-md-4" style="padding: 10px;">
                <div class="item-dash col-md-12" style="background-color: white;height: 300px;padding: 20px;padding-top: 25px;">
                    <label style="font-weight: 900;">Documents Recents</label>

                    <ul style="width: 100%;padding: 10px;">
                        <li><strong style="font-weight: 600;">Bon d'achat BA001</strong>
                            <p style="float: right;font-size: 12px;color: grey;">Mardi 01 2017
                            </p>
                            <p style="font-size: 13px;color: grey;">Approuve</p>
                        </li>
                        <li><label style="font-">Bon d'achat BA001</label>
                            <p style="float: right;font-size: 12px;color: grey;">Mardi 01 2017
                            </p>
                            <p style="font-size: 13px;color: grey;">Approuve</p>
                        </li>
                        <li><label style="font-">Bon d'achat BA001</label>
                            <p style="float: right;font-size: 12px;color: grey;">Mardi 01 2017
                            </p>
                            <p style="font-size: 13px;color: grey;">Approuve</p>
                        </li>
                        <li><label style="font-">Bon d'achat BA001</label>
                            <p style="float: right;font-size: 12px;color: grey;">Mardi 01 2017
                            </p>
                            <p style="font-size: 13px;color: grey;">Approuve</p>
                        </li>

                    </ul>
                </div>
            </div>
            <div class="col-md-4" style="padding: 10px;">
                <div class="item-dash col-md-12" style="background-color: white;height: 300px;padding: 20px;padding-top: 25px;">
                    <label style="font-weight: 900;">Documents Recents</label>

                    <ul style="width: 100%;padding: 10px;">
                        <li><strong style="font-weight: 600;">Bon d'achat BA001</strong>
                            <p style="float: right;font-size: 12px;color: grey;">Mardi 01 2017
                            </p>
                            <p style="font-size: 13px;color: grey;">Approuve</p>
                        </li>
                        <li><label style="font-">Bon d'achat BA001</label>
                            <p style="float: right;font-size: 12px;color: grey;">Mardi 01 2017
                            </p>
                            <p style="font-size: 13px;color: grey;">Approuve</p>
                        </li>
                        <li><label style="font-">Bon d'achat BA001</label>
                            <p style="float: right;font-size: 12px;color: grey;">Mardi 01 2017
                            </p>
                            <p style="font-size: 13px;color: grey;">Approuve</p>
                        </li>
                        <li><label style="font-">Bon d'achat BA001</label>
                            <p style="float: right;font-size: 12px;color: grey;">Mardi 01 2017
                            </p>
                            <p style="font-size: 13px;color: grey;">Approuve</p>
                        </li>

                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>


<script src="{{% static 'ErpProject/js/Chart.min.js' %}}"></script>
<script src="{{% static 'ErpProject/js/chart-pie-demo.js' %}}"></script>
<script src="{{% static 'ErpProject/js/chart-area-demo.js' %}}"></script>

{{% endblock %}}
    '''.format(nomModule)
    return texte_a_ajouter

def genCssOrangeTemplate(nomModule):
    texte_a_ajouter = u'''
/******************************************************************/
/*  MODULE {0} (Couleur customisée)
/******************************************************************/
/** Degradé pour le menu lateral **/
.module_{1} {{
    background: -moz-linear-gradient(top,rgba(92, 52, 33, 0.7) 0%,rgba(116, 72, 54, 0.79) 29%,rgba(155, 125, 90, 0.89) 62%,rgb(175, 146, 126) 100%);
    background: -webkit-linear-gradient(top,rgba(92, 52, 33, 0.7) 0%,rgba(116, 72, 54, 0.79) 29%,rgba(155, 125, 90, 0.89) 62%,rgb(175, 146, 126) 100%);
    background: linear-gradient(to bottom,rgba(92, 52, 33, 0.7) 0%,rgba(116, 72, 54, 0.79) 29%,rgba(155, 125, 90, 0.89) 62%,rgb(175, 146, 126) 100%);
    filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#b3d64f0d', endColorstr='#e58f4e',GradientType=0 ); /* IE6-9 */
}}
.color_{1}s {{
    background: rgb(104, 53, 28);
    background: -moz-linear-gradient(left,rgba(104, 53, 28, 0.7) 0%,rgba(143, 83, 56, 0.79) 29%,rgba(153, 117, 77, 0.89) 62%,rgb(214, 163, 127) 100%);
    background: -webkit-linear-gradient(left,rgba(104, 53, 28, 0.7) 0%,rgba(143, 83, 56, 0.79) 29%,rgba(153, 117, 77, 0.89) 62%,rgb(214, 163, 127) 100%);
    background: linear-gradient(to right,rgba(104, 53, 28, 0.7) 0%,rgba(143, 83, 56, 0.79) 29%,rgba(153, 117, 77, 0.89) 62%,rgb(214, 163, 127) 100%);
    filter: progid: DXImageTransform.Microsoft.gradient( startColorstr='#ff6821', endColorstr='#fd9526', GradientType=1);
    border: none;
    color: white;
}}
/** Liste Active item dans le navbar **/
.breadcrumbs2 .primary_color_module_{1} a {{
    background: #723c21 !important;
    color: #ffffff !important;
}}
.breadcrumbs2 .primary_color_module_{1}:before {{
    border-color: #8f4c2b #8f4c2b #8f4c2b transparent !important;
}}
.breadcrumbs2 .primary_color_module_{1} :after {{
    border-left-color: #8f4c2b !important;
}}
.active_module_{1} {{
    border-bottom: 4px solid rgba(104, 53, 28, 0.7) !important;
}}
.active_module_{1} > a {{
    color: rgba(214, 79, 13, 1) !important;
}}
/** Graphique, Bouton, Barre de nav ...**/
.primary_color_module_{1} {{
    background-color: rgba(214, 79, 13, 1) !important;
    color: white !important;
}}
.secondary_color_module_{1} {{
    background-color: rgba(214, 79, 13, 0.6) !important;
    color: white !important;
}}
.thirdy_color_module_{1} {{
    background-color: rgba(214, 79, 13, 0.2) !important;
    color: white !important;
}}
.primary_color_module_{1}:hover {{
    background-color: #d64f0d !important;
    color: white !important;
}}
.breadcrumbs2 .primary_color_module_{1} a {{
    background: #d64f0d !important;
    color: #ffffff !important;
}}
.breadcrumbs2 .primary_color_module_{1}:before {{
    border-color: #d64f0d #d64f0d #d64f0d transparent !important;
}}
.breadcrumbs2 .primary_color_module_{1} :after {{
    border-left-color: #d64f0d !important;
}}
.module_{1} .head {{
    background-color: #d64f0d !important;
    padding: 10px!important;
    color: white!important;
}}
/******************************************************************/
/*  FIN MODULE {0}
/******************************************************************/

    '''.format(unidecode.unidecode(nomModule.upper()), unidecode.unidecode(nomModule.lower()))
    return texte_a_ajouter

def genCssVertTemplate(nomModule):
    texte_a_ajouter = u'''
/******************************************************************/
/*  MODULE {0} (Couleur customisée)
/******************************************************************/
/** Degradé pour le menu lateral **/
.module_{1} {{
    background: -moz-linear-gradient(top,rgba(27, 124, 79, 0.8) 0%,rgba(53, 143, 101, 0.8) 2%,rgba(81, 163, 125, 0.8) 28%,rgba(115, 177, 148, 0.8) 71%,rgba(104, 179, 144, 0.8) 100%);
    background: -webkit-linear-gradient(top,rgba(27, 124, 79, 0.8) 0%,rgba(53, 143, 101, 0.8) 2%,rgba(81, 163, 125, 0.8) 28%,rgba(115, 177, 148, 0.8) 71%,rgba(104, 179, 144, 0.8) 100%);
    background: linear-gradient(to bottom,rgba(27, 124, 79, 0.8) 0%,rgba(53, 143, 101, 0.8) 2%,rgba(81, 163, 125, 0.8) 28%,rgba(115, 177, 148, 0.8) 71%,rgba(104, 179, 144, 0.8) 100%);
    filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#cc999900', endColorstr='#c1b507',Gradi0ntType=0 ); /* IE6-9 */
}}
.color_{1}s {{
    background: -moz-linear-gradient(top,rgba(27, 124, 79, 0.8) 0%,rgba(53, 143, 101, 0.8) 2%,rgba(81, 163, 125, 0.8) 28%,rgba(115, 177, 148, 0.8) 71%,rgba(104, 179, 144, 0.8) 100%);
    background: -webkit-linear-gradient(top,rgba(27, 124, 79, 0.8) 0%,rgba(53, 143, 101, 0.8) 2%,rgba(81, 163, 125, 0.8) 28%,rgba(115, 177, 148, 0.8) 71%,rgba(104, 179, 144, 0.8) 100%);
    background: linear-gradient(to bottom,rgba(27, 124, 79, 0.8) 0%,rgba(53, 143, 101, 0.8) 2%,rgba(81, 163, 125, 0.8) 28%,rgba(115, 177, 148, 0.8) 71%,rgba(104, 179, 144, 0.8) 100%);
    filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#cc999900', endColorstr='#c1b507',Gradi0ntType=0 ); /* IE6-9 */
}}
/** Liste Active item dans le navbar **/
.breadcrumbs2 .primary_color_module_{1} a {{
	background: rgb(20, 102, 71) !important;
	color: #ffffff !important;
}}
.breadcrumbs2 .primary_color_module_{1}:before {{
	border-color: #991b58 #991b58 #991b58 transparent !important;
}}
.breadcrumbs2 .primary_color_module_{1} :after {{
	border-left-color: #991b58 !important;
}}
.active_module_{1} {{
	border-bottom: 4px solid rgb(20, 102, 71) !important;
}}
.active_module_{1} > a {{
	color: rgb(20, 102, 71) !important;
}}
/** Graphique, Bouton, Barre de nav ...**/
.primary_color_module_{1} {{
    background-color: rgba(27, 124, 79, 0.8) !important;
    color: white !important;
}}
.primary_color_module_{1}:hover {{
	background-color: #d5ab47 !important;
	color: white !important;
}}
.secondary_color_module_{1} {{
	background-color: rgba(31, 126, 82, 0.8) !important;
	color: white !important;
}}
.thirdy_color_module_{1} {{
	background-color: rgba(27, 124, 79, 0.2) !important;
	color: white !important;
}}
.primary_color_module_{1}:hover {{
	background-color: rgba(154, 194, 175, 0.2) !important;
	color: white !important;
}}
.module_{1} .head {{
	background-color: rgba(27, 124, 79, 0.8)!important;
	padding: 10px!important;
	color: white!important;
}}
/******************************************************************/
/*  FIN MODULE {0}
/******************************************************************/

    '''.format(unidecode.unidecode(nomModule.upper()), unidecode.unidecode(nomModule.lower()))
    return texte_a_ajouter

def genCssBleuTemplate(nomModule):
    texte_a_ajouter = u'''
/******************************************************************/
/*  MODULE {0} (Couleur customisée)
/******************************************************************/
/** Degradé pour le menu lateral **/
.module_{1} {{
	background: -moz-linear-gradient(top,rgba(1, 79, 141, 0.7) 0%,rgba(11, 89, 151, 0.79) 30%,rgba(46, 160, 161, 0.89) 64%,rgba(66, 206, 161, 1) 100%);
	background: -webkit-linear-gradient(top,rgba(1, 79, 141, 0.7) 0%,rgba(11, 89, 151, 0.79) 30%,rgba(46, 160, 161, 0.89) 64%,rgba(66, 206, 161, 1) 100%);
	background: linear-gradient(to bottom,rgba(1, 79, 141, 0.7) 0%,rgba(11, 89, 151, 0.79) 30%,rgba(46, 160, 161, 0.89) 64%,rgba(66, 206, 161, 1) 100%);
	filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#b3014f8d', endColorstr='#42cea1',GradientType=0 ); /* IE6-9 */
}}
.color_{1}s {{
	background: rgb(102, 114, 250);
	/* Old browsers */
	background: -moz-linear-gradient(left,rgba(102, 114, 250, 1) 0%,rgba(103, 132, 250, 1) 29%,rgba(104, 152, 252, 1) 52%,rgba(106, 200, 252, 1) 100%);
	background: -webkit-linear-gradient(left,rgba(102, 114, 250, 1) 0%,rgba(103, 132, 250, 1) 29%,rgba(104, 152, 252, 1) 52%,rgba(106, 200, 252, 1) 100%);
	background: linear-gradient(to right,rgba(102, 114, 250, 1) 0%,rgba(103, 132, 250, 1) 29%,rgba(104, 152, 252, 1) 52%,rgba(106, 200, 252, 1) 100%);
	filter: progid: DXImageTransform.Microsoft.gradient( startColorstr='#6672fa', endColorstr='#6ac8fc', GradientType=1);
	color: white;
}}
/** Liste Active item dans le navbar **/
.breadcrumbs2 .primary_color_module_{1} a {{
	background: #216ca8 !important;
	color: #ffffff !important;
}}
.breadcrumbs2 .primary_color_module_{1}:before {{
	border-color: #216ca8 #216ca8 #216ca8 transparent !important;
}}
.breadcrumbs2 .primary_color_module_{1} :after {{
	border-left-color: #216ca8!important;
}}
.active_module_{1} {{
	border-bottom: 4px solid #216ca8 !important;
}}
.active_module_{1} > a {{
	color: #216ca8 !important;
}}
/** Graphique, Bouton, Barre de nav ...**/
.primary_color_module_{1} {{
	background-color: rgba(33, 108, 168, 1)!important;
	color: white!important;
}}
.secondary_color_module_{1} {{
	background-color: rgba(33, 108, 168, 0.6)!important;
	color: white!important;
}}
.thirdy_color_module_{1} {{
	background-color: rgba(33, 108, 168, 0.2)!important;
	color: white!important;
}}
.primary_color_module_{1}:hover {{
	background-color: #216ca8!important;
	color: white!important;
}}
.module_{1} .head {{
	background-color: rgba(33, 108, 168, 1)!important;
	padding: 10px!important;
	color: white!important;
}}
/******************************************************************/
/*  FIN MODULE {0}
/******************************************************************/

    '''.format(unidecode.unidecode(nomModule.upper()), unidecode.unidecode(nomModule.lower()))
    return texte_a_ajouter

def genCssBleuCielTemplate(nomModule):
    texte_a_ajouter = u'''
/******************************************************************/
/*  MODULE {0} (Couleur customisée)
/******************************************************************/
/** Degradé pour le menu lateral **/
.module_{1} {{
	background: -moz-linear-gradient(top,rgba(117, 114, 220, 0.7) 0%,rgba(106, 121, 227, 0.79) 29%,rgba(100, 129, 237, 0.89) 62%,rgb(155, 160, 199) 100%);
	background: -webkit-linear-gradient(top,rgba(117, 114, 220, 0.7) 0%,rgba(106, 121, 227, 0.79) 29%,rgba(100, 129, 237, 0.89) 62%,rgb(155, 160, 199) 100%);
	background: linear-gradient(to bottom,rgba(117, 114, 220, 0.7) 0%,rgba(106, 121, 227, 0.79) 29%,rgba(100, 129, 237, 0.89) 62%,rgb(155, 160, 199) 100%);
	filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#b3d64f0d', endColorstr='#e58f4e',GradientType=0 ); /* IE6-9 */
}}
.color_{1}s {{
	background: rgb(117, 114, 220);
	background: -moz-linear-gradient(left,rgba(117, 114, 220, 0.7) 0%,rgba(106, 121, 227, 0.79) 29%,rgba(100, 129, 237, 0.89) 62%,rgb(155, 160, 199) 100%);
	background: -webkit-linear-gradient(left,rgba(117, 114, 220, 0.7) 0%,rgba(106, 121, 227, 0.79) 29%,rgba(100, 129, 237, 0.89) 62%,rgb(155, 160, 199) 100%);
	background: linear-gradient(to right,rgba(117, 114, 220, 0.7) 0%,rgba(106, 121, 227, 0.79) 29%,rgba(100, 129, 237, 0.89) 62%,rgb(155, 160, 199) 100%);
	filter: progid: DXImageTransform.Microsoft.gradient( startColorstr='#ff6821', endColorstr='#fd9526', GradientType=1);
	border: none;
	color: white;
}}
/** Liste Active item dans le navbar **/
.breadcrumbs2 .primary_color_module_{1} a {{
	background: #6977E2 !important;
	color: #ffffff !important;
}}
.breadcrumbs2 .primary_color_module_{1}:before {{
	border-color: #7572DC #7572DC #7572DC transparent !important;
}}
.breadcrumbs2 .primary_color_module_{1} :after {{
	border-left-color: #7572DC !important;
}}
.active_module_{1} {{
	border-bottom: 4px solid rgba(117, 114, 220, 0.7) !important;
}}
.active_module_{1} > a {{
	color: rgba(106, 121, 227, 1) !important;
}}
/** Graphique, Bouton, Barre de nav ...**/
.primary_color_module_{1} {{
	background-color: rgba(106, 121, 227, 1) !important;
	color: white !important;
}}
.secondary_color_module_{1} {{
	background-color: rgba(106, 121, 227, 0.6) !important;
	color: white !important;
}}
.thirdy_color_module_{1} {{
	background-color: rgba(106, 121, 227, 0.2) !important;
	color: white !important;
}}
.primary_color_module_{1}:hover {{
	background-color: #6A79E3 !important;
	color: white !important;
}}
.breadcrumbs2 .primary_color_module_{1} a {{
	background: #6A79E3 !important;
	color: #ffffff !important;
}}
.breadcrumbs2 .primary_color_module_{1}:before {{
	border-color: #6A79E3 #6A79E3 #6A79E3 transparent !important;
}}
.breadcrumbs2 .primary_color_module_{1} :after {{
	border-left-color: #6A79E3 !important;
}}
.module_{1} .head {{
	background-color: #6A79E3 !important;
	padding: 10px!important;
	color: white!important;
}}
/******************************************************************/
/*  FIN MODULE {0}
/******************************************************************/

    '''.format(unidecode.unidecode(nomModule.upper()), unidecode.unidecode(nomModule.lower()))
    return texte_a_ajouter

def genCssMagentaTemplate(nomModule):
    texte_a_ajouter = u'''
/******************************************************************/
/*  MODULE {0} (Couleur customisée)
/******************************************************************/
/** Degradé pour le menu lateral **/
.module_{1} {{
	background: -moz-linear-gradient(top,rgba(89, 15, 92, 0.7) 0%,rgba(118, 39, 121, 0.7) 30%,rgba(162, 88, 163, 0.7) 64%,rgba(192, 157, 194, 0.7) 100%);
	background: -webkit-linear-gradient(top,rgba(89, 15, 92, 0.7) 0%,rgba(118, 39, 121, 0.7) 30%,rgba(162, 88, 163, 0.7) 64%,rgba(192, 157, 194, 0.7) 100%);
	background: linear-gradient(to bottom,rgba(89, 15, 92, 0.7) 0%,rgba(118, 39, 121, 0.7) 30%,rgba(162, 88, 163, 0.7) 64%,rgba(192, 157, 194, 0.7) 100%);
	filter: progid: DXImageTransform.Microsoft.gradient( startColorstr='#b361188d', endColorstr='#c21e65', GradientType=0);
}}
.color_{1}s {{
	background: rgba(89, 15, 92, 0.7);
	background: -moz-linear-gradient(left,rgba(89, 15, 92, 0.7) 0%,rgba(89, 15, 92, 0.7) 29%,rgba(89, 15, 92, 0.7) 52%,rgba(89, 15, 92, 0.7) 100%);
	background: -webkit-linear-gradient(left,rgba(89, 15, 92, 0.7) 0%,rgba(89, 15, 92, 0.7) 29%,rgba(89, 15, 92, 0.7) 52%,rgba(89, 15, 92, 0.7) 100%);
	background: linear-gradient(to right,rgba(89, 15, 92, 0.7) 0%,rgba(89, 15, 92, 0.7) 29%,rgba(89, 15, 92, 0.7) 52%,rgba(89, 15, 92, 0.7) 100%);
	filter: progid: DXImageTransform.Microsoft.gradient( startColorstr='#494949', endColorstr='#989898', GradientType=1);
}}
/** Liste Active item dans le navbar **/
.active_module_{1} {{
	border-bottom: 4px solid rgb(89, 15, 92) !important;
}}
.active_module_{1} > a {{
	color: rgb(89, 15, 92) !important;
}}
/** Graphique, Bouton, Barre de nav ...**/
.primary_color_module_{1} {{
	background-color: rgba(89, 15, 92, 0.7) !important;
	color: white !important;
}}
.secondary_color_module_{1} {{
	background-color: rgba(162, 88, 163, 0.7) !important;
	color: white !important;
}}
.thirdy_color_module_{1} {{
	background-color: rgba(192, 157, 194, 0.2) !important;
	color: white !important;
}}
.primary_color_module_{1}:hover {{
	background-color: #8600a7 !important;
	color: white !important;
}}
.module_{1} .head {{
	background-color: rgba(89, 15, 92, 0.7) !important;
	padding: 10px!important;
	color: white!important;
}}
/******************************************************************/
/*  FIN MODULE {0}
/******************************************************************/

    '''.format(unidecode.unidecode(nomModule.upper()), unidecode.unidecode(nomModule.lower()))
    return texte_a_ajouter

def genCssPourpreTemplate(nomModule):
    texte_a_ajouter = u'''
/******************************************************************/
/*  MODULE {0} (Couleur customisée)
/******************************************************************/
/** Degradé pour le menu lateral **/
.module_{1} {{
	background: rgb(169,3,41);
	background: -moz-linear-gradient(top,  rgba(169, 3, 41, 0.05) 0%, rgba(169, 3, 41, 0.84) 29%, rgb(143,2,34) 62%,rgb(109,0,25) 100%);
	background: -webkit-linear-gradient(top,  rgba(169, 3, 41, 0.05) 0%, rgba(169, 3, 41, 0.84) 29%, rgb(143,2,34) 62%,rgb(109,0,25) 100%);
	background: linear-gradient(to bottom,  rgba(169, 3, 41, 0.05) 0%, rgba(169, 3, 41, 0.84) 29%, rgb(143,2,34) 62%,rgb(109,0,25) 100%);
	filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#a90329', endColorstr='#6d0019',GradientType=0 );

}}
.color_{1}s {{
	background: rgb(169,3,41);
	background: -moz-linear-gradient(top,  rgba(169, 3, 41, 0.05) 0%, rgba(169, 3, 41, 0.84) 29%, rgb(143,2,34) 62%,rgb(109,0,25) 100%);
	background: -webkit-linear-gradient(top,  rgba(169, 3, 41, 0.05) 0%, rgba(169, 3, 41, 0.84) 29%, rgb(143,2,34) 62%,rgb(109,0,25) 100%);
	background: linear-gradient(to bottom,  rgba(169, 3, 41, 0.05) 0%, rgba(169, 3, 41, 0.84) 29%, rgb(143,2,34) 62%,rgb(109,0,25) 100%);
	filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#a90329', endColorstr='#6d0019',GradientType=0 );
}}

/** Liste Active item dans le navbar **/
.breadcrumbs2 .primary_color_module_{1} a {{
	background: #991b58 !important;
	color: #ffffff !important;
}}
.breadcrumbs2 .primary_color_module_{1}:before {{
border-color: #991b58 #991b58 #991b58 transparent !important;
}}
.breadcrumbs2 .primary_color_module_{1} :after {{
	border-left-color: #991b58 !important;
}}
.active_module_{1} {{
	border-bottom: 4px solid #991b58 !important;
}}
.active_module_{1} > a {{
	color: #991b58 !important;
}}
/** Graphique, Bouton, Barre de nav ...**/
.primary_color_module_{1}_new_color{{
	background:#BD6C93;
	color:#000;
}}
.primary_color_module_{1} {{
	background-color: rgba(153, 27, 88, 1) !important;
	color: white !important;
}}
.secondary_color_module_{1} {{
	background-color: rgba(153, 27, 88, 0.6) !important;
	color: white !important;
}}
.thirdy_color_module_{1} {{
	background-color: rgba(153, 27, 88, 0.2) !important;
	color: white !important;
}}
.primary_color_module_{1}:hover {{
	background-color: #991b58 !important;
	color: white !important;
}}
.secondary_color_module_{1} {{
	background-color: rgba(33, 108, 168, 0.6);
	color: white;
}}
.thirdy_color_module_{1} {{
	background-color: rgba(33, 108, 168, 0.2);
	color: white;
}}
.primary_color_module_{1}:hover {{
	background-color: #216ca8;
	color: white;
}}
.module_{1} .head {{
	background-color: rgba(153, 27, 88, 1) !important;
	padding: 10px!important;
	color: white!important;
}}
/******************************************************************/
/*  FIN MODULE {0}
/******************************************************************/
    '''.format(unidecode.unidecode(nomModule.upper()), unidecode.unidecode(nomModule.lower()))
    return texte_a_ajouter


def genDAOofModelContentType(content_type_id, module_id):
    module = dao_module.toGetModule(module_id)
    nomModule = module.nom_application

    content_type = ContentType.objects.get(id = content_type_id)
    model_class = content_type.model_class()

    #Standardisation denomination modele
    nom_modele = content_type.model.replace("model_","").capitalize()
    nom_modele_verbose = model_class._meta.verbose_name
    nom_modele_verbose_plural = model_class._meta.verbose_name_plural
    nom_modele_class = model_class.__name__

    list_nom_champ = []
    list_type_champ = []
    list_champs = []
    for field in model_class._meta.get_fields():
        if field.name not in ("id", "statut", "etat", "creation_date", "update_date", "auteur") and field.__class__.__name__ != "ManyToOneRel": list_nom_champ.append(field.name)

    for field in model_class._meta.get_fields():
        if field.name not in ("id", "statut", "etat", "creation_date", "update_date", "auteur") and field.__class__.__name__ != "ManyToOneRel": list_type_champ.append(field.__class__.__name__)

    for field in model_class._meta.get_fields():
        if field.name not in ("id", "statut", "etat", "creation_date", "update_date", "auteur") and field.__class__.__name__ != "ManyToOneRel": list_champs.append(field)

    #Creation dossier dao
    try:
        path = os.path.abspath(os.path.curdir)
        path = path + "\\{0}\\dao".format(nomModule)
        os.mkdir(path)
    except Exception as e:
        pass

    print("Dossier Dao cree")
    nomdao="dao_{0}".format(nom_modele.lower())
    path = path + "\\{0}.py".format(nomdao)

    fichier = codecs.open(path,"w", encoding='utf-8')

    # WRITE import lib
    if nomModule == "ErpBackOffice": texte_a_ajouter_dao = "from __future__ import unicode_literals\nfrom {0}.models import *\nfrom django.utils import timezone".format(nomModule,nom_modele_class,nomdao)
    else : texte_a_ajouter_dao = "from __future__ import unicode_literals\nfrom {0}.models import *\nfrom ErpBackOffice.models import *\nfrom django.utils import timezone".format(nomModule,nom_modele_class,nomdao)

    # WRITE Class Dao and Properties
    texte_a_ajouter_dao = texte_a_ajouter_dao + "\n\nclass {}(object):".format(nomdao)
    for i in range(0,len(list_nom_champ)):
        nom_champ = ""
        try:
            nom_champ = list_nom_champ[i]
            nom_champ = nom_champ.lower()
        except Exception as e:
            pass
        try:
            texte_add = ""
            type_data = str(list_type_champ[i])
            if type_data in ("CharField", "EmailField") :
                texte_add = "\n\t{0} = ''".format(nom_champ)
            elif type_data == "IntegerField":
                texte_add = "\n\t{0} = 0".format(nom_champ)
            elif type_data == "DateTimeField":
                texte_add = "\n\t{0} = '2010-01-01 00:00:00'".format(nom_champ)
            elif type_data == "DateField":
                texte_add = "\n\t{0} = '2010-01-01'".format(nom_champ)
            elif type_data == "FloatField":
                texte_add = "\n\t{0} = 0.0".format(nom_champ)
            elif type_data == "BooleanField" :
                texte_add = "\n\t{0} = False".format(nom_champ)
            elif type_data == "ManyToManyField" :
                texte_add = "\n\t{0} = []".format(nom_champ)
            elif type_data in ("ForeignKey", "OneToOneField"):
                texte_add = "\n\t{0}_id = None".format(nom_champ)
            else:
                texte_add = "\n\t{0} = None".format(nom_champ)
        except Exception as e:
            pass
        texte_a_ajouter_dao = texte_a_ajouter_dao + texte_add

    # WRITE toList() Function
    texte_a_ajouter_dao = texte_a_ajouter_dao + "\n\n\t@staticmethod\n\tdef toList():\n\t\treturn {1}.objects.all().order_by('creation_date')".format(nom_modele,nom_modele_class)

    # WRITE toCreate() Function declaration
    text_parenthese = "\n\n\t@staticmethod\n\tdef toCreate("
    for i in range(0,len(list_nom_champ)):
        nom_champ = ""
        type_data = ""
        default_value = ""
        is_null = True
        try:
            nom_champ = list_nom_champ[i]
            nom_champ = nom_champ.lower()
            type_data = str(list_type_champ[i])
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass
        # Contrôle quand on n'a pas défini une valeur par defaut et que le champ est requis
        check_nullable = True
        if inspect.isclass(default_value) == True and is_null == False and type_data != "ManyToManyField": check_nullable = False

        if type_data in ("ForeignKey", "OneToOneField"): nom_champ = "{0}_id".format(nom_champ)

        if check_nullable:
            if type_data == "ManyToManyField":
                text_parenthese = text_parenthese + "{0} = [], ".format(nom_champ)
            elif type_data in ("EmailField", "CharField"):
                text_parenthese = text_parenthese + "{0} = '', ".format(nom_champ)
            else:
                text_parenthese = text_parenthese + "{0} = None, ".format(nom_champ)
        else: text_parenthese = text_parenthese + "{0}, ".format(nom_champ)


    text_parenthese = text_parenthese[:len(text_parenthese)-2]
    text_parenthese = text_parenthese + "):"
    texte_a_ajouter_dao = texte_a_ajouter_dao + text_parenthese

    # WRITE toCreate() Function Body
    text_tocreate = "\n\t\ttry:\n\t\t\t{0} = {1}()".format(nom_modele.lower(),nomdao)
    for i in range(0,len(list_nom_champ)):
        nom_champ = ""
        type_data = ""
        try:
            nom_champ = list_nom_champ[i]
            nom_champ = nom_champ.lower()
            type_data = str(list_type_champ[i])
        except Exception as e:
            pass
        if type_data in ("ForeignKey", "OneToOneField"): nom_champ = "{0}_id".format(nom_champ)
        text_tocreate = text_tocreate + "\n\t\t\t{0}.{1} = {1}".format(nom_modele.lower(),nom_champ)
    texte_a_ajouter_dao = texte_a_ajouter_dao + text_tocreate
    texte_a_ajouter_dao = texte_a_ajouter_dao + "\n\t\t\treturn {0}\n\t\texcept Exception as e:\n\t\t\t#print('ERREUR LORS DE LA CREATION DE LA {1}')\n\t\t\t#print(e)\n\t\t\treturn None".format(nom_modele.lower(),nom_modele.upper(),nom_modele.capitalize())

    # WRITE toSave() Function
    text_tosave = "\n\n\t@staticmethod\n\tdef toSave(auteur, objet_dao_{0}):\n\t\ttry:\n\t\t\t{0}  = Model_{2}()".format(nom_modele.lower(),nom_modele.upper(),nom_modele.capitalize())
    for i in range(0,len(list_nom_champ)):
        nom_champ = ""
        type_data = ""
        default_value = ""
        is_null = True
        try:
            nom_champ = list_nom_champ[i]
            type_data = str(list_type_champ[i])
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass
        # Contrôle quand on n'a pas défini une valeur par defaut et que le champ est requis
        check_nullable = True
        if inspect.isclass(default_value) == True and is_null == False and type_data != "ManyToManyField": check_nullable = False

        if type_data in ("ForeignKey", "OneToOneField"): nom_champ = "{0}_id".format(nom_champ)
        if type_data != "ManyToManyField":
            if type_data in ("ImageField", "FileField") or check_nullable:
                text_tosave = text_tosave + "\n\t\t\tif objet_dao_{0}.{1} != None : {0}.{1} = objet_dao_{0}.{1}".format(nom_modele.lower(), nom_champ.lower(), nom_modele.capitalize())
            else: text_tosave = text_tosave + "\n\t\t\t{0}.{1} = objet_dao_{0}.{1}".format(nom_modele.lower(), nom_champ.lower(), nom_modele.capitalize())
    texte_a_ajouter_dao = texte_a_ajouter_dao + text_tosave
    texte_a_ajouter_dao = texte_a_ajouter_dao + "\n\t\t\tif auteur != None : {0}.auteur_id = auteur.id\n\n\t\t\t{0}.save()".format(nom_modele.lower())

    for field in model_class._meta.get_fields():
        if field.name not in ("id", "statut", "etat", "creation_date", "update_date", "auteur") and field.__class__.__name__ != "ManyToOneRel" and field.__class__.__name__ == 'ManyToManyField' and field.related_model != None:
            texte_a_ajouter_dao = texte_a_ajouter_dao + "\n\n\t\t\t#Ajout Champs (ManyToMany - Creation)\n\t\t\tfor i in range(0, len(objet_dao_{0}.{1})):\n\t\t\t\ttry:\n\t\t\t\t\tobjet = {2}.objects.get(pk = objet_dao_{0}.{1}[i])\n\t\t\t\t\t{0}.{1}.add(objet)\n\t\t\t\texcept Exception as e: pass".format(nom_modele.lower(),nom_champ.lower(), field.related_model.__name__)

    texte_a_ajouter_dao = texte_a_ajouter_dao + "\n\n\t\t\treturn True, {0}, ''\n\t\texcept Exception as e:\n\t\t\t#print('ERREUR LORS DE L ENREGISTREMENT DE LA {1}')\n\t\t\t#print(e)\n\t\t\treturn False, None, e".format(nom_modele.lower(),nom_modele.upper(),nom_modele.capitalize())

    # WRITE toUpdate() Function
    text_toupdate = "\n\n\t@staticmethod\n\tdef toUpdate(id, objet_dao_{0}):\n\t\ttry:\n\t\t\t{0} = Model_{2}.objects.get(pk = id)".format(nom_modele.lower(),nom_modele.upper(),nom_modele.capitalize())
    for i in range(0,len(list_nom_champ)):
        nom_champ = ""
        type_data = ""
        try:
            nom_champ = list_nom_champ[i]
            nom_champ = nom_champ.lower()
            type_data = str(list_type_champ[i])
        except Exception as e:
            pass
        if type_data in ("ForeignKey", "OneToOneField"): nom_champ = "{0}_id".format(nom_champ)
        if type_data != "ManyToManyField":
            if type_data in ("ImageField", "FileField"):
                text_toupdate = text_toupdate + "\n\t\t\tif objet_dao_{0}.{1} != None : {0}.{1} = objet_dao_{0}.{1}".format(nom_modele.lower(), nom_champ.lower(), nom_modele.capitalize())
            else: text_toupdate = text_toupdate + "\n\t\t\t{0}.{1} = objet_dao_{0}.{1}".format(nom_modele.lower(), nom_champ.lower(), nom_modele.capitalize())
    texte_a_ajouter_dao = texte_a_ajouter_dao + text_toupdate
    texte_a_ajouter_dao = texte_a_ajouter_dao + "\n\t\t\t{0}.save()".format(nom_modele.lower(),nom_modele.upper(),nom_modele.capitalize())

    for field in model_class._meta.get_fields():
        if field.name not in ("id", "statut", "etat", "creation_date", "update_date", "auteur") and field.__class__.__name__ != "ManyToOneRel" and field.__class__.__name__ == 'ManyToManyField' and field.related_model != None:
            texte_a_ajouter_dao = texte_a_ajouter_dao + "\n\n\t\t\t#Mise à jour Champs (ManyToMany - Creation)\n\t\t\t{1}_old = {0}.{1}.all()\n\t\t\t{1}_updated = []\n\t\t\tfor i in range(0, len(objet_dao_{0}.{1})):\n\t\t\t\ttry:\n\t\t\t\t\tobjet = {2}.objects.get(pk = objet_dao_{0}.{1}[i])\n\t\t\t\t\tif objet not in {1}_old: {0}.{1}.add(objet)\n\t\t\t\t\t{1}_updated.append(objet.id)\n\t\t\t\texcept Exception as e: pass\n\t\t\t# Suppression éléments qui n'existent plus\n\t\t\tfor item in {1}_old:\n\t\t\t\tif item.id not in {1}_updated: {0}.{1}.remove(item)".format(nom_modele.lower(),nom_champ.lower(), field.related_model.__name__)

    texte_a_ajouter_dao = texte_a_ajouter_dao + "\n\n\t\t\treturn True, {0}, ''\n\t\texcept Exception as e:\n\t\t\t#print('ERREUR LORS DE LA MODIFICATION DE LA {1}')\n\t\t\t#print(e)\n\t\t\treturn False, None, e".format(nom_modele.lower(),nom_modele.upper(),nom_modele.capitalize())

    # WRITE toGet() Function
    text_toget = "\n\n\t@staticmethod\n\tdef toGet(id):\n\t\ttry:\n\t\t\treturn Model_{2}.objects.get(pk = id)\n\t\texcept Exception as e:\n\t\t\treturn None".format(nom_modele.lower(),nom_modele.upper(),nom_modele.capitalize())
    texte_a_ajouter_dao = texte_a_ajouter_dao + text_toget

    # WRITE toDelete() Function
    text_todelete = "\n\n\t@staticmethod\n\tdef toDelete(id):\n\t\ttry:\n\t\t\t{0} = Model_{2}.objects.get(pk = id)\n\t\t\t{0}.delete()\n\t\t\treturn True\n\t\texcept Exception as e:\n\t\t\treturn False".format(nom_modele.lower(),nom_modele.upper(),nom_modele.capitalize())
    texte_a_ajouter_dao = texte_a_ajouter_dao + text_todelete

    fichier.write(texte_a_ajouter_dao)
    fichier.close()
    print("Fichier Dao cree")


def genTemplateOfContentType(content_type_id, module_id, relateds = []):
    content_type = ContentType.objects.get(id = content_type_id)
    model_class = content_type.model_class()
    module = dao_module.toGetModule(module_id)
    #Standardisation denomination modele
    nom_modele = content_type.model.replace("model_","").capitalize()
    nom_modele_verbose = model_class._meta.verbose_name
    nom_modele_verbose_plural = model_class._meta.verbose_name_plural
    nom_modele_class = model_class.__name__
    nomdao="dao_{0}".format(nom_modele.lower())
    nom_pattern = 'module_{0}'.format(unidecode.unidecode(module.nom_module.lower()))
    nomModule = module.nom_application
    nameModuleUp = nom_pattern.upper()

    list_champs = []
    for field in model_class._meta.get_fields():
        if field.name not in ("id", "statut", "etat", "creation_date", "update_date", "auteur") and field.__class__.__name__ != "ManyToOneRel": list_champs.append(field)

    # CREATION FONCTIONS CRUD DANS views.py
    path = os.path.abspath(os.path.curdir)
    path = path + "\\{0}\\views.py".format(nomModule)
    fichier = codecs.open(path,"a", encoding='utf-8')

    # GET LISTER
    texte_a_ajouter_views_py = "\n\n# {2} CONTROLLERS\nfrom {4}.dao.{1} import {1}\n\ndef get_lister_{0}(request):\n\ttry:\n\t\tpermission_number = 0\n\t\tmodules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)\n\t\tif response != None: return response\n\n\t\t#*******Filtre sur les règles **********#\n\t\tmodel = dao_model.toListModel({1}.toList(), permission_number, groupe_permissions, identite.utilisateur(request))\n\t\t#******* End Regle *******************#\n\n\t\ttry:\n\t\t\tview = str(request.GET.get('view','list'))\n\t\texcept Exception as e:\n\t\t\tview = 'list'\n\t\tmodel = pagination.toGet(request, model)\n\n\t\tcontext = {{\n\t\t\t'title' : 'Liste des {3}',\n\t\t\t'model' : model,\n\t\t\t'view' : view,\n\t\t\t'utilisateur' : utilisateur,\n\t\t\t'modules' : modules,\n\t\t\t'sous_modules': sous_modules,\n\t\t\t'module' : vars_module,\n\t\t\t'organisation': dao_organisation.toGetMainOrganisation()\n\t\t}}\n\t\ttemplate = loader.get_template('ErpProject/{4}/{0}/list.html')\n\t\treturn HttpResponse(template.render(context, request))\n\texcept Exception as e:\n\t\treturn auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)".format(nom_modele.lower(),nomdao,nom_modele.upper(),nom_modele_verbose_plural.lower(),nomModule)

    # GET CREER
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\ndef get_creer_{0}(request):\n\ttry:\n\t\tpermission_number = 0\n\t\tmodules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)\n\t\tif response != None: return response\n\n\t\tcontext = {{\n\t\t\t'title' : 'Créer un nouvel objet {1}',\n\t\t\t'utilisateur' : utilisateur,\n\t\t\t'isPopup': True if 'isPopup' in request.GET else False,\n\t\t\t'modules' : modules,\n\t\t\t'sous_modules': sous_modules,\n\t\t\t'module' : vars_module,\n\t\t\t'organisation' : dao_organisation.toGetMainOrganisation(),\n\t\t\t'model' : {2}(),".format(nom_modele.lower(),nom_modele_verbose,nom_modele_class)
    related_models = []
    for field in model_class._meta.get_fields():
        if field.name not in ("id", "statut", "etat", "creation_date", "update_date", "auteur") and field.__class__.__name__ != "ManyToOneRel" and field.__class__.__name__ in ('ForeignKey', 'ManyToManyField', 'OneToOneField') and field.related_model != None and field.related_model.__name__  not in related_models:
            related_model = field.related_model.__name__
            texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\t\t\t'{0}s' : {1}.objects.all(),".format(related_model.replace("Model_", "").lower(), related_model)
            related_models.append(related_model)
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\t\t}}\n\t\ttemplate = loader.get_template('ErpProject/{1}/{0}/add.html')\n\t\treturn HttpResponse(template.render(context, request))\n\texcept Exception as e:\n\t\treturn auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)".format(nom_modele.lower(),nomModule)

    # POST CREER
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n@transaction.atomic\ndef post_creer_{0}(request):\n\tsid = transaction.savepoint()\n\ttry:".format(nom_modele.lower())
    texte_boucle = ""
    for i in range(0, len(list_champs)):
        nom_champ = ""
        type_data = ""
        default_value = dao_model()
        is_null = False
        try:
            nom_champ = list_champs[i].name.lower()
            type_data = str(list_champs[i].__class__.__name__)
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass

        # Contrôle quand on n'a pas défini une valeur par defaut et que le champ est requis
        texte_check_nullable = ""
        if inspect.isclass(default_value) == True and is_null == False and type_data != "ManyToManyField":
            if type_data in ("ForeignKey", "OneToOneField"): texte_check_nullable = "\n\t\tif {0}_id in (None, '') : return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, 'Champ obligatoire non saisi', msg = 'Le Champ \\'{1}\\' est obligatoire, Veuillez le renseigner SVP!')".format(nom_champ, list_champs[i].verbose_name)
            else : texte_check_nullable = "\n\t\tif {0} in (None, '') : return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, 'Champ obligatoire non saisi', msg = 'Le Champ \\'{1}\\' est obligatoire, Veuillez le renseigner SVP!')".format(nom_champ, list_champs[i].verbose_name)

        # Attribution des champs
        if type_data in ("ForeignKey", "OneToOneField"):
            texte_boucle = texte_boucle + "\n\n\t\t{0}_id = makeIntId(request.POST['{0}_id'])".format(nom_champ) + texte_check_nullable
        elif type_data == "ManyToManyField":
            texte_boucle = texte_boucle + "\n\n\t\t{0} = request.POST.getlist('{0}', None)".format(nom_champ)
        elif type_data == "DateTimeField":
            texte_boucle = texte_boucle + "\n\n\t\t{0} = str(request.POST['{0}']){1}\n\t\t{0} = timezone.datetime(int({0}[6:10]), int({0}[3:5]), int({0}[0:2]), int({0}[11:13]), int({0}[14:16]))".format(nom_champ, texte_check_nullable)
        elif type_data == "DateField":
            texte_boucle = texte_boucle + "\n\n\t\t{0} = str(request.POST['{0}']){1}\n\t\t{0} = date(int({0}[6:10]), int({0}[3:5]), int({0}[0:2]))".format(nom_champ, texte_check_nullable)
        elif type_data == "FloatField":
            texte_boucle = texte_boucle + "\n\n\t\t{0} = makeFloat(request.POST['{0}'])".format(nom_champ)  + texte_check_nullable
        elif type_data == "BooleanField":
            texte_boucle = texte_boucle + "\n\n\t\t{0} = True if '{0}' in request.POST else False".format(nom_champ)
        elif type_data == "EmailField":
            texte_boucle = texte_boucle + "\n\n\t\t{0} = str(request.POST['{0}'])".format(nom_champ)  + texte_check_nullable
        elif type_data == "CharField":
            texte_boucle = texte_boucle + "\n\n\t\t{0} = str(request.POST['{0}'])".format(nom_champ)  + texte_check_nullable
        elif type_data == "IntegerField":
            texte_boucle = texte_boucle + "\n\n\t\t{0} = makeInt(request.POST['{0}'])".format(nom_champ)  + texte_check_nullable
        elif type_data in ("ImageField", "FileField"):
            texte_boucle = texte_boucle + "\n\n\t\t{0} = request.FILES['{0}'] if '{0}' in request.FILES else None".format(nom_champ)
        else:
            texte_boucle = texte_boucle + "\n\n\t\t{0} = request.POST['{0}']".format(nom_champ)  + texte_check_nullable

    texte_a_ajouter_views_py = texte_a_ajouter_views_py + texte_boucle
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\tauteur = identite.utilisateur(request)"

    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\t{0} = {1}.toCreate(".format(nom_modele.lower(),nomdao,nom_modele.capitalize())
    text_parenthese = ""
    for i in range(0,len(list_champs)):
        nom_champ = ""
        type_data = ""
        default_value = ""
        is_null = True
        try:
            nom_champ = list_champs[i].name.lower()
            type_data = str(list_champs[i].__class__.__name__)
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass

        # Contrôle quand on n'a pas défini une valeur par defaut et que le champ est requis
        check_nullable = True
        if inspect.isclass(default_value) == True and is_null == False and type_data != "ManyToManyField": check_nullable = False

        if type_data in ("ForeignKey", "OneToOneField"): nom_champ = "{0}_id".format(nom_champ)
        if check_nullable: text_parenthese = text_parenthese + "{0} = {0}, ".format(nom_champ)
        else: text_parenthese = text_parenthese + "{0}, ".format(nom_champ)
    text_parenthese = text_parenthese[:len(text_parenthese)-2]
    text_parenthese = text_parenthese + ")"
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + text_parenthese
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\t\tsaved, {0}, message = {1}.toSave(auteur, {0})\n\n\t\tif saved == False: raise Exception(message)".format(nom_modele.lower(),nomdao ,nom_modele.capitalize())
    for i in range(0, len(relateds)):
        if relateds[i] != "":
            list_relateds = relateds[i].split(",")
            content_id = list_relateds[0]
            field_name = list_relateds[1]
            model_related = ContentType.objects.get(pk = content_id)
            model_class_related = model_related.model_class()
            nom_model_class_related = model_related.model_class().__name__
            nom_model_related = nom_model_class_related.replace("Model_", "").lower()
            input_name_related = "{}_{}_ids".format(nom_model_related, field_name)
            texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\t#Ajout Champ (OneToMany - Creation)\n\t\t{1} = request.POST.getlist('{1}', [])\n\t\tfor i in range(0, len({1})):\n\t\t\ttry:\n\t\t\t\tobjet = {2}.objects.get(pk = {1}[i])\n\t\t\t\tobjet.{3} = {0}\n\t\t\t\tobjet.save()\n\t\t\texcept Exception as e: pass".format(nom_modele.lower(), input_name_related, nom_model_class_related, field_name)
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\tif 'isPopup' in request.POST:\n\t\t\tpopup_response_data = json.dumps({{'value': str({0}.id),'obj': str({0})}})\n\t\t\treturn TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', {{ 'popup_response_data': popup_response_data }})\n\n\t\ttransaction.savepoint_commit(sid)\n\t\tmessages.add_message(request, messages.SUCCESS, 'L\\'enregistrement est effectué avec succès!')".format(nom_modele.lower())
    texte_a_ajouter_views_py= texte_a_ajouter_views_py + "\n\t\treturn HttpResponseRedirect(reverse('{1}_detail_{0}', args=({0}.id,)))\n\texcept Exception as e:\n\t\ttransaction.savepoint_rollback(sid)\n\t\treturn auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)".format(nom_modele.lower(), nom_pattern, nom_modele.upper())

    # GET DETAILS
    texte_a_ajouter_views_py= texte_a_ajouter_views_py + "\n\ndef get_details_{0}(request,ref):\n\ttry:\n\t\tpermission_number = 0\n\t\tmodules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)\n\t\tif response != None: return response".format(nom_modele.lower())
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\tref = int(ref)\n\t\t{0} = {1}.toGet(ref)\n\t\tcontext = {{\n\t\t\t'title' : 'Détails sur l\\'objet {7} : {{}}'.format({0}),\n\t\t\t'model' : {0},\n\t\t\t'utilisateur' : utilisateur,\n\t\t\t'modules' : modules,\n\t\t\t'sous_modules': sous_modules,\n\t\t\t'module' : vars_module,\n\t\t\t'organisation': dao_organisation.toGetMainOrganisation(),\n\t\t}}\n\t\ttemplate = loader.get_template('ErpProject/{3}/{0}/item.html')\n\t\treturn HttpResponse(template.render(context, request))\n\texcept Exception as e:\n\t\treturn auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e, reverse('{5}_list_{0}'))".format(nom_modele.lower(), nomdao, nom_modele.capitalize(), nomModule, nameModuleUp, nom_pattern, nom_modele.upper(), nom_modele_verbose)

    # GET MODIFIER
    texte_a_ajouter_views_py = texte_a_ajouter_views_py +"\n\ndef get_modifier_{0}(request,ref):\n\ttry:\n\t\tpermission_number = 0\n\t\tmodules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)\n\t\tif response != None: return response\n\n\t\tref = int(ref)\n\t\tmodel = {1}.toGet(ref)\n\t\tcontext = {{\n\t\t\t'title' : 'Modifier {2}',\n\t\t\t'model':model,\n\t\t\t'utilisateur': utilisateur,\n\t\t\t'modules' : modules,\n\t\t\t'sous_modules': sous_modules,\n\t\t\t'module' : vars_module,\n\t\t\t'organisation': dao_organisation.toGetMainOrganisation(),".format(nom_modele.lower(),nomdao,nom_modele_verbose,nameModuleUp,nomModule)
    related_models = []
    for field in model_class._meta.get_fields():
        if field.name not in ("id", "statut", "etat", "creation_date", "update_date", "auteur") and field.__class__.__name__ != "ManyToOneRel" and field.__class__.__name__ in ('ForeignKey', 'ManyToManyField', 'OneToOneField') and field.related_model != None and field.related_model.__name__  not in related_models:
            related_model = field.related_model.__name__
            texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\t\t\t'{0}s' : {1}.objects.all(),".format(related_model.replace("Model_", "").lower(), related_model)
            related_models.append(related_model)
    texte_a_ajouter_views_py = texte_a_ajouter_views_py +"\n\t\t}}\n\t\ttemplate = loader.get_template('ErpProject/{4}/{0}/update.html')\n\t\treturn HttpResponse(template.render(context, request))\n\texcept Exception as e:\n\t\treturn auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)".format(nom_modele.lower(),nomdao,nom_modele_verbose,nameModuleUp,nomModule)

    #POST MODIFIER
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n@transaction.atomic\ndef post_modifier_{0}(request):\n\tsid = transaction.savepoint()\n\tid = int(request.POST['ref'])\n\ttry:".format(nom_modele.lower())
    texte_boucle = ""
    for i in range(0, len(list_champs)):
        nom_champ = ""
        type_data = ""
        default_value = dao_model()
        is_null = False
        try:
            nom_champ = list_champs[i].name.lower()
            type_data = str(list_champs[i].__class__.__name__)
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass

        # Contrôle quand on n'a pas défini une valeur par defaut et que le champ est requis
        texte_check_nullable = ""
        if inspect.isclass(default_value) == True and is_null == False and type_data != "ManyToManyField":
            if type_data in ("ForeignKey", "OneToOneField"): texte_check_nullable = "\n\t\tif {0}_id in (None, '') : return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, 'Champ obligatoire non saisi', msg = 'Le Champ \\'{1}\\' est obligatoire, Veuillez le renseigner SVP!')".format(nom_champ, list_champs[i].verbose_name)
            else : texte_check_nullable = "\n\t\tif {0} in (None, '') : return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, 'Champ obligatoire non saisi', msg = 'Le Champ \\'{1}\\' est obligatoire, Veuillez le renseigner SVP!')".format(nom_champ, list_champs[i].verbose_name)

        # Attribution des champs
        if type_data in ("ForeignKey", "OneToOneField"):
            texte_boucle = texte_boucle + "\n\n\t\t{0}_id = makeIntId(request.POST['{0}_id'])".format(nom_champ) + texte_check_nullable
        elif type_data == "ManyToManyField":
            texte_boucle = texte_boucle + "\n\n\t\t{0} = request.POST.getlist('{0}', None)".format(nom_champ)
        elif type_data == "DateTimeField":
            texte_boucle = texte_boucle + "\n\n\t\t{0} = str(request.POST['{0}']){1}\n\t\t{0} = timezone.datetime(int({0}[6:10]), int({0}[3:5]), int({0}[0:2]), int({0}[11:13]), int({0}[14:16]))".format(nom_champ, texte_check_nullable)
        elif type_data == "DateField":
            texte_boucle = texte_boucle + "\n\n\t\t{0} = str(request.POST['{0}']){1}\n\t\t{0} = date(int({0}[6:10]), int({0}[3:5]), int({0}[0:2]))".format(nom_champ, texte_check_nullable)
        elif type_data == "FloatField":
            texte_boucle = texte_boucle + "\n\n\t\t{0} = makeFloat(request.POST['{0}'])".format(nom_champ)  + texte_check_nullable
        elif type_data == "BooleanField":
            texte_boucle = texte_boucle + "\n\n\t\t{0} = True if '{0}' in request.POST else False".format(nom_champ)
        elif type_data == "EmailField":
            texte_boucle = texte_boucle + "\n\n\t\t{0} = str(request.POST['{0}'])".format(nom_champ)  + texte_check_nullable
        elif type_data == "CharField":
            texte_boucle = texte_boucle + "\n\n\t\t{0} = str(request.POST['{0}'])".format(nom_champ)  + texte_check_nullable
        elif type_data == "IntegerField":
            texte_boucle = texte_boucle + "\n\n\t\t{0} = makeInt(request.POST['{0}'])".format(nom_champ)  + texte_check_nullable
        elif type_data in ("ImageField", "FileField"):
            texte_boucle = texte_boucle + "\n\n\t\t{0} = request.FILES['{0}'] if '{0}' in request.FILES else None".format(nom_champ)
        else:
            texte_boucle = texte_boucle + "\n\n\t\t{0} = request.POST['{0}']".format(nom_champ)  + texte_check_nullable

    texte_a_ajouter_views_py = texte_a_ajouter_views_py + texte_boucle
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\t\tauteur = identite.utilisateur(request)"
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\t{0} = {1}.toCreate(".format(nom_modele.lower(),nomdao,nom_modele.capitalize())
    text_parenthese = ""
    for i in range(0,len(list_champs)):
        nom_champ = ""
        type_data = ""
        default_value = ""
        is_null = True
        try:
            nom_champ = list_champs[i].name.lower()
            type_data = str(list_champs[i].__class__.__name__)
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass

        # Contrôle quand on n'a pas défini une valeur par defaut et que le champ est requis
        check_nullable = True
        if inspect.isclass(default_value) == True and is_null == False and type_data != "ManyToManyField": check_nullable = False

        if type_data in ("ForeignKey", "OneToOneField"): nom_champ = "{0}_id".format(nom_champ)
        if check_nullable: text_parenthese = text_parenthese + "{0} = {0}, ".format(nom_champ)
        else: text_parenthese = text_parenthese + "{0}, ".format(nom_champ)
    text_parenthese = text_parenthese[:len(text_parenthese)-2]
    text_parenthese = text_parenthese + ")"
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + text_parenthese
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\t\tsaved, {0}, message = {1}.toUpdate(id, {0})\n\n\t\tif saved == False: raise Exception(message)".format(nom_modele.lower(), nomdao, nom_modele.capitalize())
    for i in range(0, len(relateds)):
        if relateds[i] != "":
            list_relateds = relateds[i].split(",")
            content_id = list_relateds[0]
            field_name = list_relateds[1]
            model_related = ContentType.objects.get(pk = content_id)
            model_class_related = model_related.model_class()
            nom_model_class_related = model_related.model_class().__name__
            nom_model_related = nom_model_class_related.replace("Model_", "").lower()
            input_name_related = "{}_{}_ids".format(nom_model_related, field_name)
            related_query_name = model_class_related._meta.get_field(field_name).related_query_name()
            if related_query_name.startswith("model_") : related_query_name = "{}_set".format(related_query_name)
            texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\t#MAJ Champ (OneToMany - Modification)\n\t\t{1} = request.POST.getlist('{1}', [])\n\t\t{0}.{4}.all().update({3} = None)\n\t\tfor i in range(0, len({1})):\n\t\t\ttry:\n\t\t\t\tobjet = {2}.objects.get(pk = {1}[i])\n\t\t\t\tobjet.{3} = {0}\n\t\t\t\tobjet.save()\n\t\t\texcept Exception as e: pass".format(nom_modele.lower(), input_name_related, nom_model_class_related, field_name, related_query_name)
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\ttransaction.savepoint_commit(sid)\n\t\tmessages.add_message(request, messages.SUCCESS, 'La modification est effectuée avec succès!')"
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\t\treturn HttpResponseRedirect(reverse('{1}_detail_{0}', args=({0}.id,)))\n\texcept Exception as e:\n\t\ttransaction.savepoint_rollback(sid)\n\t\treturn auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)".format(nom_modele.lower(), nom_pattern, nom_modele.upper())

    # GET UPLOAD
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\ndef get_upload_{0}(request):\n\ttry:\n\t\tpermission_number = 0\n\t\tmodules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)\n\t\tif response != None: return response\n\n\t\tcontext = {{\n\t\t\t'title' : 'Import de la liste des {1}',\n\t\t\t'utilisateur' : utilisateur,\n\t\t\t'isPopup': True if 'isPopup' in request.GET else False,\n\t\t\t'modules' : modules,\n\t\t\t'sous_modules': sous_modules,\n\t\t\t'module' : vars_module,\n\t\t\t'organisation' : dao_organisation.toGetMainOrganisation(),".format(nom_modele.lower() ,nom_modele_verbose_plural.lower(), nom_modele_class)
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\t\t}}\n\t\ttemplate = loader.get_template('ErpProject/{1}/{0}/upload.html')\n\t\treturn HttpResponse(template.render(context, request))\n\texcept Exception as e:\n\t\treturn auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)".format(nom_modele.lower(),nomModule)

    # POST UPLOAD
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n@transaction.atomic\ndef post_upload_{0}(request):\n\tsid = transaction.savepoint()\n\ttry:\n\t\tmedia_dir = settings.MEDIA_ROOT\n\t\tfile_name = ''\n\t\trandomId = randint(111, 999)\n\t\tif 'file_upload' in request.FILES:\n\t\t\tfile = request.FILES['file_upload']\n\t\t\taccount_file_dir = 'excel/'\n\t\t\tmedia_dir = media_dir + '/' + account_file_dir\n\t\t\tsave_path = os.path.join(media_dir, str(randomId) + '.xlsx')\n\t\t\tif default_storage.exists(save_path):\n\t\t\t\tdefault_storage.delete(save_path)\n\t\t\tfile_name = default_storage.save(save_path, file)\n\t\telse: file_name = ''\n\t\tsheet = str(request.POST['sheet'])\n\n\t\tdf = pd.read_excel(io=file_name, sheet_name=sheet)\n\t\tdf = df.fillna('') #Replace all nan value\n\n\t\tauteur = identite.utilisateur(request)\n\n\t\tfor i in df.index:".format(nom_modele.lower())
    texte_boucle = ""
    for i in range(0, len(list_champs)):
        nom_champ = ""
        type_data = ""
        default_value = dao_model()
        is_null = False
        try:
            nom_champ = list_champs[i].name.lower()
            type_data = str(list_champs[i].__class__.__name__)
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass

        # Contrôle quand on n'a pas défini une valeur par defaut et que le champ est requis
        texte_check_nullable = ""
        if inspect.isclass(default_value) == True and is_null == False and type_data != "ManyToManyField":
            if type_data in ("ForeignKey", "OneToOneField"): texte_check_nullable = "\n\t\tif {0}_id in (None, '') : return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, 'Champ obligatoire non saisi', msg = 'Le Champ \\'{1}\\' est obligatoire, Veuillez le renseigner SVP!')".format(nom_champ, list_champs[i].verbose_name)
            else : texte_check_nullable = "\n\t\t\tif {0} in (None, '') : return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, 'Champ obligatoire non saisi', msg = 'Le Champ \\'{1}\\' est obligatoire, Veuillez le renseigner SVP!')".format(nom_champ, list_champs[i].verbose_name)

        # Attribution des champs
        if type_data not in ("ImageField", "FileField", "ManyToManyField"):
            if type_data in ("ForeignKey", "OneToOneField"):
                texte_boucle = texte_boucle + "\n\t\t\t{0}_id = makeIntId(str(df['{0}_id'][i]))".format(nom_champ) + texte_check_nullable
            elif type_data == "DateTimeField":
                texte_boucle = texte_boucle + "\n\t\t\t{0} = str(df['{0}'][i]){1}\n\t\t\t{0} = timezone.datetime(int({0}[6:10]), int({0}[3:5]), int({0}[0:2]), int({0}[11:13]), int({0}[14:16]))".format(nom_champ, texte_check_nullable)
            elif type_data == "DateField":
                texte_boucle = texte_boucle + "\n\t\t\t{0} = str(df['{0}'][i]){1}\n\t\t\t{0} = date(int({0}[6:10]), int({0}[3:5]), int({0}[0:2]))".format(nom_champ, texte_check_nullable)
            elif type_data == "FloatField":
                texte_boucle = texte_boucle + "\n\t\t\t{0} = makeStringFromFloatExcel(df['{0}'][i])".format(nom_champ)  + texte_check_nullable
            elif type_data == "BooleanField":
                texte_boucle = texte_boucle + "\n\t\t\t{0} = True if str(df['{0}'][i]) == 'True' else False".format(nom_champ)
            elif type_data == "EmailField":
                texte_boucle = texte_boucle + "\n\t\t\t{0} = str(df['{0}'][i])".format(nom_champ)  + texte_check_nullable
            elif type_data == "CharField":
                texte_boucle = texte_boucle + "\n\t\t\t{0} = str(df['{0}'][i])".format(nom_champ)  + texte_check_nullable
            elif type_data == "IntegerField":
                texte_boucle = texte_boucle + "\n\t\t\t{0} = makeInt(df['{0}'][i])".format(nom_champ)  + texte_check_nullable
            else:
                texte_boucle = texte_boucle + "\n\t\t\t{0} = str(df['{0}'][i])".format(nom_champ)  + texte_check_nullable

    texte_a_ajouter_views_py = texte_a_ajouter_views_py + texte_boucle

    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\t\t{0} = {1}.toCreate(".format(nom_modele.lower(),nomdao,nom_modele.capitalize())
    text_parenthese = ""
    for i in range(0,len(list_champs)):
        nom_champ = ""
        type_data = ""
        default_value = ""
        is_null = True
        try:
            nom_champ = list_champs[i].name.lower()
            type_data = str(list_champs[i].__class__.__name__)
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass

        # Contrôle quand on n'a pas défini une valeur par defaut et que le champ est requis
        check_nullable = True
        if inspect.isclass(default_value) == True and is_null == False and type_data != "ManyToManyField": check_nullable = False

        if type_data in ("ForeignKey", "OneToOneField"): nom_champ = "{0}_id".format(nom_champ)
        if type_data not in ("ImageField", "FileField", "ManyToManyField"):
            if check_nullable: text_parenthese = text_parenthese + "{0} = {0}, ".format(nom_champ)
            else: text_parenthese = text_parenthese + "{0}, ".format(nom_champ)
    text_parenthese = text_parenthese[:len(text_parenthese)-2]
    text_parenthese = text_parenthese + ")"
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + text_parenthese
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\t\t\tsaved, {0}, message = {1}.toSave(auteur, {0})\n\n\t\t\tif saved == False: raise Exception(message)\n\n\t\ttransaction.savepoint_commit(sid)\n\t\tmessages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')".format(nom_modele.lower(),nomdao,nom_modele.capitalize())
    texte_a_ajouter_views_py= texte_a_ajouter_views_py + "\n\t\treturn HttpResponseRedirect(reverse('{1}_list_{0}'))\n\texcept Exception as e:\n\t\ttransaction.savepoint_rollback(sid)\n\t\treturn auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)".format(nom_modele.lower(),nom_pattern,nom_modele.upper())

    fichier.write(texte_a_ajouter_views_py)
    fichier.close()

    # CREATION DES TEMPLATES CRUD ET UPLOAD DU MODELE

    # TEMPLATE LIST
    path = os.path.abspath(os.path.curdir)
    path = path + "\\templates\\ErpProject\\{0}\\{1}".format(nomModule,nom_modele.lower())
    try:
        os.mkdir(path)
    except Exception as e:
        pass
    path = path + "\\list.html"
    fichier = codecs.open(path,"w", encoding='utf-8')

    texteTemplate = '''
{{% extends "ErpProject/{0}/shared/layout.html" %}}
{{% block page %}} {{% load humanize %}} {{%load static %}} {{% load account_filters %}}
<div class="row">
    <ul class="breadcrumb">
        <li><a href="{{% url 'backoffice_index' %}}"><span class="mif-home"></span></a></li>
        <li><a class="leaf chargement-au-click" href="{{% url 'module_{1}_index' %}}">Module {4}</a></li>
        <li>{{{{ title }}}}</li>
    </ul>
</div>

<div class="row"  style="padding-top: 30px;">
    <div class="col-lg-12">
        <h2>{{{{ title }}}}</h2>
        <strong style="float: right;color: grey;opacity: 0.4;margin-top: -30px;">{{% now "jS F Y H:i" %}}</strong>
        <div class="separ" style="background-color: grey;opacity: 0.2"></div>
        <div class="panel panel-default" style="border: none;">
            <div class="panel panel-body" style="background-color:#f5f5f5;border: none;border-radius: none;">
                <div class="row">
                    <div class="col-md-3">
                        <button style="width: 100%;" onclick="javascript:window.location.assign('{{% url '{2}_add_{3}' %}}')" class="theme-btn theme-btn-sm rounded primary_color_{{{{module.name|lower}}}}" style="width: 100%;">
                            Créer
                        </button>
                    </div>
                    <div class="col-md-3">
                        <div id="btn-view" data-role="group" data-group-type="one-state">
                            <button id="btn-tree" onclick="javascript:window.location.assign('{{% url '{2}_list_{3}' %}}?view=list')" class="button btn-typeview btn-secondary {{% if view == "list" %}}{{{{ "active" }}}}{{% endif %}}"><span class="mif-list"></span></button>
                            <button id="btn-kanban" onclick="javascript:window.location.assign('{{% url '{2}_list_{3}' %}}?view=kanban')" class="button btn-typeview btn-secondary {{% if view == "kanban" %}}{{{{ "active" }}}}{{% endif %}}"><span class="mif-apps"></span></button>
                        </div>
                    </div>
                </div><br>

                <hr class="hr-ligne">
                <!-- Appel de la fonction message -->
                {{% include 'ErpProject/ErpBackOffice/widget/message.html' with messages=messages only %}}<br>

                {{% if view == "list" %}}
                <div id="list-view" class="row" style="margin-top: 10px;">
                    <table id="data_table" class="display nowrap border bordered striped" cellspacing="0" style="overflow: auto; position: relative; display: inline-block; width:100%">
                        <thead>
                            <tr>
                                <th style="width: 20px; background-color:#2e416a; white"></th>'''.format(nomModule, unidecode.unidecode(module.nom_module.lower()), nom_pattern, nom_modele.lower(), module.nom_module.capitalize())
    textebcl=""
    for i in range(0,len(list_champs)):
        nom_champ = ""
        nom_champ_verbose = ""
        type_data = ""
        try:
            nom_champ = list_champs[i].name.lower()
            nom_champ_verbose = list_champs[i].verbose_name
            type_data = str(list_champs[i].__class__.__name__)
        except Exception as e:
            pass
        if type_data not in  ("ManyToManyField", "ImageField", "FileField"):
            textebcl = textebcl + '''
                                <th>{0}</th>'''.format(nom_champ_verbose)
    textebcl = textebcl + '''
                                <th>Date de création</th>
                                <th>Créé par</th>'''
    texteTemplate = texteTemplate + textebcl

    texteTemplate= texteTemplate + '''
                            </tr>
                        </thead>
                        <tbody>
                            {{% for item in model %}}
                            <tr>
                                <td>
                                    <label class="small-check">
                                        <input type="checkbox"><span class="check"></span>
                                    </label>
                                </td>
                                <td>
                                    <a class="lien chargement-au-click" href="{{% url '{0}_detail_{1}' item.id %}}">{{{{ item.{2} }}}}</a>
                                </td>'''.format(nom_pattern, nom_modele.lower(), list_champs[0].name)

    textebcl = ""
    for i in range(1,len(list_champs)):
        nom_champ = ""
        nom_champ_verbose = ""
        type_data = ""
        try:
            nom_champ = list_champs[i].name.lower()
            nom_champ_verbose = list_champs[i].verbose_name
            type_data = str(list_champs[i].__class__.__name__)
        except Exception as e:
            pass
        if type_data not in  ("ManyToManyField", "ImageField", "FileField"):
            if type_data == "FloatField" and len(list_champs[i].choices) == 0:
                textebcl = textebcl + '''
                                <td>{{{{item.{0}|monetary}}}}</td>'''.format(nom_champ)
            elif type_data == "CharField" and len(list_champs[i].choices) == 0:
                textebcl = textebcl + '''
                                <td>{{{{item.{0}|truncatechars:22}}}}</td>'''.format(nom_champ)
            elif type_data == "BooleanField":
                textebcl = textebcl + '''
                                <td>{{{{item.{0}|boolean}}}}</td>'''.format(nom_champ)
            elif type_data == "DateTimeField":
                textebcl = textebcl + '''
                                <td>{{{{item.{0}|date:"d/m/Y H:i"}}}}</td>'''.format(nom_champ)
            elif type_data == "DateField":
                textebcl = textebcl + '''
                                <td>{{{{item.{0}|date:"d/m/Y"}}}}</td>'''.format(nom_champ)
            elif type_data in ("CharField", "IntegerField", "FloatField") and len(list_champs[i].choices) > 0:
                textebcl = textebcl + '''
                                <td>{{{{ item.value_{0} }}}}</td>'''.format(nom_champ)
            else :
                textebcl = textebcl + '''
                                <td>{{{{item.{0}}}}}</td>'''.format(nom_champ)

    texteTemplate = texteTemplate + textebcl

    texteTemplate = texteTemplate + '''
                                <td>{{{{item.creation_date|date:'d/m/Y'}}}}</td>
                                <td>{{{{item.auteur.nom_complet}}}}</td>
                            </tr>
                            {{% endfor %}}
                        </tbody>
                    </table>
                </div>
                {{% elif view == "kanban" %}}

                <!-- Vue de type card -->
                <div id="kanban-view" class="row" style="margin-top: 10px">
                    {{% for item in model %}}
                    <div class="col-md-4">
                        <div class="card-item" style="margin-top: 10px; margin-bottom: 15px">
                            <div class="card-item-content">
                                <div class="thumb">
                                </div>
                                <div class="texts">
                                    <a class="link chargement-au-click" href="{{% url '{0}_detail_{1}' item.id %}}">{{{{ item.{2} }}}}</a><br>
                                    <div class="mt-2"></div>
                                    <span class="inner-text">Créé par : {{{{ item.auteur.nom_complet }}}}</span><br>
                                    <span class="inner-text">Créé le : {{{{ item.creation_date|date:'d/m/Y' }}}}</span><br>
                                    <a href="{{% url '{0}_detail_{1}' item.id %}}" class="mt-3 btn btn-block btn-wide rounded chargement-au-click">voir detail</a>
                                </div>
                            </div>
                        </div>
                    </div>
                    {{% endfor %}}
                </div>
                {{% endif %}}
            </div>
        </div>
    </div>
    <!-- /.col-lg-12 -->
</div>
{{% include 'ErpProject/ErpBackOffice/widget/datatable.html' with type_view=view %}}
{{% endblock %}}
'''.format(nom_pattern, nom_modele.lower(), list_champs[0].name)
    fichier.write(texteTemplate)
    fichier.close()

    # TEMPLATE ADD
    path = os.path.abspath(os.path.curdir)
    path = path + "\\templates\\ErpProject\\{0}\\{1}".format(nomModule, nom_modele.lower())
    path = path + "\\add.html"
    fichier = codecs.open(path,"w", encoding='utf-8')
    texteTemplateLayout = '''
{{% extends "ErpProject/{0}/shared/layout.html" %}}
{{% block page %}} {{% load humanize %}} {{%load static %}} {{% load account_filters %}}
<div class="row">
    <ul class="breadcrumb">
        <li><a href="{{% url 'backoffice_index' %}}"><span class="mif-home"></span></a></li>
        <li><a class="chargement-au-click" href="{{% url 'module_{1}_index' %}}">Module {4}</a></li>
        <li><a class="chargement-au-click" href="{{% url '{2}_list_{3}' %}}">Liste des {5}</a></li>
        <li>{{{{ title }}}}</li>
    </ul>
</div>

<div class="row">
    <div class="col-lg-12">
        <h2>{{{{ title }}}}</h2>

        <strong style="float: right;color: grey;opacity: 0.4;margin-top: -30px;">{{% now "jS F Y H:i" %}}</strong>
        <div class="separ" style="background-color: grey;opacity: 0.2"></div>

        <div class="panel panel-default" style="border: none; margin-top: 1rem;">
            <div class="panel panel-body" style="background-color:#f5f5f5;border: none;border-radius: none;">
                <div class="row">
                    <button onclick="javascript:document.getElementById('submit').click()" class="theme-btn theme-btn-sm rounded primary_color_{{{{module.name|lower}}}}">Valider</button>
                    {{% if not isPopup %}}<button onclick="javascript:window.location.assign('{{% url '{2}_get_upload_{3}' %}}')" class="theme-btn theme-btn-sm rounded chargement-au-click">Importer les données à partir excel</button>{{% endif %}}
                    <button onclick="javascript:window.location.assign('{{% url '{2}_list_{3}' %}}')" class="theme-btn theme-btn-sm rounded" style="width: 20%;margin-left: 5px">Annuler</button>
                </div>

                <hr class="hr-ligne">
                <!-- Appel de la fonction message -->
                {{% include 'ErpProject/ErpBackOffice/widget/message.html' with messages=messages only %}}<br>

                <form id="form" method="POST" action="{{% url '{2}_post_add_{3}' %}}"  enctype="multipart/form-data" data-role="validator" data-show-required-state="false" data-hint-mode="line" data-hint-background="bg-red" data-hint-color="fg-white" data-hide-error="5000"
                    novalidate="novalidate" data-on-error-input="notifyOnErrorInput" data-show-error-hint="false">
                    {{% csrf_token %}}
                    <input id="submit" type="submit" style="display: none">
                    {{% if isPopup %}}<input id="isPopup" name="isPopup" value="1" type="text" style="display: none">{{% endif %}}
                    <div class="row">'''.format(nomModule, unidecode.unidecode(module.nom_module.lower()), nom_pattern, nom_modele.lower(), module.nom_module.capitalize(), nom_modele_verbose_plural)

    textebcl = ""
    for i in range(0,len(list_champs)):
        nom_champ = ""
        nom_champ_verbose = ""
        type_data = ""
        try:
            nom_champ = list_champs[i].name.lower()
            nom_champ_verbose = list_champs[i].verbose_name
            type_data = str(list_champs[i].__class__.__name__)
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass

        # Contrôle quand on n'a pas défini une valeur par defaut et que le champ est requis
        is_required = False
        if inspect.isclass(default_value) == True and is_null == False and type_data != "ManyToManyField": is_required = True

        if type_data == "FloatField" and len(list_champs[i].choices) == 0:
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True :
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control number full-size" data-role="input">
                                <input name="{0}" id="{0}" type="number" step="0.01" '''.format(nom_champ)
            if is_required == True :
                textebcl = textebcl + 'data-validate-func="required, number" data-validate-hint="Saisissez un nombre valide sur le champ {} SVP !">'.format(nom_champ_verbose)
            else : textebcl = textebcl + 'data-validate-func="number" data-validate-hint="Saisissez un nombre valide sur le champ {} SVP !">'.format(nom_champ_verbose)
            textebcl = textebcl + '''
                            </div>
                        </div>'''
        elif type_data == "CharField" and len(list_champs[i].choices) == 0:
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True :
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"

            if list_champs[i].max_length != None and list_champs[i].max_length > 500:
                textebcl = textebcl + '''
                            <div class="input-control text full-size">
                                <textarea name="{0}" id="{0}" '''.format(nom_champ)
                if is_required == True :
                    textebcl = textebcl + 'data-validate-func="required" data-validate-hint="Saisissez le champ {} SVP !">'.format(nom_champ_verbose)
                else : textebcl = textebcl + "></textarea>"
            else:
                textebcl = textebcl + '''
                            <div class="input-control text full-size" data-role="input">
                                <input name="{0}" id="{0}" type="text" '''.format(nom_champ)
                if is_required == True :
                    textebcl = textebcl + 'data-validate-func="required" data-validate-hint="Saisissez le champ {} SVP !">'.format(nom_champ_verbose)
                else : textebcl = textebcl + ">"
            textebcl = textebcl + '''
                            </div>
                        </div>'''
        elif type_data == "EmailField":
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True :
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control email full-size" data-role="input">
                                <input name="{0}" id="{0}" type="email" '''.format(nom_champ)
            if is_required == True :
                textebcl = textebcl + 'data-validate-func="required, email" data-validate-hint="Saisissez une adresse email valide sur le champ {} SVP !">'.format(nom_champ_verbose)
            else : textebcl = textebcl + ">"
            textebcl = textebcl + '''
                            </div>
                        </div>'''
        elif type_data == "IntegerField" and len(list_champs[i].choices) == 0:
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True :
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control number full-size" data-role="input">
                                <input name="{0}" id="{0}" type="number" '''.format(nom_champ)
            if is_required == True :
                textebcl = textebcl + 'data-validate-func="required, number" data-validate-hint="Saisissez un nombre valide sur le champ {} SVP !">'.format(nom_champ_verbose)
            else : textebcl = textebcl + 'data-validate-func="number" data-validate-hint="Saisissez un nombre valide sur le champ {} SVP !">'.format(nom_champ_verbose)
            textebcl = textebcl + '''
                            </div>
                        </div>'''
        elif type_data == "ImageField":
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{0}</label>
                            <div class="tile-container">
                                <input class="image_upload" name="{1}" id="{1}" type="file" accept="image/*" style="display:none;">
                                <a id="trigger-input-file" href="#" class="trigger-input-file tile-wide fg-white shadow" style="height: 100px!important; width: 100px!important;" data-role="tile">
                                    <div class="tile-content slide-up">
                                        <div class="slide">
                                            <img class="image_preview" src="{{% static 'ErpProject/image/upload/articles/default.png' %}}" style="height: 100px; width: 100px;">
                                        </div>
                                        <div class="slide-over op-dark padding10" style="text-align: center!important; opacity: 60%!important;">
                                            <span class="icon mif-pencil" style="text-align: center!important; font-size: 40px!important;"></span>
                                        </div>
                                    </div>
                                </a>
                            </div>
                        </div>'''.format(nom_champ_verbose, nom_champ)
        elif type_data == "FileField":
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{0}</label>
                            <div class="input-control file full-size" data-role="input">
                                <input name="{1}" id="{1}" type="file"><button class="button"><span class="mif-folder"></span></button>
                            </div>
                        </div>'''.format(nom_champ_verbose, nom_champ)
        elif type_data == "ForeignKey":
            related_model = list_champs[i].related_model.__name__
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True :
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size">
                                <select name="{0}_id" id="{0}_id" class="selectpicker form-control" data-live-search="true" title="Sélectionner une option">
                                    <option value="">Sélectionnez une option</option>
                                    <option class="create_option" value='-100' data-url="/{1}/{2}/add?isPopup=1">Créer nouveau...</option>
                                    {{% for item in {2}s %}}<option value="{{{{ item.id }}}}">{{{{ item }}}}</option>{{% endfor %}}
                                </select>
                            </div>
                        </div>'''.format(nom_champ, module.url_vers.replace("/", ""), related_model.replace("Model_", "").lower())
        elif type_data == "OneToOneField":
            related_model = list_champs[i].related_model.__name__
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True :
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size">
                                <select name="{0}_id" id="{0}_id">
                                    <option value="">Sélectionnez une option</option>
                                    <option class="create_option" value='-100' data-url="/{1}/{2}/add?isPopup=1">Créer nouveau...</option>
                                    {{% for item in {2}s %}}<option value="{{{{ item.id }}}}">{{{{ item }}}}</option>{{% endfor %}}
                                </select>
                            </div>
                        </div>'''.format(nom_champ, module.url_vers.replace("/", ""), related_model.replace("Model_", "").lower())
        elif type_data == "ManyToManyField":
            related_model = list_champs[i].related_model.__name__
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True :
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="text full-size">
                                <select multiple="multiple" class="multi-select multi_select2" name="{0}" id="{0}">
                                    {{% for item in {1}s %}}<option value="{{{{ item.id }}}}">{{{{item}}}}</option>{{% endfor %}}
                                </select>
                            </div>
                        </div>'''.format(nom_champ, related_model.replace("Model_", "").lower())
        elif type_data == "BooleanField":
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label class="input-control checkbox small-check full-size">
                                <input name="{1}" id="{1}" type="checkbox">
                                <span class="check"></span><span class="caption">{0}</span>'''.format(nom_champ_verbose, nom_champ)
            if is_required == True :
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            </label>
                        </div>'''
        elif type_data == "DateTimeField":
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True :
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size datetimepicker">
                                <input type="text" name="{1}" id="{1}" value="{{% now "d/m/Y H:i" %}}">
                                <div class="button"><span class="glyphicon glyphicon-screenshot far fa-calendar" style="margin-right:3px;"></span><span class="glyphicon glyphicon-screenshot far fa-clock"></span></div>
                            </div>
                        </div>'''.format(nom_champ_verbose, nom_champ)
        elif type_data == "DateField":
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True :
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size"  data-format="dd/mm/yyyy" data-role="datepicker" data-locale="fr">
                                <input type="text" name="{1}" id="{1}" value="{{% now "d/m/Y" %}}">
                                <div class="button"><span class="mif-calendar"></span></div>
                            </div>
                        </div>'''.format(nom_champ_verbose, nom_champ)
        elif type_data in ("CharField", "IntegerField", "FloatField") and len(list_champs[i].choices) > 0:
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True :
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size">
                                <select name="{0}" id="{0}">
                                    <option value="">Sélectionnez une option</option>
                                    {{% for item in model.list_{0} %}}<option value="{{{{ item.id }}}}">{{{{ item.designation }}}}</option>{{% endfor %}}
                                </select>
                            </div>
                        </div>'''.format(nom_champ)
        else :
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True :
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size" data-role="input">
                                <input name="{0}" id="{0}" type="text" '''.format(nom_champ)
            if is_required == True :
                textebcl = textebcl + 'data-validate-func="required" data-validate-hint="Saisissez le champ {} SVP !">'.format(nom_champ_verbose)
            else : textebcl = textebcl + ">"
            textebcl = textebcl + '''
                            </div>
                        </div>'''

    texteTemplateLayout = texteTemplateLayout + textebcl
    texteTemplateLayout = texteTemplateLayout + '''
                    </div>'''

    if len(relateds) > 0:
        texteTemplateLayout = texteTemplateLayout + '''
                    <br><br>
                    <div class="row">
                        <ul class="nav nav-tabs navtab-bg">
                            <li class="active"><a href="#frame_autres" data-toggle="tab" aria-expanded="false"><span>Autres informations</span></a></li>
                        </ul>
                        <div class="tab-content">
                            <div class="tab-pane active" id="frame_autres">
                                <div class="row margin20 no-margin-left no-margin-right">'''
        for i in range(0, len(relateds)):
            if relateds[i] != "":
                list_relateds = relateds[i].split(",")
                content_id = list_relateds[0]
                field_name = list_relateds[1]
                model_related = ContentType.objects.get(pk = content_id)
                model_class_related = model_related.model_class()
                nom_model_class_related = model_related.model_class().__name__
                nom_model_related = nom_model_class_related.replace("Model_", "").lower()
                input_name_related = "{}_{}_ids".format(nom_model_related, field_name)
                related_query_name = model_class_related._meta.get_field(field_name).related_query_name()
                if related_query_name.startswith("model_") : related_query_name = "{}_set".format(related_query_name)

                texteTemplateLayout = texteTemplateLayout + '''
                                <div class="col-md-6">
                                    <div class="section-otm" data-compteur="1">
                                        <table class="table bordered no-margin" style="width:100%;">
                                            <thead>
                                                <tr>
                                                    <th width="90%">{0}</th>
                                                    <th width="10%"></th>
                                                </tr>
                                            </thead>
                                            <tbody class="tbl_posts_body">
                                                <tr>
                                                    <td>
                                                        <div class="input-control text full-size">
                                                            <select class="selectpicker form-control" data-live-search="true" title="sélectionner une option" name="{3}" id="{3}-1">
                                                                <option value="">Sélectionnez une nouvelle option {0}</option>
                                                                <option class="create_option" value='-100' data-url="/{1}/{2}/add?isPopup=1">Créer nouveau...</option>
                                                            </select>
                                                        </div>
                                                    </td>
                                                    <td>
                                                        <div class="pagination no-border">
                                                            <span class="item delete-record" title="Supprimer la ligne"><span class="mif-cross fg-red"></span></span>
                                                        </div>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        <br><button type="button" class="button rounded add-record">Ajouter</button>
                                        <table class="sample_table" style="display:none;">
                                            <tr>
                                                <td>
                                                    <div class="input-control text full-size">
                                                        <select class="form-control" data-live-search="true" title="Sélectionner une option" name="{3}" id="">
                                                            <option value="">Sélectionnez une nouvelle option {0}</option>
                                                            <option class="create_option" value='-100' data-url="/{1}/{2}/add?isPopup=1">Créer nouveau...</option>
                                                        </select>
                                                    </div>
                                                </td>
                                                <td>
                                                    <div class="pagination no-border">
                                                        <span class="item delete-record" title="Supprimer la ligne"><span class="mif-cross fg-red"></span></span>
                                                    </div>
                                                </td>
                                            </tr>
                                        </table>
                                    </div>'''.format(model_class_related._meta.verbose_name, module.url_vers.replace("/", ""), nom_model_related, input_name_related)
        texteTemplateLayout = texteTemplateLayout + '''
                                </div>
                            </div>
                        </div>
                    </div>'''

    texteTemplateLayout = texteTemplateLayout + '''
                </form>
            </div>
        </div>
    </div>
    <!-- /.col-lg-12 -->
</div>
{% endblock %}'''
    fichier.write(texteTemplateLayout)
    fichier.close()


    # TEMPLATE ITEM
    path = os.path.abspath(os.path.curdir)
    path = path + "\\templates\\ErpProject\\{0}\\{1}".format(nomModule,nom_modele.lower())
    path = path + "\\item.html"
    fichier = codecs.open(path,"w", encoding='utf-8')

    texteTemplateLayout = '''
{{% extends "ErpProject/{0}/shared/layout.html" %}}
{{% block page %}} {{% load humanize %}} {{%load static %}} {{% load account_filters %}}
<div class="row">
    <ul class="breadcrumb">
        <li><a href="{{% url 'backoffice_index' %}}"><span class="mif-home"></span></a></li>
        <li><a class="chargement-au-click" href="{{% url 'module_{1}_index' %}}">Module {4}</a></li>
        <li><a class="chargement-au-click" href="{{% url '{2}_list_{3}' %}}">Liste des {5}</a></li>
        <li>{{{{ title }}}}</li>
    </ul>
</div>

<div class="row">
    <div class="col-lg-12">
        <h2>{{{{ title }}}}</h2>

        <strong style="float: right;color: grey;opacity: 0.4;margin-top: -30px;">{{% now "jS F Y H:i" %}}</strong>
        <div class="separ" style="background-color: grey;opacity: 0.2"></div>

        <!-- GESTION DU WORKFLOW -->
        {{% include 'ErpProject/ErpBackOffice/widget/workflow.html' with utilisateur=utilisateur model=model content_type_id=content_type_id historique=historique roles=roles etapes_suivantes=etapes_suivantes url_add="{2}_add_{3}" url_detail="{2}_detail_{3}" csrf_token=csrf_token module=module type_doc="{6}" only %}}
        <!--FIN GESTION DU WORKFLOW-->

        <div class="panel panel-default" style="border: none; margin-top: 1rem;">
            <div class="panel panel-body" style="background-color:#f5f5f5;border: none;border-radius: none;">
                <div class="row">
                    <button onclick="javascript:window.location.assign('{{% url '{2}_update_{3}' model.id %}}')" class="theme-btn theme-btn-sm rounded primary_color_{{{{module.name|lower}}}}">Modifier</button>
                    <button onclick="javascript:window.location.assign('{{% url '{2}_list_{3}' %}}')" class="theme-btn theme-btn-sm rounded" style="width: 20%;margin-left: 5px">Annuler</button>
                </div>

                <hr class="hr-ligne">
                <!-- Appel de la fonction message -->
                {{% include 'ErpProject/ErpBackOffice/widget/message.html' with messages=messages only %}}<br>

                <div class="row">'''.format(nomModule, unidecode.unidecode(module.nom_module.lower()), nom_pattern, nom_modele.lower(), module.nom_module.capitalize(), nom_modele_verbose_plural, nom_champ_verbose)

    textebcl = ""
    for i in range(0,len(list_champs)):
        nom_champ = ""
        nom_champ_verbose = ""
        type_data = ""
        try:
            nom_champ = list_champs[i].name.lower()
            nom_champ_verbose = list_champs[i].verbose_name
            type_data = str(list_champs[i].__class__.__name__)
        except Exception as e:
            pass

        if type_data == "FloatField" and len(list_champs[i].choices) == 0:
            textebcl = textebcl + '''
                    <div class="col-md-6">
                        <p>{1} :<br>
                            <span class="sub-alt-header">{{{{model.{0}|monetary}}}}</span>
                        </p>
                    </div>'''.format(nom_champ, nom_champ_verbose)
        elif type_data == "BooleanField":
            textebcl = textebcl + '''
                    <div class="col-md-6">
                        <label class="input-control checkbox small-check full-size">
                            <input name="{0}" id="{0}"  {{% if model.{0} is True %}}{{{{ "checked" }}}}{{% endif %}} type="checkbox" disabled="disabled">
                            <span class="check"></span>
                            <span class="caption">{1}</span>
                        </label>
                    </div>'''.format(nom_champ, nom_champ_verbose)
        elif type_data in ("ForeignKey", "OneToOneField"):
            related_model = list_champs[i].related_model.__name__
            textebcl = textebcl + '''
                    <div class="col-md-6">
                        <p>{1} :<br>
                            {{% if model.{0} is None %}}
                            <span class="sub-alt-header"> - </span>
                            {{% else %}}
                            <span class="sub-alt-header"><a class="link chargement-au-click" href="{{% url '{2}_detail_{3}' model.{0}_id %}}">{{{{ model.{0} }}}}</a></span>
                            {{% endif %}}
                        </p>
                    </div>'''.format(nom_champ, nom_champ_verbose, nom_pattern, related_model.replace("Model_", "").lower())
        elif type_data == "ImageField":
            textebcl = textebcl + '''
                    <div class="col-md-6">
                        <p>{1} :<br>
                            {{% if model.{0} %}}
                            <img class="" src="{{% static model.{0}.url %}}" style="height: 100px; width: 100px;">
                            {{% else %}}
                            <img src="{{% static 'ErpProject/image/upload/articles/default.png' %}}" style="height: 100px; width: 100px;">
                            {{% endif %}}
                        </p>
                    </div>'''.format(nom_champ, nom_champ_verbose)
        elif type_data == "FileField":
            textebcl = textebcl + '''
                    <div class="col-md-6">
                        <p>{1} :<br>
                            {{% if model.{0} %}}
                            <a href="{{% static model.{0}.url %}}"><img src="{{% static 'ErpProject/image/document.png' %}}" style="height: 70px; width: 70px;"></a>
                            <br><span style=" color: #000; font-size: 9px;">{{{{model.{0}.name|truncatechars:25}}}}</span>
                            {{% else %}}<span class="sub-alt-header">Aucun document attaché</span>{{% endif %}}
                        </p>
                    </div>'''.format(nom_champ, nom_champ_verbose)
        elif type_data == "ManyToManyField":
            textebcl = textebcl + '''
                    <div class="col-md-6">
                        <p class="fg-gray">
                            <label>{1} :</label><br>
                            {{% for item in model.{0}.all %}}
                                <span class="sub-alt-header badge badge-light"> {{{{ item }}}} </span><br>
                            {{% endfor %}}
                        </p>
                    </div>'''.format(nom_champ, nom_champ_verbose)
        elif type_data == "DateTimeField":
            textebcl = textebcl + '''
                    <div class="col-md-6">
                        <p>{1} :<br>
                            <span class="sub-alt-header">{{{{model.{0}|date:"d/m/Y H:i"}}}}</span>
                        </p>
                    </div>'''.format(nom_champ, nom_champ_verbose)
        elif type_data == "DateField":
            textebcl = textebcl + '''
                    <div class="col-md-6">
                        <p>{1} :<br>
                            <span class="sub-alt-header">{{{{model.{0}|date:"d/m/Y"}}}}</span>
                        </p>
                    </div>'''.format(nom_champ, nom_champ_verbose)
        elif type_data in ("CharField", "IntegerField", "FloatField") and len(list_champs[i].choices) > 0:
            textebcl = textebcl + '''
                    <div class="col-md-6">
                        <p>{1} :<br>
                            <span class="sub-alt-header">{{{{ model.value_{0} }}}}</span>
                        </p>
                    </div>'''.format(nom_champ, nom_champ_verbose)
        else :
            textebcl = textebcl + '''
                    <div class="col-md-6">
                        <p>{1} :<br>
                            <span class="sub-alt-header">{{{{ model.{0} }}}}</span>
                        </p>
                    </div>'''.format(nom_champ, nom_champ_verbose)

    texteTemplateLayout = texteTemplateLayout + textebcl
    texteTemplateLayout = texteTemplateLayout + '''
                </div>'''


    if len(relateds) > 0:
        texteTemplateLayout = texteTemplateLayout + '''
                <br><br>
                <div class="row">
                    <ul class="nav nav-tabs navtab-bg">
                        <li class="active"><a href="#frame_autres" data-toggle="tab" aria-expanded="false"><span>Autres informations</span></a></li>
                    </ul>
                    <div class="tab-content">
                        <div class="tab-pane active" id="frame_autres">
                            <div class="row margin20 no-margin-left no-margin-right">'''
        for i in range(0, len(relateds)):
            if relateds[i] != "":
                list_relateds = relateds[i].split(",")
                content_id = list_relateds[0]
                field_name = list_relateds[1]
                model_related = ContentType.objects.get(pk = content_id)
                model_class_related = model_related.model_class()
                nom_model_class_related = model_related.model_class().__name__
                nom_model_related = nom_model_class_related.replace("Model_", "").lower()
                input_name_related = "{}_{}_ids".format(nom_model_related, field_name)
                related_query_name = model_class_related._meta.get_field(field_name).related_query_name()
                if related_query_name.startswith("model_") : related_query_name = "{}_set".format(related_query_name)

                texteTemplateLayout = texteTemplateLayout + '''
                                <div class="col-md-6">
                                    <table class="table bordered no-margin" style="width:100%;">
                                        <thead><tr><th>{0}</th></tr></thead>
                                        <tbody class="tbl_posts_body">
                                            {{% for item in model.{1}.all %}}
                                                <tr><td><span class="sub-alt-header">{{{{ item }}}}</span></td></tr>
                                            {{% endfor %}}
                                        </tbody>
                                    </table>
                                </div>'''.format(model_class_related._meta.verbose_name_plural, related_query_name)

    texteTemplateLayout = texteTemplateLayout + '''
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''
    fichier.write(texteTemplateLayout)
    fichier.close()


    #TEMPLATE UPDATE
    path = os.path.abspath(os.path.curdir)
    path = path + "\\templates\\ErpProject\\{0}\\{1}".format(nomModule,nom_modele.lower())
    path = path + "\\update.html"
    fichier = codecs.open(path,"w", encoding='utf-8')

    texteTemplateLayout = '''
{{% extends "ErpProject/{0}/shared/layout.html" %}}
{{% block page %}} {{% load humanize %}} {{%load static %}} {{% load account_filters %}}
<div class="row">
    <ul class="breadcrumb">
        <li><a href="{{% url 'backoffice_index' %}}"><span class="mif-home"></span></a></li>
        <li><a class="chargement-au-click" href="{{% url 'module_{1}_index' %}}">Module {4}</a></li>
        <li><a class="chargement-au-click" href="{{% url '{2}_list_{3}' %}}">Liste des {5}</a></li>
        <li><a class="chargement-au-click" href="{{% url '{2}_detail_{3}' model.id %}}">{{{{ model }}}}</a></li>
        <li>{{{{ title }}}}</li>
    </ul>
</div>

<div class="row">
    <div class="col-lg-12">
        <h2>{{{{ title }}}}</h2>

        <strong style="float: right;color: grey;opacity: 0.4;margin-top: -30px;">{{% now "jS F Y H:i" %}}</strong>
        <div class="separ" style="background-color: grey;opacity: 0.2"></div>

        <div class="panel panel-default" style="border: none; margin-top: 1rem;">
            <div class="panel panel-body" style="background-color:#f5f5f5;border: none;border-radius: none;">
                <div class="row">
                    <button onclick="javascript:document.getElementById('submit').click()" class="theme-btn theme-btn-sm rounded primary_color_{{{{module.name|lower}}}}">Valider</button>
                    <button onclick="javascript:window.location.assign('{{% url '{2}_detail_{3}' model.id %}}')" class="theme-btn theme-btn-sm rounded" style="width: 20%;margin-left: 5px">Annuler</button>
                </div>

                <hr class="hr-ligne">
                <!-- Appel de la fonction message -->
                {{% include 'ErpProject/ErpBackOffice/widget/message.html' with messages=messages only %}}<br>

                <form id="form" method="POST" action="{{% url '{2}_post_update_{3}' %}}"  enctype="multipart/form-data" data-role="validator" data-show-required-state="false" data-hint-mode="line" data-hint-background="bg-red" data-hint-color="fg-white" data-hide-error="5000"
                    novalidate="novalidate" data-on-error-input="notifyOnErrorInput" data-show-error-hint="false">
                    {{% csrf_token %}}
                    <input id="submit" type="submit" style="display: none">
                    <input type="text"  id="ref" name="ref" value ="{{{{ model.id }}}}" style="display: none">
                    {{% if isPopup %}}<input id="isPopup" name="isPopup" value="1" type="text" style="display: none">{{% endif %}}
                    <div class="row">'''.format(nomModule, unidecode.unidecode(module.nom_module.lower()), nom_pattern, nom_modele.lower(), module.nom_module.capitalize(), nom_modele_verbose_plural)

    textebcl = ""
    for i in range(0,len(list_champs)):
        nom_champ = ""
        nom_champ_verbose = ""
        type_data = ""
        try:
            nom_champ = list_champs[i].name.lower()
            nom_champ_verbose = list_champs[i].verbose_name
            type_data = str(list_champs[i].__class__.__name__)
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass

        # Contrôle quand on n'a pas défini une valeur par defaut et que le champ est requis
        is_required = False
        if inspect.isclass(default_value) == True and is_null == False and type_data != "ManyToManyField": is_required = True

        if type_data == "FloatField" and len(list_champs[i].choices) == 0:
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True :
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control number full-size" data-role="input">
                                <input value="{{{{ model.{0}|input_float }}}}" name="{0}" id="{0}" type="number" step="0.01" '''.format(nom_champ)
            if is_required == True :
                textebcl = textebcl + 'data-validate-func="required, number" data-validate-hint="Saisissez un nombre valide sur le champ {} SVP !">'.format(nom_champ_verbose)
            else : textebcl = textebcl + 'data-validate-func="number" data-validate-hint="Saisissez un nombre valide sur le champ {} SVP !">'.format(nom_champ_verbose)
            textebcl = textebcl + '''
                            </div>
                        </div>'''
        elif type_data == "CharField" and len(list_champs[i].choices) == 0:
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True :
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            if list_champs[i].max_length != None and list_champs[i].max_length > 500 :
                textebcl = textebcl + '''
                            <div class="input-control text full-size">
                                <textarea name="{0}" id="{0}" '''.format(nom_champ)
                if is_required == True :
                    textebcl = textebcl + 'data-validate-func="required" data-validate-hint="Saisissez le champ {} SVP !">'.format(nom_champ_verbose)
                else : textebcl = textebcl + ">{{{{ model.{0} }}}}</textarea>".format(nom_champ)
            else:
                textebcl = textebcl + '''
                            <div class="input-control text full-size" data-role="input">
                                <input value="{{{{ model.{0} }}}}" name="{0}" id="{0}" type="text" '''.format(nom_champ)
                if is_required == True :
                    textebcl = textebcl + 'data-validate-func="required" data-validate-hint="Saisissez le champ {} SVP !">'.format(nom_champ_verbose)
                else : textebcl = textebcl + ">"
            textebcl = textebcl + '''
                            </div>
                        </div>'''
        elif type_data == "EmailField":
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True :
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control email full-size" data-role="input">
                                <input value="{{{{ model.{0} }}}}" name="{0}" id="{0}" type="email" '''.format(nom_champ)
            if is_required == True :
                textebcl = textebcl + 'data-validate-func="required, email" data-validate-hint="Saisissez une adresse email valide sur le champ {} SVP !">'.format(nom_champ_verbose)
            else : textebcl = textebcl + ">"
            textebcl = textebcl + '''
                            </div>
                        </div>'''
        elif type_data == "IntegerField" and len(list_champs[i].choices) == 0:
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True :
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control number full-size" data-role="input">
                                <input value="{{{{ model.{0} }}}}" name="{0}" id="{0}" type="number" '''.format(nom_champ)
            if is_required == True :
                textebcl = textebcl + 'data-validate-func="required, number" data-validate-hint="Saisissez un nombre valide sur le champ {} SVP !">'.format(nom_champ_verbose)
            else : textebcl = textebcl + 'data-validate-func="number" data-validate-hint="Saisissez un nombre valide sur le champ {} SVP !">'.format(nom_champ_verbose)
            textebcl = textebcl + '''
                            </div>
                        </div>'''
        elif type_data == "ImageField":
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{0}</label>
                            <div class="tile-container">
                                <input class="image_upload" name="{1}" id="{1}" type="file" accept="image/*" style="display:none;">
                                <a id="trigger-input-file" href="#" class="trigger-input-file tile-wide fg-white shadow" style="height: 100px!important; width: 100px!important;" data-role="tile">
                                    <div class="tile-content slide-up">
                                        <div class="slide">
                                            {{% if model.{1} %}}<img class="image_preview" src="{{% static model.{1}.url %}}" style="height: 100px; width: 100px;"> {{% else %}}
                                            <img class="image_preview" src="{{% static 'ErpProject/image/upload/articles/default.png' %}}" style="height: 100px; width: 100px;">{{% endif %}}
                                        </div>
                                        <div class="slide-over op-dark padding10" style="text-align: center!important; opacity: 60%!important;">
                                            <span class="icon mif-pencil" style="text-align: center!important; font-size: 40px!important;"></span>
                                        </div>
                                    </div>
                                </a>
                            </div>
                        </div>'''.format(nom_champ_verbose, nom_champ)
        elif type_data == "FileField":
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{0}</label>
                                {{% if model.document %}}
                                <span style=" color: #000; font-size: 10px;">Actuellement: <a href="{{% static model.document.url %}}">{{{{model.document.name|truncatechars:45}}}}</a></span>
                                {{% else %}}<span style=" color: #000; font-size: 10px;">Actuellement: Aucun document attaché</span>{{% endif %}}
                            <div class="input-control file full-size" data-role="input">
                                <input name="{1}" id="{1}" type="file"><button class="button"><span class="mif-folder"></span></button>
                            </div>
                        </div>'''.format(nom_champ_verbose, nom_champ)
        elif type_data == "ForeignKey":
            related_model = list_champs[i].related_model.__name__
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True :
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size">
                                <select name="{0}_id" id="{0}_id">
                                    <option value="">Sélectionnez une option</option>
                                    <option class="create_option" value='-100' data-url="/{1}/{2}/add?isPopup=1">Créer nouveau...</option>
                                    {{% for item in {2}s %}}<option {{% if model.{0}_id == item.id %}}{{{{ "selected" }}}}{{% endif %}} value="{{{{ item.id }}}}">{{{{ item }}}}</option>{{% endfor %}}
                                </select>
                            </div>
                        </div>'''.format(nom_champ, module.url_vers.replace("/", ""), related_model.replace("Model_", "").lower())
        elif type_data == "OneToOneField":
            related_model = list_champs[i].related_model.__name__
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True :
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size">
                                <select name="{0}_id" id="{0}_id">
                                    <option value="">Sélectionnez une option</option>
                                    <option class="create_option" value='-100' data-url="/{1}/{2}/add?isPopup=1">Créer nouveau...</option>
                                    {{% for item in {2}s %}}<option {{% if model.{0}_id == item.id %}}{{{{ "selected" }}}}{{% endif %}} value="{{{{ item.id }}}}">{{{{ item }}}}</option>{{% endfor %}}
                                </select>
                            </div>
                        </div>'''.format(nom_champ, module.url_vers.replace("/", ""), related_model.replace("Model_", "").lower())
        elif type_data == "ManyToManyField":
            related_model = list_champs[i].related_model.__name__
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True :
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="text full-size">
                                <select multiple="multiple" class="multi-select multi_select2" name="{0}" id="{0}">
                                    {{% for item in {1}s %}}<option {{% for object in model.{0}.all %}} {{% if object.id == item.id %}}{{{{ "selected" }}}}{{% endif %}}{{% endfor %}} value="{{{{ item.id }}}}">{{{{item}}}}</option>{{% endfor %}}
                                </select>
                            </div>
                        </div>'''.format(nom_champ, related_model.replace("Model_", "").lower())
        elif type_data == "BooleanField":
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label class="input-control checkbox small-check full-size">
                                <input name="{1}" id="{1}" {{% if model.{1} == True %}} {{{{ "checked" }}}} {{% endif %}} type="checkbox">
                                <span class="check"></span><span class="caption">{0}</span>'''.format(nom_champ_verbose, nom_champ)
            if is_required == True :
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            </label>
                        </div>'''
        elif type_data == "DateTimeField":
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True :
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size datetimepicker">
                                <input type="text" name="{1}" id="{1}" value="{{{{ model.{1}|date:"d/m/Y H:i" }}}}">
                                <div class="button"><span class="glyphicon glyphicon-screenshot far fa-calendar" style="margin-right:3px;"></span><span class="glyphicon glyphicon-screenshot far fa-clock"></span></div>
                            </div>
                        </div>'''.format(nom_champ_verbose, nom_champ)
        elif type_data == "DateField":
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True :
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size"  data-format="dd/mm/yyyy" data-role="datepicker" data-locale="fr">
                                <input type="text" name="{1}" id="{1}" value="{{{{ model.{1}|date:"d/m/Y" }}}}">
                                <div class="button"><span class="mif-calendar"></span></div>
                            </div>
                        </div>'''.format(nom_champ_verbose, nom_champ)
        elif type_data in ("CharField", "IntegerField", "FloatField") and len(list_champs[i].choices) > 0:
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True :
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size">
                                <select name="{0}" id="{0}">
                                    <option value="">Sélectionnez une option</option>
                                    {{% for item in model.list_{0} %}}<option {{% if model.{0} == item.id %}}{{{{ "selected" }}}}{{% endif %}} value="{{{{ item.id }}}}">{{{{ item.designation }}}}</option>{{% endfor %}}
                                </select>
                            </div>
                        </div>'''.format(nom_champ)
        else :
            textebcl = textebcl + '''
                        <div class="col-md-6">
                            <label>{}</label>'''.format(nom_champ_verbose)
            if is_required == True :
                textebcl = textebcl + "<span style='font-weight: bold; font-size: 14px; margin-left: 5px; color: red;'>*</span>"
            textebcl = textebcl + '''
                            <div class="input-control text full-size" data-role="input">
                                <input value="{{{{ model.{0} }}}}" name="{0}" id="{0}" type="text" '''.format(nom_champ)
            if is_required == True :
                textebcl = textebcl + 'data-validate-func="required" data-validate-hint="Saisissez le champ {} SVP !">'.format(nom_champ_verbose)
            else : textebcl = textebcl + ">"
            textebcl = textebcl + '''
                            </div>
                        </div>'''

    texteTemplateLayout = texteTemplateLayout + textebcl
    texteTemplateLayout = texteTemplateLayout + '''
                    </div>'''

    if len(relateds) > 0:
        texteTemplateLayout = texteTemplateLayout + '''
                    <br><br>
                    <div class="row">
                        <ul class="nav nav-tabs navtab-bg">
                            <li class="active"><a href="#frame_autres" data-toggle="tab" aria-expanded="false"><span>Autres informations</span></a></li>
                        </ul>
                        <div class="tab-content">
                            <div class="tab-pane active" id="frame_autres">
                                <div class="row margin20 no-margin-left no-margin-right">'''
        for i in range(0, len(relateds)):
            if relateds[i] != "":
                list_relateds = relateds[i].split(",")
                content_id = list_relateds[0]
                field_name = list_relateds[1]
                model_related = ContentType.objects.get(pk = content_id)
                model_class_related = model_related.model_class()
                nom_model_class_related = model_related.model_class().__name__
                nom_model_related = nom_model_class_related.replace("Model_", "").lower()
                input_name_related = "{}_{}_ids".format(nom_model_related, field_name)
                related_query_name = model_class_related._meta.get_field(field_name).related_query_name()
                if related_query_name.startswith("model_") : related_query_name = "{}_set".format(related_query_name)

                texteTemplateLayout = texteTemplateLayout + '''
                                <div class="col-md-6">
                                    <div class="section-otm" data-compteur="1">
                                        <table class="table bordered no-margin" style="width:100%;">
                                            <thead>
                                                <tr>
                                                    <th width="90%">{0}</th>
                                                    <th width="10%"></th>
                                                </tr>
                                            </thead>
                                            <tbody class="tbl_posts_body">
                                                {{% for item in model.{4}.all %}}
                                                <tr>
                                                    <td>
                                                        <div class="input-control text full-size">
                                                            <select class="selectpicker form-control" data-live-search="true" title="sélectionner une option" name="{3}" id="{3}-1">
                                                                <option value="">Sélectionnez une nouvelle option {0}</option>
                                                                <option class="create_option" value='-100' data-url="/{1}/{2}/add?isPopup=1">Créer nouveau...</option>
                                                                <option {{{{ "selected" }}}} value="{{{{ item.id }}}}"> {{{{ item }}}} </option>
                                                            </select>
                                                        </div>
                                                    </td>
                                                    <td>
                                                        <div class="pagination no-border">
                                                            <span class="item delete-record" title="Supprimer la ligne"><span class="mif-cross fg-red"></span></span>
                                                        </div>
                                                    </td>
                                                </tr>
                                                {{% endfor %}}
                                            </tbody>
                                        </table>
                                        <br><button type="button" class="button rounded add-record">Ajouter</button>
                                        <table class="sample_table" style="display:none;">
                                            <tr>
                                                <td>
                                                    <div class="input-control text full-size">
                                                        <select class="form-control" data-live-search="true" title="Sélectionner une option" name="{3}" id="">
                                                            <option value="">Sélectionnez une nouvelle option {0}</option>
                                                            <option class="create_option" value='-100' data-url="/{1}/{2}/add?isPopup=1">Créer nouveau...</option>
                                                        </select>
                                                    </div>
                                                </td>
                                                <td>
                                                    <div class="pagination no-border">
                                                        <span class="item delete-record" title="Supprimer la ligne"><span class="mif-cross fg-red"></span></span>
                                                    </div>
                                                </td>
                                            </tr>
                                        </table>
                                    </div>'''.format(model_class_related._meta.verbose_name, module.url_vers.replace("/", ""), nom_model_related, input_name_related, related_query_name)
        texteTemplateLayout = texteTemplateLayout + '''
                                </div>
                            </div>
                        </div>
                    </div>'''

    texteTemplateLayout = texteTemplateLayout + '''
                </form>
            </div>
        </div>
    </div>
    <!-- /.col-lg-12 -->
</div>
{% endblock %}'''
    fichier.write(texteTemplateLayout)
    fichier.close()

    # TEMPLATE UPLOAD
    path = os.path.abspath(os.path.curdir)
    path = path + "\\templates\\ErpProject\\{0}\\{1}".format(nomModule, nom_modele.lower())
    path = path + "\\upload.html"
    fichier = codecs.open(path,"w", encoding='utf-8')
    texteTemplateLayout = '''
{{% extends "ErpProject/{0}/shared/layout.html" %}}
{{% block page %}} {{% load humanize %}} {{%load static %}} {{% load account_filters %}}
<div class="row">
    <ul class="breadcrumb">
        <li><a href="{{% url 'backoffice_index' %}}"><span class="mif-home"></span></a></li>
        <li><a class="chargement-au-click" href="{{% url 'module_{1}_index' %}}">Module {4}</a></li>
        <li><a class="chargement-au-click" href="{{% url '{2}_add_{3}' %}}">Création nouvel objet {5}</a></li>
        <li>{{{{ title }}}}</li>
    </ul>
</div>

<div class="row">
    <div class="col-lg-12">
        <h2>{{{{ title }}}}</h2>

        <strong style="float: right;color: grey;opacity: 0.4;margin-top: -30px;">{{% now "jS F Y H:i" %}}</strong>
        <div class="separ" style="background-color: grey;opacity: 0.2"></div>

        <div class="panel panel-default" style="border: none; margin-top: 1rem;">
            <div class="panel panel-body" style="background-color:#f5f5f5;border: none;border-radius: none;">
                <div class="row">
                    <button onclick="selectFile()" class="theme-btn theme-btn-sm rounded primary_color_{{{{module.name|lower}}}} chargement-au-click">Choisir un fichier</button>
                    <button id="btn-register" style="display:none;" onclick="enregistrer()" class="theme-btn theme-btn-sm rounded primary_color_{{{{module.name|lower}}}}">Valider</button>
                    <button onclick="javascript:window.location.assign('{{% url '{2}_add_{3}' %}}')" class="theme-btn theme-btn-sm rounded" style="width: 20%;margin-left: 5px">Annuler</button>
                </div>

                <hr class="hr-ligne">
                <!-- Appel de la fonction message -->
                {{% include 'ErpProject/ErpBackOffice/widget/message.html' with messages=messages only %}}<br>

                <form id="form" method="POST" action="{{% url '{2}_post_upload_{3}' %}}"  enctype="multipart/form-data" data-role="validator" data-show-required-state="false" data-hint-mode="line" data-hint-background="bg-red" data-hint-color="fg-white" data-hide-error="5000"
                    novalidate="novalidate" data-on-error-input="notifyOnErrorInput" data-show-error-hint="false">
                    {{% csrf_token %}}
                    <input id="submit" type="submit" style="display: none">
                    <input type="file" id="input-excel" name="file_upload" style="display:none;"/>
                    <input type="text" id="sheet" name="sheet" style="display:none;"/>
                </form>
                <div id="upload_wrapper">
                </div>

                <div id="bg" class="row no-margin-left no-margin-right" style="padding-top:300px;">
                    <div class="col-md-3 xs-hidden"></div>
                    <div class="col-md-6 col-xs-12">
                        <h3>Choisissez un fichier CSV ou Excel à importer.</h3>
                        <span class="fg-gray" style="text-align:center;">Les fichiers Excel sont recommandés pour le formatage des champs.<br> <a href="/static/ErpProject/file/import/import_{3}.xlsx" download> Cliquez ici</a> pour télécharger le modèle de fichier d'import avec les entêtes récommandés </span>
                    </div>
                    <div class="col-md-3 xs-hidden"></div>
                </div>

            </div>
        </div>
    </div>
    <!-- /.col-lg-12 -->
</div> '''.format(nomModule, unidecode.unidecode(module.nom_module.lower()), nom_pattern, nom_modele.lower(), module.nom_module.capitalize(), nom_modele_verbose)

    texteTemplateLayout = texteTemplateLayout + '''
<script type="text/javascript" src="{% static 'ErpProject/js/FileSaver.min.js' %}"></script>
<script type="text/javascript" src="{% static 'ErpProject/js/xlsx.full.min.js' %}"></script>
<script>
    function enregistrer(){
        document.getElementById('submit').click();
    }

    function selectFile() {
        $('input[id=input-excel]').click();
    }

    //Import excel
    $('#input-excel').change(function(e){
        var reader = new FileReader();
        reader.readAsArrayBuffer(e.target.files[0]);
        reader.onload = function(e) {
            var data = new Uint8Array(reader.result);
            var wb = XLSX.read(data,{type:'array'});
            var ws_name = wb.SheetNames[0];
            console.log(ws_name);
            $("#sheet").val(ws_name);
            $("#upload_wrapper").children().remove();
            var sheet = wb.Sheets[ws_name];
            var htmlstr = XLSX.write(wb,{sheet: ws_name, type:'binary',bookType:'html'});
            htmlstr = decodeURIComponent(escape(htmlstr));
            $('#upload_wrapper')[0].innerHTML += htmlstr;
            $('#upload_wrapper table').addClass("display nowrap border bordered striped table-overflow");
            $('#upload_wrapper table').css('overflow', 'auto');
            $('#upload_wrapper table').css('position', 'relative');
            $('#upload_wrapper table').css('display', 'inline-block');
            $('#upload_wrapper table').css('width', '100%');

            $('#bg').css('display', 'none');
            $('#btn-register').css('display', 'inline');
        }
    });
</script>
{% endblock %}
'''
    fichier.write(texteTemplateLayout)
    fichier.close()

    # CRUD AND URLS URLS
    path = os.path.abspath(os.path.curdir)
    path = path + "\\{0}\\urls.py".format(nomModule)
    fichier = codecs.open(path,"a", encoding='utf-8')

    texte_a_ajouter_urls_py_dossier_ap="\n#{2} URLS\n#=====================================\n#{2} CRUD URLS\nurlpatterns.append(url(r'^{0}/list', views.get_lister_{0}, name = '{1}_list_{0}'))".format(nom_modele.lower(),nom_pattern, nom_modele.upper())
    texte_a_ajouter_urls_py_dossier_ap= texte_a_ajouter_urls_py_dossier_ap + "\nurlpatterns.append(url(r'^{0}/add', views.get_creer_{0}, name = '{1}_add_{0}'))".format(nom_modele.lower(),nom_pattern)
    texte_a_ajouter_urls_py_dossier_ap= texte_a_ajouter_urls_py_dossier_ap + "\nurlpatterns.append(url(r'^{0}/post_add', views.post_creer_{0}, name = '{1}_post_add_{0}'))".format(nom_modele.lower(),nom_pattern)
    texte_a_ajouter_urls_py_dossier_ap= texte_a_ajouter_urls_py_dossier_ap + "\nurlpatterns.append(url(r'^{0}/item/(?P<ref>[0-9]+)/$', views.get_details_{0}, name = '{1}_detail_{0}'))".format(nom_modele.lower(),nom_pattern)
    texte_a_ajouter_urls_py_dossier_ap= texte_a_ajouter_urls_py_dossier_ap + "\nurlpatterns.append(url(r'^{0}/item/post_update/$', views.post_modifier_{0}, name = '{1}_post_update_{0}'))".format(nom_modele.lower(),nom_pattern)
    texte_a_ajouter_urls_py_dossier_ap= texte_a_ajouter_urls_py_dossier_ap + "\nurlpatterns.append(url(r'^{0}/item/(?P<ref>[0-9]+)/update$', views.get_modifier_{0}, name = '{1}_update_{0}'))".format(nom_modele.lower(),nom_pattern)
    texte_a_ajouter_urls_py_dossier_ap= texte_a_ajouter_urls_py_dossier_ap + "\n#{2} UPLOAD URLS\nurlpatterns.append(url(r'^{0}/upload/add', views.get_upload_{0}, name = '{1}_get_upload_{0}'))".format(nom_modele.lower(),nom_pattern, nom_modele.upper())
    texte_a_ajouter_urls_py_dossier_ap= texte_a_ajouter_urls_py_dossier_ap + "\nurlpatterns.append(url(r'^{0}/upload/post_add', views.post_upload_{0}, name = '{1}_post_upload_{0}'))\n".format(nom_modele.lower(),nom_pattern)
    fichier.write(texte_a_ajouter_urls_py_dossier_ap)
    fichier.close()


def genReportingOfContentType(content_type_id, module_id):
    content_type = ContentType.objects.get(id = content_type_id)
    model_class = content_type.model_class()
    module = dao_module.toGetModule(module_id)
    #Standardisation denomination modele
    nom_modele = content_type.model.replace("model_","").capitalize()
    nom_modele_verbose = model_class._meta.verbose_name
    nom_modele_verbose_plural = model_class._meta.verbose_name_plural
    nom_modele_class = model_class.__name__
    nomdao="dao_{0}".format(nom_modele.lower())
    nom_pattern = 'module_{0}'.format(unidecode.unidecode(module.nom_module.lower()))
    nomModule = module.nom_application
    nameModuleUp = nom_pattern.upper()

    list_champs = []
    for field in model_class._meta.get_fields():
        if field.name not in ("id", "statut", "etat", "creation_date", "update_date", "auteur") and field.__class__.__name__ != "ManyToOneRel": list_champs.append(field)

    # CREATION FONCTIONS RAPPORT DANS views.py
    path = os.path.abspath(os.path.curdir)
    path = path + "\\{0}\\views.py".format(nomModule)
    fichier = codecs.open(path, "a", encoding='utf-8')

    # GET GENERER RAPPORT
    texte_a_ajouter_views_py = "\n\n# {2} REPORTING CONTROLLERS\ndef get_generer_{0}(request):\n\ttry:\n\t\tpermission_number = 0\n\t\tmodules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)\n\t\tif response != None: return response\n\n\t\tcontext = {{\n\t\t\t'title' : 'Rapport {3}',\n\t\t\t'devises' : dao_devise.toListDevisesActives(),\n\t\t\t'utilisateur' : utilisateur,\n\t\t\t'modules' : modules,\n\t\t\t'sous_modules': sous_modules,\n\t\t\t'module' : vars_module,\n\t\t\t'organisation': dao_organisation.toGetMainOrganisation()\n\t\t}}\n\t\ttemplate = loader.get_template('ErpProject/{4}/{0}/generate.html')\n\t\treturn HttpResponse(template.render(context, request))\n\texcept Exception as e:\n\t\treturn auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)".format(nom_modele.lower(),nomdao,nom_modele.upper(),nom_modele_verbose.lower(),nomModule)

    # POST TRAITER RAPPORT
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\ndef post_traiter_{0}(request, utilisateur = None, modules = [], sous_modules = [], enum_module = vars_module):\n\t#On recupère et format les inputs reçus\n\tdate_debut = request.POST['date_debut']\n\tdate_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))\n\n\tdate_fin = request.POST['date_fin']\n\tdate_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]), 23, 59, 59)\n\n\t#On récupère les données suivant le filtre défini\n\tmodel = {2}.objects.filter(creation_date__range = [date_debut, date_fin]).order_by('-creation_date')\n\n\tcontext = {{\n\t\t'title' : 'Rapport {1}',\n\t\t'model' : model,\n\t\t'date_debut' : request.POST['date_debut'],\n\t\t'date_fin' : request.POST['date_fin'],\n\t\t'utilisateur' : utilisateur,\n\t\t'modules' : modules,\n\t\t'sous_modules': sous_modules,\n\t\t'module' : enum_module,\n\t\t'organisation' : dao_organisation.toGetMainOrganisation(),\n\t}}\n\treturn context".format(nom_modele.lower(),nom_modele_verbose,nom_modele_class)

    # POST GENERER RAPPORT
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\ndef post_generer_{0}(request):\n\ttry:\n\t\tpermission_number = 0\n\t\tmodules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)\n\t\tif response != None: return response\n\n\t\tcontext = post_traiter_{0}(request, utilisateur, modules, sous_modules)\n\t\ttemplate = loader.get_template('ErpProject/{4}/{0}/generated.html')\n\t\treturn HttpResponse(template.render(context, request))\n\texcept Exception as e:\n\t\treturn auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)".format(nom_modele.lower(),nomdao,nom_modele.upper(),nom_modele_verbose.lower(),nomModule)

    # POST IMPRIMER RAPPORT
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\ndef post_imprimer_rapport_{0}(request):\n\ttry:\n\t\tcontext = post_traiter_{0}(request)\n\t\treturn weasy_print('ErpProject/{2}/reporting/rapport_{0}.html', 'rapport_{0}.pdf', context)\n\texcept Exception as e:\n\t\treturn auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e, reverse('{1}_get_generer_{0}'))".format(nom_modele.lower(), nom_pattern, nomModule)

    fichier.write(texte_a_ajouter_views_py)
    fichier.close()

    # CREATION DES TEMPLATES REPORTING DU MODELE

    # TEMPLATE GENERATE
    path = os.path.abspath(os.path.curdir)
    path = path + "\\templates\\ErpProject\\{0}\\{1}".format(nomModule, nom_modele.lower())
    path = path + "\\generate.html"
    fichier = codecs.open(path,"w", encoding='utf-8')
    texteTemplateLayout = '''
{{% extends "ErpProject/{0}/shared/layout.html" %}}
{{% block page %}} {{% load humanize %}} {{%load static %}} {{% load account_filters %}}
<div class="row">
    <ul class="breadcrumb">
        <li><a href="{{% url 'backoffice_index' %}}"><span class="mif-home"></span></a></li>
        <li><a class="chargement-au-click" href="{{% url 'module_{1}_index' %}}">Module {4}</a></li>
        <li>{{{{ title }}}}</li>
    </ul>
</div>

<div class="row">
    <h2 class="text-light no-margin-left">{{{{ title }}}}</h2>
</div>

<div class="row">
    <button onclick="javascript:document.getElementById('submit').click()" class="theme-btn theme-btn-sm rounded primary_color_{{{{module.name|lower}}}}">Valider</button>
    <button onclick="javascript:window.location.assign('{{% url 'module_{1}_index' %}}')" class="theme-btn theme-btn-sm rounded" style="width: 20%;margin-left: 5px">Annuler</button>
</div>

<hr class="hr-ligne">
<!-- Appel de la fonction message -->
{{% include 'ErpProject/ErpBackOffice/widget/message.html' with messages=messages only %}}<br>

<div class="row item-content" style="margin-top: 10px">
    <form id="form" method="POST" action="{{% url '{2}_post_generer_{3}' %}}"
        data-role="validator"
        data-show-required-state="false"
        data-hint-mode="line"
        data-hint-background="bg-red"
        data-hint-color="fg-white"
        data-hide-error="5000"
        novalidate="novalidate"
        data-on-error-input="notifyOnErrorInput"
        data-show-error-hint="false">
        {{% csrf_token %}}
        <input id="submit" type="submit" style="display: none">

        <div class="row">
            <div class="col-md-12">
                <div class="row">
                    <div class="col-md-6">
                        <label>Date de début :</label>
                        <div id="input-date-debut" class="input-control text full-size"  data-format="dd/mm/yyyy" data-role="datepicker" data-locale="fr">
                            <input readonly type="text" name="date_debut" id="date_debut" readonly
                                data-validate-func="required"
                                data-validate-hint="Précisez la date de début svp.">
                            <div class="button"><span class="mif-calendar"></span></div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <label>Date de fin :</label>
                        <div id="input-date-fin" class="input-control text full-size"  data-format="dd/mm/yyyy" data-role="datepicker" data-locale="fr">
                            <input readonly type="text" name="date_fin" id="date_fin" readonly
                                data-validate-func="required"
                                data-validate-hint="Précisez la date de fin svp.">
                            <div class="button"><span class="mif-calendar"></span></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </form>
</div>
{{% endblock %}}'''.format(nomModule, unidecode.unidecode(module.nom_module.lower()), nom_pattern, nom_modele.lower(), module.nom_module.capitalize(), nom_modele_verbose_plural)

    fichier.write(texteTemplateLayout)
    fichier.close()


    # TEMPLATE GENERATED
    path = os.path.abspath(os.path.curdir)
    path = path + "\\templates\\ErpProject\\{0}\\{1}".format(nomModule,nom_modele.lower())
    path = path + "\\generated.html"
    fichier = codecs.open(path,"w", encoding='utf-8')

    texteTemplate = '''
{{% extends "ErpProject/{0}/shared/layout.html" %}}
{{% block page %}} {{% load humanize %}} {{%load static %}} {{% load account_filters %}}
<div class="row">
    <ul class="breadcrumb">
        <li><a href="{{% url 'backoffice_index' %}}"><span class="mif-home"></span></a></li>
        <li><a class="chargement-au-click" href="{{% url 'module_{1}_index' %}}">Module {4}</a></li>
        <li>{{{{ title }}}}</li>
    </ul>
</div>

<div class="row">
    <button onclick="javascript:document.getElementById('submit').click()" class="theme-btn theme-btn-sm rounded primary_color_{{{{module.name|lower}}}}">Imprimer</button>
    <button id="btn_export" class="theme-btn theme-btn-sm rounded chargement-au-click">Exporter en Excel</button>
    <button onclick="javascript:window.location.assign('{{% url '{2}_get_generer_{3}' %}}')" class="theme-btn theme-btn-sm rounded" style="width: 20%;margin-left: 5px">Annuler</button>
</div>

<form id="form" method="POST" action="{{% url '{2}_post_imprimer_rapport_{3}' %}}">
    {{% csrf_token %}}
    <input id="submit" type="submit" style="display: none">
    <input type="text" name="date_debut" value="{{{{ date_debut }}}}" style="display: none">
    <input type="text" name="date_fin" value="{{{{ date_fin }}}}" style="display: none">
</form>
<hr class="hr-ligne">
<div id="divToPrint" class="row item-content" style="margin-top: 20px" style="padding-top: 30px">
    <p class="align-center header">{{{{ title }}}}</p>
    <div class="row">
        <p>
            Période :<br>
            <span class="sub-header">Du {{{{ date_debut }}}} au {{{{ date_fin }}}} </span>
            <br>
            <br>
        </p>
    </div>
    <br>
    <br>
    <table id="rapport" class="table bordered no-margin" style="width: 950px">
        <tr style="background-color:#f1f1f1">'''.format(nomModule, unidecode.unidecode(module.nom_module.lower()), nom_pattern, nom_modele.lower(), module.nom_module.capitalize())

    textebcl=""
    for i in range(0,len(list_champs)):
        nom_champ = ""
        nom_champ_verbose = ""
        type_data = ""
        try:
            nom_champ = list_champs[i].name.lower()
            nom_champ_verbose = list_champs[i].verbose_name
            type_data = str(list_champs[i].__class__.__name__)
        except Exception as e:
            pass
        if type_data not in  ("ManyToManyField", "ImageField", "FileField"):
            textebcl = textebcl + '''
            <th>{0}</th>'''.format(nom_champ_verbose)
    textebcl = textebcl + '''
            <th>Date de création</th>
            <th>Créé par</th>'''
    texteTemplate = texteTemplate + textebcl

    texteTemplate= texteTemplate + '''
        </tr>
        {{% for item in model %}}
        <tr>'''.format(nom_pattern, nom_modele.lower(), list_champs[0].name)

    textebcl = ""
    for i in range(0,len(list_champs)):
        nom_champ = ""
        nom_champ_verbose = ""
        type_data = ""
        try:
            nom_champ = list_champs[i].name.lower()
            nom_champ_verbose = list_champs[i].verbose_name
            type_data = str(list_champs[i].__class__.__name__)
        except Exception as e:
            pass
        if type_data not in  ("ManyToManyField", "ImageField", "FileField"):
            if type_data == "FloatField" and len(list_champs[i].choices) == 0:
                textebcl = textebcl + '''
            <td>{{{{item.{0}|monetary}}}}</td>'''.format(nom_champ)
            elif type_data == "CharField" and len(list_champs[i].choices) == 0:
                textebcl = textebcl + '''
            <td>{{{{item.{0}|truncatechars:22}}}}</td>'''.format(nom_champ)
            elif type_data == "BooleanField":
                textebcl = textebcl + '''
            <td>{{{{item.{0}|boolean}}}}</td>'''.format(nom_champ)
            elif type_data == "DateTimeField":
                textebcl = textebcl + '''
            <td>{{{{item.{0}|date:"d/m/Y H:i"}}}}</td>'''.format(nom_champ)
            elif type_data == "DateField":
                textebcl = textebcl + '''
            <td>{{{{item.{0}|date:"d/m/Y"}}}}</td>'''.format(nom_champ)
            elif type_data in ("CharField", "IntegerField", "FloatField") and len(list_champs[i].choices) > 0:
                textebcl = textebcl + '''
            <td>{{{{ item.value_{0} }}}}</td>'''.format(nom_champ)
            else :
                textebcl = textebcl + '''
            <td>{{{{item.{0}}}}}</td>'''.format(nom_champ)

    texteTemplate = texteTemplate + textebcl

    texteTemplate = texteTemplate + '''
            <td>{{{{item.creation_date|date:'d/m/Y'}}}}</td>
            <td>{{{{item.auteur.nom_complet}}}}</td>
        </tr>
        {{% endfor %}}
    </table>
</div>
{{% include 'ErpProject/ErpBackOffice/widget/export_excel.html' with btn_id="btn_export" table_id="rapport" filename="rapport_{1}" only %}}
{{% endblock %}}
'''.format(nom_pattern, nom_modele.lower(), list_champs[0].name)
    fichier.write(texteTemplate)
    fichier.close()


    # TEMPLATE RAPPORT
    path = os.path.abspath(os.path.curdir)
    path = path + "\\templates\\ErpProject\\{0}\\reporting".format(nomModule, nom_modele.lower())
    try:
        os.mkdir(path)
    except Exception as e:
        pass
    path = path + "\\rapport_{1}.html".format(nomModule, nom_modele.lower())
    fichier = codecs.open(path,"w", encoding='utf-8')

    texteTemplate = '''
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>{{{{ title }}}}</title>
        <meta name="description" content="{{{{ title }}}}">
        <meta name="author" content="MelodyERP">
    </head>
    {{%load static %}}{{% load account_filters %}}{{% load humanize %}}

    <body>
        <div id="report">
            <h2 class="align-center header">{{{{ title }}}}</h2>
            <span class="date-text">Le {{% now " d/m/Y" %}}</span>
            <div class="row">
                <p>
                    Période :<br>
                    <span class="sub-header">Du {{{{ date_debut }}}} au {{{{ date_fin }}}} </span>
                    <br>
                    <br>
                </p>
            </div>
            <br>
            <table id="rapport" class="table bordered no-margin" style="width: 100%">
                <tr style="background-color:#f1f1f1">'''.format(nomModule, unidecode.unidecode(module.nom_module.lower()), nom_pattern, nom_modele.lower(), module.nom_module.capitalize())

    textebcl=""
    for i in range(0,len(list_champs)):
        nom_champ = ""
        nom_champ_verbose = ""
        type_data = ""
        try:
            nom_champ = list_champs[i].name.lower()
            nom_champ_verbose = list_champs[i].verbose_name
            type_data = str(list_champs[i].__class__.__name__)
        except Exception as e:
            pass
        if type_data not in  ("ManyToManyField", "ImageField", "FileField"):
            textebcl = textebcl + '''
                    <th>{0}</th>'''.format(nom_champ_verbose)
    textebcl = textebcl + '''
                    <th>Date de création</th>
                    <th>Créé par</th>'''
    texteTemplate = texteTemplate + textebcl

    texteTemplate= texteTemplate + '''
                </tr>
                {{% for item in model %}}
                <tr>'''.format(nom_pattern, nom_modele.lower(), list_champs[0].name)

    textebcl = ""
    for i in range(0,len(list_champs)):
        nom_champ = ""
        nom_champ_verbose = ""
        type_data = ""
        try:
            nom_champ = list_champs[i].name.lower()
            nom_champ_verbose = list_champs[i].verbose_name
            type_data = str(list_champs[i].__class__.__name__)
        except Exception as e:
            pass
        if type_data not in  ("ManyToManyField", "ImageField", "FileField"):
            if type_data == "FloatField" and len(list_champs[i].choices) == 0:
                textebcl = textebcl + '''
                    <td>{{{{item.{0}|monetary}}}}</td>'''.format(nom_champ)
            elif type_data == "CharField" and len(list_champs[i].choices) == 0:
                textebcl = textebcl + '''
                    <td>{{{{item.{0}|truncatechars:22}}}}</td>'''.format(nom_champ)
            elif type_data == "BooleanField":
                textebcl = textebcl + '''
                    <td>{{{{item.{0}|boolean}}}}</td>'''.format(nom_champ)
            elif type_data == "DateTimeField":
                textebcl = textebcl + '''
                    <td>{{{{item.{0}|date:"d/m/Y H:i"}}}}</td>'''.format(nom_champ)
            elif type_data == "DateField":
                textebcl = textebcl + '''
                    <td>{{{{item.{0}|date:"d/m/Y"}}}}</td>'''.format(nom_champ)
            elif type_data in ("CharField", "IntegerField", "FloatField") and len(list_champs[i].choices) > 0:
                textebcl = textebcl + '''
                    <td>{{{{ item.value_{0} }}}}</td>'''.format(nom_champ)
            else :
                textebcl = textebcl + '''
                    <td>{{{{item.{0}}}}}</td>'''.format(nom_champ)

    texteTemplate = texteTemplate + textebcl

    texteTemplate = texteTemplate + '''
                    <td>{{{{item.creation_date|date:'d/m/Y'}}}}</td>
                    <td>{{{{item.auteur.nom_complet}}}}</td>
                </tr>
                {{% endfor %}}
            </table>
        </div>
    </body>
</html>
'''.format(nom_pattern, nom_modele.lower(), list_champs[0].name)
    fichier.write(texteTemplate)
    fichier.close()


    # CRUD AND URLS URLS
    path = os.path.abspath(os.path.curdir)
    path = path + "\\{0}\\urls.py".format(nomModule)
    fichier = codecs.open(path,"a", encoding='utf-8')

    texte_a_ajouter_urls_py_dossier_ap= "\n#{2} REPORTING URLS\nurlpatterns.append(url(r'^{0}/generate', views.get_generer_{0}, name = '{1}_get_generer_{0}'))".format(nom_modele.lower(),nom_pattern, nom_modele.upper())
    texte_a_ajouter_urls_py_dossier_ap= texte_a_ajouter_urls_py_dossier_ap + "\nurlpatterns.append(url(r'^{0}/post_generate', views.post_generer_{0}, name = '{1}_post_generer_{0}'))".format(nom_modele.lower(),nom_pattern)
    texte_a_ajouter_urls_py_dossier_ap= texte_a_ajouter_urls_py_dossier_ap + "\nurlpatterns.append(url(r'^{0}/print_generate', views.post_imprimer_rapport_{0}, name = '{1}_post_imprimer_rapport_{0}'))\n".format(nom_modele.lower(),nom_pattern)
    fichier.write(texte_a_ajouter_urls_py_dossier_ap)
    fichier.close()

def genAPIOfContentType(content_type_id, module_id):
    content_type = ContentType.objects.get(id = content_type_id)
    model_class = content_type.model_class()
    module = dao_module.toGetModule(module_id)
    #Standardisation denomination modele
    nom_modele = content_type.model.replace("model_","").capitalize()
    nom_modele_verbose = model_class._meta.verbose_name
    nom_modele_verbose_plural = model_class._meta.verbose_name_plural
    nom_modele_class = model_class.__name__
    nomdao="dao_{0}".format(nom_modele.lower())
    nom_pattern = 'module_{0}'.format(unidecode.unidecode(module.nom_module.lower()))
    nomModule = module.nom_application
    nameModuleUp = nom_pattern.upper()

    list_champs = []
    for field in model_class._meta.get_fields():
        #if field.name not in ("id", "statut", "etat", "creation_date", "update_date", "auteur") and field.__class__.__name__ != "ManyToOneRel": list_champs.append(field)
        if field.__class__.__name__ != "ManyToOneRel": list_champs.append(field)

    # CREATION FONCTIONS API DANS views.py
    path = os.path.abspath(os.path.curdir)
    path = path + "\\{0}\\views.py".format(nomModule)
    fichier = codecs.open(path,"a", encoding='utf-8')

    # API GET LIST
    texte_a_ajouter_views_py = "\n\n# {2} API CONTROLLERS\ndef get_list_{0}(request):\n\ttry:\n\t\tcontext = {{}}\n\t\t#token = request.META.get('HTTP_TOKEN')\n\t\t#if not token: raise Exception('Erreur, Token manquant')\n\n\t\tfiltered = False\n\t\tif 'filtered' in request.GET : filtered = str(request.GET['filtered'])\n\t\tdate_from = None\n\t\tif 'date_from' in request.GET : date_from = request.GET['date_from']\n\t\tdate_to = None\n\t\tif 'date_to' in request.GET : date_to = request.GET['date_to']\n\t\tquery = ''\n\t\tif 'query' in request.GET : query = str(request.GET['query'])\n\n\t\tlistes = []\n\t\tmodel = dao_{0}.toList()\n\t\t#model = pagination.toGet(request, model)\n\n\t\tfor item in model:\n\t\t\telement = {{".format(nom_modele.lower(), nomdao, nom_modele.upper(), nom_modele_verbose.lower(),nomModule)

    texte_boucle = ""
    for i in range(0, len(list_champs)):
        nom_champ = ""
        type_data = ""
        default_value = dao_model()
        is_null = False
        try:
            nom_champ = list_champs[i].name.lower()
            type_data = str(list_champs[i].__class__.__name__)
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass

        # Attribution des champs
        if type_data != "ManyToManyField":
            if type_data in ("ForeignKey", "OneToOneField"):
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}_id' : makeIntId(item.{0}_id),".format(nom_champ)
            elif type_data == "DateTimeField":
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : item.{0},".format(nom_champ)
            elif type_data == "DateField":
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : item.{0},".format(nom_champ)
            elif type_data == "FloatField":
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : makeFloat(item.{0}),".format(nom_champ)
            elif type_data == "BooleanField":
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : item.{0},".format(nom_champ)
            elif type_data == "EmailField":
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : str(item.{0}),".format(nom_champ)
            elif type_data == "CharField":
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : str(item.{0}),".format(nom_champ)
            elif type_data == "IntegerField":
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : makeInt(item.{0}),".format(nom_champ)
            elif type_data in ("ImageField", "FileField"):
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : item.{0}.url if item.{0} != None else None,".format(nom_champ)
            else:
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : item.{0},".format(nom_champ)

    texte_a_ajouter_views_py = texte_a_ajouter_views_py + texte_boucle
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\t\t\t}\n\t\t\tlistes.append(element)"
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\tcontext = {{\n\t\t\t'error' : False,\n\t\t\t'message' : 'Liste récupérée',\n\t\t\t'datas' : listes\n\t\t}}\n\t\treturn JsonResponse(context, safe=False)\n\texcept Exception as e:\n\t\treturn auth.toReturnApiFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)".format(nom_modele.lower(),nomdao,nom_modele.upper(),nom_modele_verbose.lower(),nomModule)

    # API GET ITEM
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\ndef get_item_{0}(request):\n\ttry:\n\t\tcontext = {{}}\n\t\t#token = request.META.get('HTTP_TOKEN')\n\t\t#if not token: raise Exception('Erreur, Token manquant')\n\n\t\tid = 0\n\t\tif 'id' in request.GET : id = int(request.GET['id'])\n\n\t\titem = {{}}\n\t\tmodel = dao_{0}.toGet(id)\n\t\tif model != None :\n\t\t\titem = {{".format(nom_modele.lower(), nomdao, nom_modele.upper(), nom_modele_verbose.lower(),nomModule)

    texte_boucle = ""
    for i in range(0, len(list_champs)):
        nom_champ = ""
        type_data = ""
        default_value = dao_model()
        is_null = False
        try:
            nom_champ = list_champs[i].name.lower()
            type_data = str(list_champs[i].__class__.__name__)
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass

        # Attribution des champs
        if type_data != "ManyToManyField":
            if type_data in ("ForeignKey", "OneToOneField"):
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}_id' : makeIntId(model.{0}_id),".format(nom_champ)
            elif type_data == "DateTimeField":
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : model.{0},".format(nom_champ)
            elif type_data == "DateField":
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : model.{0},".format(nom_champ)
            elif type_data == "FloatField":
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : makeFloat(model.{0}),".format(nom_champ)
            elif type_data == "BooleanField":
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : model.{0},".format(nom_champ)
            elif type_data == "EmailField":
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : str(model.{0}),".format(nom_champ)
            elif type_data == "CharField":
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : str(model.{0}),".format(nom_champ)
            elif type_data == "IntegerField":
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : makeInt(model.{0}),".format(nom_champ)
            elif type_data in ("ImageField", "FileField"):
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : model.{0}.url if model.{0} != None else None,".format(nom_champ)
            else:
                texte_boucle = texte_boucle + "\n\t\t\t\t'{0}' : model.{0},".format(nom_champ)

    texte_a_ajouter_views_py = texte_a_ajouter_views_py + texte_boucle
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\t\t\t}"
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\tcontext = {{\n\t\t\t'error' : False,\n\t\t\t'message' : 'Objet récupéré',\n\t\t\t'item' : item\n\t\t}}\n\t\treturn JsonResponse(context, safe=False)\n\texcept Exception as e:\n\t\treturn auth.toReturnApiFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)".format(nom_modele.lower(),nomdao,nom_modele.upper(),nom_modele_verbose.lower(),nomModule)


    # API POST CREATE
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n@api_view(['POST'])\n@transaction.atomic\ndef post_create_{0}(request):\n\tsid = transaction.savepoint()\n\ttry:\n\t\tcontext = {{}}\n\t\t#token = request.META.get('HTTP_TOKEN')\n\t\t#if not token: raise Exception('Erreur, Token manquant')\n".format(nom_modele.lower(), nomdao, nom_modele.upper(), nom_modele_verbose.lower(), nomModule)

    texte_boucle = ""
    for i in range(0, len(list_champs)):
        nom_champ = ""
        type_data = ""
        default_value = dao_model()
        is_null = False
        try:
            nom_champ = list_champs[i].name.lower()
            type_data = str(list_champs[i].__class__.__name__)
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass

        if nom_champ not in ("id", "statut", "etat", "creation_date", "update_date"):
            # Contrôle quand on n'a pas défini une valeur par defaut et que le champ est requis
            texte_check_nullable = ""
            if inspect.isclass(default_value) == True and is_null == False and type_data != "ManyToManyField":
                if type_data in ("ForeignKey", "OneToOneField"): texte_check_nullable = "\n\t\tif {0}_id in (None, '') : return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, 'Champ obligatoire non saisi', msg = 'Le Champ \\'{1}\\' est obligatoire, Veuillez le renseigner SVP!')".format(nom_champ, list_champs[i].verbose_name)
                else : texte_check_nullable = "\n\t\tif {0} in (None, '') : return auth.toReturnApiFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, 'Champ obligatoire non saisi', msg = 'Le Champ \\'{1}\\' est obligatoire, Veuillez le renseigner SVP!')".format(nom_champ, list_champs[i].verbose_name)

            # Attribution des champs

            if type_data in ("ForeignKey", "OneToOneField"):
                texte_boucle = texte_boucle + "\n\n\t\t{0}_id = None\n\t\tif '{0}' in request.POST : {0}_id = makeIntId(request.POST['{0}_id'])".format(nom_champ) + texte_check_nullable
            elif type_data == "ManyToManyField":
                texte_boucle = texte_boucle + "\n\n\t\t{0} = []".format(nom_champ)
            elif type_data == "DateTimeField":
                texte_boucle = texte_boucle + "\n\n\t\t{0} = ''\n\t\tif '{0}' in request.POST : {0} = str(request.POST['{0}']){1}\n\t\t{0} = timezone.datetime(int({0}[6:10]), int({0}[3:5]), int({0}[0:2]), int({0}[11:13]), int({0}[14:16]))".format(nom_champ, texte_check_nullable)
            elif type_data == "DateField":
                texte_boucle = texte_boucle + "\n\n\t\t{0} = ''\n\t\tif '{0}' in request.POST : {0} = str(request.POST['{0}']){1}\n\t\t{0} = date(int({0}[6:10]), int({0}[3:5]), int({0}[0:2]))".format(nom_champ, texte_check_nullable)
            elif type_data == "FloatField":
                texte_boucle = texte_boucle + "\n\n\t\t{0} = 0.0\n\t\tif '{0}' in request.POST : {0} = makeFloat(request.POST['{0}'])".format(nom_champ)  + texte_check_nullable
            elif type_data == "BooleanField":
                texte_boucle = texte_boucle + "\n\n\t\t{0} = True if '{0}' in request.POST else False".format(nom_champ)
            elif type_data == "EmailField":
                texte_boucle = texte_boucle + "\n\n\t\t{0} = ''\n\t\tif '{0}' in request.POST : {0} = str(request.POST['{0}'])".format(nom_champ)  + texte_check_nullable
            elif type_data == "CharField":
                texte_boucle = texte_boucle + "\n\n\t\t{0} = ''\n\t\tif '{0}' in request.POST : {0} = str(request.POST['{0}'])".format(nom_champ)  + texte_check_nullable
            elif type_data == "IntegerField":
                texte_boucle = texte_boucle + "\n\n\t\t{0} = 0\n\t\tif '{0}' in request.POST : {0} = makeInt(request.POST['{0}'])".format(nom_champ)  + texte_check_nullable
            elif type_data in ("ImageField", "FileField"):
                texte_boucle = texte_boucle + "\n\n\t\t{0} = request.FILES['{0}'] if '{0}' in request.FILES else None".format(nom_champ)
            else:
                texte_boucle = texte_boucle + "\n\n\t\t{0} = ''\n\t\tif '{0}' in request.POST : {0} = request.POST['{0}']".format(nom_champ)  + texte_check_nullable
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + texte_boucle

    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\tauteur = dao_utilisateur.toGetUtilisateur(auteur_id)\n\n\t\t{0} = {1}.toCreate(".format(nom_modele.lower(), nomdao, nom_modele.capitalize())
    text_parenthese = ""
    for i in range(0,len(list_champs)):
        nom_champ = ""
        type_data = ""
        default_value = ""
        is_null = True
        try:
            nom_champ = list_champs[i].name.lower()
            type_data = str(list_champs[i].__class__.__name__)
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass

        # Contrôle quand on n'a pas défini une valeur par defaut et que le champ est requis
        check_nullable = True
        if inspect.isclass(default_value) == True and is_null == False and type_data != "ManyToManyField": check_nullable = False

        if nom_champ not in ("id", "statut", "etat", "creation_date", "update_date", "auteur"):
            if type_data in ("ForeignKey", "OneToOneField"): nom_champ = "{0}_id".format(nom_champ)
            if check_nullable: text_parenthese = text_parenthese + "{0} = {0}, ".format(nom_champ)
            else: text_parenthese = text_parenthese + "{0}, ".format(nom_champ)

    text_parenthese = text_parenthese[:len(text_parenthese)-2]
    text_parenthese = text_parenthese + ")"
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + text_parenthese

    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\t\tsaved, {0}, message = dao_{0}.toSave(auteur, {0})\n\n\t\tif saved == False: raise Exception(message)\n\n\t\tobjet = {{".format(nom_modele.lower())

    texte_boucle = ""
    for i in range(0, len(list_champs)):
        nom_champ = ""
        type_data = ""
        default_value = dao_model()
        is_null = False
        try:
            nom_champ = list_champs[i].name.lower()
            type_data = str(list_champs[i].__class__.__name__)
            default_value = list_champs[i].default
            is_null = list_champs[i].null
        except Exception as e:
            pass
        # Attribution des champs
        if type_data != "ManyToManyField":
            if type_data in ("ForeignKey", "OneToOneField"):
                texte_boucle = texte_boucle + "\n\t\t\t'{0}_id' : makeIntId({1}.{0}_id),".format(nom_champ, nom_modele.lower())
            elif type_data == "DateTimeField":
                texte_boucle = texte_boucle + "\n\t\t\t'{0}' : {1}.{0},".format(nom_champ, nom_modele.lower())
            elif type_data == "DateField":
                texte_boucle = texte_boucle + "\n\t\t\t'{0}' : {1}.{0},".format(nom_champ, nom_modele.lower())
            elif type_data == "FloatField":
                texte_boucle = texte_boucle + "\n\t\t\t'{0}' : makeFloat({1}.{0}),".format(nom_champ, nom_modele.lower())
            elif type_data == "BooleanField":
                texte_boucle = texte_boucle + "\n\t\t\t'{0}' : {1}.{0},".format(nom_champ, nom_modele.lower())
            elif type_data == "EmailField":
                texte_boucle = texte_boucle + "\n\t\t\t'{0}' : str({1}.{0}),".format(nom_champ, nom_modele.lower())
            elif type_data == "CharField":
                texte_boucle = texte_boucle + "\n\t\t\t'{0}' : str({1}.{0}),".format(nom_champ, nom_modele.lower())
            elif type_data == "IntegerField":
                texte_boucle = texte_boucle + "\n\t\t\t'{0}' : makeInt({1}.{0}),".format(nom_champ, nom_modele.lower())
            elif type_data in ("ImageField", "FileField"):
                texte_boucle = texte_boucle + "\n\t\t\t'{0}' : {1}.{0}.url if {1}.{0} != None else None,".format(nom_champ, nom_modele.lower())
            else:
                texte_boucle = texte_boucle + "\n\t\t\t'{0}' : {1}.{0},".format(nom_champ, nom_modele.lower())
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + texte_boucle

    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\t\t}\n\t\ttransaction.savepoint_commit(sid)"
    texte_a_ajouter_views_py = texte_a_ajouter_views_py + "\n\n\t\tcontext = {{\n\t\t\t'error' : False,\n\t\t\t'message' : 'Enregistrement éffectué avec succès',\n\t\t\t'item' : objet\n\t\t}}\n\t\treturn JsonResponse(context, safe=False)\n\texcept Exception as e:\n\t\ttransaction.savepoint_rollback(sid)\n\t\treturn auth.toReturnApiFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)".format(nom_modele.lower(),nomdao,nom_modele.upper(),nom_modele_verbose.lower(),nomModule)

    fichier.write(texte_a_ajouter_views_py)
    fichier.close()


    # CRUD AND URLS URLS
    path = os.path.abspath(os.path.curdir)
    path = path + "\\{0}\\urls.py".format(nomModule)
    fichier = codecs.open(path,"a", encoding='utf-8')

    texte_a_ajouter_urls_py_dossier_ap= "\n#{2} API URLS\nurlpatterns.append(url(r'^api/{0}/list', views.get_list_{0}, name = '{1}_api_list_{0}'))".format(nom_modele.lower(), nom_pattern, nom_modele.upper())
    texte_a_ajouter_urls_py_dossier_ap= texte_a_ajouter_urls_py_dossier_ap + "\nurlpatterns.append(url(r'^api/{0}/item', views.get_item_{0}, name = '{1}_api_item_{0}'))".format(nom_modele.lower(), nom_pattern)
    texte_a_ajouter_urls_py_dossier_ap= texte_a_ajouter_urls_py_dossier_ap + "\nurlpatterns.append(url(r'^api/{0}/create', views.post_create_{0}, name = '{1}_api_create_{0}'))\n".format(nom_modele.lower(), nom_pattern)
    fichier.write(texte_a_ajouter_urls_py_dossier_ap)
    fichier.close()
