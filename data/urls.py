from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

# -----------------------------------------------------
# Distpatch URLs.-
# -----------------------------------------------------
urlpatterns = patterns("data.views",

		# -----------------------------------------------------
		# -----------------------------------------------------
		# url(r'^delete/(.*)/$',			"delete",	name='kain_delete',	),

		# -----------------------------------------------------
		# DEFAULT
		# -----------------------------------------------------
		url(r'^.*$',				"root",		name='data_home'	),
)
