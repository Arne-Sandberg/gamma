from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

# -----------------------------------------------------
# Distpatch URLs.-
# -----------------------------------------------------
urlpatterns = patterns("folder.views",
		url(r'^add/$',               	"add", 		name='folder_add'		),
		url(r'^mod/$',          	"mod", 		name='folder_mod'		),
		url(r'^rem/$',          	"rem", 		name='folder_rem'		),
		url(r'^read/$',          	"read", 	name='folder_read'		),
		url(r'^write/$',          	"write", 	name='folder_write'		),
		url(r'^zip/$',          	"compress", 	name='folder_zip'		),
		url(r'^(.*)/$',			"folder",	name='folder_folder'		),
		url(r'^root$',			"folder",	name='folder_root'		),
		url(r'^.*$',			"folder",	name='folder_home'		),
)
