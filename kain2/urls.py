from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

# -----------------------------------------------------
# Distpatch URLs.-
# -----------------------------------------------------
urlpatterns = patterns("kain2.views",

		# -----------------------------------------------------
		# CGI 
		# -----------------------------------------------------
		url(r'^cgi/search/$',			"cgi_search",    name='kain_cgi_search',),
		url(r'^cgi/delete/(.*)/$',		"cgi_delete",    name='kain_cgi_del',	),
		url(r'^cgi/user/(.*)/$',		"cgi_user",      name='kain_cgi_user',	),
		url(r'^cgi/pass/(.*)/$',		"cgi_pass",      name='kain_cgi_pass',	),
		url(r'^cgi/url/(.*)/$',			"cgi_url",       name='kain_cgi_url',	),
		url(r'^cgi/name/(.*)/$',		"cgi_name",      name='kain_cgi_name',	),
		url(r'^cgi/add/$',			"cgi_add",       name='kain_cgi_add',	),

		# -----------------------------------------------------
		# VIEW 
		# -----------------------------------------------------
		url(r'^root/$',				"root",		name='kain_root',	),
		url(r'^folder/(.*)/$',			"folder",	name='kain_folder',	),

		# -----------------------------------------------------
		# CONTROLLER 
		# -----------------------------------------------------
		url(r'^add/$',				"add",		name='kain_add'		),
		url(r'^edit/(.*)/$',			"edit",		name='kain_edit',	),
		url(r'^delete/(.*)/$',			"delete",	name='kain_delete',	),

		# -----------------------------------------------------
		# DEFAULT
		# -----------------------------------------------------
		url(r'^.*$',				"root",		name='kain_home'	),
)
