from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

# -----------------------------------------------------
# Distpatch URLs.-
# -----------------------------------------------------
urlpatterns = patterns("data.views",

		# -----------------------------------------------------
		# CGI
		# -----------------------------------------------------
		url(r'^cgi/search/$',                   "cgi.search",  		name='data_cgi_search' 		),

		# -----------------------------------------------------
		# CGI FOLDER.-
		# -----------------------------------------------------
		url(r'^cgi/folder/add/$',               "folder.add", 		name='data_folder_add'		),
		url(r'^cgi/folder/mod/$',          	"folder.mod", 		name='data_folder_mod'		),
		url(r'^cgi/folder/rem/$',          	"folder.rem", 		name='data_folder_rem'		),
		url(r'^cgi/folder/read/$',          	"folder.read", 		name='data_folder_read'		),
		url(r'^cgi/folder/write/$',          	"folder.write", 	name='data_folder_write'	),

		# -----------------------------------------------------
		# CONTROLLER
		# -----------------------------------------------------
		url(r'^rem/(.*)/(.*)/$',		"form.rem",		name='data_rem',		),
		url(r'^mod/(.*)/(.*)/$',		"form.mod",		name='data_mod',		),
		url(r'^get/(.*)/(.*)/$',		"file.get",		name='data_get',		),
		url(r'^upl/(.*)/$',			"file.upload",		name='data_upload',		),

		# -----------------------------------------------------
		# VIEW
		# -----------------------------------------------------
		url(r'^gallery/(.*)/(.*)/$',		"view.gallery",		name='data_gallery'		),
		url(r'^file/(.*)/$',			"view.file",		name='data_file'		),
		url(r'^folder/(.*)/$',			"view.folder",		name='data_folder'		),
		url(r'^root$',				"view.folder",		name='data_root'		),

		# -----------------------------------------------------
		# DEFAULT
		# -----------------------------------------------------
		url(r'^.*$',				"view.folder",		name='data_home'		),
)
