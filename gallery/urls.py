from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

# -----------------------------------------------------
# Distpatch URLs.-
# -----------------------------------------------------
urlpatterns = patterns("gallery.views",
		url(r'^playlist/(.*)/$',	"playlist",	name='file_playlist'	),
		url(r'^add/$',          	"add", 		name='file_add'		),
		url(r'^mod/$',          	"mod", 		name='file_mod'		),
		url(r'^get/(.*)/$',          	"get", 		name='file_get'		),
		url(r'^fetch/$',          	"fetch", 	name='file_fetch'	),
		url(r'^rem/$',          	"rem", 		name='file_rem'		),
		url(r'^(.*)/$',			"gallery",	name='file_gallery'	),
)
